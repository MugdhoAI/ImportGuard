"""Account pages, session routes, and export history endpoints."""

from pathlib import Path
from typing import Annotated, Any
from urllib.parse import quote

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services import auth, store
from app.services import billing as billing_state

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")

SESSION_COOKIE = "ig_session"
GUEST_COOKIE = "ig_guest"


def get_viewer(request: Request) -> dict[str, Any | None]:
    session_id = request.cookies.get(SESSION_COOKIE)
    session = store.get_session(session_id) if session_id else None
    user = store.get_user_by_id(session["user_id"]) if session else None
    if user is None:
        return {"user": None, "session": None}
    return {"user": user, "session": session}


def current_user(request: Request) -> dict[str, Any] | None:
    return get_viewer(request)["user"]


def require_user(request: Request) -> dict[str, Any]:
    user = current_user(request)
    if user is None:
        raise HTTPException(401, "Sign in required.")
    return user


def require_admin(request: Request) -> dict[str, Any]:
    user = require_user(request)
    if not auth.is_admin(user):
        raise HTTPException(403, "Admin access required.")
    return user


def clear_session(request: Request, response: Response) -> None:
    session_id = request.cookies.get(SESSION_COOKIE)
    if session_id:
        store.delete_session(session_id)
    _clear_session(response)


_CRUMBS = {
    "/": "Home",
    "/home": "Home",
    "/dashboard": "Dashboard",
    "/app": "Workspace",
    "/workspace": "Workspace",
    "/history": "Import history",
    "/exports": "Exports",
    "/exports/pending": "Pending downloads",
    "/billing": "Billing",
    "/payments": "Payments",
    "/teams": "Teams",
    "/settings": "Settings",
    "/help": "Help",
    "/admin": "Admin",
    "/login": "Sign in",
    "/signup": "Sign up",
    "/forgot-password": "Forgot password",
    "/reset-password": "Reset password",
    "/invitations/accept": "Team invitation",
}


def crumb_for(path: str) -> str:
    if path in _CRUMBS:
        return _CRUMBS[path]
    if path.startswith("/exports/"):
        return "Export detail"
    if path.startswith("/teams/"):
        return "Team detail"
    return "ImportGuard"


def shell_context(request: Request) -> dict[str, Any]:
    viewer = get_viewer(request)
    session = viewer["session"] or {}
    user = viewer["user"]
    return {
        "app_shell": True,
        "current_user": user,
        "csrf_token": session.get("csrf_token", ""),
        "is_admin": auth.is_admin(user),
        "crumb": crumb_for(request.url.path),
        "sidebar_plan": (
            billing_state.current_state(user["id"]) if user is not None else None
        ),
    }


def list_for_viewer(request: Request) -> list[dict[str, Any]]:
    viewer = get_viewer(request)
    if viewer["user"] is not None:
        return store.list_exports(user_id=viewer["user"]["id"])
    if request.cookies.get(GUEST_COOKIE):
        return store.list_exports(
            guest_token_hash=store.hash_guest_token(request.cookies[GUEST_COOKIE])
        )
    return []


def owned_export(request: Request, export_id: str) -> dict[str, Any]:
    row = store.get_export(export_id)
    if row is None:
        raise HTTPException(404, "Export not found.")
    user = current_user(request)
    if user is not None and row["user_id"] == user["id"]:
        return row
    guest_token = request.cookies.get(GUEST_COOKIE)
    if guest_token and row["guest_token_hash"] == store.hash_guest_token(guest_token):
        return row
    raise HTTPException(404, "Export not found.")


def team_role_or_404(team_id: int, user_id: int) -> str:
    role = store.team_role(team_id, user_id)
    if role is None:
        raise HTTPException(404, "Team not found.")
    return role


def require_team_manager(team_id: int, user_id: int) -> None:
    if team_role_or_404(team_id, user_id) not in ("owner", "admin"):
        raise HTTPException(403, "Team owners or admins only.")


def require_csrf(request: Request, token: str) -> dict[str, Any]:
    viewer = get_viewer(request)
    if viewer["user"] is None or not auth.csrf_valid(viewer["session"], token):
        raise HTTPException(403, "Invalid session token.")
    assert viewer["session"] is not None
    return {"user": viewer["user"], "session": viewer["session"]}


def client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _secure(request: Request) -> bool:
    return request.url.scheme == "https"


def _set_session(response: Response, session_id: str, request: Request) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        session_id,
        max_age=30 * 24 * 3600,
        httponly=True,
        samesite="lax",
        secure=_secure(request),
        path="/",
    )


def _clear_session(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")


def _clear_guest(response: Response) -> None:
    response.delete_cookie(GUEST_COOKIE, path="/")


def _safe_next(value: str | None) -> str:
    if value and value.startswith("/") and not value.startswith("//") and "\\" not in value:
        return value
    return "/dashboard"


def _auth_page(
    request: Request, mode: str, error: str | None, status: int = 200,
    notice: str | None = None,
):
    return templates.TemplateResponse(
        request,
        "auth.html",
        {
            "mode": mode,
            "error": error,
            "notice": notice,
            "retention_days": settings.export_retention_days,
        },
        status_code=status,
    )


def _page(request: Request, template_name: str, context: dict[str, Any] | None = None,
          status: int = 200):
    return templates.TemplateResponse(
        request, template_name, {**shell_context(request), **(context or {})},
        status_code=status,
    )


def _standalone(request: Request, template_name: str, context: dict[str, Any] | None = None,
                status: int = 200):
    """Render a pre-auth page without the application shell, like login."""
    return templates.TemplateResponse(
        request, template_name, context or {}, status_code=status
    )


def _start_session_response(
    request: Request, user: dict[str, Any], target: str
) -> RedirectResponse:
    guest_token = request.cookies.get(GUEST_COOKIE)
    if guest_token:
        store.claim_guest_exports(guest_token, user["id"])
    session = store.create_session(user["id"])
    store.purge_expired_sessions()
    response = RedirectResponse(target, status_code=303)
    _set_session(response, session["id"], request)
    _clear_guest(response)
    return response


@router.get("/login")
def login_page(request: Request):
    if get_viewer(request)["user"] is not None:
        return RedirectResponse("/dashboard", status_code=303)
    notice = None
    if request.query_params.get("notice") == "reset":
        notice = "Password reset. Sign in with your new password."
    return _auth_page(request, "login", None, notice=notice)


@router.get("/signup")
def signup_page(request: Request):
    if get_viewer(request)["user"] is not None:
        return RedirectResponse("/dashboard", status_code=303)
    return _auth_page(request, "signup", None)


@router.post("/auth/signup")
def signup(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    full_name: Annotated[str, Form()] = "",
):
    try:
        user = auth.register(email, password, client_ip(request))
        if full_name.strip():
            store.set_user_name(user["id"], full_name)
            user = store.get_user_by_id(user["id"]) or user
    except auth.AuthError as exc:
        return _auth_page(request, "signup", str(exc), status=400)
    return _start_session_response(request, user, "/dashboard")


@router.post("/auth/login")
def login(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    next: Annotated[str, Form()] = "/dashboard",
):
    try:
        user = auth.authenticate(email, password, client_ip(request))
    except auth.AuthError as exc:
        return _auth_page(request, "login", str(exc), status=401)
    return _start_session_response(request, user, _safe_next(next))


@router.post("/auth/logout")
def logout(request: Request, csrf_token: Annotated[str, Form()]):
    viewer = get_viewer(request)
    if not auth.csrf_valid(viewer["session"], csrf_token):
        raise HTTPException(403, "Invalid session token.")
    assert viewer["session"] is not None
    store.delete_session(viewer["session"]["id"])
    response = RedirectResponse("/home", status_code=303)
    _clear_session(response)
    return response


@router.post("/auth/delete")
def delete_account(
    request: Request,
    csrf_token: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    viewer = get_viewer(request)
    if viewer["user"] is None or not auth.csrf_valid(viewer["session"], csrf_token):
        raise HTTPException(403, "Invalid session token.")
    try:
        auth.authenticate(viewer["user"]["email"], password, client_ip(request))
    except auth.AuthError as exc:
        raise HTTPException(401, str(exc)) from exc
    store.delete_account(viewer["user"]["id"])
    response = RedirectResponse("/", status_code=303)
    _clear_session(response)
    return response


@router.get("/api/exports")
def export_history(request: Request):
    viewer = get_viewer(request)
    if viewer["user"] is not None:
        exports = store.list_exports(user_id=viewer["user"]["id"])
    elif request.cookies.get(GUEST_COOKIE):
        exports = store.list_exports(
            guest_token_hash=store.hash_guest_token(request.cookies[GUEST_COOKIE])
        )
    else:
        exports = []
    return {"exports": exports}


@router.post("/api/exports/claim")
def claim_exports(request: Request):
    viewer = get_viewer(request)
    guest_token = request.cookies.get(GUEST_COOKIE)
    if viewer["user"] is None or not guest_token:
        raise HTTPException(401, "Sign in with a guest session to claim exports.")
    claimed = store.claim_guest_exports(guest_token, viewer["user"]["id"])
    return {"claimed": claimed}


@router.get("/api/exports/{export_id}/download")
def download_export(request: Request, export_id: str):
    user = require_user(request)
    row = store.get_export(export_id)
    if (
        row is None
        or row["package_stored"] != 1
        or row["package"] is None
        or row["user_id"] != user["id"]
    ):
        raise HTTPException(404, "Export not found.")
    store.mark_export_downloaded(export_id)
    assert row["package"] is not None
    return Response(
        bytes(row["package"]),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="importguard-export-{export_id}.zip"',
            "Cache-Control": "no-store",
        },
    )


_EXPORT_DETAIL_KEYS = (
    "id", "filename", "file_sha256", "input_rows", "accepted_rows", "rejected_rows",
    "package_stored", "downloaded_at", "download_count",
    "created_at", "expires_at",
)


def export_status(row: dict[str, Any]) -> str:
    if row.get("downloaded_at"):
        return "downloaded"
    if not row.get("package_stored"):
        return "expired-file"
    return "pending"


def validation_status(row: dict[str, Any]) -> str:
    return "needs_review" if row.get("rejected_rows") else "completed"


@router.get("/history")
def history_page(request: Request):
    exports = list_for_viewer(request)
    query = request.query_params.get("q", "").strip()
    status = request.query_params.get("status", "")
    if query:
        lowered = query.lower()
        exports = [row for row in exports if lowered in row["filename"].lower()]
    if status in ("completed", "needs_review"):
        exports = [row for row in exports if validation_status(row) == status]
    else:
        status = ""
    try:
        page_number = max(1, int(request.query_params.get("page", "1")))
    except ValueError:
        page_number = 1
    per_page = 20
    total_pages = max(1, -(-len(exports) // per_page))
    page_number = min(page_number, total_pages)
    rows = exports[(page_number - 1) * per_page : page_number * per_page]
    return _page(
        request,
        "history.html",
        {
            "exports": rows,
            "q": query,
            "status": status,
            "page_number": page_number,
            "total_pages": total_pages,
            "total_count": len(exports),
        },
    )


@router.get("/api/exports/{export_id}")
def export_detail_api(request: Request, export_id: str):
    row = owned_export(request, export_id)
    detail = {key: row.get(key) for key in _EXPORT_DETAIL_KEYS}
    detail["status"] = export_status(row)
    return detail


@router.get("/exports")
def exports_page(request: Request):
    exports = list_for_viewer(request)
    pending = sum(1 for row in exports if row["downloaded_at"] is None)
    return _page(request, "exports.html", {"exports": exports, "pending_count": pending})


@router.get("/exports/pending")
def pending_page(request: Request):
    user = require_user(request)
    return _page(
        request,
        "pending.html",
        {"exports": store.list_exports(user_id=user["id"], only_pending=True)},
    )


@router.get("/exports/{export_id}")
def export_detail_page(request: Request, export_id: str):
    row = owned_export(request, export_id)
    return _page(
        request, "export_detail.html",
        {"export": row, "status": export_status(row)},
    )


@router.get("/help")
def help_page(request: Request):
    return _page(
        request, "help.html", {"retention_days": settings.export_retention_days}
    )


def _settings_context(user: dict[str, Any], session: dict[str, Any]) -> dict[str, Any]:
    return {
        "plan_name": billing_state.current_state(user["id"])["plan_name"],
        "sessions": store.list_sessions(user["id"]),
        "current_session_id": session["id"],
    }


@router.get("/settings")
def settings_page(request: Request):
    viewer = get_viewer(request)
    if viewer["user"] is None or viewer["session"] is None:
        raise HTTPException(401, "Sign in required.")
    notice = request.query_params.get("notice", "")
    messages = {
        "password": "Password changed. Other sessions were signed out.",
        "session": "Session revoked.",
        "profile": "Profile updated.",
    }
    return _page(
        request,
        "settings.html",
        {
            **_settings_context(viewer["user"], viewer["session"]),
            "notice": messages.get(notice),
        },
    )


@router.post("/settings/profile")
def settings_profile(
    request: Request,
    csrf_token: Annotated[str, Form()],
    name: Annotated[str, Form()] = "",
):
    ctx = require_csrf(request, csrf_token)
    try:
        store.set_user_name(ctx["user"]["id"], name)
    except store.StoreError as exc:
        return _page(
            request, "settings.html",
            {**_settings_context(ctx["user"], ctx["session"]), "error": str(exc)},
            status=400,
        )
    return RedirectResponse("/settings?notice=profile", status_code=303)


@router.post("/settings/password")
def settings_password(
    request: Request,
    csrf_token: Annotated[str, Form()],
    current_password: Annotated[str, Form()],
    new_password: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    try:
        auth.change_password(
            ctx["user"]["id"], current_password, new_password,
            keep_session_id=ctx["session"]["id"],
        )
    except auth.AuthError as exc:
        return _page(
            request, "settings.html",
            {**_settings_context(ctx["user"], ctx["session"]), "error": str(exc)},
            status=400,
        )
    return RedirectResponse("/settings?notice=password", status_code=303)


@router.post("/settings/sessions/revoke")
def settings_revoke_session(
    request: Request,
    csrf_token: Annotated[str, Form()],
    session_id: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    if not store.revoke_session(ctx["user"]["id"], session_id):
        raise HTTPException(404, "Session not found.")
    if session_id == ctx["session"]["id"]:
        response = RedirectResponse("/home", status_code=303)
        _clear_session(response)
        return response
    return RedirectResponse("/settings?notice=session", status_code=303)


@router.get("/forgot-password")
def forgot_page(request: Request):
    return _standalone(request, "forgot.html", {})


@router.post("/forgot-password")
def forgot_submit(request: Request, email: Annotated[str, Form()]):
    try:
        auth.request_password_reset(email)
    except auth.AuthError as exc:
        message = str(exc)
        if message.startswith("Password reset by email is not configured"):
            return _standalone(request, "forgot.html", {"notice": message})
        return _standalone(request, "forgot.html", {"error": message}, status=400)
    return _standalone(
        request, "forgot.html",
        {"notice": "If that address has an account, a reset link is on its way."},
    )


@router.get("/reset-password")
def reset_page(request: Request):
    return _standalone(
        request, "reset.html", {"token": request.query_params.get("token", "")}
    )


@router.post("/reset-password")
def reset_submit(
    request: Request,
    token: Annotated[str, Form()],
    new_password: Annotated[str, Form()],
):
    try:
        auth.reset_password(token, new_password)
    except auth.AuthError as exc:
        return _standalone(
            request, "reset.html", {"token": token, "error": str(exc)}, status=400
        )
    return RedirectResponse("/login?notice=reset", status_code=303)


@router.get("/teams")
def teams_page(request: Request):
    user = require_user(request)
    return _page(request, "teams.html", {"teams": store.user_teams(user["id"])})


@router.post("/teams")
def team_create(
    request: Request,
    csrf_token: Annotated[str, Form()],
    name: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    clean = name.strip()[:80]
    if not clean:
        return _page(
            request, "teams.html",
            {"teams": store.user_teams(ctx["user"]["id"]), "error": "Give the team a name."},
            status=400,
        )
    team = store.create_team(clean, ctx["user"]["id"])
    return RedirectResponse(f"/teams/{team['id']}", status_code=303)


def _team_activity(team_id: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for member in store.team_members(team_id):
        if member["status"] != "active":
            continue
        for row in store.list_exports(user_id=member["user_id"]):
            row["member_email"] = member["email"]
            rows.append(row)
    rows.sort(key=lambda row: row["created_at"], reverse=True)
    return rows[:20]


def _team_detail_page(
    request: Request, team_id: int, user: dict[str, Any],
    extra: dict[str, Any] | None = None, status: int = 200,
):
    role = team_role_or_404(team_id, user["id"])
    team = next(t for t in store.user_teams(user["id"]) if t["id"] == team_id)
    context: dict[str, Any] = {
        "team": team,
        "role": role,
        "members": store.team_members(team_id),
        "invitations": (
            store.team_invitations(team_id) if role in ("owner", "admin") else []
        ),
        "activity": _team_activity(team_id),
    }
    if extra:
        context.update(extra)
    return _page(request, "team_detail.html", context, status=status)


@router.get("/teams/{team_id}")
def team_page(request: Request, team_id: int):
    user = require_user(request)
    return _team_detail_page(request, team_id, user)


@router.post("/teams/{team_id}/invite")
def team_invite(
    request: Request,
    team_id: int,
    csrf_token: Annotated[str, Form()],
    email: Annotated[str, Form()],
    role: Annotated[str, Form()] = "member",
):
    ctx = require_csrf(request, csrf_token)
    require_team_manager(team_id, ctx["user"]["id"])
    try:
        invite = store.create_invitation(
            team_id, auth.normalize_email(email), role, ctx["user"]["id"]
        )
    except (auth.AuthError, store.StoreError) as exc:
        return _team_detail_page(
            request, team_id, ctx["user"], {"error": str(exc)}, status=400
        )
    return _team_detail_page(
        request, team_id, ctx["user"],
        {"invite_link": f"/invitations/accept?token={invite['token']}"},
    )


@router.post("/teams/{team_id}/role")
def team_set_role(
    request: Request,
    team_id: int,
    csrf_token: Annotated[str, Form()],
    user_id: Annotated[int, Form()],
    role: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    require_team_manager(team_id, ctx["user"]["id"])
    try:
        store.set_member_role(team_id, user_id, role)
    except store.StoreError as exc:
        return _team_detail_page(
            request, team_id, ctx["user"], {"error": str(exc)}, status=400
        )
    return RedirectResponse(f"/teams/{team_id}", status_code=303)


@router.post("/teams/{team_id}/remove")
def team_remove_member(
    request: Request,
    team_id: int,
    csrf_token: Annotated[str, Form()],
    user_id: Annotated[int, Form()],
):
    ctx = require_csrf(request, csrf_token)
    require_team_manager(team_id, ctx["user"]["id"])
    try:
        if user_id == ctx["user"]["id"]:
            store.leave_team(team_id, user_id)
            return RedirectResponse("/teams", status_code=303)
        store.remove_member(team_id, user_id)
    except store.StoreError as exc:
        return _team_detail_page(
            request, team_id, ctx["user"], {"error": str(exc)}, status=400
        )
    return RedirectResponse(f"/teams/{team_id}", status_code=303)


@router.post("/teams/{team_id}/leave")
def team_leave(
    request: Request, team_id: int, csrf_token: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    try:
        store.leave_team(team_id, ctx["user"]["id"])
    except store.StoreError as exc:
        return _team_detail_page(
            request, team_id, ctx["user"], {"error": str(exc)}, status=400
        )
    return RedirectResponse("/teams", status_code=303)


@router.post("/teams/{team_id}/invitations/revoke")
def team_revoke_invite(
    request: Request,
    team_id: int,
    csrf_token: Annotated[str, Form()],
    token: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    require_team_manager(team_id, ctx["user"]["id"])
    store.revoke_invitation(team_id, token)
    return RedirectResponse(f"/teams/{team_id}", status_code=303)


@router.get("/invitations/accept")
def invite_accept_page(request: Request):
    token = request.query_params.get("token", "")
    invite = store.get_invitation(token) if token else None
    if invite is None:
        return _page(request, "invite_accept.html", {"invalid": True}, status=404)
    if current_user(request) is None:
        target = quote(f"/invitations/accept?token={token}", safe="")
        return RedirectResponse(f"/login?next={target}", status_code=303)
    return _page(request, "invite_accept.html", {"invite": invite})


@router.post("/invitations/accept")
def invite_accept(
    request: Request,
    csrf_token: Annotated[str, Form()],
    token: Annotated[str, Form()],
):
    ctx = require_csrf(request, csrf_token)
    try:
        team = store.accept_invitation(token, ctx["user"]["id"])
    except store.StoreError as exc:
        return _page(
            request, "invite_accept.html",
            {"invite": store.get_invitation(token), "error": str(exc)}, status=400,
        )
    return RedirectResponse(f"/teams/{team['id']}", status_code=303)


@router.get("/admin")
def admin_page(request: Request):
    require_admin(request)
    subs = store.admin_subscriptions(limit=50)
    return _page(
        request,
        "admin.html",
        {
            "overview": store.admin_overview(),
            "subscriptions": subs["subscriptions"],
            "subscriptions_total": subs["total"],
            "provider": billing_state.provider().name,
        },
    )


@router.get("/api/admin/overview")
def admin_overview_api(request: Request):
    require_admin(request)
    return store.admin_overview()


@router.get("/api/admin/subscriptions")
def admin_subscriptions_api(request: Request):
    require_admin(request)
    return store.admin_subscriptions(limit=50)

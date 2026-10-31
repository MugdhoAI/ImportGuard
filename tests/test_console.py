"""Console route tests: pages and APIs called directly, no test server.

TestClient cannot bind sockets in restricted sandboxes, so these tests call
the route functions with synthetic requests against the session test database.
"""

import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, Request

from app.api import accounts as console
from app.api.accounts import GUEST_COOKIE, SESSION_COOKIE
from app.api.routes import auth_logout, auth_me, pending_exports
from app.services import auth, store

PASSWORD = "a-strong-password"


def _request(path="/", cookies=None, query=b""):
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": query,
        "headers": [],
        "server": ("testserver", 80),
        "client": ("testclient", 50000),
    }
    request = Request(scope)
    if cookies:
        request._cookies = cookies
    return request


def _signup(email, ip):
    user = auth.register(email, PASSWORD, ip)
    session = store.create_session(user["id"])
    return user, session


def _session_cookies(session):
    return {SESSION_COOKIE: session["id"]}


def _export(filename, user_id=None, guest_token=None, package=b"zip-bytes", **over):
    kwargs = {
        "filename": filename,
        "file_sha256": "deadbeef",
        "input_rows": 3,
        "accepted_rows": 2,
        "rejected_rows": 1,
        "recipe_json": "{}",
        "report_json": "{}",
        "package": package,
        "user_id": user_id,
        "guest_token": guest_token,
    }
    kwargs.update(over)
    return store.record_export(**kwargs)


def _body(response):
    return bytes(response.body).decode()


def test_auth_me_and_logout_cycle():
    guest = json.loads(auth_me(_request("/api/auth/me")).body)
    assert guest == {"authenticated": False, "user": None}
    user, session = _signup("me@example.test", "10.200.0.1")
    signed = json.loads(auth_me(_request("/api/auth/me", _session_cookies(session))).body)
    assert signed["authenticated"] is True
    assert signed["user"]["email"] == user["email"]
    cleared = auth_logout(_request("/api/auth/logout", _session_cookies(session)))
    assert json.loads(cleared.body) == {"ok": True}
    assert SESSION_COOKIE in cleared.headers["set-cookie"]
    assert store.get_session(session["id"]) is None


def test_pending_exports_json_requires_user_and_filters_downloaded():
    with pytest.raises(HTTPException) as exc:
        pending_exports(_request("/api/exports/pending"))
    assert exc.value.status_code == 401
    user, session = _signup("pend@example.test", "10.200.0.2")
    cookies = _session_cookies(session)
    waiting = _export("waiting.csv", user_id=user["id"])
    finished = _export("finished.csv", user_id=user["id"])
    store.mark_export_downloaded(finished["id"])
    rows = pending_exports(_request("/api/exports/pending", cookies))
    assert [row["id"] for row in rows] == [waiting["id"]]


def test_history_page_guest_gate_and_user_download():
    guest_token = store.new_token()
    guest_row = _export("guest-history.csv", guest_token=guest_token)
    page = _body(
        console.history_page(_request("/history", {GUEST_COOKIE: guest_token}))
    )
    assert "guest-history.csv" in page
    assert "Sign in to download" in page
    assert f"/api/exports/{guest_row['id']}/download" not in page
    user, session = _signup("hist@example.test", "10.200.0.3")
    own = _export("own-history.csv", user_id=user["id"])
    user_page = _body(
        console.history_page(_request("/history", _session_cookies(session)))
    )
    assert f"/api/exports/{own['id']}/download" in user_page
    assert "guest-history.csv" not in user_page


def test_exports_page_pending_banner_only_when_waiting():
    user, session = _signup("banner@example.test", "10.200.0.4")
    cookies = _session_cookies(session)
    waiting = _export("banner-wait.csv", user_id=user["id"])
    page = _body(console.exports_page(_request("/exports", cookies)))
    assert "pending download" in page
    assert 'href="/exports/pending"' in page
    store.mark_export_downloaded(waiting["id"])
    quiet = _body(console.exports_page(_request("/exports", cookies)))
    assert "pending download" not in quiet


def test_pending_page_requires_user_and_lists_waiting_only():
    with pytest.raises(HTTPException) as exc:
        console.pending_page(_request("/exports/pending"))
    assert exc.value.status_code == 401
    user, session = _signup("restore@example.test", "10.200.0.5")
    waiting = _export("restore-me.csv", user_id=user["id"])
    done = _export("restored.csv", user_id=user["id"])
    store.mark_export_downloaded(done["id"])
    page = _body(console.pending_page(_request("/exports/pending", _session_cookies(session))))
    assert waiting["filename"] in page
    assert done["filename"] not in page


def test_export_detail_page_and_api_enforce_ownership():
    owner, owner_session = _signup("detail@example.test", "10.200.0.6")
    stranger, stranger_session = _signup("stranger@example.test", "10.200.0.7")
    row = _export("Detail.csv", user_id=owner["id"])
    page = _body(
        console.export_detail_page(
            _request(f"/exports/{row['id']}", _session_cookies(owner_session)), row["id"]
        )
    )
    assert "Detail.csv" in page and "Pending" in page
    with pytest.raises(HTTPException) as exc:
        console.export_detail_page(
            _request(f"/exports/{row['id']}", _session_cookies(stranger_session)), row["id"]
        )
    assert exc.value.status_code == 404
    with pytest.raises(HTTPException) as exc:
        console.export_detail_page(_request("/exports/missing"), "missing")
    assert exc.value.status_code == 404
    detail = console.export_detail_api(
        _request(f"/api/exports/{row['id']}", _session_cookies(owner_session)), row["id"]
    )
    assert detail["status"] == "pending"
    assert "package" not in detail
    guest_token = store.new_token()
    guest_row = _export("guest-detail.csv", guest_token=guest_token)
    guest_page = _body(
        console.export_detail_page(
            _request(f"/exports/{guest_row['id']}", {GUEST_COOKIE: guest_token}),
            guest_row["id"],
        )
    )
    assert "guest-detail.csv" in guest_page
    assert "Sign in to download" in guest_page


def test_export_status_transitions():
    assert console.export_status({"downloaded_at": None, "package_stored": 1}) == "pending"
    assert (
        console.export_status({"downloaded_at": "2026-01-01", "package_stored": 1})
        == "downloaded"
    )
    assert console.export_status({"downloaded_at": None, "package_stored": 0}) == "expired-file"


def test_download_gate_marks_owner_downloads():
    owner, owner_session = _signup("dl@example.test", "10.200.0.8")
    stranger, stranger_session = _signup("dl-stranger@example.test", "10.200.0.9")
    row = _export("download-me.csv", user_id=owner["id"])
    with pytest.raises(HTTPException) as exc:
        console.download_export(_request(f"/api/exports/{row['id']}/download"), row["id"])
    assert exc.value.status_code == 401
    with pytest.raises(HTTPException) as exc:
        console.download_export(
            _request(f"/api/exports/{row['id']}/download", _session_cookies(stranger_session)),
            row["id"],
        )
    assert exc.value.status_code == 404
    response = console.download_export(
        _request(f"/api/exports/{row['id']}/download", _session_cookies(owner_session)),
        row["id"],
    )
    assert response.status_code == 200
    assert response.body == b"zip-bytes"
    fetched = store.get_export(row["id"])
    assert fetched is not None and fetched["downloaded_at"] is not None
    assert fetched["download_count"] == 1
    nostore = _export("nostore.csv", user_id=owner["id"], package=None)
    with pytest.raises(HTTPException) as exc:
        console.download_export(
            _request(
                f"/api/exports/{nostore['id']}/download", _session_cookies(owner_session)
            ),
            nostore["id"],
        )
    assert exc.value.status_code == 404


def test_settings_page_and_password_change():
    with pytest.raises(HTTPException) as exc:
        console.settings_page(_request("/settings"))
    assert exc.value.status_code == 401
    user, session = _signup("settings@example.test", "10.200.0.10")
    other = store.create_session(user["id"])
    cookies = _session_cookies(session)
    page = _body(console.settings_page(_request("/settings", cookies)))
    assert "settings@example.test" in page
    assert "Change password" in page and "Sessions" in page
    bad = console.settings_password(
        _request("/settings", cookies), session["csrf_token"], "wrong-password",
        "brand-new-password",
    )
    assert bad.status_code == 400
    assert "Current password" in _body(bad)
    done = console.settings_password(
        _request("/settings", cookies), session["csrf_token"], PASSWORD, "brand-new-password",
    )
    assert (done.status_code, done.headers["location"]) == (303, "/settings?notice=password")
    assert store.get_session(session["id"]) is not None
    assert store.get_session(other["id"]) is None
    assert auth.authenticate("settings@example.test", "brand-new-password", "10.200.0.11")
    with pytest.raises(HTTPException) as exc:
        console.settings_password(
            _request("/settings", cookies), "wrong-token", PASSWORD, "another-new-pass",
        )
    assert exc.value.status_code == 403


def test_settings_session_revoke_branches():
    user, session = _signup("revoke@example.test", "10.200.0.12")
    other = store.create_session(user["id"])
    cookies = _session_cookies(session)
    gone = console.settings_revoke_session(
        _request("/settings", cookies), session["csrf_token"], other["id"]
    )
    assert (gone.status_code, gone.headers["location"]) == (303, "/settings?notice=session")
    assert store.get_session(other["id"]) is None
    with pytest.raises(HTTPException) as exc:
        console.settings_revoke_session(
            _request("/settings", cookies), session["csrf_token"], "missing"
        )
    assert exc.value.status_code == 404
    foreign, foreign_session = _signup("revoke-foreign@example.test", "10.200.0.13")
    assert foreign["id"] != user["id"]
    with pytest.raises(HTTPException) as exc:
        console.settings_revoke_session(
            _request("/settings", cookies), session["csrf_token"], foreign_session["id"]
        )
    assert exc.value.status_code == 404
    current = console.settings_revoke_session(
        _request("/settings", cookies), session["csrf_token"], session["id"]
    )
    assert (current.status_code, current.headers["location"]) == (303, "/home")
    assert "Max-Age=0" in current.headers["set-cookie"]
    assert store.get_session(session["id"]) is None


def test_forgot_and_reset_pages():
    bad = console.forgot_submit(_request("/forgot-password"), "not-an-email")
    assert bad.status_code == 400
    notice = _body(console.forgot_submit(_request("/forgot-password"), "who@example.test"))
    assert "not configured" in notice
    assert 'value="abc"' in _body(
        console.reset_page(_request("/reset-password", query=b"token=abc")))
    failed = console.reset_submit(_request("/reset-password"), "bogus-token", "new-password-1")
    assert failed.status_code == 400
    assert "no longer valid" in _body(failed)
    user = auth.register("resetme@example.test", "first-password-1", "10.200.0.14")
    token = store.create_password_reset(user["id"])
    done = console.reset_submit(_request("/reset-password"), token, "second-password-2")
    assert (done.status_code, done.headers["location"]) == (303, "/login?notice=reset")


def test_teams_create_and_list():
    with pytest.raises(HTTPException) as exc:
        console.teams_page(_request("/teams"))
    assert exc.value.status_code == 401
    user, session = _signup("teams@example.test", "10.200.0.15")
    cookies = _session_cookies(session)
    assert "No teams yet" in _body(console.teams_page(_request("/teams", cookies)))
    empty = console.team_create(_request("/teams", cookies), session["csrf_token"], "  ")
    assert empty.status_code == 400
    created = console.team_create(_request("/teams", cookies), session["csrf_token"], "Acme")
    assert created.status_code == 303
    team_id = int(created.headers["location"].rsplit("/", 1)[1])
    assert store.team_role(team_id, user["id"]) == "owner"
    assert "Acme" in _body(console.teams_page(_request("/teams", cookies)))
    with pytest.raises(HTTPException) as exc:
        console.team_create(_request("/teams", cookies), "wrong-token", "Nope")
    assert exc.value.status_code == 403


def _teamed(email, team_name, ip):
    user, session = _signup(email, ip)
    created = console.team_create(
        _request("/teams", _session_cookies(session)), session["csrf_token"], team_name
    )
    return user, session, int(created.headers["location"].rsplit("/", 1)[1])


def test_team_page_visibility_by_membership():
    owner, owner_session, team_id = _teamed("t-owner@example.test", "Visible", "10.200.0.16")
    member = auth.register("t-member@example.test", PASSWORD, "10.200.0.17")
    invite = store.create_invitation(team_id, member["email"], "member", owner["id"])
    store.accept_invitation(invite["token"], member["id"])
    member_session = store.create_session(member["id"])
    outsider, outsider_session = _signup("t-outsider@example.test", "10.200.0.18")
    assert outsider["id"] != owner["id"]
    with pytest.raises(HTTPException) as exc:
        console.team_page(
            _request(f"/teams/{team_id}", _session_cookies(outsider_session)), team_id
        )
    assert exc.value.status_code == 404
    member_page = _body(
        console.team_page(_request(f"/teams/{team_id}", _session_cookies(member_session)), team_id)
    )
    assert "Visible" in member_page
    assert "Invite a teammate" not in member_page
    owner_page = _body(
        console.team_page(_request(f"/teams/{team_id}", _session_cookies(owner_session)), team_id)
    )
    assert "Invite a teammate" in owner_page


def test_team_invite_permissions_and_validation():
    owner, owner_session, team_id = _teamed("i-owner@example.test", "Invites", "10.200.0.19")
    member = auth.register("i-member@example.test", PASSWORD, "10.200.0.20")
    invite = store.create_invitation(team_id, member["email"], "member", owner["id"])
    store.accept_invitation(invite["token"], member["id"])
    member_session = store.create_session(member["id"])
    with pytest.raises(HTTPException) as exc:
        console.team_invite(
            _request(f"/teams/{team_id}", _session_cookies(member_session)),
            team_id, member_session["csrf_token"], "new@example.test", "member",
        )
    assert exc.value.status_code == 403
    owner_cookies = _session_cookies(owner_session)
    bad_role = console.team_invite(
        _request(f"/teams/{team_id}", owner_cookies), team_id,
        owner_session["csrf_token"], "new@example.test", "owner",
    )
    assert bad_role.status_code == 400
    bad_email = console.team_invite(
        _request(f"/teams/{team_id}", owner_cookies), team_id,
        owner_session["csrf_token"], "not-an-email", "member",
    )
    assert bad_email.status_code == 400
    created = console.team_invite(
        _request(f"/teams/{team_id}", owner_cookies), team_id,
        owner_session["csrf_token"], "new@example.test", "member",
    )
    assert created.status_code == 200
    assert "/invitations/accept?token=" in _body(created)


def test_team_role_remove_leave_and_revoke():
    owner, owner_session, team_id = _teamed("m-owner@example.test", "Manage", "10.200.0.21")
    member = auth.register("m-member@example.test", PASSWORD, "10.200.0.22")
    invite = store.create_invitation(team_id, member["email"], "member", owner["id"])
    store.accept_invitation(invite["token"], member["id"])
    cookies = _session_cookies(owner_session)
    csrf = owner_session["csrf_token"]
    demote = console.team_set_role(
        _request(f"/teams/{team_id}", cookies), team_id, csrf, owner["id"], "member"
    )
    assert demote.status_code == 400
    assert "at least one owner" in _body(demote)
    promoted = console.team_set_role(
        _request(f"/teams/{team_id}", cookies), team_id, csrf, member["id"], "admin"
    )
    assert promoted.status_code == 303
    assert store.team_role(team_id, member["id"]) == "admin"
    pending = store.create_invitation(team_id, "rev@example.test", "member", owner["id"])
    revoked = console.team_revoke_invite(
        _request(f"/teams/{team_id}", cookies), team_id, csrf, pending["token"]
    )
    assert revoked.status_code == 303
    assert store.get_invitation(pending["token"]) is None
    removed = console.team_remove_member(
        _request(f"/teams/{team_id}", cookies), team_id, csrf, member["id"]
    )
    assert removed.status_code == 303
    assert store.team_role(team_id, member["id"]) is None
    stuck = console.team_leave(_request(f"/teams/{team_id}", cookies), team_id, csrf)
    assert stuck.status_code == 400
    assert "last owner" in _body(stuck)


def test_team_member_self_remove_redirects_to_list():
    owner, owner_session, team_id = _teamed("s-owner@example.test", "SelfRm", "10.200.0.23")
    member = auth.register("s-member@example.test", PASSWORD, "10.200.0.24")
    invite = store.create_invitation(team_id, member["email"], "member", owner["id"])
    store.accept_invitation(invite["token"], member["id"])
    # Owners/managers route; a member removing themselves uses leave instead.
    member_session = store.create_session(member["id"])
    with pytest.raises(HTTPException) as exc:
        console.team_remove_member(
            _request(f"/teams/{team_id}", _session_cookies(member_session)),
            team_id, member_session["csrf_token"], member["id"],
        )
    assert exc.value.status_code == 403
    left = console.team_leave(
        _request(f"/teams/{team_id}", _session_cookies(member_session)),
        team_id, member_session["csrf_token"],
    )
    assert (left.status_code, left.headers["location"]) == (303, "/teams")
    assert store.team_role(team_id, member["id"]) is None
    assert owner["id"] != member["id"]


def test_invitation_accept_flow():
    owner, _, team_id = _teamed("a-owner@example.test", "JoinUs", "10.200.0.25")
    invite = store.create_invitation(team_id, "joiner@example.test", "member", owner["id"])
    missing = console.invite_accept_page(_request("/invitations/accept", query=b"token=nope"))
    assert missing.status_code == 404
    guest = console.invite_accept_page(
        _request("/invitations/accept", query=f"token={invite['token']}".encode())
    )
    assert guest.status_code == 303
    assert guest.headers["location"].startswith("/login?next=%2Finvitations%2Faccept%3Ftoken%3D")
    wrong = auth.register("wrong-addr@example.test", PASSWORD, "10.200.0.26")
    wrong_session = store.create_session(wrong["id"])
    denied = console.invite_accept(
        _request("/invitations/accept", _session_cookies(wrong_session)),
        wrong_session["csrf_token"], invite["token"],
    )
    assert denied.status_code == 400
    assert "different email" in _body(denied)
    joiner = auth.register("joiner@example.test", PASSWORD, "10.200.0.27")
    joiner_session = store.create_session(joiner["id"])
    confirm = _body(
        console.invite_accept_page(
            _request(
                "/invitations/accept",
                _session_cookies(joiner_session),
                query=f"token={invite['token']}".encode(),
            )
        )
    )
    assert "JoinUs" in confirm
    accepted = console.invite_accept(
        _request("/invitations/accept", _session_cookies(joiner_session)),
        joiner_session["csrf_token"], invite["token"],
    )
    assert (accepted.status_code, accepted.headers["location"]) == (303, f"/teams/{team_id}")
    assert store.team_role(team_id, joiner["id"]) == "member"
    reused = console.invite_accept(
        _request("/invitations/accept", _session_cookies(joiner_session)),
        joiner_session["csrf_token"], invite["token"],
    )
    assert reused.status_code == 400


def test_admin_gate_and_overview(monkeypatch):
    with pytest.raises(HTTPException) as exc:
        console.admin_page(_request("/admin"))
    assert exc.value.status_code == 401
    user, session = _signup("plain@example.test", "10.200.0.28")
    with pytest.raises(HTTPException) as exc:
        console.admin_page(_request("/admin", _session_cookies(session)))
    assert exc.value.status_code == 403
    with pytest.raises(HTTPException) as exc:
        console.admin_overview_api(_request("/api/admin/overview", _session_cookies(session)))
    assert exc.value.status_code == 403
    monkeypatch.setattr(auth, "settings", SimpleNamespace(admin_emails=user["email"]))
    page = _body(console.admin_page(_request("/admin", _session_cookies(session))))
    assert "Admin" in page
    assert "No payment provider is configured" in page
    overview = console.admin_overview_api(
        _request("/api/admin/overview", _session_cookies(session))
    )
    assert overview["users"] >= 1
    assert overview["payments_configured"] is False
    subs = console.admin_subscriptions_api(
        _request("/api/admin/subscriptions", _session_cookies(session))
    )
    assert subs["total"] >= 0


def test_help_page_renders():
    page = _body(console.help_page(_request("/help")))
    assert "The import workflow" in page
    assert "pending downloads" in page


def test_validation_status_unit():
    assert console.validation_status({"rejected_rows": 0}) == "completed"
    assert console.validation_status({"rejected_rows": 2}) == "needs_review"


def test_crumb_for_exact_and_prefix_paths():
    assert console.crumb_for("/home") == "Home"
    assert console.crumb_for("/exports/pending") == "Pending downloads"
    assert console.crumb_for("/exports/abc123") == "Export detail"
    assert console.crumb_for("/teams/7") == "Team detail"
    assert console.crumb_for("/nope") == "ImportGuard"


def test_history_search_status_and_pagination():
    user, session = _signup("filter@example.test", "10.200.0.29")
    cookies = _session_cookies(session)
    clean = _export("clean-ledger.csv", user_id=user["id"], accepted_rows=3, rejected_rows=0)
    messy = _export("messy-leads.csv", user_id=user["id"])
    other = _export("other-file.csv", user_id=user["id"], accepted_rows=3, rejected_rows=0)
    assert clean["id"] and messy["id"] and other["id"]
    found = _body(console.history_page(_request("/history", cookies, query=b"q=ledger")))
    assert "clean-ledger.csv" in found
    assert "messy-leads.csv" not in found
    flagged = _body(
        console.history_page(_request("/history", cookies, query=b"status=needs_review"))
    )
    assert "messy-leads.csv" in flagged
    assert "clean-ledger.csv" not in flagged
    assert "Needs review" in flagged
    completed = _body(
        console.history_page(_request("/history", cookies, query=b"status=completed"))
    )
    assert "clean-ledger.csv" in completed
    assert "Completed" in completed
    bogus = _body(console.history_page(_request("/history", cookies, query=b"status=bogus")))
    assert "messy-leads.csv" in bogus and "clean-ledger.csv" in bogus
    for index in range(21):
        _export(f"bulk-{index:02d}.csv", user_id=user["id"])
    second = _body(console.history_page(_request("/history", cookies, query=b"page=2")))
    assert "Page 2 of 2" in second
    assert "bulk-00.csv" in second
    assert "bulk-20.csv" not in second
    clamped = _body(console.history_page(_request("/history", cookies, query=b"page=99")))
    assert "Page 2 of 2" in clamped
    fallback = _body(console.history_page(_request("/history", cookies, query=b"page=no")))
    assert "Page 1 of 2" in fallback
    empty = _body(console.history_page(_request("/history", cookies, query=b"q=zzz-nope")))
    assert "No imports match these filters" in empty


def test_shell_carries_crumb_plan_and_groups():
    user, session = _signup("shellctx@example.test", "10.200.0.30")
    page = _body(console.settings_page(_request("/settings", _session_cookies(session))))
    assert "YOUR DATA" in page
    assert "Free plan" in page
    assert "of 25 exports" in page
    assert 'aria-current="page">Settings</span>' in page
    assert user["email"] in page
    guest = _body(console.history_page(_request("/history")))
    assert "sidebar-plan" not in guest
    assert 'aria-current="page">Import history</span>' in guest


def test_home_guest_marketing_and_user_operational():
    from app.main import home as home_route

    guest = _body(home_route(_request("/home")))
    assert "Good work starts with a clean import." in guest
    user, session = _signup("homely@example.test", "10.200.0.31")
    _export("home-file.csv", user_id=user["id"])
    mine = _body(home_route(_request("/home", _session_cookies(session))))
    assert "What are we importing today?" in mine
    assert "home-file.csv" in mine
    assert "monthly exports used" in mine


def test_dashboard_attention_stat():
    from app.main import dashboard as dashboard_route

    user, session = _signup("attn@example.test", "10.200.0.32")
    _export("attn-clean.csv", user_id=user["id"], accepted_rows=3, rejected_rows=0)
    _export("attn-messy.csv", user_id=user["id"])
    page = _body(dashboard_route(_request("/dashboard", _session_cookies(session))))
    assert "Needs attention" in page
    assert 'href="/history?status=needs_review"' in page


def test_team_activity_lists_member_metadata_without_foreign_downloads():
    owner, owner_session, team_id = _teamed("act-owner@example.test", "Activity", "10.200.0.33")
    member = auth.register("act-member@example.test", PASSWORD, "10.200.0.34")
    invite = store.create_invitation(team_id, member["email"], "member", owner["id"])
    store.accept_invitation(invite["token"], member["id"])
    own = _export("owner-file.csv", user_id=owner["id"])
    shared = _export("member-file.csv", user_id=member["id"])
    page = _body(
        console.team_page(
            _request(f"/teams/{team_id}", _session_cookies(owner_session)), team_id
        )
    )
    assert "Shared history" in page
    assert "member-file.csv" in page
    assert "act-member@example.test" in page
    assert f"/api/exports/{own['id']}/download" in page
    assert f"/api/exports/{shared['id']}/download" not in page


def test_settings_profile_name_roundtrip():
    user, session = _signup("named@example.test", "10.200.0.35")
    cookies = _session_cookies(session)
    saved = console.settings_profile(
        _request("/settings", cookies), session["csrf_token"], "  Dana Doe  "
    )
    assert (saved.status_code, saved.headers["location"]) == (303, "/settings?notice=profile")
    page = _body(console.settings_page(_request("/settings", cookies)))
    assert "Dana Doe" in page
    assert store.get_user_by_id(user["id"])["name"] == "Dana Doe"
    blank = console.settings_profile(
        _request("/settings", cookies), session["csrf_token"], "  "
    )
    assert blank.status_code == 400
    assert "display name" in _body(blank)


def test_forgot_and_reset_pages_are_standalone():
    assert "Application navigation" not in _body(console.forgot_page(_request("/forgot")))
    assert "Application navigation" not in _body(console.reset_page(_request("/reset")))


def test_every_page_renders_with_expected_status_and_no_none_leak(monkeypatch):
    import app.main as main

    user, session = _signup("sweep@example.test", "10.200.0.36")
    cookies = _session_cookies(session)
    row = _export("sweep-file.csv", user_id=user["id"])
    team = store.create_team("Sweep Team", user["id"])
    invite = store.create_invitation(team["id"], user["email"], "member", user["id"])
    guest_cases = [
        (main.home, ("/home",), 200),
        (main.dashboard, ("/dashboard",), 200),
        (main.billing, ("/billing",), 200),
        (main.payments, ("/payments",), 200),
        (main.workspace, ("/app",), 200),
        (main.workspace_alias, ("/workspace",), 200),
        (main.privacy, ("/privacy",), 200),
        (console.history_page, ("/history",), 200),
        (console.exports_page, ("/exports",), 200),
        (console.help_page, ("/help",), 200),
        (console.forgot_page, ("/forgot-password",), 200),
        (console.reset_page, ("/reset-password",), 200),
        (console.login_page, ("/login",), 200),
        (console.signup_page, ("/signup",), 200),
    ]
    for view, (path,), status in guest_cases:
        response = view(_request(path))
        assert response.status_code == status, path
        assert "None" not in _body(response), path
    authed_cases = [
        (console.pending_page, ("/exports/pending",), 200),
        (console.settings_page, ("/settings",), 200),
        (console.teams_page, ("/teams",), 200),
    ]
    for view, (path,), status in authed_cases:
        response = view(_request(path, cookies))
        assert response.status_code == status, path
        assert "None" not in _body(response), path
    detail = console.export_detail_page(
        _request(f"/exports/{row['id']}", cookies), row["id"]
    )
    assert detail.status_code == 200
    assert "None" not in _body(detail)
    team_page = console.team_page(
        _request(f"/teams/{team['id']}", cookies), team["id"]
    )
    assert team_page.status_code == 200
    assert "None" not in _body(team_page)
    accept = console.invite_accept_page(
        _request("/invitations/accept", cookies, query=f"token={invite['token']}".encode())
    )
    assert accept.status_code == 200
    assert "None" not in _body(accept)
    with pytest.raises(HTTPException) as exc:
        console.admin_page(_request("/admin", cookies))
    assert exc.value.status_code == 403
    monkeypatch.setattr(auth, "settings", SimpleNamespace(admin_emails=user["email"]))
    admin = console.admin_page(_request("/admin", cookies))
    assert admin.status_code == 200
    assert "None" not in _body(admin)

"""FastAPI entrypoint for the local ImportGuard application."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.accounts import get_viewer, list_for_viewer, shell_context
from app.api.accounts import router as accounts_router
from app.api.routes import router
from app.config import settings
from app.services import billing as billing_state

ROOT = Path(__file__).resolve().parent
FRONTEND_DIST = ROOT.parent / "frontend" / "dist"
LANDING_CACHE_HEADERS = {
    "Cache-Control": "no-cache, max-age=0, must-revalidate",
    "Pragma": "no-cache",
}
app = FastAPI(title="ImportGuard", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=ROOT / "templates")
app.include_router(router)
app.include_router(accounts_router)
if FRONTEND_DIST.is_dir():
    app.mount("/web", StaticFiles(directory=FRONTEND_DIST), name="frontend")


@app.get("/")
def landing(request: Request):
    built_landing = FRONTEND_DIST / "index.html"
    if built_landing.is_file():
        return FileResponse(
            built_landing,
            headers=LANDING_CACHE_HEADERS,
        )
    response = templates.TemplateResponse(request, "landing.html", {})
    response.headers.update(LANDING_CACHE_HEADERS)
    return response


@app.get("/app")
def workspace(request: Request):
    return templates.TemplateResponse(
        request,
        "app.html",
        {
            **shell_context(request),
            "meta_enabled": settings.allow_meta_api_calls and bool(settings.model_api_key),
        },
    )


@app.get("/workspace")
def workspace_alias(request: Request):
    return workspace(request)


@app.get("/home")
def home(request: Request):
    viewer = get_viewer(request)
    user = viewer["user"]
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            **shell_context(request),
            "exports": list_for_viewer(request)[:5],
            "billing": billing_state.current_state(user["id"] if user else None),
        },
    )


@app.get("/dashboard")
def dashboard(request: Request):
    viewer = get_viewer(request)
    user = viewer["user"]
    exports = list_for_viewer(request)
    billing = billing_state.current_state(user["id"] if user else None)
    total_rows = sum(row["accepted_rows"] + row["rejected_rows"] for row in exports)
    accepted_rows = sum(row["accepted_rows"] for row in exports)
    success_rate = f"{(accepted_rows / total_rows) * 100:.1f}%" if total_rows else "—"
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            **shell_context(request),
            "exports": exports,
            "saved_count": len(exports),
            "rows_total": total_rows,
            "attention_count": sum(1 for row in exports if row["rejected_rows"] > 0),
            "success_rate": success_rate,
            "billing": billing,
            "retention_days": settings.export_retention_days,
        },
    )


@app.get("/billing")
def billing(request: Request):
    viewer = get_viewer(request)
    user = viewer["user"]
    state = billing_state.current_state(user["id"] if user else None)
    return templates.TemplateResponse(
        request, "billing.html", {**shell_context(request), "billing": state}
    )


@app.get("/payments")
def payments(request: Request):
    return product_page(request, "payments")


def product_page(request: Request, page: str):
    return templates.TemplateResponse(
        request, "product_page.html", {**shell_context(request), "page": page}
    )


@app.get("/privacy")
def privacy(request: Request):
    return templates.TemplateResponse(request, "privacy.html", {})

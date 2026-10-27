"""FastAPI entrypoint for the local ImportGuard application."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.config import settings

ROOT = Path(__file__).resolve().parent
FRONTEND_DIST = ROOT.parent / "frontend" / "dist"
app = FastAPI(title="ImportGuard", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=ROOT / "templates")
app.include_router(router)
if FRONTEND_DIST.is_dir():
    app.mount("/web", StaticFiles(directory=FRONTEND_DIST), name="frontend")


@app.get("/")
def landing(request: Request):
    built_landing = FRONTEND_DIST / "index.html"
    if built_landing.is_file():
        return FileResponse(built_landing)
    return templates.TemplateResponse(request, "landing.html", {})


@app.get("/app")
def workspace(request: Request):
    return templates.TemplateResponse(
        request,
        "app.html",
        {"meta_enabled": settings.allow_meta_api_calls and bool(settings.model_api_key)},
    )


@app.get("/privacy")
def privacy(request: Request):
    return templates.TemplateResponse(request, "privacy.html", {})

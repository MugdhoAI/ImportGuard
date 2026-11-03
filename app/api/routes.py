"""CSV API routes; uploads are processed in memory, export packages recorded."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from app.api.accounts import GUEST_COOKIE, clear_session, current_user, get_viewer, require_user
from app.config import settings
from app.models.schemas import MappingEntry, TargetField
from app.services import store
from app.services.csv_service import (
    CSVError,
    build_zip,
    load_recipe,
    parse_csv,
    process_csv,
    suggest_local,
)
from app.services.meta_client import MetaUnavailable, suggest_mappings
from app.services.rate_limit import RateLimitExceeded, api_limiter

logger = logging.getLogger("importguard.exports")

router = APIRouter()
ROOT = Path(__file__).resolve().parents[2]
PROCESSING_GATE = asyncio.Semaphore(max(1, settings.max_concurrent_processing))


def _api_limit(request: Request, bucket: str, limit: int) -> None:
    try:
        client_host = request.client.host if request.client else "unknown"
        api_limiter.check(
            f"{bucket}:{client_host}", limit, settings.auth_rate_window_seconds
        )
    except RateLimitExceeded as exc:
        raise HTTPException(
            429,
            "This endpoint is receiving too many requests. Try again shortly.",
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc


async def read_upload(upload: UploadFile) -> bytes:
    if not upload.filename or Path(upload.filename).suffix.lower() != ".csv":
        raise HTTPException(400, "Choose a .csv file.")
    data = await upload.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(413, "File exceeds the configured upload limit.")
    return data


def json_model(raw: str, model: type, label: str):
    try:
        if len(raw) > 64 * 1024:
            raise ValueError("request field too large")
        value = json.loads(raw)
        if model is list:
            item_model = TargetField if label == "schema" else MappingEntry
            return [item_model.model_validate(v) for v in value]
        return model.model_validate(value)
    except (ValueError, TypeError, ValidationError) as exc:
        raise HTTPException(422, f"Invalid {label} data.") from exc


def parse_or_http(data: bytes):
    try:
        return parse_csv(
            data,
            max_bytes=settings.max_upload_bytes,
            max_rows=settings.max_data_rows,
            max_columns=settings.max_columns,
        )
    except CSVError as exc:
        raise HTTPException(400, str(exc)) from exc


def export_identity(request: Request) -> dict[str, Any]:
    """Resolve the export owner: signed-in user, guest cookie, or new guest."""
    viewer = get_viewer(request)
    if viewer["user"] is not None:
        return {"user_id": viewer["user"]["id"], "guest_token": None, "issue_guest": False}
    guest_token = request.cookies.get(GUEST_COOKIE)
    if guest_token:
        return {"user_id": None, "guest_token": guest_token, "issue_guest": False}
    return {"user_id": None, "guest_token": store.new_token(), "issue_guest": True}


def maybe_record_export(
    request: Request,
    response: Response,
    filename: str,
    parsed: dict[str, Any],
    result: dict[str, Any],
    report: dict[str, Any],
    package: bytes,
) -> None:
    """Persist a restorable export record. Never fails the user's download."""
    try:
        identity = export_identity(request)
        row = store.record_export(
            filename=filename,
            file_sha256=parsed["sha256"],
            input_rows=report["input_rows"],
            accepted_rows=report["accepted_rows"],
            rejected_rows=report["rejected_rows"],
            recipe_json=json.dumps(result["recipe"], ensure_ascii=False),
            report_json=json.dumps(result["report"], ensure_ascii=False),
            package=package,
            user_id=identity["user_id"],
            guest_token=identity["guest_token"],
        )
        store.purge_expired_exports()
        response.headers["X-Export-Id"] = row["id"]
        if identity["issue_guest"] and identity["guest_token"]:
            response.set_cookie(
                GUEST_COOKIE,
                identity["guest_token"],
                max_age=90 * 24 * 3600,
                httponly=True,
                samesite="lax",
                secure=request.url.scheme == "https",
                path="/",
            )
    except Exception as exc:
        logger.warning("Export recording skipped: %s", type(exc).__name__)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/examples/registrations.csv")
def example_csv():
    return Response(
        (ROOT / "examples/registrations.csv").read_bytes(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="registrations.csv"'},
    )


@router.get("/examples/registrations_schema.json")
def example_schema():
    return Response(
        (ROOT / "examples/registrations_schema.json").read_bytes(),
        media_type="application/json",
    )


@router.post("/api/profile")
async def profile(request: Request, file: Annotated[UploadFile, File()]):
    _api_limit(request, "profile", settings.api_profile_limit_per_window)
    parsed = parse_or_http(await read_upload(file))
    return {
        "filename": Path(file.filename or "upload.csv").name,
        "headers": parsed["headers"],
        "row_count": parsed["row_count"],
        "columns": parsed["columns"],
        "preview": parsed["rows"][:10],
        "sha256": parsed["sha256"],
    }


@router.post("/api/suggest-mappings")
async def mappings(
    request: Request,
    file: Annotated[UploadFile, File()],
    schema_data: Annotated[str, Form()],
    mode: Annotated[str, Form()] = "local",
    include_samples: Annotated[bool, Form()] = False,
):
    _api_limit(request, "suggest", settings.api_suggest_limit_per_window)
    parsed = parse_or_http(await read_upload(file))
    schema = json_model(schema_data, list, "schema")
    if mode == "local":
        return {"source": "local", "mappings": suggest_local(parsed["headers"], schema)}
    if mode != "meta":
        raise HTTPException(400, "Unknown mapping mode.")
    samples = {c["name"]: c["samples"] for c in parsed["columns"]} if include_samples else None
    try:
        return {"source": "meta", "mappings": suggest_mappings(parsed["headers"], schema, samples)}
    except MetaUnavailable as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        # Do not reflect provider exception text, which can contain request details.
        raise HTTPException(502, "Meta request failed; manual mapping is still available.") from exc


@router.post("/api/process")
async def process(
    request: Request,
    file: Annotated[UploadFile, File()],
    schema_data: Annotated[str, Form()],
    mappings_json: Annotated[str, Form()],
):
    _api_limit(request, "process", settings.api_process_limit_per_window)
    async with PROCESSING_GATE:
        parsed = parse_or_http(await read_upload(file))
        schema = json_model(schema_data, list, "schema")
        mappings = json_model(mappings_json, list, "mappings")
        try:
            result, report = process_csv(parsed, schema, mappings)
            package = build_zip(result, schema)
            response = Response(
                package,
                media_type="application/zip",
                headers={
                    "Content-Disposition": 'attachment; filename="importguard-export.zip"',
                    "X-Input-Rows": str(report["input_rows"]),
                    "X-Accepted-Rows": str(report["accepted_rows"]),
                    "X-Rejected-Rows": str(report["rejected_rows"]),
                    "Cache-Control": "no-store",
                },
            )
            maybe_record_export(
                request, response, Path(file.filename or "upload.csv").name,
                parsed, result, report, package,
            )
            return response
        except CSVError as exc:
            raise HTTPException(422, str(exc)) from exc


@router.post("/api/replay")
async def replay(
    request: Request,
    file: Annotated[UploadFile, File()],
    recipe_file: Annotated[UploadFile, File()],
):
    _api_limit(request, "replay", settings.api_replay_limit_per_window)
    async with PROCESSING_GATE:
        parsed = parse_or_http(await read_upload(file))
        if not recipe_file.filename or Path(recipe_file.filename).suffix.lower() != ".json":
            raise HTTPException(400, "Choose a recipe.json file.")
        raw_recipe = await recipe_file.read(64 * 1024 + 1)
        if len(raw_recipe) > 64 * 1024:
            raise HTTPException(413, "Recipe exceeds the 64 KB limit.")
        try:
            recipe = load_recipe(raw_recipe)
            result, report = process_csv(parsed, recipe.schema_fields, recipe.mappings)
        except CSVError as exc:
            raise HTTPException(422, str(exc)) from exc
        package = build_zip(result, recipe.schema_fields)
        response = Response(
            package,
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="importguard-replay.zip"',
                "X-Input-Rows": str(report["input_rows"]),
                "X-Accepted-Rows": str(report["accepted_rows"]),
                "X-Rejected-Rows": str(report["rejected_rows"]),
                "Cache-Control": "no-store",
            },
        )
        maybe_record_export(
            request, response, Path(file.filename or "upload.csv").name,
            parsed, result, report, package,
        )
        return response


@router.get("/api/auth/me")
def auth_me(request: Request) -> JSONResponse:
    user = current_user(request)
    if user is None:
        return JSONResponse({"authenticated": False, "user": None})
    return JSONResponse(
        {
            "authenticated": True,
            "user": {"id": user["id"], "email": user["email"], "name": user["name"]},
        }
    )


@router.post("/api/auth/logout")
def auth_logout(request: Request) -> JSONResponse:
    response = JSONResponse({"ok": True})
    clear_session(request, response)
    return response


@router.get("/api/exports/pending")
def pending_exports(request: Request) -> list[dict[str, Any]]:
    user = require_user(request)
    return store.list_exports(user_id=user["id"], only_pending=True)

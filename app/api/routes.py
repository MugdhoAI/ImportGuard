"""Stateless API routes; upload data is processed in request memory only."""

import json
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import ValidationError

from app.config import settings
from app.models.schemas import MappingEntry, TargetField
from app.services.csv_service import (
    CSVError,
    build_zip,
    load_recipe,
    parse_csv,
    process_csv,
    suggest_local,
)
from app.services.meta_client import MetaUnavailable, suggest_mappings

router = APIRouter()
ROOT = Path(__file__).resolve().parents[2]


async def read_upload(upload: UploadFile) -> bytes:
    if not upload.filename or Path(upload.filename).suffix.lower() != ".csv":
        raise HTTPException(400, "Choose a .csv file.")
    data = await upload.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(413, "File exceeds the configured upload limit.")
    return data


def json_model(raw: str, model: type, label: str):
    try:
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
async def profile(file: Annotated[UploadFile, File()]):
    parsed = parse_or_http(await read_upload(file))
    return {
        "filename": Path(file.filename or "upload.csv").name,
        "headers": parsed["headers"],
        "row_count": parsed["row_count"],
        "columns": parsed["columns"],
        "sha256": parsed["sha256"],
    }


@router.post("/api/suggest-mappings")
async def mappings(
    file: Annotated[UploadFile, File()],
    schema_data: Annotated[str, Form()],
    mode: Annotated[str, Form()] = "local",
    include_samples: Annotated[bool, Form()] = False,
):
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
    file: Annotated[UploadFile, File()],
    schema_data: Annotated[str, Form()],
    mappings_json: Annotated[str, Form()],
):
    parsed = parse_or_http(await read_upload(file))
    schema = json_model(schema_data, list, "schema")
    mappings = json_model(mappings_json, list, "mappings")
    try:
        result, report = process_csv(parsed, schema, mappings)
        return Response(
            build_zip(result, schema),
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="importguard-export.zip"',
                "X-Input-Rows": str(report["input_rows"]),
                "X-Accepted-Rows": str(report["accepted_rows"]),
                "X-Rejected-Rows": str(report["rejected_rows"]),
                "Cache-Control": "no-store",
            },
        )
    except CSVError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post("/api/replay")
async def replay(file: Annotated[UploadFile, File()], recipe_file: Annotated[UploadFile, File()]):
    parsed = parse_or_http(await read_upload(file))
    raw_recipe = await recipe_file.read(64 * 1024 + 1)
    try:
        recipe = load_recipe(raw_recipe)
        result, report = process_csv(parsed, recipe.schema_fields, recipe.mappings)
    except CSVError as exc:
        raise HTTPException(422, str(exc)) from exc
    return Response(
        build_zip(result, recipe.schema_fields),
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="importguard-replay.zip"',
            "X-Input-Rows": str(report["input_rows"]),
            "X-Accepted-Rows": str(report["accepted_rows"]),
            "X-Rejected-Rows": str(report["rejected_rows"]),
            "Cache-Control": "no-store",
        },
    )

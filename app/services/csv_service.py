"""Bounded, deterministic CSV processing and export functions."""

import csv
import hashlib
import io
import json
import re
import zipfile
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from pydantic import ValidationError

from app.models.schemas import MappingEntry, Recipe, TargetField


class CSVError(ValueError):
    """Safe, user-facing CSV or recipe validation error."""


def parse_csv(
    data: bytes, *, max_bytes: int = 5 * 1024 * 1024, max_rows: int = 5000, max_columns: int = 100
) -> dict[str, Any]:
    if len(data) > max_bytes:
        raise CSVError(f"File exceeds the {max_bytes // (1024 * 1024)} MB limit.")
    try:
        text = data.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError as exc:
        raise CSVError("CSV must use UTF-8 encoding (UTF-8 with BOM is supported).") from exc
    if not text.strip():
        raise CSVError("The file is empty.")
    rows = []
    row_numbers = []
    try:
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        previous_line = 0
        for row in reader:
            row_numbers.append(previous_line + 1)
            rows.append(row)
            previous_line = reader.line_num
    except csv.Error as exc:
        raise CSVError("CSV structure is malformed. Check quoting and delimiters.") from exc
    if not rows:
        raise CSVError("The file is empty.")
    headers = rows[0]
    if not headers or len(headers) > max_columns:
        raise CSVError(f"CSV must have between 1 and {max_columns} columns.")
    if any(not h.strip() for h in headers):
        raise CSVError("Column headers cannot be blank.")
    if len(set(headers)) != len(headers):
        raise CSVError("Duplicate column headers are not allowed.")
    body = rows[1:]
    if not body:
        raise CSVError("CSV needs a header and at least one data row.")
    if len(body) > max_rows:
        raise CSVError(f"CSV exceeds the {max_rows} data row limit.")
    records = []
    for number, row in enumerate(body, start=2):
        if len(row) != len(headers):
            raise CSVError(f"Row {number} has {len(row)} cells; expected {len(headers)}.")
        records.append(dict(zip(headers, row, strict=True)))
    profile = [
        {
            "name": h,
            "empty_count": sum(not r[h].strip() for r in records),
            "samples": [r[h] for r in records[:3]],
        }
        for h in headers
    ]
    return {
        "headers": headers,
        "rows": records,
        "row_numbers": row_numbers[1:],
        "row_count": len(records),
        "columns": profile,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def validate_plan(
    headers: list[str], schema: list[TargetField], mappings: list[MappingEntry]
) -> None:
    if not schema:
        raise CSVError("Add at least one target field.")
    names = [field.name for field in schema]
    if len(names) != len(set(names)):
        raise CSVError("Target field names must be unique.")
    targets = [item.target_field for item in mappings]
    sources = [item.source_column for item in mappings if item.source_column is not None]
    if len(targets) != len(set(targets)) or len(sources) != len(set(sources)):
        raise CSVError("Each source and target field can be mapped only once.")
    if set(targets) != set(names):
        raise CSVError("Provide exactly one mapping choice for every target field.")
    for item in mappings:
        if item.source_column is not None and item.source_column not in headers:
            raise CSVError("A mapping references a source column that is not in this CSV.")
        if item.target_field not in names:
            raise CSVError("A mapping references an unknown target field.")


def _transform(value: str, operation: str) -> str:
    if operation == "trim":
        return value.strip()
    if operation == "collapse_whitespace":
        return " ".join(value.split())
    if operation == "lowercase":
        return value.lower()
    if operation == "uppercase":
        return value.upper()
    return value


def _validate_value(value: str, field: TargetField) -> str | None:
    if not value.strip():
        return f"{field.name}: required value is blank" if field.required else None
    try:
        if field.type == "integer" and not re.fullmatch(r"[+-]?\d+", value):
            return f"{field.name}: expected a base-10 integer"
        if field.type == "integer":
            int(value, 10)
        elif field.type == "decimal":
            if not Decimal(value).is_finite():
                raise InvalidOperation
        elif field.type == "boolean" and value.casefold() not in {
            "true",
            "false",
            "yes",
            "no",
            "1",
            "0",
        }:
            return f"{field.name}: expected true/false, yes/no, or 1/0"
        elif field.type == "date_iso":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                return f"{field.name}: expected date in YYYY-MM-DD format"
            date.fromisoformat(value)
    except (ValueError, InvalidOperation):
        return f"{field.name}: invalid {field.type} value"
    return None


def process_csv(
    parsed: dict[str, Any], schema: list[TargetField], mappings: list[MappingEntry]
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_plan(parsed["headers"], schema, mappings)
    by_target = {m.target_field: m for m in mappings}
    accepted, rejected = [], []
    for index, source in enumerate(parsed["rows"]):
        source_number = parsed.get("row_numbers", list(range(2, parsed["row_count"] + 2)))[index]
        output, errors = {}, []
        for field in schema:
            mapping = by_target[field.name]
            value = (
                _transform(source[mapping.source_column], mapping.operation)
                if mapping.source_column is not None
                else ""
            )
            output[field.name] = value
            issue = _validate_value(value, field)
            if issue:
                errors.append(issue)
        if errors:
            rejected.append(
                {
                    "_source_row_number": str(source_number),
                    "_errors": json.dumps(errors, ensure_ascii=False),
                    **source,
                }
            )
        else:
            accepted.append(output)
    recipe = Recipe(schema=schema, mappings=mappings).model_dump(mode="json", by_alias=True)
    report = {
        "created_at": datetime.now(UTC).isoformat(),
        "input_rows": parsed["row_count"],
        "accepted_rows": len(accepted),
        "rejected_rows": len(rejected),
        "input_sha256": parsed["sha256"],
        "recipe_version": 1,
        "mapping_count": len(mappings),
    }
    assert report["input_rows"] == report["accepted_rows"] + report["rejected_rows"]
    return {
        "accepted": accepted,
        "rejected": rejected,
        "recipe": recipe,
        "report": report,
        "source_headers": parsed["headers"],
    }, report


def _safe_cell(value: str) -> str:
    # Prefix formula-leading values, preserving raw values in the processing model.
    if value.startswith(("=", "+", "@", "\t", "\r")) or (
        value.startswith("-") and not re.fullmatch(r"-\d+(?:\.\d+)?", value)
    ):
        return "'" + value
    return value


def _csv_bytes(headers: list[str], records: list[dict[str, str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output, fieldnames=headers, extrasaction="ignore", lineterminator="\r\n"
    )
    writer.writeheader()
    for record in records:
        writer.writerow({key: _safe_cell(str(record.get(key, ""))) for key in headers})
    return output.getvalue().encode("utf-8")


def build_zip(result: dict[str, Any], schema: list[TargetField]) -> bytes:
    accepted_headers = [field.name for field in schema]
    rejected_headers = ["_source_row_number", "_errors", *result["source_headers"]]
    payloads = {
        "accepted.csv": _csv_bytes(accepted_headers, result["accepted"]),
        "rejected.csv": _csv_bytes(rejected_headers, result["rejected"]),
        "recipe.json": json.dumps(result["recipe"], ensure_ascii=False, indent=2).encode(),
        "report.json": json.dumps(result["report"], ensure_ascii=False, indent=2).encode(),
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, payload in payloads.items():
            archive.writestr(name, payload)
    return buffer.getvalue()


def load_recipe(data: bytes) -> Recipe:
    if len(data) > 64 * 1024:
        raise CSVError("Recipe exceeds the 64 KB limit.")
    try:
        return Recipe.model_validate_json(data)
    except (ValidationError, ValueError) as exc:
        raise CSVError("Recipe is invalid or uses an unsupported version or operation.") from exc


def suggest_local(headers: list[str], schema: list[TargetField]) -> list[dict[str, Any]]:
    normalized = {re.sub(r"[^a-z0-9]", "", h.lower()): h for h in headers}
    suggestions = []
    for field in schema:
        key = re.sub(r"[^a-z0-9]", "", field.name.lower())
        suggestions.append(
            {
                "source_column": normalized.get(key),
                "target_field": field.name,
                "operation": "identity",
                "needs_review": True,
                "confidence": "medium" if key in normalized else "low",
                "note": "Local normalized-header suggestion; review before processing.",
            }
        )
    return suggestions

import io
import json
import zipfile

import pytest

from app.models.schemas import MappingEntry, TargetField
from app.services.csv_service import (
    CSVError,
    build_zip,
    load_recipe,
    parse_csv,
    process_csv,
    validate_plan,
)


def test_parse_profile_and_utf8_bom():
    result = parse_csv('\ufeffid,name\n001,Zoë\n002,"A, B"\n'.encode())
    assert result["headers"] == ["id", "name"]
    assert result["row_count"] == 2
    assert result["rows"][0]["id"] == "001"
    assert result["columns"][1]["empty_count"] == 0


def test_rejected_row_number_uses_physical_lines_with_quoted_newlines():
    parsed = parse_csv(b'id,value\n1,"first line\nsecond line"\n2,\n')
    schema = [TargetField(name="id"), TargetField(name="value")]
    mappings = [
        MappingEntry(source_column="id", target_field="id"),
        MappingEntry(source_column="value", target_field="value"),
    ]
    result, _ = process_csv(parsed, schema, mappings)
    assert result["rejected"][0]["_source_row_number"] == "4"


@pytest.mark.parametrize(
    "data, fragment",
    [
        (b"", "empty"),
        (b"id,name", "at least one"),
        (b"id,id\n1,2\n", "Duplicate"),
        (b"id,\n1,2\n", "blank"),
        (b"id,name\n1\n", "Row 2"),
        (b'id,name\n"oops,ok\n', "malformed"),
        (b"id\n\xff\n", "UTF-8"),
    ],
)
def test_rejects_bad_csv(data, fragment):
    with pytest.raises(CSVError, match=fragment):
        parse_csv(data)


def test_enforces_byte_row_and_column_limits():
    with pytest.raises(CSVError, match="MB limit"):
        parse_csv(b"123456", max_bytes=5)
    with pytest.raises(CSVError, match="row limit"):
        parse_csv(b"id\n1\n2\n", max_rows=1)
    with pytest.raises(CSVError, match="columns"):
        parse_csv(b"a,b\n1,2\n", max_columns=1)


def test_rejects_oversized_column_profile():
    parsed = parse_csv(b"a,b\n1,2\n")
    assert [column["name"] for column in parsed["columns"]] == ["a", "b"]


def test_validation_partitions_rows_preserves_order_and_replays_recipe():
    parsed = parse_csv(b"Reg No,Full Name,Payment\n00127, Amina ,yes\n00128,Leo,maybe\n00129,,no\n")
    schema = [
        TargetField(name="student_id"),
        TargetField(name="name"),
        TargetField(name="paid", type="boolean"),
    ]
    mappings = [
        MappingEntry(source_column="Reg No", target_field="student_id"),
        MappingEntry(source_column="Full Name", target_field="name", operation="trim"),
        MappingEntry(source_column="Payment", target_field="paid"),
    ]
    result, report = process_csv(parsed, schema, mappings)
    assert [r["student_id"] for r in result["accepted"]] == ["00127"]
    assert [r["_source_row_number"] for r in result["rejected"]] == ["3", "4"]
    assert report["input_rows"] == report["accepted_rows"] + report["rejected_rows"] == 3
    recipe = load_recipe(json.dumps(result["recipe"]).encode())
    again, _ = process_csv(parsed, recipe.schema_fields, recipe.mappings)
    assert again["accepted"] == result["accepted"]
    assert again["rejected"] == result["rejected"]


@pytest.mark.parametrize(
    "field_type,value,valid",
    [
        ("integer", "-12", True),
        ("integer", "12.0", False),
        ("decimal", "1.20", True),
        ("decimal", "NaN", False),
        ("boolean", "YES", True),
        ("boolean", "perhaps", False),
        ("date_iso", "2026-02-28", True),
        ("date_iso", "03/04/2026", False),
        ("date_iso", "2026-02-30", False),
    ],
)
def test_strict_types(field_type, value, valid):
    data = parse_csv(f"value\n{value}\n".encode())
    field = TargetField(name="out", type=field_type)
    result, _ = process_csv(
        data, [field], [MappingEntry(source_column="value", target_field="out")]
    )
    assert bool(result["accepted"]) is valid


def test_plan_rejects_unknown_and_duplicate_references():
    field = [TargetField(name="out")]
    with pytest.raises(CSVError, match="not in this CSV"):
        validate_plan(["a"], field, [MappingEntry(source_column="missing", target_field="out")])
    with pytest.raises(CSVError, match="only once"):
        validate_plan(
            ["a"],
            [TargetField(name="x"), TargetField(name="y")],
            [
                MappingEntry(source_column="a", target_field="x"),
                MappingEntry(source_column="a", target_field="y"),
            ],
        )


def test_recipe_rejects_unknown_operation_and_version():
    with pytest.raises(CSVError, match="invalid"):
        load_recipe(b'{"version":2,"schema":[],"mappings":[]}')
    with pytest.raises(CSVError, match="invalid"):
        load_recipe(
            b'{"version":1,"schema":[],"mappings":[{"source_column":"x","target_field":"y","operation":"exec","needs_review":true}]}'
        )


def test_safe_export_and_zip_contract():
    parsed = parse_csv(b"input\n=1+1\n-15\n@cmd\n")
    schema = [TargetField(name="value")]
    mappings = [MappingEntry(source_column="input", target_field="value")]
    result, _ = process_csv(parsed, schema, mappings)
    archive = zipfile.ZipFile(io.BytesIO(build_zip(result, schema)))
    assert set(archive.namelist()) == {"accepted.csv", "rejected.csv", "recipe.json", "report.json"}
    exported = archive.read("accepted.csv").decode()
    assert "'=1+1" in exported and "-15" in exported and "'@cmd" in exported
    recipe_text = archive.read("recipe.json").decode()
    assert "'=1+1" not in recipe_text and "'@cmd" not in recipe_text

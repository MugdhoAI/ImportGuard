import pytest

from app.models.schemas import MappingEntry, TargetField
from app.services.csv_service import parse_csv, process_csv


def _run(value, operation, field_type="string"):
    parsed = parse_csv(f'value\n"{value}"\n'.encode())
    field = TargetField(name="out", type=field_type)
    mapping = MappingEntry(source_column="value", target_field="out", operation=operation)
    result, _ = process_csv(parsed, [field], [mapping])
    return result


@pytest.mark.parametrize(
    "value, operation, expected",
    [
        ("  Keep  Me  ", "identity", "  Keep  Me  "),
        ("  hello  ", "trim", "hello"),
        ("Amina   Begum", "collapse_whitespace", "Amina Begum"),
        ("  Amina   Begum  ", "collapse_whitespace", "Amina Begum"),
        ("HeLLo World", "lowercase", "hello world"),
        ("HeLLo World", "uppercase", "HELLO WORLD"),
    ],
)
def test_transform_operations(value, operation, expected):
    result = _run(value, operation)
    assert result["accepted"] == [{"out": expected}]
    assert result["rejected"] == []


def test_identity_is_the_default_operation():
    parsed = parse_csv(b"value\n  spaced  \n")
    field = TargetField(name="out")
    mapping = MappingEntry(source_column="value", target_field="out")
    assert mapping.operation == "identity"
    result, _ = process_csv(parsed, [field], [mapping])
    assert result["accepted"] == [{"out": "  spaced  "}]


def test_trim_runs_before_integer_validation():
    trimmed = _run(" 42 ", "trim", field_type="integer")
    assert trimmed["accepted"] == [{"out": "42"}]
    untrimmed = _run(" 42 ", "identity", field_type="integer")
    assert untrimmed["accepted"] == []
    assert len(untrimmed["rejected"]) == 1

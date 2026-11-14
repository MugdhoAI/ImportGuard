from app.models.schemas import TargetField
from app.services.csv_service import suggest_local


def test_suggest_local_matches_exact_headers():
    schema = [TargetField(name="student_id"), TargetField(name="name")]
    suggestions = suggest_local(["student_id", "name"], schema)
    assert [s["source_column"] for s in suggestions] == ["student_id", "name"]
    assert [s["confidence"] for s in suggestions] == ["medium", "medium"]


def test_suggest_local_matches_after_normalization():
    schema = [
        TargetField(name="student_id"),
        TargetField(name="full_name"),
        TargetField(name="payment_date"),
    ]
    suggestions = suggest_local(["Student ID", "Full-Name", "PAYMENT DATE"], schema)
    assert [s["source_column"] for s in suggestions] == [
        "Student ID",
        "Full-Name",
        "PAYMENT DATE",
    ]
    assert all(s["confidence"] == "medium" for s in suggestions)


def test_suggest_local_unmatched_field_gets_no_source_and_low_confidence():
    schema = [TargetField(name="student_id"), TargetField(name="nickname")]
    suggestions = suggest_local(["Student ID", "Name"], schema)
    assert suggestions[0]["source_column"] == "Student ID"
    assert suggestions[1]["source_column"] is None
    assert suggestions[1]["confidence"] == "low"


def test_suggest_local_always_needs_review_and_uses_identity():
    schema = [TargetField(name="email"), TargetField(name="missing_field")]
    suggestions = suggest_local(["Email"], schema)
    assert [s["target_field"] for s in suggestions] == ["email", "missing_field"]
    assert all(s["needs_review"] is True for s in suggestions)
    assert all(s["operation"] == "identity" for s in suggestions)


def test_suggest_local_with_no_headers_returns_low_confidence_for_all():
    schema = [TargetField(name="email")]
    suggestions = suggest_local([], schema)
    assert suggestions[0]["source_column"] is None
    assert suggestions[0]["confidence"] == "low"

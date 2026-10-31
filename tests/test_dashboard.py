"""Dashboard route tests: guest, user, isolation, and download links."""

import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _process(client_):
    schema = [{"name": "id", "type": "string", "required": True}]
    mappings = [
        {
            "source_column": "ID",
            "target_field": "id",
            "operation": "identity",
            "needs_review": True,
        }
    ]
    return client_.post(
        "/api/process",
        files={"file": ("dash.csv", b"ID\n001\n002\n")},
        data={"schema_data": json.dumps(schema), "mappings_json": json.dumps(mappings)},
    )


def test_guest_dashboard_empty_then_lists_session_exports():
    fresh = TestClient(app)
    empty = fresh.get("/dashboard").text
    assert "Dashboard" in empty
    assert "No saved activity yet" in empty
    assert "Create an account" in empty
    export_id = _process(fresh).headers["X-Export-Id"]
    page = fresh.get("/dashboard").text
    assert "dash.csv" in page
    assert "Sign in to download" in page
    assert "/login?next=/dashboard" in page
    assert f"/api/exports/{export_id}/download" not in page
    assert "<strong>1</strong>" in page


def test_user_dashboard_isolated_per_account():
    first, second = TestClient(app), TestClient(app)
    password = "a-strong-password"
    first.post("/auth/signup", data={"email": "dash1@example.test", "password": password})
    second.post("/auth/signup", data={"email": "dash2@example.test", "password": password})
    _process(first)
    assert "dash1@example.test" in first.get("/dashboard").text
    assert "dash.csv" in first.get("/dashboard").text
    assert "dash.csv" not in second.get("/dashboard").text
    assert "No saved activity yet" in second.get("/dashboard").text

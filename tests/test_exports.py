"""Export recording, restoration, and guest-claim tests."""

import io
import json
import os
import zipfile
from types import SimpleNamespace

from fastapi import Request
from fastapi.responses import Response
from fastapi.testclient import TestClient

from app.api.accounts import GUEST_COOKIE, SESSION_COOKIE
from app.api.routes import export_identity, maybe_record_export
from app.main import app
from app.services import auth, store

client = TestClient(app)


def _request(path="/api/process", cookies=None):
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [],
        "server": ("testserver", 80),
        "client": ("testclient", 50000),
    }
    request = Request(scope)
    if cookies:
        request._cookies = cookies
    return request


def _result(report_rows=(3, 2, 1)):
    total, accepted, rejected = report_rows
    return (
        {"recipe": {"version": 1}, "report": {"input_rows": total}},
        {"input_rows": total, "accepted_rows": accepted, "rejected_rows": rejected},
    )


def test_export_identity_branches():
    assert export_identity(_request())["issue_guest"] is True
    assert export_identity(_request())["guest_token"]
    keeping = export_identity(_request(cookies={GUEST_COOKIE: "guest-abc"}))
    assert (keeping["guest_token"], keeping["issue_guest"]) == ("guest-abc", False)
    user = auth.register("idn@example.test", "a-strong-password", "10.9.0.1")
    session = store.create_session(user["id"])
    owned = export_identity(_request(cookies={SESSION_COOKIE: session["id"]}))
    assert (owned["user_id"], owned["guest_token"]) == (user["id"], None)


def test_maybe_record_export_sets_header_and_guest_cookie_once():
    result, report = _result()
    parsed = {"sha256": "deadbeef", "headers": ["a"]}
    first = Response(b"zip")
    maybe_record_export(_request(), first, "in.csv", parsed, result, report, b"zip-bytes")
    assert first.headers["X-Export-Id"]
    guest = first.headers["set-cookie"]
    assert GUEST_COOKIE in guest
    token = [part for part in guest.split(";")[0].split("=")][1]
    second = Response(b"zip")
    maybe_record_export(
        _request(cookies={GUEST_COOKIE: token}), second, "in.csv", parsed, result, report, b"z"
    )
    assert second.headers["X-Export-Id"]
    assert "set-cookie" not in second.headers


def test_maybe_record_export_never_breaks_download(monkeypatch):
    def _boom(*args, **kwargs):
        raise RuntimeError("db gone")

    monkeypatch.setattr(store, "record_export", _boom)
    result, report = _result()
    response = Response(b"zip")
    maybe_record_export(_request(), response, "in.csv", {"sha256": "x"}, result, report, b"z")
    assert "X-Export-Id" not in response.headers


def _process(client_, filename="in.csv"):
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
        files={"file": (filename, b"ID\n001\n002\n")},
        data={"schema_data": json.dumps(schema), "mappings_json": json.dumps(mappings)},
    )


def test_process_records_guest_export_and_restores_it():
    response = _process(client)
    assert response.status_code == 200
    export_id = response.headers["X-Export-Id"]
    assert client.cookies.get(GUEST_COOKIE)
    history = client.get("/api/exports").json()["exports"]
    assert [row["id"] for row in history] == [export_id]
    assert history[0]["package_stored"] == 1
    assert "package" not in history[0]
    assert client.get(f"/api/exports/{export_id}/download").status_code == 401
    signup = client.post(
        "/auth/signup",
        data={"email": "restore-claim@example.test", "password": "a-strong-password"},
        follow_redirects=False,
    )
    assert signup.status_code == 303
    pending = client.get("/api/exports/pending").json()
    assert [row["id"] for row in pending] == [export_id]
    download = client.get(f"/api/exports/{export_id}/download")
    assert download.status_code == 200
    assert set(zipfile.ZipFile(io.BytesIO(download.content)).namelist()) == {
        "accepted.csv",
        "rejected.csv",
        "recipe.json",
        "report.json",
    }
    assert client.get("/api/exports/pending").json() == []
    client.cookies.clear()


def test_signup_claims_guest_exports():
    response = _process(client)
    export_id = response.headers["X-Export-Id"]
    signup = client.post(
        "/auth/signup",
        data={"email": "claim@example.test", "password": "a-strong-password"},
        follow_redirects=False,
    )
    assert signup.status_code == 303
    history = client.get("/api/exports").json()["exports"]
    assert [row["id"] for row in history] == [export_id]
    assert client.get(f"/api/exports/{export_id}/download").status_code == 200


def test_download_rejects_foreign_and_missing_packages(monkeypatch):
    client.cookies.clear()
    other = TestClient(app)
    export_id = _process(other).headers["X-Export-Id"]
    assert client.get(f"/api/exports/{export_id}/download").status_code == 401
    client.post(
        "/auth/signup",
        data={"email": "foreign@example.test", "password": "a-strong-password"},
    )
    assert client.get(f"/api/exports/{export_id}/download").status_code == 404
    other.cookies.clear()
    other.post(
        "/auth/signup",
        data={"email": "bigowner@example.test", "password": "a-strong-password"},
    )
    monkeypatch.setattr(
        store,
        "settings",
        SimpleNamespace(
            database_path=os.environ["IMPORTGUARD_DB"],
            export_retention_days=7,
            max_stored_package_bytes=1,
        ),
    )
    big_id = _process(other).headers["X-Export-Id"]
    assert other.get(f"/api/exports/{big_id}/download").status_code == 404
    row = store.get_export(big_id)
    assert row is not None and row["package_stored"] == 0
    client.cookies.clear()
    other.cookies.clear()

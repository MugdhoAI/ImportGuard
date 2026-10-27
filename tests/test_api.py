import io
import json
import zipfile

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pages_health_and_examples():
    assert client.get("/health").json() == {"status": "ok"}
    assert "predictable" in client.get("/").text
    assert "Choose your source" in client.get("/app").text
    assert "Privacy" in client.get("/privacy").text
    assert client.get("/examples/registrations.csv").status_code == 200


def test_profile_rejects_bad_extension_and_reports_local_profile():
    assert client.post("/api/profile", files={"file": ("data.txt", b"id\n1\n")}).status_code == 400
    response = client.post("/api/profile", files={"file": ("data.csv", b"id,name\n001,Amina\n")})
    assert response.status_code == 200
    assert response.json()["row_count"] == 1


def test_process_export_and_recipe_replay():
    data = b"ID,Flag\n001,true\n002,maybe\n"
    schema = [
        {"name": "id", "type": "string", "required": True},
        {"name": "flag", "type": "boolean", "required": True},
    ]
    mappings = [
        {
            "source_column": "ID",
            "target_field": "id",
            "operation": "identity",
            "needs_review": True,
        },
        {
            "source_column": "Flag",
            "target_field": "flag",
            "operation": "identity",
            "needs_review": True,
        },
    ]
    response = client.post(
        "/api/process",
        files={"file": ("in.csv", data)},
        data={"schema_data": json.dumps(schema), "mappings_json": json.dumps(mappings)},
    )
    assert response.status_code == 200
    assert response.headers["x-accepted-rows"] == "1"
    package = zipfile.ZipFile(io.BytesIO(response.content))
    recipe = package.read("recipe.json")
    assert set(package.namelist()) == {"accepted.csv", "rejected.csv", "recipe.json", "report.json"}
    replay = client.post(
        "/api/replay",
        files={
            "file": ("second.csv", b"ID,Flag\n003,false\n"),
            "recipe_file": ("recipe.json", recipe, "application/json"),
        },
    )
    assert replay.status_code == 200
    assert replay.headers["x-accepted-rows"] == "1"
    assert b"003,false" in zipfile.ZipFile(io.BytesIO(replay.content)).read("accepted.csv")


def test_manual_suggestions_work_and_meta_path_stays_disabled():
    data = b"student id,name\n001,Amina\n"
    schema = [{"name": "studentid", "type": "string", "required": True}]
    local = client.post(
        "/api/suggest-mappings",
        files={"file": ("a.csv", data)},
        data={"schema_data": json.dumps(schema), "mode": "local"},
    )
    assert local.status_code == 200 and local.json()["source"] == "local"
    meta = client.post(
        "/api/suggest-mappings",
        files={"file": ("a.csv", data)},
        data={"schema_data": json.dumps(schema), "mode": "meta"},
    )
    assert meta.status_code == 503
    assert "disabled" in meta.json()["detail"]

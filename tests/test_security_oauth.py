"""Targeted OAuth configuration and abuse-protection tests."""

import json
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import auth, oauth, store
from app.services.rate_limit import SlidingWindowLimiter


def test_sliding_window_limiter_blocks_and_expires(monkeypatch):
    limiter = SlidingWindowLimiter()
    clock = iter([100.0, 100.1, 106.0])
    monkeypatch.setattr("app.services.rate_limit.monotonic", lambda: next(clock))
    limiter.check("ip", 1, 5)
    try:
        limiter.check("ip", 1, 5)
    except Exception as exc:
        assert getattr(exc, "retry_after", 0) >= 1
    else:
        raise AssertionError("second request should be rate limited")
    limiter.check("ip", 1, 5)


def test_profile_endpoint_rate_limit_is_configurable(monkeypatch):
    from app.api import routes

    routes.api_limiter.clear()
    monkeypatch.setattr(
        routes,
        "settings",
        SimpleNamespace(
            api_profile_limit_per_window=1,
            auth_rate_window_seconds=300,
            max_upload_bytes=1024 * 1024,
            max_data_rows=5000,
            max_columns=100,
        ),
    )
    client = TestClient(app)
    files = {"file": ("sample.csv", b"id\n1\n", "text/csv")}
    assert client.post("/api/profile", files=files).status_code == 200
    assert client.post("/api/profile", files=files).status_code == 429
    routes.api_limiter.clear()


def test_upload_limits_and_malformed_encoding_are_rejected(monkeypatch):
    from app.api import routes

    routes.api_limiter.clear()
    monkeypatch.setattr(
        routes,
        "settings",
        SimpleNamespace(
            api_profile_limit_per_window=120,
            auth_rate_window_seconds=300,
            max_upload_bytes=4,
            max_data_rows=5000,
            max_columns=100,
        ),
    )
    client = TestClient(app)
    oversized = client.post("/api/profile", files={"file": ("large.csv", b"id\n123\n")})
    assert oversized.status_code == 413
    malformed = client.post("/api/profile", files={"file": ("bad.csv", b"\xff\n")})
    assert malformed.status_code == 400
    assert "UTF-8" in malformed.json()["detail"]
    routes.api_limiter.clear()


def test_concurrent_processing_requests_complete_without_cross_request_failure():
    schema = [{"name": "id", "type": "string", "required": True}]
    mappings = [{
        "source_column": "id", "target_field": "id", "operation": "identity",
        "needs_review": True,
    }]

    def process_once(_index):
        client = TestClient(app)
        return client.post(
            "/api/process",
            files={"file": ("parallel.csv", b"id\n1\n")},
            data={
                "schema_data": json.dumps(schema),
                "mappings_json": json.dumps(mappings),
            },
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(process_once, range(2)))
    observed = [
        (response.status_code, response.headers["x-accepted-rows"])
        for response in responses
    ]
    assert observed == [(200, "1"), (200, "1")]


def test_oauth_options_are_honest_when_unconfigured():
    client = TestClient(app)
    page = client.get("/signup").text
    assert "Google unavailable" in page
    assert "GitHub unavailable" in page
    assert "/auth/oauth/google" not in page
    assert "/auth/oauth/github" not in page
    unavailable = client.get("/auth/oauth/google", follow_redirects=False)
    assert unavailable.status_code == 303
    assert "oauth_status=unavailable" in unavailable.headers["location"]


def test_oauth_callback_rejects_missing_or_expired_state(tmp_path):
    response = TestClient(app).get(
        "/auth/oauth/google/callback?state=missing&code=code",
        follow_redirects=False,
    )
    assert response.status_code == 400
    assert "session expired" in response.text
    db = str(tmp_path / "oauth-expired-test.db")
    state = store.create_oauth_state(
        provider="google", code_verifier="verifier", next_path="/dashboard",
        ttl_seconds=-1, db_path=db,
    )
    assert store.consume_oauth_state(state, db_path=db) is None


def test_signup_failures_share_the_auth_cooldown():
    auth._failed_logins.clear()
    auth._failed_accounts.clear()
    ip = "198.51.100.88"
    for _ in range(10):
        try:
            auth.register("not-an-email", "a-strong-password", ip)
        except auth.AuthError:
            pass
    try:
        auth.register("not-an-email", "a-strong-password", ip)
    except auth.AuthError as exc:
        assert "Too many attempts" in str(exc)
    else:
        raise AssertionError("signup should be throttled after repeated failures")


def test_auth_failures_are_limited_per_account_across_ips():
    auth._failed_logins.clear()
    auth._failed_accounts.clear()
    for index in range(10):
        try:
            auth.authenticate("locked@example.test", "wrong-password", f"198.51.100.{index}")
        except auth.AuthError:
            pass
    with pytest.raises(auth.AuthError, match="Too many attempts"):
        auth.authenticate("locked@example.test", "wrong-password", "203.0.113.44")


def test_oauth_begin_uses_state_and_pkce(monkeypatch):
    configured = SimpleNamespace(
        google_oauth_client_id="google-client",
        google_oauth_client_secret="google-secret",
        google_oauth_redirect_uri="http://127.0.0.1:8000/auth/oauth/google/callback",
        github_oauth_client_id="",
        github_oauth_client_secret="",
        github_oauth_redirect_uri="",
        oauth_state_ttl_seconds=600,
    )
    monkeypatch.setattr(oauth, "settings", configured)
    monkeypatch.setattr(oauth.store, "create_oauth_state", lambda **kwargs: "state-token")
    url = oauth.begin("google", next_path="/dashboard")
    query = parse_qs(urlparse(url).query)
    assert query["state"] == ["state-token"]
    assert query["code_challenge_method"] == ["S256"]
    assert query["redirect_uri"] == [configured.google_oauth_redirect_uri]


def test_oauth_finish_creates_and_then_reuses_verified_identity(monkeypatch):
    db = None  # pytest's isolated application database is used by the store.
    configured = SimpleNamespace(
        google_oauth_client_id="google-client",
        google_oauth_client_secret="google-secret",
        google_oauth_redirect_uri="http://127.0.0.1:8000/auth/oauth/google/callback",
        github_oauth_client_id="",
        github_oauth_client_secret="",
        github_oauth_redirect_uri="",
        oauth_state_ttl_seconds=600,
    )
    monkeypatch.setattr(oauth, "settings", configured)
    monkeypatch.setattr(oauth, "exchange_code", lambda provider, code, verifier: "access-token")
    monkeypatch.setattr(
        oauth,
        "fetch_identity",
        lambda provider, token: {
            "subject": "google-subject-test",
            "email": "oauth-new@example.test",
            "name": "OAuth Tester",
        },
    )
    state = {
        "provider": "google", "code_verifier": "verifier", "user_id": None,
        "next_path": "/dashboard",
    }
    first = oauth.finish("google", state, "code", None)
    assert first["user"]["email"] == "oauth-new@example.test"
    linked = store.get_oauth_account("google", "google-subject-test", db)
    assert linked and linked["user_id"] == first["user"]["id"]
    second = oauth.finish("google", state, "code", None)
    assert second["user"]["id"] == first["user"]["id"]


def test_oauth_link_requires_exact_signed_in_email(monkeypatch):
    configured = SimpleNamespace(
        google_oauth_client_id="google-client",
        google_oauth_client_secret="google-secret",
        google_oauth_redirect_uri="http://127.0.0.1:8000/auth/oauth/google/callback",
        github_oauth_client_id="",
        github_oauth_client_secret="",
        github_oauth_redirect_uri="",
        oauth_state_ttl_seconds=600,
    )
    monkeypatch.setattr(oauth, "settings", configured)
    monkeypatch.setattr(oauth, "exchange_code", lambda provider, code, verifier: "access-token")
    monkeypatch.setattr(
        oauth,
        "fetch_identity",
        lambda provider, token: {
            "subject": "google-link-test",
            "email": "other@example.test",
            "name": "Other",
        },
    )
    with pytest.raises(oauth.OAuthError, match="does not match"):
        oauth.finish(
            "google",
            {"provider": "google", "code_verifier": "verifier", "user_id": 9},
            "code",
            {"id": 9, "email": "owner@example.test"},
        )

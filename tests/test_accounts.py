"""Account route tests: signup/login/logout/delete and export endpoints.

All requests share the TestClient IP, so keep total failing-auth attempts in
this file well under the 10-per-window login throttle.
"""

from fastapi.testclient import TestClient

from app.api.accounts import GUEST_COOKIE, SESSION_COOKIE
from app.main import app
from app.services import store

client = TestClient(app)


def _signup(email, password="a-strong-password"):
    return client.post(
        "/auth/signup", data={"email": email, "password": password}, follow_redirects=False
    )


def _login(email, password="a-strong-password", **extra):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password, **extra},
        follow_redirects=False,
    )


def _csrf():
    session = store.get_session(client.cookies.get(SESSION_COOKIE))
    assert session is not None
    return session["csrf_token"]


def test_auth_pages_render_and_redirect_when_signed_in():
    assert "Create account" in client.get("/signup").text
    assert "Sign in to your workspace" in client.get("/login").text
    assert _signup("pages@example.test").status_code == 303
    assert client.get("/login", follow_redirects=False).status_code == 303
    assert client.get("/signup", follow_redirects=False).status_code == 303
    client.post("/auth/logout", data={"csrf_token": _csrf()})


def test_signup_validates_and_sets_session():
    response = _signup("new@example.test")
    assert response.status_code == 303
    assert response.headers["location"] == "/dashboard"
    assert client.cookies.get(SESSION_COOKIE)
    assert _signup("new@example.test").status_code == 400
    assert _signup("not-an-email").status_code == 400
    assert _signup("short@example.test", "short").status_code == 400
    client.post("/auth/logout", data={"csrf_token": _csrf()})


def test_login_success_failure_and_next_sanitization():
    _signup("luis@example.test")
    client.post("/auth/logout", data={"csrf_token": _csrf()})
    good = _login("luis@example.test")
    assert good.status_code == 303
    assert client.cookies.get(SESSION_COOKIE)
    client.post("/auth/logout", data={"csrf_token": _csrf()})
    bad = _login("luis@example.test", "wrong-password")
    assert bad.status_code == 401
    assert "Invalid email or password" in bad.text
    evil = _login("luis@example.test", "a-strong-password", next="//evil.test/x")
    assert evil.headers["location"] == "/dashboard"
    client.post("/auth/logout", data={"csrf_token": _csrf()})


def test_logout_requires_csrf_and_clears_session():
    _signup("mia@example.test")
    assert client.post("/auth/logout", data={"csrf_token": "wrong"}).status_code == 403
    response = client.post("/auth/logout", data={"csrf_token": _csrf()}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/home"


def test_delete_account_removes_user_and_history():
    _signup("ned@example.test")
    response = client.post(
        "/auth/delete",
        data={"csrf_token": _csrf(), "password": "wrong-password"},
        follow_redirects=False,
    )
    assert response.status_code == 401
    gone = client.post(
        "/auth/delete",
        data={"csrf_token": _csrf(), "password": "a-strong-password"},
        follow_redirects=False,
    )
    assert gone.status_code == 303
    assert store.get_user_by_email("ned@example.test") is None
    assert _login("ned@example.test").status_code == 401


def test_export_endpoints_require_ownership():
    assert client.get("/api/exports").json() == {"exports": []}
    assert client.get("/api/exports/nope/download").status_code == 401
    assert client.post("/api/exports/claim").status_code == 401
    client.cookies.set(GUEST_COOKIE, "guest-without-exports")
    assert client.get("/api/exports").json() == {"exports": []}
    client.cookies.clear()
    _signup("gate@example.test")
    assert client.get("/api/exports/nope/download").status_code == 404
    client.post("/auth/logout", data={"csrf_token": _csrf()})

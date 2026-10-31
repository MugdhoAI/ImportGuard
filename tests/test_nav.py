"""Navigation tests: complete sidebar and auth state on every shell page."""

from fastapi.testclient import TestClient

from app.api.accounts import SESSION_COOKIE
from app.main import app
from app.services import store

client = TestClient(app)
SHELL_PAGES = (
    "/home", "/dashboard", "/app", "/workspace", "/billing", "/payments",
    "/history", "/exports", "/help",
)
NAV_LINKS = (
    "/home", "/dashboard", "/app", "/history", "/exports",
    "/billing", "/payments", "/teams", "/settings", "/help",
)
GUEST_MARKED = (
    "/home", "/dashboard", "/app", "/history", "/exports",
    "/billing", "/payments", "/help",
)


def test_guest_sidebar_complete_with_sign_in():
    for path in SHELL_PAGES:
        page = client.get(path).text
        for destination in NAV_LINKS:
            assert f'href="{destination}"' in page
        assert 'href="/login"' in page
        assert 'href="/signup"' in page
        assert "Sign out" not in page


def test_current_page_marked_for_each_destination():
    for destination in GUEST_MARKED:
        page = client.get(destination).text
        assert f'href="{destination}" aria-current="page"' in page
    workspace = client.get("/workspace").text
    assert 'href="/app" aria-current="page"' in workspace


def test_signed_in_sidebar_shows_user_and_working_sign_out():
    client.post(
        "/auth/signup",
        data={"email": "nav@example.test", "password": "a-strong-password"},
        follow_redirects=False,
    )
    page = client.get("/dashboard").text
    assert "nav@example.test" in page
    assert "Sign out" in page
    assert 'href="/admin"' not in page
    teams = client.get("/teams").text
    assert 'href="/teams" aria-current="page"' in teams
    settings_page = client.get("/settings").text
    assert 'href="/settings" aria-current="page"' in settings_page
    session = store.get_session(client.cookies.get(SESSION_COOKIE))
    assert session is not None
    assert session["csrf_token"] in page
    response = client.post(
        "/auth/logout", data={"csrf_token": session["csrf_token"]}, follow_redirects=False
    )
    assert response.status_code == 303
    assert "Sign in" in client.get("/dashboard").text

"""Auth service unit tests: hashing, validation, register, login, throttling."""

import pytest

from app.services import auth


def test_password_hash_roundtrip_and_rejects_wrong_or_malformed():
    hashed = auth.hash_password("correct-horse-99")
    assert auth.verify_password("correct-horse-99", hashed)
    assert not auth.verify_password("wrong-password", hashed)
    assert not auth.verify_password("correct-horse-99", "not-a-hash")
    assert not auth.verify_password("correct-horse-99", "md5$1$ab$cd")


def test_email_normalization_and_validation():
    assert auth.normalize_email("  Ana@Example.Test ") == "ana@example.test"
    for bad in ("no-at-sign", "a@b", "@x.test", "a b@c.test", "x" * 250 + "@y.test"):
        with pytest.raises(auth.AuthError, match="valid email"):
            auth.normalize_email(bad)


def test_password_length_bounds():
    auth.validate_password("exactly-10")
    with pytest.raises(auth.AuthError, match="10 and 128"):
        auth.validate_password("short")
    with pytest.raises(auth.AuthError, match="10 and 128"):
        auth.validate_password("x" * 129)


def test_register_duplicate_and_authenticate(tmp_path):
    db = str(tmp_path / "auth.db")
    user = auth.register("uma@example.test", "a-strong-password", "10.1.0.1", db)
    assert user["email"] == "uma@example.test"
    with pytest.raises(auth.AuthError, match="already exists"):
        auth.register("uma@example.test", "another-password", "10.1.0.2", db)
    assert auth.authenticate("uma@example.test", "a-strong-password", "10.1.0.3", db)["id"]
    with pytest.raises(auth.AuthError, match="Invalid email or password"):
        auth.authenticate("uma@example.test", "wrong-password", "10.1.0.4", db)
    with pytest.raises(auth.AuthError, match="Invalid email or password"):
        auth.authenticate("ghost@example.test", "a-strong-password", "10.1.0.5", db)


def test_failed_logins_throttle_then_release(tmp_path, monkeypatch):
    db = str(tmp_path / "throttle.db")
    auth.register("vic@example.test", "a-strong-password", "10.2.0.9", db)
    for _ in range(10):
        with pytest.raises(auth.AuthError, match="Invalid email or password"):
            auth.authenticate("vic@example.test", "wrong-password", "10.2.0.1", db)
    with pytest.raises(auth.AuthError, match="Too many attempts"):
        auth.authenticate("vic@example.test", "wrong-password", "10.2.0.1", db)
    monkeypatch.setattr(auth, "_now", lambda: auth.time.monotonic() + 301)
    assert auth.authenticate("vic@example.test", "a-strong-password", "10.2.0.1", db)["email"]


def test_csrf_token_must_match_session():
    session = {"csrf_token": "token-abc"}
    assert auth.csrf_valid(session, "token-abc")
    assert not auth.csrf_valid(session, "token-wrong")
    assert not auth.csrf_valid(session, None)
    assert not auth.csrf_valid(None, "token-abc")


def test_is_admin_matches_configured_emails(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(
        auth, "settings", SimpleNamespace(admin_emails=" Boss@Example.test,ops@example.test ")
    )
    assert auth.is_admin({"email": "boss@example.test"})
    assert auth.is_admin({"email": "ops@example.test"})
    assert not auth.is_admin({"email": "user@example.test"})
    assert not auth.is_admin(None)
    monkeypatch.setattr(auth, "settings", SimpleNamespace(admin_emails=""))
    assert not auth.is_admin({"email": "boss@example.test"})


def test_change_password_rotates_and_keeps_current_session(tmp_path):
    from app.services import store

    db = str(tmp_path / "change.db")
    user = auth.register("wren@example.test", "old-password-1", "10.3.0.1", db)
    current = store.create_session(user["id"], db_path=db)
    other = store.create_session(user["id"], db_path=db)
    with pytest.raises(auth.AuthError, match="Current password"):
        auth.change_password(user["id"], "wrong-password", "new-password-2", db)
    auth.change_password(
        user["id"], "old-password-1", "new-password-2", db,
        keep_session_id=current["id"],
    )
    assert store.get_session(current["id"], db) is not None
    assert store.get_session(other["id"], db) is None
    assert auth.authenticate("wren@example.test", "new-password-2", "10.3.0.2", db)["id"]
    with pytest.raises(auth.AuthError, match="Invalid email or password"):
        auth.authenticate("wren@example.test", "old-password-1", "10.3.0.3", db)


def test_request_password_reset_is_honest_and_validates_email(tmp_path):
    db = str(tmp_path / "forgot.db")
    auth.register("xan@example.test", "a-strong-password", "10.4.0.1", db)
    with pytest.raises(auth.AuthError, match="not configured"):
        auth.request_password_reset("xan@example.test", db)
    with pytest.raises(auth.AuthError, match="not configured"):
        auth.request_password_reset("ghost@example.test", db)
    with pytest.raises(auth.AuthError, match="valid email"):
        auth.request_password_reset("not-an-email", db)


def test_reset_password_roundtrip_and_single_use(tmp_path):
    from app.services import store

    db = str(tmp_path / "reset.db")
    user = auth.register("yara@example.test", "first-password-1", "10.5.0.1", db)
    session = store.create_session(user["id"], db_path=db)
    with pytest.raises(auth.AuthError, match="no longer valid"):
        auth.reset_password("bogus-token", "second-password-2", db)
    token = store.create_password_reset(user["id"], db)
    auth.reset_password(token, "second-password-2", db)
    assert store.get_session(session["id"], db) is None
    assert auth.authenticate("yara@example.test", "second-password-2", "10.5.0.2", db)["id"]
    with pytest.raises(auth.AuthError, match="no longer valid"):
        auth.reset_password(token, "third-password-3", db)

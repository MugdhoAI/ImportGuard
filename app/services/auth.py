"""Local email/password accounts with server-side sessions (stdlib only)."""

import hashlib
import hmac
import re
import secrets
import time
from threading import Lock
from typing import Any

from app.config import settings
from app.services import store

PBKDF2_ITERATIONS = 600_000
MAX_FAILED_PER_WINDOW = 10
THROTTLE_WINDOW_SECONDS = 300

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_failed_logins: dict[str, list[float]] = {}
_failed_accounts: dict[str, list[float]] = {}
_failure_lock = Lock()


class AuthError(ValueError):
    """Safe, user-facing authentication error."""


def _now() -> float:
    return time.monotonic()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2-sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, iterations, salt_hex, hash_hex = stored.split("$")
        if scheme != "pbkdf2-sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(digest.hex(), hash_hex)
    except (ValueError, TypeError):
        return False


def normalize_email(email: str) -> str:
    cleaned = email.strip().lower()
    if len(cleaned) > 254 or EMAIL_RE.match(cleaned) is None:
        raise AuthError("Enter a valid email address.")
    return cleaned


def validate_password(password: str) -> None:
    if not 10 <= len(password) <= 128:
        raise AuthError("Use a password between 10 and 128 characters.")


def _recent(bucket: dict[str, list[float]], key: str, window: int) -> list[float]:
    cutoff = _now() - window
    attempts = [hit for hit in bucket.get(key, []) if hit > cutoff]
    bucket[key] = attempts
    return attempts


def guard(client_ip: str, email: str | None = None) -> None:
    window = settings.auth_rate_window_seconds
    with _failure_lock:
        attempts = _recent(_failed_logins, client_ip, window)
        if len(attempts) >= settings.auth_failure_limit_per_ip:
            raise AuthError("Too many attempts. Try again in a few minutes.")
        if email:
            account_key = email.strip().lower()[:254]
            if (
                len(_recent(_failed_accounts, account_key, window))
                >= settings.auth_failure_limit_per_account
            ):
                raise AuthError("Too many attempts. Try again in a few minutes.")


def note_failure(client_ip: str, email: str | None = None) -> None:
    now = _now()
    with _failure_lock:
        _failed_logins.setdefault(client_ip, []).append(now)
        if email:
            _failed_accounts.setdefault(email.strip().lower()[:254], []).append(now)


def register(
    email: str, password: str, client_ip: str, db_path: str | None = None
) -> dict[str, Any]:
    guard(client_ip, email)
    try:
        address = normalize_email(email)
        validate_password(password)
        return store.create_user(address, hash_password(password), db_path)
    except (AuthError, store.StoreError) as exc:
        note_failure(client_ip, email)
        if isinstance(exc, store.StoreError):
            raise AuthError("Unable to create an account with those details.") from exc
        raise


def authenticate(
    email: str, password: str, client_ip: str, db_path: str | None = None
) -> dict[str, Any]:
    guard(client_ip, email)
    try:
        address = normalize_email(email)
    except AuthError:
        note_failure(client_ip, email)
        raise AuthError("Invalid email or password.") from None
    user = store.get_user_by_email(address, db_path)
    if user is None or not verify_password(password, user["password_hash"]):
        note_failure(client_ip, email)
        raise AuthError("Invalid email or password.")
    return user


def csrf_valid(session: dict[str, Any] | None, token: str | None) -> bool:
    if session is None or not token:
        return False
    return hmac.compare_digest(str(session.get("csrf_token", "")), token)


def is_admin(user: dict[str, Any] | None) -> bool:
    if user is None:
        return False
    allowed = {email.strip().lower() for email in settings.admin_emails.split(",") if email.strip()}
    return user["email"] in allowed


def change_password(
    user_id: int,
    current_password: str,
    new_password: str,
    db_path: str | None = None,
    keep_session_id: str | None = None,
) -> None:
    user = store.get_user_by_id(user_id, db_path)
    if user is None or not verify_password(current_password, user["password_hash"]):
        raise AuthError("Current password is incorrect.")
    validate_password(new_password)
    store.set_password_hash(user_id, hash_password(new_password), db_path)
    store.delete_user_sessions(user_id, db_path, except_session_id=keep_session_id)


def request_password_reset(email: str, db_path: str | None = None) -> None:
    """Request a reset email. Delivery does not exist yet, for any address."""
    normalize_email(email)
    raise AuthError(
        "Password reset by email is not configured on this server. "
        "Contact the server operator to regain access."
    )


def reset_password(token: str, new_password: str, db_path: str | None = None) -> None:
    validate_password(new_password)
    try:
        store.consume_password_reset(token, hash_password(new_password), db_path)
    except store.StoreError as exc:
        raise AuthError(str(exc)) from exc

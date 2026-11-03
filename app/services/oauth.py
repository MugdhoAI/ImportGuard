"""Configuration-gated Google and GitHub OAuth with state, PKCE, and identity linking."""

import base64
import hashlib
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from app.config import settings
from app.services import auth, store


class OAuthError(ValueError):
    """Safe user-facing OAuth error."""


@dataclass(frozen=True)
class Provider:
    key: str
    label: str
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    user_endpoint: str
    scopes: tuple[str, ...]

    @property
    def configured(self) -> bool:
        return bool(self.client_id and self.client_secret and self.redirect_uri)


def providers() -> dict[str, Provider]:
    return {
        "google": Provider(
            "google", "Google", settings.google_oauth_client_id,
            settings.google_oauth_client_secret, settings.google_oauth_redirect_uri,
            "https://accounts.google.com/o/oauth2/v2/auth",
            "https://oauth2.googleapis.com/token",
            "https://openidconnect.googleapis.com/v1/userinfo",
            ("openid", "email", "profile"),
        ),
        "github": Provider(
            "github", "GitHub", settings.github_oauth_client_id,
            settings.github_oauth_client_secret, settings.github_oauth_redirect_uri,
            "https://github.com/login/oauth/authorize",
            "https://github.com/login/oauth/access_token",
            "https://api.github.com/user",
            ("read:user", "user:email"),
        ),
    }


def provider_for(name: str) -> Provider:
    provider = providers().get(name.lower())
    if provider is None:
        raise OAuthError("Unknown sign-in provider.")
    return provider


def options() -> list[dict[str, Any]]:
    return [
        {"key": provider.key, "label": provider.label, "configured": provider.configured}
        for provider in providers().values()
    ]


def _safe_next(value: str | None, default: str = "/dashboard") -> str:
    if value and value.startswith("/") and not value.startswith("//") and "\\" not in value:
        return value
    return default


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def begin(
    provider_name: str, *, next_path: str = "/dashboard", user_id: int | None = None,
) -> str:
    provider = provider_for(provider_name)
    if not provider.configured:
        raise OAuthError(f"{provider.label} sign-in is not configured on this server.")
    verifier = secrets.token_urlsafe(48)
    state = store.create_oauth_state(
        provider=provider.key,
        code_verifier=verifier,
        next_path=_safe_next(next_path, "/settings" if user_id else "/dashboard"),
        user_id=user_id,
    )
    params = {
        "client_id": provider.client_id,
        "redirect_uri": provider.redirect_uri,
        "response_type": "code",
        "scope": " ".join(provider.scopes),
        "state": state,
        "code_challenge": _challenge(verifier),
        "code_challenge_method": "S256",
    }
    if provider.key == "google":
        params.update({"access_type": "online", "prompt": "select_account"})
    return f"{provider.authorization_endpoint}?{urlencode(params)}"


def _request_json(response: httpx.Response) -> dict[str, Any]:
    if response.status_code >= 400:
        raise OAuthError("The OAuth provider rejected the request.")
    try:
        data = response.json()
    except ValueError as exc:
        raise OAuthError("The OAuth provider returned an invalid response.") from exc
    if not isinstance(data, dict):
        raise OAuthError("The OAuth provider returned an invalid response.")
    return data


def exchange_code(provider: Provider, code: str, verifier: str) -> str:
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            response = client.post(
                provider.token_endpoint,
                data={
                    "client_id": provider.client_id,
                    "client_secret": provider.client_secret,
                    "code": code,
                    "redirect_uri": provider.redirect_uri,
                    "grant_type": "authorization_code",
                    "code_verifier": verifier,
                },
                headers={"Accept": "application/json"},
            )
        data = _request_json(response)
    except OAuthError:
        raise
    except httpx.HTTPError as exc:
        raise OAuthError("The OAuth provider could not be reached.") from exc
    token = data.get("access_token")
    if not isinstance(token, str) or not token:
        raise OAuthError("The OAuth provider did not return an access token.")
    return token


def fetch_identity(provider: Provider, access_token: str) -> dict[str, str]:
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            profile_response = client.get(
                provider.user_endpoint,
                headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
            )
            profile = _request_json(profile_response)
            if provider.key == "github":
                emails_response = client.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github+json",
                    },
                )
                if emails_response.status_code >= 400:
                    raise OAuthError("GitHub did not return a verified email address.")
                emails = emails_response.json()
                if not isinstance(emails, list):
                    raise OAuthError("GitHub returned an invalid email response.")
                verified = [item for item in emails if item.get("verified") and item.get("primary")]
                verified = verified or [item for item in emails if item.get("verified")]
                if not verified:
                    raise OAuthError("GitHub did not return a verified email address.")
                profile["email"] = verified[0].get("email")
    except (httpx.HTTPError, ValueError, TypeError) as exc:
        raise OAuthError("The OAuth provider returned an invalid identity response.") from exc
    email = str(profile.get("email") or "").strip().lower()
    if not email:
        raise OAuthError("The provider did not return an email address.")
    if provider.key == "google" and profile.get("email_verified") is not True:
        raise OAuthError("The Google email address is not verified.")
    subject = str(profile.get("sub") or profile.get("id") or "").strip()
    if not subject:
        raise OAuthError("The provider did not return a stable account identifier.")
    try:
        email = auth.normalize_email(email)
    except auth.AuthError as exc:
        raise OAuthError("The provider returned an invalid email address.") from exc
    return {
        "subject": subject,
        "email": email,
        "name": str(profile.get("name") or profile.get("login") or "")[:80],
    }


def finish(
    provider_name: str,
    state_record: dict[str, Any],
    code: str,
    current_user: dict[str, Any] | None,
) -> dict[str, Any]:
    provider = provider_for(provider_name)
    if state_record["provider"] != provider.key:
        raise OAuthError("OAuth state does not match the provider.")
    if state_record["user_id"] is not None:
        if current_user is None or int(state_record["user_id"]) != int(current_user["id"]):
            raise OAuthError("Your session changed before account linking completed.")
    token = exchange_code(provider, code, state_record["code_verifier"])
    identity = fetch_identity(provider, token)
    existing = store.get_oauth_account(provider.key, identity["subject"])
    if existing:
        if current_user is not None and existing["user_id"] != current_user["id"]:
            raise OAuthError("This provider account is already linked to another account.")
        user = store.get_user_by_id(existing["user_id"])
        if user is None:
            raise OAuthError("The linked account is no longer available.")
        return {"user": user, "linked": False}
    email_user = store.get_user_by_email(identity["email"])
    if current_user is not None:
        if identity["email"] != current_user["email"]:
            raise OAuthError("The provider email does not match your signed-in account.")
        try:
            store.link_oauth_account(
                provider=provider.key,
                subject=identity["subject"],
                user_id=current_user["id"],
                email=identity["email"],
            )
        except store.StoreError as exc:
            raise OAuthError("This provider identity could not be linked safely.") from exc
        return {"user": current_user, "linked": True}
    if email_user is not None:
        raise OAuthError(
            "An account already exists for this email. Sign in with your password, "
            "then link the provider from Settings."
        )
    try:
        user = store.create_oauth_user(
            email=identity["email"],
            password_hash=auth.hash_password(secrets.token_urlsafe(32)),
            provider=provider.key,
            subject=identity["subject"],
            name=identity["name"],
        )
    except store.StoreError as exc:
        raise OAuthError("The OAuth account could not be created safely. Try again.") from exc
    return {"user": user, "linked": False}

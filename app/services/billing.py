"""Provider-neutral billing: plans, entitlements, and a provider seam.

No payment provider is integrated. Upgrades stay visibly unavailable until a
provider is selected and server-side credentials plus webhook handling are
configured and approved. Adding a provider means implementing
:class:`BillingProvider`, routing its verified webhooks to
:func:`apply_provider_event`, and storing the resulting plan/status with
:func:`store.set_subscription` -- no template or API-shape changes required.
"""

from datetime import UTC, datetime
from typing import Any, Protocol

from app.config import settings
from app.services import store

PLANS: dict[str, dict[str, Any]] = {
    "free": {
        "name": "Free",
        "monthly_exports": 25,
        "history_days": 7,
        "features": ("CSV workspace", "Recipe replay", "7-day export history"),
    },
    "pro": {
        "name": "Pro",
        "monthly_exports": 500,
        "history_days": 90,
        "features": ("Everything in Free", "90-day export history", "Priority processing"),
    },
    "business": {
        "name": "Business",
        "monthly_exports": None,
        "history_days": 365,
        "features": ("Everything in Pro", "Unlimited exports", "Team workspaces"),
    },
}


class BillingUnavailable(RuntimeError):
    """Raised when billing needs a provider that is not configured."""


class BillingProvider(Protocol):
    """Seam a real payment provider implements. Never called without one."""

    name: str

    def checkout_url(self, user_id: int, plan: str) -> str:
        """Return a server-created checkout URL for the plan."""
        ...  # pragma: no cover

    def parse_webhook(self, payload: bytes, signature: str) -> dict[str, Any]:
        """Verify and parse a provider webhook into a normalized event."""
        ...  # pragma: no cover


class NullProvider:
    """Default provider: checkout and webhooks are explicitly unavailable."""

    name = "none"

    def checkout_url(self, user_id: int, plan: str) -> str:
        raise BillingUnavailable(
            "Checkout is not configured. Select a payment provider first."
        )

    def parse_webhook(self, payload: bytes, signature: str) -> dict[str, Any]:
        raise BillingUnavailable(
            "Webhook handling is not configured. Select a payment provider first."
        )


def provider() -> BillingProvider:
    """Return the configured provider. Only the null provider exists today."""
    return NullProvider()


def month_start(now: datetime | None = None) -> datetime:
    current = now or datetime.now(UTC)
    return current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def plan_for(code: str) -> dict[str, Any]:
    return PLANS.get(code, PLANS["free"])


def current_state(user_id: int | None, db_path: str | None = None) -> dict[str, Any]:
    """Billing snapshot for the UI. Guests read as free with no usage."""
    if user_id is None:
        plan = PLANS["free"]
        return {
            "plan": "free",
            "plan_name": plan["name"],
            "status": "active",
            "provider": None,
            "usage": 0,
            "limit": plan["monthly_exports"],
            "history_days": plan["history_days"],
            "features": plan["features"],
        }
    subscription = store.get_subscription(user_id, db_path)
    plan = plan_for(subscription["plan"])
    usage = store.count_exports_since(user_id, month_start(), db_path)
    return {
        "plan": subscription["plan"],
        "plan_name": plan["name"],
        "status": subscription["status"],
        "provider": subscription["provider"],
        "usage": usage,
        "limit": plan["monthly_exports"],
        "history_days": plan["history_days"],
        "features": plan["features"],
    }


def exports_allowed(state: dict[str, Any]) -> bool:
    """Quota gate. Permissive until quota enforcement is explicitly enabled."""
    if not settings.billing_enforce_quotas:
        return True
    limit = state["limit"]
    if limit is None:
        return True
    return state["usage"] < limit and state["status"] == "active"


def apply_provider_event(event: dict[str, Any], db_path: str | None = None) -> dict[str, Any]:
    """Persist a verified provider event. Only called with a real provider."""
    return store.set_subscription(
        int(event["user_id"]),
        plan=str(event["plan"]),
        status=str(event.get("status", "active")),
        provider=event.get("provider"),
        provider_ref=event.get("provider_ref"),
        db_path=db_path,
    )

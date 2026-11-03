"""Billing tests: plans, entitlements, provider seam, billing page."""

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import billing, store

client = TestClient(app)


def test_plans_define_limits_and_planned_prices():
    assert set(billing.PLANS) == {"free", "pro", "business"}
    for code, plan in billing.PLANS.items():
        assert plan["name"] and plan["history_days"] > 0
        assert plan["price_usd"] >= 0 and plan["price_label"], code
    assert billing.PLANS["free"]["price_usd"] == 0
    assert billing.PLANS["pro"]["price_usd"] == 6.99
    assert billing.PLANS["business"]["price_usd"] == 19.99
    assert billing.PLANS["free"]["monthly_exports"] == 25
    assert billing.PLANS["business"]["monthly_exports"] is None


def test_current_state_for_guest_and_user(tmp_path):
    db = str(tmp_path / "billing.db")
    guest = billing.current_state(None, db)
    assert (guest["plan"], guest["usage"], guest["limit"]) == ("free", 0, 25)
    user = store.create_user("bill@example.test", "hash", db)
    store.record_export(
        user_id=user["id"],
        filename="a.csv",
        file_sha256="x",
        input_rows=2,
        accepted_rows=2,
        rejected_rows=0,
        recipe_json="{}",
        report_json="{}",
        package=b"z",
        db_path=db,
    )
    state = billing.current_state(user["id"], db)
    assert (state["plan_name"], state["usage"], state["limit"]) == ("Free", 1, 25)


def test_quota_gate_permissive_until_enforced(monkeypatch):
    state = {"usage": 99, "limit": 25, "status": "active"}
    assert billing.exports_allowed(state) is True
    monkeypatch.setattr(billing, "settings", SimpleNamespace(billing_enforce_quotas=True))
    assert billing.exports_allowed(state) is False
    assert billing.exports_allowed({"usage": 1, "limit": 25, "status": "active"}) is True
    assert billing.exports_allowed({"usage": 1, "limit": 25, "status": "past_due"}) is False
    assert billing.exports_allowed({"usage": 999, "limit": None, "status": "active"}) is True


def test_null_provider_refuses_checkout_and_webhooks():
    provider = billing.provider()
    assert provider.name == "none"
    with pytest.raises(billing.BillingUnavailable, match="not configured"):
        provider.checkout_url(1, "pro")
    with pytest.raises(billing.BillingUnavailable, match="not configured"):
        provider.parse_webhook(b"{}", "sig")


def test_apply_provider_event_persists_subscription(tmp_path):
    db = str(tmp_path / "sub.db")
    user = store.create_user("sub@example.test", "hash", db)
    row = billing.apply_provider_event(
        {"user_id": user["id"], "plan": "pro", "provider": "acme", "provider_ref": "sub_1"},
        db,
    )
    assert (row["plan"], row["provider"], row["provider_ref"]) == ("pro", "acme", "sub_1")


def test_billing_page_guest_and_user_states():
    guest = TestClient(app)
    page = guest.get("/billing").text
    assert "CURRENT PLAN" in page and "Free" in page
    assert "No invoices available" in page
    assert "Delete my account" not in page
    guest.post("/auth/signup", data={"email": "pay@example.test", "password": "a-strong-password"})
    user_page = guest.get("/billing").text
    assert "pay@example.test" in user_page
    assert "Delete my account" in user_page
    assert "Provider setup required" in user_page

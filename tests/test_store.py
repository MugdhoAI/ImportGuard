"""Store layer tests: users, sessions, exports, subscriptions, retention."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from app.services import store


@pytest.fixture()
def db(tmp_path):
    return str(tmp_path / "store.db")


def _settings(**overrides):
    values = {
        "session_days": 30,
        "export_retention_days": 7,
        "max_stored_package_bytes": 8 * 1024 * 1024,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def _export_kwargs(**overrides):
    values = {
        "filename": "in.csv",
        "file_sha256": "abc123",
        "input_rows": 3,
        "accepted_rows": 2,
        "rejected_rows": 1,
        "recipe_json": "{}",
        "report_json": "{}",
        "package": b"zip-bytes",
    }
    values.update(overrides)
    return values


def test_user_create_duplicate_and_lookup(db):
    user = store.create_user("ana@example.test", "hash-1", db)
    assert user["id"] == 1
    with pytest.raises(store.StoreError, match="already exists"):
        store.create_user("ana@example.test", "hash-2", db)
    assert store.get_user_by_email("ana@example.test", db)["id"] == 1
    assert store.get_user_by_email("nobody@example.test", db) is None
    assert store.get_user_by_id(1, db)["email"] == "ana@example.test"


def test_session_lifecycle_and_expiry(db):
    user = store.create_user("ben@example.test", "hash", db)
    session = store.create_session(user["id"], db_path=db)
    assert session["id"] and session["csrf_token"]
    assert store.get_session(session["id"], db)["user_id"] == user["id"]
    expired = store.create_session(user["id"], days=-1, db_path=db)
    assert store.get_session(expired["id"], db) is None
    assert store.get_session("missing", db) is None
    store.delete_session(session["id"], db)
    assert store.get_session(session["id"], db) is None


def test_purge_expired_sessions(db):
    user = store.create_user("cid@example.test", "hash", db)
    store.create_session(user["id"], db_path=db)
    store.create_session(user["id"], days=-1, db_path=db)
    assert store.purge_expired_sessions(db) == 1


def test_export_record_restore_and_ownership(db):
    user = store.create_user("dee@example.test", "hash", db)
    guest = store.new_token()
    mine = store.record_export(user_id=user["id"], **_export_kwargs(), db_path=db)
    assert mine["package_stored"] == 1
    guest_row = store.record_export(
        guest_token=guest, **_export_kwargs(filename="g.csv"), db_path=db
    )
    fetched = store.get_export(mine["id"], db)
    assert fetched["package"] == b"zip-bytes"
    assert fetched["accepted_rows"] == 2
    assert store.get_export("missing", db) is None
    assert [row["id"] for row in store.list_exports(user_id=user["id"], db_path=db)] == [mine["id"]]
    hashed = store.hash_guest_token(guest)
    assert [row["id"] for row in store.list_exports(guest_token_hash=hashed, db_path=db)] == [
        guest_row["id"]
    ]
    assert "package" not in store.list_exports(user_id=user["id"], db_path=db)[0]


def test_export_package_size_cap_and_expiry(db, monkeypatch):
    monkeypatch.setattr(store, "settings", _settings(max_stored_package_bytes=4))
    big = store.record_export(
        user_id=store.create_user("eli@example.test", "hash", db)["id"],
        **_export_kwargs(package=b"too-big-bytes"),
        db_path=db,
    )
    assert big["package_stored"] == 0
    assert store.get_export(big["id"], db)["package"] is None
    monkeypatch.setattr(store, "settings", _settings(export_retention_days=-1))
    stale = store.record_export(
        user_id=store.create_user("fay@example.test", "hash", db)["id"],
        **_export_kwargs(),
        db_path=db,
    )
    assert store.get_export(stale["id"], db) is None
    assert store.purge_expired_exports(db) >= 0


def test_claim_guest_exports_transfers_live_rows_only(db):
    user = store.create_user("gus@example.test", "hash", db)
    guest = store.new_token()
    first = store.record_export(guest_token=guest, **_export_kwargs(), db_path=db)
    assert store.claim_guest_exports(guest, user["id"], db) == 1
    assert store.claim_guest_exports(guest, user["id"], db) == 0
    owned = [row["id"] for row in store.list_exports(user_id=user["id"], db_path=db)]
    assert owned == [first["id"]]


def test_delete_account_removes_everything(db):
    user = store.create_user("hal@example.test", "hash", db)
    session = store.create_session(user["id"], db_path=db)
    store.record_export(user_id=user["id"], **_export_kwargs(), db_path=db)
    store.get_subscription(user["id"], db)
    store.delete_account(user["id"], db)
    assert store.get_user_by_id(user["id"], db) is None
    assert store.get_session(session["id"], db) is None
    assert store.list_exports(user_id=user["id"], db_path=db) == []


def test_subscription_defaults_and_updates(db):
    user = store.create_user("ivy@example.test", "hash", db)
    sub = store.get_subscription(user["id"], db)
    assert (sub["plan"], sub["status"], sub["provider"]) == ("free", "active", None)
    updated = store.set_subscription(
        user["id"], plan="pro", status="past_due", provider="acme", db_path=db
    )
    assert (updated["plan"], updated["status"], updated["provider"]) == ("pro", "past_due", "acme")
    assert store.get_subscription(user["id"], db)["plan"] == "pro"


def test_count_exports_since_bounds_usage_window(db):
    user = store.create_user("jan@example.test", "hash", db)
    store.record_export(user_id=user["id"], **_export_kwargs(), db_path=db)
    store.record_export(user_id=user["id"], **_export_kwargs(), db_path=db)
    assert store.count_exports_since(user["id"], datetime.now(UTC) - timedelta(days=30), db) == 2
    assert store.count_exports_since(user["id"], datetime.now(UTC) + timedelta(days=1), db) == 0


def test_list_exports_isolates_users_and_guests(db):
    first = store.create_user("kate@example.test", "hash", db)
    second = store.create_user("leo@example.test", "hash", db)
    guest_a, guest_b = store.new_token(), store.new_token()
    mine = store.record_export(
        user_id=first["id"], **_export_kwargs(filename="k.csv"), db_path=db
    )
    theirs = store.record_export(
        user_id=second["id"], **_export_kwargs(filename="l.csv"), db_path=db
    )
    row_a = store.record_export(
        guest_token=guest_a, **_export_kwargs(filename="a.csv"), db_path=db
    )
    row_b = store.record_export(
        guest_token=guest_b, **_export_kwargs(filename="b.csv"), db_path=db
    )
    assert [row["id"] for row in store.list_exports(user_id=first["id"], db_path=db)] == [
        mine["id"]
    ]
    assert [row["id"] for row in store.list_exports(user_id=second["id"], db_path=db)] == [
        theirs["id"]
    ]
    assert [
        row["id"]
        for row in store.list_exports(
            guest_token_hash=store.hash_guest_token(guest_a), db_path=db
        )
    ] == [row_a["id"]]
    assert [
        row["id"]
        for row in store.list_exports(
            guest_token_hash=store.hash_guest_token(guest_b), db_path=db
        )
    ] == [row_b["id"]]
    assert store.list_exports(db_path=db) == []


def test_pending_filter_and_download_marking(db):
    user = store.create_user("max@example.test", "hash", db)
    pending = store.record_export(
        user_id=user["id"], **_export_kwargs(filename="p.csv"), db_path=db
    )
    done = store.record_export(
        user_id=user["id"], **_export_kwargs(filename="d.csv"), db_path=db
    )
    assert store.mark_export_downloaded(done["id"], db) is True
    assert store.mark_export_downloaded("missing", db) is False
    ids = [
        row["id"]
        for row in store.list_exports(user_id=user["id"], only_pending=True, db_path=db)
    ]
    assert ids == [pending["id"]]
    fetched = store.get_export(done["id"], db)
    assert fetched is not None and fetched["downloaded_at"] is not None
    assert fetched["download_count"] == 1
    assert store.mark_export_downloaded(done["id"], db) is True
    again = store.get_export(done["id"], db)
    assert again is not None and again["download_count"] == 2
    assert again["downloaded_at"] == fetched["downloaded_at"]


def test_user_sessions_list_and_selective_revoke(db):
    user = store.create_user("nia@example.test", "hash", db)
    keep = store.create_session(user["id"], db_path=db)
    drop = store.create_session(user["id"], db_path=db)
    stale = store.create_session(user["id"], days=-1, db_path=db)
    ids = {row["id"] for row in store.list_sessions(user["id"], db)}
    assert ids == {keep["id"], drop["id"]}
    assert stale["id"] not in ids
    assert store.revoke_session(user["id"], drop["id"], db) is True
    assert store.revoke_session(user["id"], "missing", db) is False
    store.delete_user_sessions(user["id"], db, except_session_id=keep["id"])
    assert store.get_session(keep["id"], db) is not None
    assert store.get_session(drop["id"], db) is None
    store.delete_user_sessions(user["id"], db)
    assert store.list_sessions(user["id"], db) == []


def test_leave_team_rules(db):
    owner = store.create_user("omar@example.test", "hash", db)
    member = store.create_user("pia@example.test", "hash", db)
    outsider = store.create_user("rae@example.test", "hash", db)
    team = store.create_team("Acme", owner["id"], db)
    store.accept_invitation(
        store.create_invitation(team["id"], member["email"], "member", owner["id"], db)["token"],
        member["id"],
        db,
    )
    with pytest.raises(store.StoreError, match="not a member"):
        store.leave_team(team["id"], outsider["id"], db)
    with pytest.raises(store.StoreError, match="last owner"):
        store.leave_team(team["id"], owner["id"], db)
    store.set_member_role(team["id"], member["id"], "owner", db)
    store.leave_team(team["id"], owner["id"], db)
    assert store.team_role(team["id"], owner["id"], db) is None
    assert store.team_role(team["id"], member["id"], db) == "owner"


def test_set_user_name_trims_and_rejects_blank(db):
    user = store.create_user("tim@example.test", "hash", db)
    store.set_user_name(user["id"], "  Tim Tester  ", db)
    assert store.get_user_by_id(user["id"], db)["name"] == "Tim Tester"
    store.set_user_name(user["id"], "x" * 200, db)
    assert store.get_user_by_id(user["id"], db)["name"] == "x" * 80
    with pytest.raises(store.StoreError, match="display name"):
        store.set_user_name(user["id"], "   ", db)


def test_get_invitation_roundtrip(db):
    owner = store.create_user("sam@example.test", "hash", db)
    team = store.create_team("Beta", owner["id"], db)
    invite = store.create_invitation(team["id"], "ted@example.test", "admin", owner["id"], db)
    fetched = store.get_invitation(invite["token"], db)
    assert fetched is not None
    assert (fetched["team_name"], fetched["email"], fetched["role"]) == (
        "Beta",
        "ted@example.test",
        "admin",
    )
    assert store.get_invitation("missing", db) is None

"""SQLite persistence for accounts, sessions, exports, and subscriptions."""

import hashlib
import secrets
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from app.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    csrf_token TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS exports (
    id TEXT PRIMARY KEY,
    user_id INTEGER NULL REFERENCES users(id) ON DELETE CASCADE,
    guest_token_hash TEXT NULL,
    filename TEXT NOT NULL,
    file_sha256 TEXT NOT NULL,
    input_rows INTEGER NOT NULL,
    accepted_rows INTEGER NOT NULL,
    rejected_rows INTEGER NOT NULL,
    recipe_json TEXT NOT NULL,
    report_json TEXT NOT NULL,
    package BLOB NULL,
    package_stored INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS exports_owner ON exports(user_id, created_at);
CREATE INDEX IF NOT EXISTS exports_guest ON exports(guest_token_hash, created_at);
CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    plan TEXT NOT NULL DEFAULT 'free',
    status TEXT NOT NULL DEFAULT 'active',
    provider TEXT NULL,
    provider_ref TEXT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS team_members (
    team_id INTEGER NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'member',
    status TEXT NOT NULL DEFAULT 'active',
    PRIMARY KEY (team_id, user_id)
);
CREATE TABLE IF NOT EXISTS invitations (
    token TEXT PRIMARY KEY,
    team_id INTEGER NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    accepted_at TEXT NULL
);
CREATE TABLE IF NOT EXISTS password_resets (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    used_at TEXT NULL
);
"""

MIGRATIONS: dict[str, dict[str, str]] = {
    "users": {"name": "TEXT NULL"},
    "exports": {"downloaded_at": "TEXT NULL", "download_count": "INTEGER NOT NULL DEFAULT 0"},
}


class StoreError(ValueError):
    """Safe, user-facing persistence error."""


def _connect(db_path: str | None = None) -> sqlite3.Connection:
    path = Path(db_path or settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    for table, columns in MIGRATIONS.items():
        existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        for column, definition in columns.items():
            if column not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
    return conn


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _iso(moment: datetime) -> str:
    return moment.isoformat()


def hash_guest_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def new_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def create_user(email: str, password_hash: str, db_path: str | None = None) -> dict[str, Any]:
    try:
        with _connect(db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                (email, password_hash, _iso(_utcnow())),
            )
            user_id = cursor.lastrowid
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row)
    except sqlite3.IntegrityError as exc:
        raise StoreError("An account with this email already exists.") from exc


def get_user_by_email(email: str, db_path: str | None = None) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int, db_path: str | None = None) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def delete_account(user_id: int, db_path: str | None = None) -> None:
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM exports WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


def create_session(
    user_id: int, days: int | None = None, db_path: str | None = None
) -> dict[str, str]:
    session_id, csrf = new_token(), new_token()
    lifetime = days if days is not None else settings.session_days
    now = _utcnow()
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO sessions (id, user_id, csrf_token, created_at, expires_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (session_id, user_id, csrf, _iso(now), _iso(now + timedelta(days=lifetime))),
        )
    return {"id": session_id, "csrf_token": csrf}


def get_session(session_id: str, db_path: str | None = None) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if row is None:
        return None
    if datetime.fromisoformat(row["expires_at"]) <= _utcnow():
        delete_session(session_id, db_path)
        return None
    return dict(row)


def delete_session(session_id: str, db_path: str | None = None) -> None:
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))


def delete_user_sessions(
    user_id: int, db_path: str | None = None, except_session_id: str | None = None
) -> None:
    with _connect(db_path) as conn:
        if except_session_id:
            conn.execute(
                "DELETE FROM sessions WHERE user_id = ? AND id != ?",
                (user_id, except_session_id),
            )
        else:
            conn.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))


def purge_expired_sessions(db_path: str | None = None) -> int:
    with _connect(db_path) as conn:
        cursor = conn.execute("DELETE FROM sessions WHERE expires_at <= ?", (_iso(_utcnow()),))
        return cursor.rowcount


def record_export(
    *,
    filename: str,
    file_sha256: str,
    input_rows: int,
    accepted_rows: int,
    rejected_rows: int,
    recipe_json: str,
    report_json: str,
    package: bytes | None,
    user_id: int | None = None,
    guest_token: str | None = None,
    db_path: str | None = None,
) -> dict[str, Any]:
    export_id = new_token(16)
    now = _utcnow()
    expires = now + timedelta(days=settings.export_retention_days)
    stored = (
        package
        if package is not None and len(package) <= settings.max_stored_package_bytes
        else None
    )
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO exports (id, user_id, guest_token_hash, filename, file_sha256,"
            " input_rows, accepted_rows, rejected_rows, recipe_json, report_json,"
            " package, package_stored, created_at, expires_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                export_id,
                user_id,
                hash_guest_token(guest_token) if guest_token else None,
                filename,
                file_sha256,
                input_rows,
                accepted_rows,
                rejected_rows,
                recipe_json,
                report_json,
                stored,
                1 if stored is not None else 0,
                _iso(now),
                _iso(expires),
            ),
        )
        row = conn.execute(
            "SELECT id, user_id, filename, file_sha256, input_rows, accepted_rows,"
            " rejected_rows, package_stored, created_at, expires_at FROM exports WHERE id = ?",
            (export_id,),
        ).fetchone()
        return dict(row)


def get_export(export_id: str, db_path: str | None = None) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM exports WHERE id = ?", (export_id,)).fetchone()
    if row is None:
        return None
    if datetime.fromisoformat(row["expires_at"]) <= _utcnow():
        with _connect(db_path) as conn:
            conn.execute("DELETE FROM exports WHERE id = ?", (export_id,))
        return None
    return dict(row)


def list_exports(
    *,
    user_id: int | None = None,
    guest_token_hash: str | None = None,
    limit: int = 50,
    only_pending: bool = False,
    db_path: str | None = None,
) -> list[dict[str, Any]]:
    if user_id is None and guest_token_hash is None:
        return []
    clauses = ["expires_at > ?"]
    params: list[Any] = [_iso(_utcnow())]
    if user_id is not None:
        clauses.append("user_id IS ?")
        params.append(user_id)
    if guest_token_hash is not None:
        clauses.append("guest_token_hash IS ?")
        params.append(guest_token_hash)
    if only_pending:
        clauses.append("downloaded_at IS NULL")
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, user_id, filename, file_sha256, input_rows, accepted_rows,"
            " rejected_rows, package_stored, downloaded_at, download_count,"
            " created_at, expires_at FROM exports WHERE " + " AND ".join(clauses) +
            " ORDER BY created_at DESC LIMIT ?",
            (*params, limit),
        ).fetchall()
        return [dict(row) for row in rows]


def mark_export_downloaded(export_id: str, db_path: str | None = None) -> bool:
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE exports SET downloaded_at = COALESCE(downloaded_at, ?),"
            " download_count = download_count + 1 WHERE id = ?",
            (_iso(_utcnow()), export_id),
        )
        return cursor.rowcount == 1


def claim_guest_exports(guest_token: str, user_id: int, db_path: str | None = None) -> int:
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE exports SET user_id = ?, guest_token_hash = NULL"
            " WHERE guest_token_hash = ? AND user_id IS NULL AND expires_at > ?",
            (user_id, hash_guest_token(guest_token), _iso(_utcnow())),
        )
        return cursor.rowcount


def purge_expired_exports(db_path: str | None = None) -> int:
    with _connect(db_path) as conn:
        cursor = conn.execute("DELETE FROM exports WHERE expires_at <= ?", (_iso(_utcnow()),))
        return cursor.rowcount


def count_exports_since(
    user_id: int, since: datetime, db_path: str | None = None
) -> int:
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS total FROM exports WHERE user_id = ? AND created_at >= ?",
            (user_id, _iso(since)),
        ).fetchone()
        return int(row["total"])


def get_subscription(user_id: int, db_path: str | None = None) -> dict[str, Any]:
    with _connect(db_path) as conn:
        row = conn.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,)).fetchone()
        if row is None:
            now = _iso(_utcnow())
            conn.execute(
                "INSERT INTO subscriptions (user_id, plan, status, updated_at)"
                " VALUES (?, 'free', 'active', ?)",
                (user_id, now),
            )
            return {
                "user_id": user_id,
                "plan": "free",
                "status": "active",
                "provider": None,
                "provider_ref": None,
                "updated_at": now,
            }
        return dict(row)


def set_subscription(
    user_id: int,
    *,
    plan: str,
    status: str,
    provider: str | None = None,
    provider_ref: str | None = None,
    db_path: str | None = None,
) -> dict[str, Any]:
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO subscriptions (user_id, plan, status, provider, provider_ref, updated_at)"
            " VALUES (?, ?, ?, ?, ?, ?)"
            " ON CONFLICT(user_id) DO UPDATE SET plan = ?, status = ?,"
            " provider = ?, provider_ref = ?, updated_at = ?",
            (
                user_id,
                plan,
                status,
                provider,
                provider_ref,
                _iso(_utcnow()),
                plan,
                status,
                provider,
                provider_ref,
                _iso(_utcnow()),
            ),
        )
        row = conn.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row)


def set_user_name(user_id: int, name: str, db_path: str | None = None) -> None:
    cleaned = name.strip()[:80]
    if not cleaned:
        raise StoreError("Enter a display name.")
    with _connect(db_path) as conn:
        conn.execute("UPDATE users SET name = ? WHERE id = ?", (cleaned, user_id))


def set_password_hash(user_id: int, password_hash: str, db_path: str | None = None) -> None:
    with _connect(db_path) as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))


def list_sessions(user_id: int, db_path: str | None = None) -> list[dict[str, Any]]:
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, created_at, expires_at FROM sessions WHERE user_id = ?"
            " AND expires_at > ? ORDER BY created_at DESC",
            (user_id, _iso(_utcnow())),
        ).fetchall()
        return [dict(row) for row in rows]


def revoke_session(user_id: int, session_id: str, db_path: str | None = None) -> bool:
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM sessions WHERE id = ? AND user_id = ?", (session_id, user_id)
        )
        return cursor.rowcount == 1


def latest_export(
    *,
    user_id: int | None = None,
    guest_token_hash: str | None = None,
    db_path: str | None = None,
) -> dict[str, Any] | None:
    rows = list_exports(
        user_id=user_id, guest_token_hash=guest_token_hash, limit=1, db_path=db_path
    )
    return rows[0] if rows else None


def search_exports(
    user_id: int,
    *,
    query: str = "",
    status: str = "",
    limit: int = 25,
    offset: int = 0,
    db_path: str | None = None,
) -> dict[str, Any]:
    clauses = ["user_id = ?", "expires_at > ?"]
    params: list[Any] = [user_id, _iso(_utcnow())]
    if query.strip():
        clauses.append("filename LIKE ?")
        params.append(f"%{query.strip()}%")
    if status == "completed":
        clauses.append("rejected_rows = 0")
    elif status == "needs_review":
        clauses.append("rejected_rows > 0")
    where = " AND ".join(clauses)
    with _connect(db_path) as conn:
        total = conn.execute(
            f"SELECT COUNT(*) AS n FROM exports WHERE {where}", params
        ).fetchone()["n"]
        rows = conn.execute(
            "SELECT id, filename, file_sha256, input_rows, accepted_rows, rejected_rows,"
            " package_stored, created_at, expires_at, downloaded_at, download_count"
            f" FROM exports WHERE {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (*params, limit, offset),
        ).fetchall()
        return {"total": int(total), "exports": [dict(row) for row in rows]}


def create_team(name: str, owner_user_id: int, db_path: str | None = None) -> dict[str, Any]:
    cleaned = name.strip()[:80]
    if not cleaned:
        raise StoreError("Enter a team name.")
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO teams (name, owner_user_id, created_at) VALUES (?, ?, ?)",
            (cleaned, owner_user_id, _iso(_utcnow())),
        )
        team_id = cursor.lastrowid
        conn.execute(
            "INSERT INTO team_members (team_id, user_id, role, status)"
            " VALUES (?, ?, 'owner', 'active')",
            (team_id, owner_user_id),
        )
        return dict(conn.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone())


def user_teams(user_id: int, db_path: str | None = None) -> list[dict[str, Any]]:
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT t.*, m.role, m.status FROM teams t"
            " JOIN team_members m ON m.team_id = t.id"
            " WHERE m.user_id = ? AND m.status = 'active' ORDER BY t.created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def team_role(team_id: int, user_id: int, db_path: str | None = None) -> str | None:
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT role FROM team_members WHERE team_id = ? AND user_id = ? AND status = 'active'",
            (team_id, user_id),
        ).fetchone()
        return row["role"] if row else None


def team_members(team_id: int, db_path: str | None = None) -> list[dict[str, Any]]:
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT u.id AS user_id, u.email, u.name, m.role, m.status FROM team_members m"
            " JOIN users u ON u.id = m.user_id WHERE m.team_id = ? ORDER BY u.email",
            (team_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def set_member_role(
    team_id: int, user_id: int, role: str, db_path: str | None = None
) -> None:
    if role not in ("owner", "admin", "member"):
        raise StoreError("Unknown role.")
    with _connect(db_path) as conn:
        owners = conn.execute(
            "SELECT COUNT(*) AS n FROM team_members"
            " WHERE team_id = ? AND role = 'owner' AND status = 'active'",
            (team_id,),
        ).fetchone()["n"]
        current = conn.execute(
            "SELECT role FROM team_members WHERE team_id = ? AND user_id = ?",
            (team_id, user_id),
        ).fetchone()
        if current is None:
            raise StoreError("Member not found.")
        if current["role"] == "owner" and role != "owner" and owners <= 1:
            raise StoreError("A team must keep at least one owner.")
        conn.execute(
            "UPDATE team_members SET role = ? WHERE team_id = ? AND user_id = ?",
            (role, team_id, user_id),
        )


def remove_member(team_id: int, user_id: int, db_path: str | None = None) -> None:
    with _connect(db_path) as conn:
        owners = conn.execute(
            "SELECT COUNT(*) AS n FROM team_members"
            " WHERE team_id = ? AND role = 'owner' AND status = 'active'",
            (team_id,),
        ).fetchone()["n"]
        current = conn.execute(
            "SELECT role FROM team_members WHERE team_id = ? AND user_id = ?",
            (team_id, user_id),
        ).fetchone()
        if current is None:
            raise StoreError("Member not found.")
        if current["role"] == "owner" and owners <= 1:
            raise StoreError("A team must keep at least one owner.")
        conn.execute(
            "DELETE FROM team_members WHERE team_id = ? AND user_id = ?", (team_id, user_id)
        )


def leave_team(team_id: int, user_id: int, db_path: str | None = None) -> None:
    with _connect(db_path) as conn:
        current = conn.execute(
            "SELECT role FROM team_members WHERE team_id = ? AND user_id = ?",
            (team_id, user_id),
        ).fetchone()
        if current is None:
            raise StoreError("You are not a member of this team.")
        if current["role"] == "owner":
            owners = conn.execute(
                "SELECT COUNT(*) AS n FROM team_members"
                " WHERE team_id = ? AND role = 'owner' AND status = 'active'",
                (team_id,),
            ).fetchone()["n"]
            if owners <= 1:
                raise StoreError("The last owner cannot leave the team.")
        conn.execute(
            "DELETE FROM team_members WHERE team_id = ? AND user_id = ?", (team_id, user_id)
        )


def create_invitation(
    team_id: int, email: str, role: str, created_by: int, db_path: str | None = None
) -> dict[str, Any]:
    if role not in ("admin", "member"):
        raise StoreError("Invitations are limited to admin or member roles.")
    token = new_token(24)
    now = _utcnow()
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO invitations (token, team_id, email, role,"
            " created_by, created_at, expires_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (token, team_id, email.strip().lower(), role, created_by, _iso(now),
             _iso(now + timedelta(days=7))),
        )
        return dict(conn.execute("SELECT * FROM invitations WHERE token = ?", (token,)).fetchone())


def get_invitation(token: str, db_path: str | None = None) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT i.*, t.name AS team_name FROM invitations i"
            " JOIN teams t ON t.id = i.team_id WHERE i.token = ?",
            (token,),
        ).fetchone()
    return dict(row) if row else None


def team_invitations(team_id: int, db_path: str | None = None) -> list[dict[str, Any]]:
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT token, team_id, email, role, created_at, expires_at, accepted_at"
            " FROM invitations WHERE team_id = ? AND accepted_at IS NULL AND expires_at > ?"
            " ORDER BY created_at DESC",
            (team_id, _iso(_utcnow())),
        ).fetchall()
        return [dict(row) for row in rows]


def accept_invitation(token: str, user_id: int, db_path: str | None = None) -> dict[str, Any]:
    with _connect(db_path) as conn:
        invite = conn.execute("SELECT * FROM invitations WHERE token = ?", (token,)).fetchone()
        if invite is None or invite["accepted_at"] is not None:
            raise StoreError("This invitation is no longer valid.")
        if datetime.fromisoformat(invite["expires_at"]) <= _utcnow():
            raise StoreError("This invitation has expired.")
        user = conn.execute("SELECT email FROM users WHERE id = ?", (user_id,)).fetchone()
        if user is None or user["email"] != invite["email"]:
            raise StoreError("This invitation was sent to a different email address.")
        conn.execute(
            "INSERT INTO team_members (team_id, user_id, role, status) VALUES (?, ?, ?, 'active')"
            " ON CONFLICT(team_id, user_id) DO UPDATE SET role = ?, status = 'active'",
            (invite["team_id"], user_id, invite["role"], invite["role"]),
        )
        conn.execute(
            "UPDATE invitations SET accepted_at = ? WHERE token = ?", (_iso(_utcnow()), token)
        )
        row = conn.execute(
            "SELECT * FROM teams WHERE id = ?", (invite["team_id"],)
        ).fetchone()
        return dict(row)


def revoke_invitation(team_id: int, token: str, db_path: str | None = None) -> bool:
    with _connect(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM invitations WHERE token = ? AND team_id = ?", (token, team_id)
        )
        return cursor.rowcount == 1


def create_password_reset(user_id: int, db_path: str | None = None) -> str:
    token = new_token(32)
    now = _utcnow()
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM password_resets WHERE user_id = ?", (user_id,))
        conn.execute(
            "INSERT INTO password_resets (token_hash, user_id, created_at, expires_at)"
            " VALUES (?, ?, ?, ?)",
            (hash_guest_token(token), user_id, _iso(now), _iso(now + timedelta(hours=1))),
        )
    return token


def consume_password_reset(
    token: str, password_hash: str, db_path: str | None = None
) -> int:
    hashed = hash_guest_token(token)
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM password_resets WHERE token_hash = ?", (hashed,)
        ).fetchone()
        if row is None or row["used_at"] is not None:
            raise StoreError("This reset link is no longer valid.")
        if datetime.fromisoformat(row["expires_at"]) <= _utcnow():
            raise StoreError("This reset link has expired.")
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, row["user_id"]),
        )
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (row["user_id"],))
        conn.execute("DELETE FROM password_resets WHERE token_hash = ?", (hashed,))
        return int(row["user_id"])


def admin_overview(db_path: str | None = None) -> dict[str, Any]:
    with _connect(db_path) as conn:
        users = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        plan_rows = conn.execute(
            "SELECT plan, COUNT(*) AS n FROM subscriptions GROUP BY plan"
        ).fetchall()
        status_rows = conn.execute(
            "SELECT status, COUNT(*) AS n FROM subscriptions GROUP BY status"
        ).fetchall()
        exports = conn.execute("SELECT COUNT(*) AS n FROM exports").fetchone()["n"]
        teams = conn.execute("SELECT COUNT(*) AS n FROM teams").fetchone()["n"]
        return {
            "users": int(users),
            "exports": int(exports),
            "teams": int(teams),
            "plan_distribution": {row["plan"]: int(row["n"]) for row in plan_rows},
            "status_distribution": {row["status"]: int(row["n"]) for row in status_rows},
            "payments_configured": False,
            "revenue_usd": None,
        }


def admin_subscriptions(
    limit: int = 50, offset: int = 0, db_path: str | None = None
) -> dict[str, Any]:
    with _connect(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM subscriptions").fetchone()["n"]
        rows = conn.execute(
            "SELECT s.user_id, u.email, s.plan, s.status, s.provider, s.provider_ref, s.updated_at"
            " FROM subscriptions s JOIN users u ON u.id = s.user_id"
            " ORDER BY s.updated_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
        return {"total": int(total), "subscriptions": [dict(row) for row in rows]}

# Project Status

> Update after every major milestone. Only record verified state.

- Current phase: Full console (settings/help/history/exports/teams/admin), export gate + pending restoration, interior shell (topbar/crumbs/preview) implemented; owner/CI full-suite run still needed
- Last updated: 2026-10-31
- Current branch: main
- Last verified implementation: `22ff452` plus uncommitted console/interior work
- Working tree: Modified tracked files plus untracked console templates, store/auth/accounts/billing modules, tests, CI, smoke script, briefs, and `PRODUCT_COMPLETION_LOOP.md`; vendor sources untouched except VERIFICATION.json timestamp
- Local app startup command: `npm.cmd --prefix frontend run build` then `C:\Users\rojina\AppData\Local\Python\pythoncore-3.14-64\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Core workflow status: Pipeline, API, UI, exports, replay, accounts, history, dashboard, provider-neutral billing, teams, admin, export gate, pending restoration implemented
- Meta API status: Adapter implemented; live smoke request verified 2026-10-30 (1 synthetic call, 3 mappings, 18.6s); mapping quality on real CSVs still needs per-suggestion review
- Latest verified tests: 91 passed + ruff clean in sandbox (20 TestClient env-blocked, updated but not run); frontend browser workflow passed earlier; axe/source/build/Hallmark passed earlier

## Milestone status

| Milestone | Status | Evidence / commit | Notes |
|---|---|---|---|
| Workspace and Git bootstrap | Implemented | `91793d8` | Local-only root commit; no remote |
| CSV pipeline and API | Implemented | Unit/API tests | Strict schema-driven validation |
| Schema and mapping | Implemented | Unit/API tests | Manual and local suggestions |
| Validation and transformations | Implemented | Unit/API tests | Strict configured types and allowlist |
| Exports and recipe replay | Implemented | Unit/API tests | Fixed ZIP member names |
| Meta adapter / fake-provider tests | Implemented | `tests/test_meta_client.py` | Invalid-model-output and failure paths covered |
| Real Meta API request | Verified 2026-10-30 | `scripts/test_meta_api.py` (owner-run) | 1 synthetic request, 3 mappings, 18.6s; round trip only, not real-CSV validation |
| Frontend end-to-end workflow | Implemented and browser verified | `/`, `/app`, `/privacy` | Workspace sample profile, local mapping, export, and UI recipe replay exercised |
| Landing redesign | Implemented and rendered | `frontend/src/pages/Landing.tsx`; captures under `docs/visual-qa/` | Verified Predictive Arc; Glass CTA adapter; working Sable dock; dark/light persisted themes; real sample pipeline |
| Landing repair | Implemented and rendered | `docs/visual-qa/landing-repair.md` and `landing-repair-*.png` | Reduced overlay, centered stack, single animated responsive dock, repaired theme click target and light contrast; canvas motion measured in browser |
| ThreeUI source and licenses | Verified | `frontend/src/vendor/threeui/VERIFICATION.json` | 24 source files and 15,176-byte Fragment Mono asset match supplied SHA-256; ThreeUI Community MIT, font OFL 1.1 |
| Payment methods | Not implemented | Product surface shell | No billing provider configured; card/bank/wallet checkout unavailable; no card data collected or stored |
| Product surface shell | Implemented, uncommitted | `app/templates/product_page.html` | Persistent left nav; Home/Dashboard/Billing/Payments verified with all five links; payments unavailable boundary shown |
| Accounts and sessions | Implemented, uncommitted | `app/services/auth.py`, `app/api/accounts.py`, `tests/test_auth.py`, `tests/test_accounts.py` | PBKDF2 auth, server sessions, CSRF, throttle; unit tests pass in sandbox, route tests need owner/CI run |
| Guest history and restoration | Implemented, uncommitted | `app/services/store.py`, `tests/test_store.py`, `tests/test_exports.py` | Bounded restorable export records, guest claim on signup; recording never fails downloads |
| Dashboard and navigation | Implemented, uncommitted | `app/templates/dashboard.html`, `tests/test_dashboard.py`, `tests/test_nav.py` | Per-user/guest history, auth-aware sidebar, mobile top bar; templates render-verified |
| Provider-neutral billing | Implemented, uncommitted | `app/services/billing.py`, `app/templates/billing.html`, `tests/test_billing.py` | Plans/entitlements, usage tracking, NullProvider seam; quotas off; no provider |
| Export gate + pending restoration | Implemented, uncommitted | `app/api/accounts.py`, `pending.html`, `tests/test_console.py` | Re-downloads auth-only; guest work claimed on login; `/exports/pending`; download marks restored |
| Customer console screens | Implemented, uncommitted | settings/help/history/exports/detail/pending templates | Password+sessions+profile, searchable/filtered history, download center; direct-call tests pass |
| Teams + admin | Implemented, uncommitted | teams/team_detail/invite_accept/admin templates | Owner/admin/member roles, invite links, shared history metadata, ADMIN_EMAILS gate; backend-enforced |
| Interior shell + workspace | Implemented, uncommitted | `base.html`, `home.html`, `app.js`, `styles.css` | Grouped nav, plan footer, breadcrumb topbar, preview table, guest save-nudge; JS syntax-checked |
| Export isolation fix | Implemented, uncommitted | `app/services/store.py`, `tests/test_store.py` | `list_exports` no longer leaks rows across users/guests; regression test added |

## Decisions needed

- Payment-provider selection/credentials and paid-checkout approval are still pending owner decisions.

## Risks/blockers

- Payment provider setup, credentials, live checkout, and any paid verification remain blocked on owner approval.
- TestClient suites (20 tests) cannot run in the sandboxed shell (loopback sockets denied); they need an owner or CI run before completion is fully verified.
- Do not infer billing behavior beyond the verified seam: paid checkout, webhooks, and quota enforcement are absent.

## Next action

Next: owner/CI run of the full pytest suite (20 updated TestClient tests unverified) + browser suite for the workspace JS changes, then commit/publish decisions (all gated on owner approval). Figma MCP setup remains a host-side task. Optional performance follow-up is lazy-loading/splitting the Three.js bundle; address the Starlette/HTTPX deprecation when upgrading the test stack. Do not make Meta API calls without explicit authorization.

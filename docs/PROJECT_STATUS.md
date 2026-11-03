# Project Status

> Update after every major milestone. Only record verified state.

- Current phase: Reference-based interior workspace/dashboard/billing/auth pass complete; landing hero preserved
- Last updated: 2026-11-03
- Current branch: main
- Last verified implementation: pending local reference-based interior checkpoint
- Working tree: intended interior changes are pending commit; pre-existing untracked `browser-run.log`, `omni.txt`, `Last_execution_prompt.md`, `importguard-workspace-full.png`, and `tatus --short` remain unstaged
- Local app startup command: `.\start-local.bat`, which builds the frontend and starts Uvicorn at `http://127.0.0.1:8000`
- Core workflow status: Pipeline, API, UI, exports, replay, accounts, history, dashboard, provider-neutral billing, teams, admin, export gate, pending restoration implemented
- Meta API status: Adapter implemented; live smoke request verified 2026-10-30 (1 synthetic call, 3 mappings, 18.6s); mapping quality on real CSVs still needs per-suggestion review
- Latest verified tests: 112 passed + Ruff clean; frontend Vitest 2 passed, Vite build passed, source verification remains unchanged and previously passed for 24 files plus Fragment Mono, and browser workflow plus custom interior QA passed against `127.0.0.1:8000`; only the known deprecation/build-size warnings remain
- URL diagnosis: no public deployment URL or deployment manifest is configured. The application is locally reachable at `http://127.0.0.1:8000` after running the launcher.

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
| Product surface shell | Implemented | `b94da00`, `app/templates/product_page.html` | Persistent left nav; Home/Dashboard/Billing/Payments verified with all five links; payments unavailable boundary shown |
| Accounts and sessions | Implemented | `b94da00`, `app/services/auth.py`, `app/api/accounts.py`, `tests/test_auth.py`, `tests/test_accounts.py` | PBKDF2 auth, server sessions, CSRF, throttle; covered by the local 111-test run |
| Guest history and restoration | Implemented | `b94da00`, `app/services/store.py`, `tests/test_store.py`, `tests/test_exports.py` | Bounded restorable export records, guest claim on signup; recording never fails downloads |
| Dashboard and navigation | Implemented | `b94da00`, `app/templates/dashboard.html`, `tests/test_dashboard.py`, `tests/test_nav.py` | Per-user/guest history, auth-aware sidebar, mobile top bar; browser/template verified |
| Provider-neutral billing | Implemented | `b94da00`, `app/services/billing.py`, `app/templates/billing.html`, `tests/test_billing.py` | Plans/entitlements, usage tracking, NullProvider seam; quotas off; no provider |
| Export gate + pending restoration | Implemented | `b94da00`, `app/api/accounts.py`, `pending.html`, `tests/test_console.py` | Re-downloads auth-only; guest work claimed on login; `/exports/pending`; download marks restored |
| Customer console screens | Implemented | `b94da00`, settings/help/history/exports/detail/pending templates | Password+sessions+profile, searchable/filtered history, download center; direct-call tests pass |
| Teams + admin | Implemented | `b94da00`, teams/team_detail/invite_accept/admin templates | Owner/admin/member roles, invite links, shared history metadata, ADMIN_EMAILS gate; backend-enforced |
| Interior shell + workspace | Implemented | `b94da00`, `base.html`, `home.html`, `app.js`, `styles.css` | Grouped nav, plan footer, breadcrumb topbar, preview table, guest save-nudge; JS syntax-checked |
| Export isolation fix | Implemented | `b94da00`, `app/services/store.py`, `tests/test_store.py` | `list_exports` no longer leaks rows across users/guests; regression test added |
| Reference-based interior pass | Implemented | Pending local checkpoint | Full-width CSV intake/preview/quality stage, data-backed dashboard metrics and usage, honest plan cards/payment state, account form polish and optional display-name persistence; landing hero untouched |

## Decisions needed

- Payment-provider selection/credentials and paid-checkout approval are still pending owner decisions.

## Risks/blockers

- Payment provider setup, credentials, live checkout, and any paid verification remain blocked on owner approval.
- The current local Python environment ran the full 111-test suite; the prior sandbox-only TestClient limitation is no longer present in this verification.
- Do not infer billing behavior beyond the verified seam: paid checkout, webhooks, and quota enforcement are absent.

## Next action

Next: review the local checkpoint and choose a deployment target only if a public URL is required; no deployment or push has been performed. Optional performance follow-up remains lazy-loading/splitting the Three.js bundle and addressing the Starlette/HTTPX deprecation. Do not make Meta API calls without explicit authorization.

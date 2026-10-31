# Product Completion Loop — ImportGuard

## Scope
Continue in ordered checkpoints through the payment-option milestone. Keep existing local CSV processing, mapping, validation, exports, replay, and Meta safety behavior intact. No commit, push, deployment, publication, external messaging, or charges.

## Loop
1. Fix CSV preview/table contrast and verify readable values in both themes.
2. Build a persistent left application shell with Home, Dashboard, Workspace, Billing, and Payments navigation.
3. Implement each route as a working product surface, connecting Workspace to the existing FastAPI CSV and Meta endpoints.
4. Add authentication/account flows only where supported by verified project requirements; keep account/security boundaries explicit.
5. Implement billing and payment-option UI; integrate a provider only when credentials and environment are available, without sending live requests or charging.
6. After each coherent change, run the narrow relevant tests, frontend build, and available browser checks; inspect failures and repair before continuing.
7. Stop at the payment-option milestone or a concrete external blocker. Record exact work, verification, blocker, and next loop item.

## Safety and constraints
Preserve existing user changes, untracked files, and secrets. Never print or copy `.env` contents. Do not use or expose provider credentials in the browser. Any external provider setup or live payment operation requiring credentials, account approval, or charges is a documented blocker, not a simulated success.

## Master directive execution (2026-10-31)

- Figma MCP: BLOCKED. (1) This session's toolset has no MCP or Figma tools, so the file cannot be opened, edited, or verified from here. (2) The likely host config path is access-denied to the sandbox user and no project MCP config exists. Host-side setup by the user is required. Figma file work, evidence transfer, and the Figma approval gate are all blocked; implementation proceeds against `IMPORTGUARD_APP_INTERIOR_VISUAL_SPEC.md` + the master directive as interim authority, with in-app screenshots as the review vehicle.
- Scope per directive: export gate + restoration, settings, help, history, exports, teams/enterprise, admin finance, topbar, workspace preview/results, interior polish. Landing/hero untouched. No provider, no charges, no live Meta calls.

## Completion checkpoint — accounts/history/billing (2026-10-31)

- Auth: email/password signup/login/logout, server sessions, CSRF, throttle, account deletion (`app/services/auth.py`, `app/api/accounts.py`, `auth.html`).
- Guest-to-export: every process/replay run records a restorable export (bounded ZIP, 7-day expiry); guests get history via browser token; signup/login claims guest rows.
- Dashboard: per-user/guest stats + history table with download links (`dashboard.html`).
- Navigation: sidebar shows all five destinations plus auth state (email + sign out, or sign in/up); mobile top bar keeps links + auth.
- Billing: plan/entitlement model, usage tracking, `BillingProvider` seam with `NullProvider`; quotas off; no provider, no prices, no charges.
- Tests: 7 new test files; 23 new sync unit tests pass in sandbox; TestClient suites committed for owner/CI (sandbox denies loopback sockets). Ruff clean; vitest/build green; 8 templates screenshot-verified at 1280/390, dark + light.
- Remaining gates: owner/CI full pytest run; commit/publish/deploy/video/submission approvals. No provider integration.

## Current checkpoint — 2026-10-31

- Completed: dark-mode CSV preview contrast fix; shared responsive left navigation; Home, Dashboard, Billing, and Payment Options pages; Workspace remains connected to existing CSV/Meta APIs.
- Completed: payment methods are clearly shown as unavailable; the page states that it neither collects nor stores payment details.
- Account flows: not implemented because verified repository requirements explicitly exclude accounts/authentication and no account-specific requirements were supplied.
- External blocker: secure checkout needs a selected provider, provider account/credentials and webhook setup, an authenticated customer identity or defined guest-checkout policy, and agreed billing/pricing terms. No credentials or charges were used.
- Verification: backend suite 34 passed; Vite production build passed with the existing >500 kB chunk warning; browser checks covered all five routes, dark preview contrast, all five mobile nav links, and no horizontal overflow at 390px.
- Next loop item: choose provider and billing requirements, then supply approved provider setup through server-side configuration before enabling checkout. Do not make live payment requests until explicitly approved.

## Completion checkpoint — console + interior (2026-10-31)

- Guest export gate + pending restoration: IMPLEMENTED + VERIFIED (sandbox). Re-downloads require auth (401 guests, 404 foreign); login/signup claims guest rows; `/exports/pending` + `/api/exports/pending`; downloads mark restored. First process download stays open (preserves verified behavior).
- Customer screens (settings/help/history/exports/detail): IMPLEMENTED + VERIFIED (sandbox). Profile/password/sessions/delete, searchable/filtered/paginated history with validation status, download center with pending banner.
- Enterprise + admin: IMPLEMENTED + VERIFIED (sandbox). Teams with owner/admin/member, invite links (manual share, no email), shared history metadata, `ADMIN_EMAILS` gate with 401/403 JSON + page parity.
- Interior shell + workspace: IMPLEMENTED + SANDBOX-CHECKED. Grouped nav (Workspace/Your data/Account), plan footer, breadcrumb topbar, operational home, 4-stat dashboard, preview table, guest save-nudge. JS syntax-checked; browser behavior needs owner run.
- Security fix: `list_exports` isolation leak fixed + regression test; dead `mark_downloaded` removed; converged on pre-existing session/name helpers.
- Verification: 91 passed / 20 env-blocked (same loopback-blocked TestClient set, updated for new contracts); ruff clean; `node --check` clean; every page render-swept (status + `None` leaks).
- Blocked (owner-gated): full TestClient suite, browser suite re-run, Figma MCP host setup, commit/push/deploy/video/submission. No live Meta calls, providers, or charges.

## Completion checkpoint — visual QA + handoff (2026-10-31)

- Static QA: VERIFIED. 51 routes, zero dead links; CSS cross-check clean (2 legacy-fallback exceptions noted).
- Visual QA: VERIFIED (manual labeled pass). 12 screenshots reviewed; 2 mobile defects fixed; 390 via emulation (headless minimum-viewport limit documented).
- Handoff: `design/` as-built package + `visual-qa/` evidence complete. Figma file work BLOCKED (no MCP tools); unblock steps in `design/FIGMA_UNBLOCK.md`.
- DESIGN APPROVAL REQUESTED from owner on the as-built interior. Independent-QA limitation disclosed (no separate agent available).

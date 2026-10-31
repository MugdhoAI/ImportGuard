# ImportGuard Implementation Map (As-Built)

Maps `IMPORTGUARD_APP_INTERIOR_VISUAL_SPEC.md` sections to shipped code.
Deviations are deliberate and documented, not oversights.

| Spec § | Shipped as | Notes / deviation |
|---|---|---|
| §4 shell + sidebar groups | `base.html`: WORKSPACE / YOUR DATA / ACCOUNT + ADMIN | Teams lives under ACCOUNT (spec predates Teams). Plan footer + account menu at bottom per spec. |
| §4 topbar | `.topbar` breadcrumb + theme toggle | No search/notifications (none real — spec forbids filler). Help + account stay in sidebar. |
| §5 workspace + preview | `app.html`/`app.js`, `/api/profile.preview` | Real 10-row preview table added; samples kept. |
| §5 export action | Immediate ZIP + history save + guest save-nudge | DEVIATION: first download stays open (preserves verified behavior + browser suite). Gate applies to re-downloads. |
| §6 gate + restoration | Sign-in-to-download links, claim-on-login, `/exports/pending` | No blocking modal (same reason as above). Restoration verified by tests. |
| §6 signup/signin | `auth.html` + forgot/reset | No password-visibility toggle (browser default); reset email honestly unavailable. |
| §7 home | `home.html` | Guest marketing preserved; users get activity + usage. |
| §8 dashboard | `dashboard.html` | 4 real metrics incl. needs-attention; no charts (no invented data). |
| §9 history | `history.html` + query/filter/page | Validation status (Completed/Needs review); search + status + pagination all real. |
| §10 exports | `exports.html`, `pending.html`, `export_detail.html` | Pending/downloaded/expired distinguished; expired never offered. |
| §11 billing | `billing.html` (unchanged structure) | No prices (unapproved); quotas from `billing.PLANS`; upgrades unavailable-honest. |
| §12 payments | `product_page.html` (unchanged) | All methods unavailable; no card collection. |
| §13 teams | `teams.html`, `team_detail.html`, `invite_accept.html` | Roles + invites + shared metadata. DEVIATION: downloads stay owner-only (no team file ownership model). |
| §14 settings | `settings.html` | Profile/password/sessions/delete. No email change, no data export (unsupported → omitted, not faked). |
| §15 admin | `admin.html`, `ADMIN_EMAILS` gate | Real counts; no revenue (no provider); sidebar-hidden for non-admins. |
| §16 states | All pages | Empty/loading (workspace)/error/disabled/restricted states implemented; dialogs n/a (no modal dialogs shipped). |
| §17 responsive | CSS media 640/600/850 | Verified 1280/768/390-emu; tables scroll; no page overflow. |
| §18 accessibility | Templates | Landmarks, labels, table headers, focus-visible (existing), reduced-motion (existing), text+color status. Axe re-run is owner-side (needs browser). |
| §19 components | `component-inventory.md` | Shared classes; no per-page styling forks. No toasts/pagination-JS (server-rendered instead). |

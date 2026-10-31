# ImportGuard Current UI Inspection

Inspection-only review of the `vispic/` screenshots against the implementation in `C:\ImportGuard`. No source files were modified. Screenshots captured 2026-10-31, 14:44–15:09 local time.

## 1. Screenshots inspected

| # | Filename | Captured | Depicts |
|---|---|---|---|
| 1 | `127.0.0.1_8000__utm_source=chatgpt.com (1).png` | 14:44 | Public landing `/`, full page (~720px wide render) |
| 2 | `127.0.0.1_8000_app.png` | 15:07 | Workspace `/app`, full page, dark |
| 3 | `Screenshot 2026-10-31 150655.png` | 15:06 | Home `/home`, dark |
| 4 | `Screenshot 2026-10-31 150719.png` | 15:07 | Dashboard `/dashboard`, guest empty state, dark |
| 5 | `Screenshot 2026-10-31 150759.png` | 15:08 | Billing `/billing`, guest, dark |
| 6 | `Screenshot 2026-10-31 150819.png` | 15:08 | Payments `/payments`, dark |
| 7 | `Screenshot 2026-10-31 150839.png` | 15:08 | Login `/login` card, dark, no sidebar |
| 8 | `Screenshot 2026-10-31 150855.png` | 15:08 | Signup `/signup` card, dark, no sidebar |
| 9 | `Screenshot 2026-10-31 150932.png` | 15:09 | Privacy `/privacy`, dark (below header) |

## 2. Existing screens and current visual state

### Public landing `/` (screenshot 1)

Exists. Dark art-directed page, visually separate from the app interior: top bar (IG ImportGuard wordmark left, Light toggle right), centered Sable dock (Home/How/Workflow/Import/Privacy/Guide), Predictive Arc dotted-glow hero with "Make every CSV import predictable." headline, glass pill CTA ("IG Start an import") plus "See the workflow ↓" link. Below: "Keep every decision in view." with numbered 01–03 steps, "Review a real sample run." with "Load synthetic sample" button and fixture panel, "Keep the recipe with the result." with "Open the workspace ↗", footer with privacy link. Typography is large tight display type; violet accents on near-black. Looks complete and polished. Only narrow-width capture exists; desktop ≥1280 not shown here.

### Home `/home` (screenshot 3)

Exists. App interior with persistent left sidebar (IG brand, WORKSPACE: Home/Dashboard/Workspace, ACCOUNT: Billing/Payments, guest Sign in/Create account, Privacy link, Theme button). Content: eyebrow + "Good work starts with a clean import." headline, "Start an import →" button, "Bring a file into a known shape." card with 01–04 step chips and "Open Workspace →", "Keep your data in view" card with three feature columns. Consistent card system, generous spacing. Complete as an overview page; it is a static launcher, not a data view.

### Dashboard `/dashboard` (screenshot 4)

Exists, guest empty state only. Same sidebar. Header with "New import →" button, three stat cards (Saved imports 0, Rows processed 0, Current plan Free), "Recent activity" card with "No saved activity yet" empty state. Layout and empty state look intentional and complete. No signed-in/populated dashboard is shown.

### Workspace `/app` (screenshot 2)

Exists and is the densest screen. Sidebar plus its own top header row (brand, LOCAL WORKSPACE badge, Privacy link, "Switch to light theme" button), then progress steps 01–04 and stacked cards: dropzone source card, prefilled target-fields table, map/review card ("Suggest locally" + disabled "Suggest with Meta AI · unavailable" + samples consent checkbox), approval + "Validate & download package" card, replay card, three explainer cards. Visually complete; the workflow reads top-to-bottom. Weakness: the header duplicates sidebar controls (second brand, second Privacy link, second theme toggle) — see §6.

### Billing `/billing` (screenshot 5)

Exists, guest view. Current-plan card ("Free", "0 of 25 monthly exports used", "Active · No provider" pill), three-column upgrade grid (Pro, Business with disabled "Provider setup required" buttons, Checkout status text), Invoices empty state. Honest unavailable-by-design presentation. No signed-in view (usage counts, delete-account form) is shown.

### Payments `/payments` (screenshot 6)

Exists. Three unavailable method rows (card, bank transfer, local methods with Unavailable/Not configured pills) plus "Checkout is not active" blocker card. Static by design; complete for its purpose. Copy issue: "No payment credentials or account service are configured" — an account service now exists (see §8).

### Login `/login` and signup `/signup` (screenshots 7–8)

Exist. Centered single cards, no sidebar: eyebrow, headline, one-line description, email + password fields, full-width violet submit, switch/guest links. Clean and consistent with the card system. No error, loading, or caps-lock states shown; no post-login redirect evidence.

### Privacy `/privacy` (screenshot 9)

Exists. Long-form notice page (header cropped out of frame): stated local-first behavior, CSV upload retention (7-day export entries, guest token, account deletion), Meta opt-in rules, synthetic-data guidance. Copy matches implemented behavior.

## 3. Screenshot-to-source-code mapping

| Screenshot | Route | Template / component | Styles | Match |
|---|---|---|---|---|
| 1 landing | `GET /` (`app/main.py:28`, serves `frontend/dist/index.html`, exists) | `frontend/src/pages/Landing.tsx`, `GlassImportButton.tsx`, `ImportGuardDock.tsx`, `PredictiveArcBackdrop.tsx` | `frontend/src/styles/landing.css` | Accurate |
| 2 workspace | `GET /app` (`app/main.py:46`) | `app/templates/app.html` + `base.html` sidebar, `app/static/js/app.js` | `app/static/css/styles.css`, `theme.css` | Accurate |
| 3 home | `GET /home` (`app/main.py:63`) | `app/templates/product_page.html` (home branch) | as above | Accurate |
| 4 dashboard | `GET /dashboard` (`app/main.py:68`) | `app/templates/dashboard.html` guest branch | as above + `.history-table` | Accurate |
| 5 billing | `GET /billing` (`app/main.py:95`) | `app/templates/billing.html` guest branch | as above | Accurate |
| 6 payments | `GET /payments` (`app/main.py:105`) | `app/templates/product_page.html` (payments branch) | as above | Accurate visually; one stale sentence (§8) |
| 7 login | `GET /login` (`app/api/accounts.py:86`) | `app/templates/auth.html` login mode | `.auth-card` rules | Accurate |
| 8 signup | `GET /signup` (`app/api/accounts.py:93`) | `app/templates/auth.html` signup mode | `.auth-card` rules | Accurate |
| 9 privacy | `GET /privacy` (`app/main.py:116`) | `app/templates/privacy.html` | as above | Accurate |

Navigation connects correctly per source: every shell page extends `base.html`, whose sidebar links all five destinations (`/home`, `/dashboard`, `/app`, `/billing`, `/payments`) with `aria-current` marking; `/workspace` aliases `/app` (`app/main.py:58`); auth links route to `/login` and `/signup`. The landing CTA links to `/app` and is a separate React bundle from the server-rendered interior (fallback `app/templates/landing.html` only serves if `frontend/dist` is absent).

## 4. Implemented versus unverified functionality

Do not treat visibility as proof of function. Status below combines screenshots with source/test evidence:

- Implemented and test-covered: CSV profile/map/validate/export/replay, recipe handling, guest export recording + restoration + claim, signup/login/logout/delete, per-user and guest dashboard history, download ownership checks, plan/usage state, NullProvider refusal. Covered by `tests/test_*.py` (sync suites green; TestClient suites committed for owner/CI run).
- Implemented, visually confirmed, not shown exercised: sign-in/out flows, populated dashboard, billing usage counts, delete-account form, CSV upload mid-flow states, sample loader result, light theme, mobile widths.
- Explicitly non-functional by design (honest placeholders): Meta suggestion button (disabled without server key), Pro/Business upgrade buttons (disabled, "Provider setup required"), all payment methods (Unavailable/Not configured), checkout blocker card.
- Unverifiable from screenshots alone: session persistence across restart, actual download bytes, claim transfer, throttle behavior, expiry cleanup, axe/contrast results.

## 5. Visual strengths

- Landing is genuinely art-directed (dark arc hero, glass CTA, dock) and clearly separated from the utilitarian interior — matches the stated priority in `IMPORTGUARD_APP_INTERIOR_VISUAL_SPEC.md` ("Preserve the existing public landing page and hero section").
- Interior has one consistent system: sidebar + eyebrow/headline headers, 16px cards, violet primary buttons, muted secondary text, dark-first with persisted light theme.
- Empty and unavailable states are explicit and honest (guest dashboard, invoices, payments, Meta button) rather than blank or fake.
- Workspace progress steps (01–04) plus numbered cards give a clear top-to-bottom workflow.

## 6. Visual weaknesses and inconsistencies

1. **Duplicated chrome on `/app`** (screenshot 2, `app/templates/app.html:5` vs `base.html` sidebar): brand, Privacy link, and theme toggle each appear twice on one screen. Other shell pages show them once.
2. **Two entry CTAs with different labels**: landing says "Start an import", Home says "Start an import →", dashboard says "New import →", empty state says "Start an import" (text link). Same destination, four labels.
3. **Sidebar bottom crowding**: Sign in, Create account, Privacy link, and full-width Theme button stack tightly at the sidebar foot (screenshots 2–6).
4. **Billing upgrade grid fragility**: the third "Checkout status" article is text-only while siblings have buttons, leaving the row visually uneven (screenshot 5).
5. **Landing-to-app typography break**: landing uses large display type and violet-on-black glow; interior uses Manrope/system small type. Intentional separation, but the handoff at `/app` is abrupt.
6. **Auth pages lack context chrome**: no brand mark or back-to-home affordance beyond text links (screenshots 7–8).

## 7. Missing screens or incomplete flows

- Signed-in dashboard with populated history table; signed-in billing with usage and delete-account form; sidebar signed-in state (email + Sign out).
- Light theme rendering of any screen; any mobile-width capture; workspace mid-flow (profile results, mapping table, errors, success summary); sample-loader result on landing.
- `/workspace` alias (same template as `/app` — likely identical, unshown), server fallback landing (`landing.html`, only serves without a frontend build), 404/500 states, form error and loading states.
- No capture shows an actual file upload, download, claim, logout, or delete-account result.

## 8. Outdated screenshots or discrepancies

- Payments copy is stale: "No payment credentials or account service are configured" (`product_page.html`, payments branch) — the account service exists now that signup/login/dashboard/billing are implemented. Screenshot 6 faithfully shows the stale text, so the screenshot is current but the copy lags the product.
- All other screenshots match the current tree: captures postdate the accounts/history/billing implementation and show its UI (guest auth links, dashboard stats, billing plan card, auth pages).
- No screenshot is outdated relative to source; coverage gaps (signed-in states, light, mobile, mid-flow) are omissions, not mismatches.

## 9. Recommended priorities for the next design stage

1. Preserve the landing page and hero untouched (per the visual spec priority and its verified state).
2. Deduplicate the `/app` header: keep the sidebar as the single chrome and reduce the workspace header to title + badge, or vice versa.
3. Correct the payments "account service" sentence to reflect accounts existing.
4. Design the unseen states before restyling: signed-in dashboard/billing, form errors, loading, upload mid-flow, light theme, and 390px layouts.
5. Unify entry-CTA labeling ("Start an import" vs "New import") and sidebar-foot spacing.
6. Rebalance the billing upgrade grid (three equal actions or a two-card row plus status note).
7. Add brand/back affordance to auth cards.
8. Capture the missing screenshots after any change and re-run this inspection before implementation phases begin.

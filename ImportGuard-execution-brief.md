# ImportGuard execution brief — review draft

**Status:** Prepared for owner review. This document does not authorize application changes, API spend, publication, or deployment. If approved, it should become the single concise execution brief in `C:\ImportGuard`; until then, existing repository instructions remain in force.

## Current checkpoint (verified 2026-10-30)

- Repository: `C:\ImportGuard`; branch `main`; HEAD `22ff452` (`docs: preserve visual redesign references and handoff`), tracking `origin/main`.
- The handoff/status documents are stale (dated 2026-10-27 and referring to branch `master`). They say the landing repair is done; the live checkout has three modified CTA files and an untracked `ImportGuard_Glass_CTA_Codex_Fix.md`. Preserve these user changes. No test/build was run for this audit.
- Current uncommitted work is narrowly about making the landing page's Three.js glass CTA one ImportGuard-branded, accessible action to `/app`. Its brief gives acceptance criteria. It has not been verified as complete. This is the proposed first implementation task after approval.
- The existing FastAPI service and deterministic, in-memory CSV workflow, optional server-side Meta adapter, Vite/React landing/workspace, privacy page, sample workflow, recipe replay, and automated checks are documented as implemented. The Meta live call is explicitly unverified; no API call is authorized by this brief.
- No product dashboard, product-specific sidebar, account/settings system, authentication, persistence, plans, quotas, checkout, or payments are documented as implemented. No such feature should be represented as available.

## Repository guidance and scope reconciliation

Read `AGENTS.md`, `CODEX_CONTINUITY_PROTOCOL.md`, `CODEX_EXECUTION_PLAN.md`, `CODEX_DESIGN_REFERENCE_GUIDE.md`, `CODEX_VISUAL_REDESIGN_PLAN.md`, `design.md`, `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md`, and the current `docs/` status, architecture, decisions, tests, and handoff records before implementation. Existing guidance protects the working CSV flow, Meta key, privacy, design assets, and no-publish/no-cost gates. Older MVP scope explicitly excluded accounts and billing. The owner's current commercial-SaaS direction supersedes that product-scope exclusion, but does not erase security, privacy, continuity, or external-action safeguards.

Keep the existing FastAPI CSV and export behavior as the core product. The screenshot is a reference only for familiar navigation hierarchy. Translate its categories into ImportGuard tasks, for example: **Dashboard**, **New import**, **Import history**, **Saved recipes**, **Usage**, **Plan & billing**, and **Settings**. Do not copy Meta's labels, layout, identity, or unrelated Chat/Image/Audio/Segment tools. Preserve the existing landing and real CSV workflow unless an approved task requires a measured change.

## Hackathon eligibility and submission check

The participant guide was not found among the repository files or Downloads during this audit. No attached guide was available in the referenced conversation payload beyond the UI screenshot. The repository execution plan contains claims attributed to that guide (public repository and a three-minute demo); these claims are **not verified** by the official pages checked and must not be treated as binding until the actual guide/official rules or portal confirm them.

Official event pages checked on 2026-10-30 state that participation is selected/accepted, virtual and worldwide subject to local law, sanctions/export restrictions, and specified organizer/Meta employment, government-affiliation, family, and household exclusions. One of the listed excluded jurisdictions/entities must be checked against the current official terms. The pages describe Indie and Startup tracks and the themes “Build for Your World” and “Push the Frontier”; they list the submission deadline as November 4, 2026, 9:00 PM ET. At the event's November date, that is **November 5, 2026, 8:00 AM Bangladesh time**. The page still says full Official Rules will be published before kickoff, so definitive submission fields, age/team conditions, project start-date/originality rules, video format/length, repository visibility, and other legal conditions remain unverified here. Confirm the participant's accepted status and review the actual current rules/guide before submission. Do not publish a repository or submit anything without approval.

ImportGuard plausibly fits **Build for Your World** as a practical CSV-import reliability tool, but theme fit is an interpretation, not an eligibility guarantee. The optional Meta mapping adapter exists; no real Meta request was verified. Do not claim a live model contribution without a real, authorized result. The product should preserve the manual deterministic workflow when Meta is unavailable.

## Proposed architecture and ordered roadmap

The current app is local-first and stateless; commercial multi-user use changes its trust and data model. Do not bolt authentication or payment UI onto it before a short architecture decision. Keep the FastAPI core and current deterministic engine; choose persistence, tenant isolation, session/auth approach, deployment target, payment provider, data-retention policy, and supported currency only after explicit review. Never store uploaded CSVs by default unless a specific user-facing feature needs it and retention/deletion behavior is designed.

1. **Gate 0 — audit and CTA finish:** preserve the dirty tree; verify only the existing CTA change against its brief, existing source guard, click/keyboard behavior, focus/accessibility, and build. Fix only defects in that task. Do not redesign the landing or add product features.
2. **Gate 1 — product and data architecture:** map routes, data flows, threats, tenancy, storage, retention/deletion, quota accounting dimensions, provider choices, and operating-cost assumptions. Present choices before implementation. Decide how a Free/Pro/Business plan can be tested without real charges. Do not finalize prices or advertise unbuilt capabilities.
3. **Gate 2 — reliable account foundation:** implement the approved authentication/session and user/tenant persistence model, authorization checks, account lifecycle, and privacy controls; preserve current single-user/local workflow where practical.
4. **Gate 3 — controlled usage and plans:** enforce server-side monthly import count plus bytes/file size, rows/columns or processing complexity, and Meta token/request budgets. Make quotas atomic and idempotent; show remaining allowance, reset timing, clear blocked/failed-job behavior, and manual fallback. Define configurable Free/Pro/Business entitlements; treat previously floated `$9.99` and `$17.99` only as unapproved examples.
5. **Gate 4 — product workspace:** add a product-specific sidebar, dashboard of real import activity/usage, onboarding that reaches a successful first import, saved history/recipes as user-scoped data, and settings for profile, privacy, security, and plan. No fake metrics or dead links.
6. **Gate 5 — billing:** select a provider only after review; implement checkout/portal and verified webhook-driven subscription state, cancellation/renewal handling, receipts/tax/currency decisions, and test-mode end-to-end coverage. Never create a paid service or make a live charge without separate approval.
7. **Gate 6 — SaaS readiness:** test tenant isolation, upload/resource limits, CSRF/session controls, abuse/rate limiting, secrets, logging, backup/deletion, accessibility, recovery, and cost ceilings. Review privacy/legal copy and actual data flows. No claim of security certification.
8. **Gate 7 — release/submission:** prepare reproducible setup, truthful demo and submission materials against the actual rules. Deployment, public repo changes, purchases, live Meta requests, and submission each remain separate explicit approval gates.

At each gate, Muse should inspect, plan only the smallest next unit, implement, run directly relevant checks, review the diff and actual UX, fix failures, and repeat. Stop at an approval gate or when that phase's acceptance criteria pass. Never batch speculative work across gates.

## Decision requested

Approve or revise the architecture/roadmap and the narrow first task: finish reviewing and verifying the already-started CTA repair. Also provide the actual participant guide/current official rules if they are in another location; until verified, submission-specific requirements remain open.

## Sources

- Official event and current eligibility/timeline: <https://events.cerebralvalley.ai/e/meta-ai-developer-hackathon>
- Official Meta event overview: <https://dev.meta.ai/events/global-hackathon>
- Official-linked application overview/waiver: <https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver> (page extraction exposed a loading shell during this check)
- Event details page: <https://cerebralvalley.ai/e/meta-ai-developer-hackathon/details> (page extraction exposed a loading shell during this check)

# ImportGuard Technical and Scope Decisions

Record material decisions, alternatives considered, and reasons. Keep entries concise and dated. Do not use this file for speculative or unverified claims.

## Decision log

### Initial constraints
- Date: 2026-10-27
- Decision: Small Python/FastAPI application with server-rendered HTML, CSS and vanilla JavaScript.
- Reason: Reduce setup/integration burden for a solo hackathon MVP.
- Alternatives not chosen initially: React/Next.js, Supabase, database, background jobs, Docker, microservices.
- Revisit only if implementation evidence establishes a need.

- Decision: Manual mapping and deterministic CSV processing must work without Meta API credentials/credits.
- Reason: Do not block useful local functionality on billing/account access.

- Decision: Keep local-only by default; no public deployment or Git push without approval.
- Reason: Avoid accidental exposure or cost.

## Further decisions

Add decisions below using:
- Date:
- Decision:
- Reason/evidence:
- Alternatives considered:
- Consequences and revisit condition:

### Implementation decisions — 2026-10-27
- Decision: Keep uploads stateless and in memory; the browser re-uploads the selected file to each endpoint.
- Reason/evidence: CSVs are capped at 5 MB and 5,000 rows, so a database/session store is unnecessary for this MVP.
- Alternatives considered: Persisting uploads or adding a database; rejected to reduce retention and scope.
- Consequences and revisit condition: The browser must keep the selected file for each workflow action.
- Decision: Use native HTML/CSS with a system font stack and no ThreeUI assets or remote fonts.
- Reason/evidence: The design references permit a native implementation; no third-party visual asset is needed for product function.
- Consequences and revisit condition: Typography uses available system fonts.
- Decision: Keep project license undecided; do not add a license grant without owner direction.
- Reason/evidence: No existing license was provided in the starter workspace.
- Consequences and revisit condition: Select an appropriate license before public release.

### Landing redesign — 2026-10-27
- Decision: Add a small Vite + React frontend while retaining FastAPI as the sole application host and backend.
- Reason/evidence: The selected Predictive Arc, GlassAiButton, and AnimatedTopDock sources are React/TypeScript components; the existing CSV routes and server-rendered workspace remain intact.
- Alternatives considered: Replacing the ThreeUI sources with static or hand-drawn visuals; rejected by the supplied design acceptance criteria.
- Consequences and revisit condition: Run `npm.cmd --prefix frontend run build` before starting FastAPI so `/` can serve the built landing page.
- Decision: Keep fetched ThreeUI canonical source files unchanged under `frontend/src/vendor/threeui/`; use separately named ImportGuard adapters and pin source verification hashes.
- Reason/evidence: Exact-source integrity and small product-specific behavior changes are both required by the design plan.
- Consequences and revisit condition: Re-run `npm run verify:sources` before changing vendor source or preparing public distribution.

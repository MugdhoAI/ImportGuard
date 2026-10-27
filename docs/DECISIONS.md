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

### Verified landing and workflow adapters — 2026-10-27
- Decision: Keep the full-screen Predictive Arc scene dark in both page themes and persist the shared theme selection across landing, workspace, and privacy routes.
- Reason/evidence: The chosen hero artwork is intentionally dark; browser navigation confirms the stored theme applies consistently to the existing FastAPI pages.
- Decision: Keep the canonical GlassAiButton HTML in a sandboxed iframe for its visual canvas, with an accessible native anchor layered over it for the product CTA.
- Reason/evidence: The source study's label and activation behavior are not ImportGuard navigation. A semantic anchor ensures keyboard focus, exact product text, and direct `/app` navigation while preserving the canonical canvas source. The app adapter is not byte-identical behavior.
- Consequences and revisit condition: Keep the source bundle unchanged, test its source hashes, and review the overlay if the vendor source changes.
- Decision: Connect the landing preview to the actual bundled synthetic CSV and the existing profile, local mapping, and process endpoints. Replay stays on the existing workspace and `/api/replay` path.
- Reason/evidence: Browser testing verifies accepted/rejected CSV package output and the replayed recipe; no illustrative fake output is used.
- Decision: Keep the compact Sable dock labels product-specific and route each to its real section/page. Use the native dock links at mobile widths.
- Decision: Honor reduced motion in the Predictive Arc renderer and provide the existing Glass CTA link when WebGL is unavailable.
- Reason/evidence: Browser tests exercised the no-WebGL fallback and a still arc under `prefers-reduced-motion`.
- Decision: Record Hallmark waivers 44c and 79 for the intentional full-viewport arc scene only; no page Floor failures, Reflex warnings, or warnings remained in the final run.
- License status: Retrieved canonical ThreeUI Community sources are under MIT terms and the Fragment Mono font is under OFL 1.1, with notices preserved in the vendor folder. Recheck current terms and attribution before public release.

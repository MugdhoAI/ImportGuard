# Codex Instructions for ImportGuard

## Read first
Before editing, read completely:
1. `CODEX_EXECUTION_PLAN.md`
2. `CODEX_DESIGN_REFERENCE_GUIDE.md`
3. `CODEX_VISUAL_REDESIGN_PLAN.md`
4. `design.md`
5. `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md`
6. `CODEX_CONTINUITY_PROTOCOL.md`

The newest design source of truth is `CODEX_VISUAL_REDESIGN_PLAN.md` + `design.md`. These supersede previous visual suggestions (light Lumora layout, Kage/Sylva worlds) for the current redesign. Preserve existing backend behavior and data integrity.

## Goal
Deliver a complete local ImportGuard application with a carefully art-directed landing page, fully functional CSV workspace and verifiable Meta AI integration when explicitly enabled. Do not optimize for speculative awards or add unnecessary product features.

## Mandatory work style
- Inspect current Git state, current routes and the last handoff before edits. Preserve the existing working code.
- Keep working, do not stop at a design plan or mockup.
- Work in small, coherent phases. After every major implementation, run tests, inspect the diff, update status/handoff/test/decision records, and create a local Git checkpoint commit according to `CODEX_CONTINUITY_PROTOCOL.md`.
- Do not stage private data, `.env`, API keys, uploaded CSVs, exports, browser profiles, build artifacts or virtual environments.
- Never claim a test, browser check, API request, hash verification or skill run happened unless it did.
- Do not push, publish, deploy or incur unexpected costs without explicit approval.

## Hallmark and visual quality
- Use Hallmark from https://github.com/Nutlope/hallmark for redesigning the existing page. Install project-locally if missing:
  `npx skills add nutlope/hallmark --agent codex`
- Follow Hallmark's actual skill file and redesign workflow. Use its rendered `sloplint` on the hero first, then the page. Fix every Floor failure; fix Reflex warnings or document each legitimate exception. Do not merely mention Hallmark in a report.
- Build the hero first and screenshot-review it before polishing below-the-fold content.
- Keep `CODEX_VISUAL_REDESIGN_PLAN.md` and `design.md` as acceptance criteria.
- The user explicitly selected PredictiveArcCanvas, AnimatedTopDock Sable, and GlassAiButton. Do not silently substitute approximations. Preserve canonical sources; any small product-specific adapter must be clearly documented and must not falsely claim byte-identical source.
- The owner supplied complete text source references for the Glass button and dock; they are in `references/threeui/`.
- The complete Predictive Arc source bundle is not included in the local reference files. Fetch the canonical JSON bundle and verify hashes before implementation. The attached Aegis HTML is a separate visual sample; it is not the Predictive Arc source. If you cannot fetch/verify the canonical source, report the blocker instead of approximating it.
- Check current source licenses/terms, required font asset and attribution before public release.

## Architecture
- Preserve the existing FastAPI backend, routes, CSV pipeline and tests.
- The requested exact ThreeUI components are React/TypeScript. A small Vite + React + TypeScript frontend is authorized only if needed to integrate those exact components. Keep FastAPI as backend and serve the built frontend from the same app. Do not add Next.js, Supabase, auth systems, databases, microservices, analytics or unrelated dependencies.
- Keep `MODEL_API_KEY` server-side only. `ALLOW_META_API_CALLS` remains false until the user explicitly authorizes actual API calls.

## Functional floor
- The real CSV workflow must continue working: upload, profile, schema edit, mapping review, safe transformations, row validation, accepted/rejected exports, report and recipe replay.
- The actual CTA opens the real workspace.
- Every dock navigation item and theme button works.
- No fake "illustrative example" presented as working-product evidence; any sample preview uses the real sample fixture/workflow.
- Implement dark default and persisted light mode. The Predictive Arc hero stays intentionally dark.
- Preserve accessibility, reduced motion, keyboard focus, responsive layouts and WebGL fallback.

## Completion report
Report exact changes, source files/hash/license status, tests actually run, viewport/browser checks, Hallmark output, unresolved issues, Git state and current commit, Meta API verification status, and exact local run/build commands.

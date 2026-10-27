# ImportGuard Session Handoff

> This file is the first handoff source for any new model/session. Update at each major checkpoint and before ending a session or nearing a context/usage limit.

- Updated at: 2026-10-27
- Session/model: Codex implementation session
- Current branch: master
- Last verified base commit: `91793d894cbfd138296094b2d2536621600b9cb0` (`feat: build ImportGuard CSV workflow MVP`); landing hero checkpoint is being committed
- Working tree state: Preserve the pre-existing uncommitted user redesign references; inspect `git status --short` and stage only implementation files
- Checkpoint type: Hallmark redesign hero and verified ThreeUI source checkpoint

## Project state

The FastAPI app and deterministic CSV workflow remain in place. The new Vite/React landing entry is served by the same FastAPI app after `npm.cmd --prefix frontend run build`.

## Completed work

- CSV profile/caps, strict schema and transformations, mapping approval, accepted/rejected export package, recipe/report, replay, landing/workspace/privacy pages, fake-provider validation.

## Current work / last action completed

- Core implementation and first test/lint iteration completed; final verification and checkpoint remain.
- Replaced the light two-column mockup with a full-height dark Predictive Arc hero; a small React lifecycle adapter calls the canonical renderer.
- Retrieved all three canonical ThreeUI bundles. All 24 source files and the 15,176-byte Fragment Mono asset match their supplied hashes; current MIT/OFL license files are saved in `frontend/src/vendor/threeui/`.
- Captured and reviewed the original landing page and hero-only desktop/phone screenshots under `docs/visual-qa/`.
- Hero CTA routes to the existing workspace. Glass CTA, Sable dock integration, theme toggle and lower workflow sections remain next.

## Tests and commands

| Command | Result | Notes |
|---|---|---|
| `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient HTTPX deprecation warning only |
| `python -m ruff check .` | Passed | All checks passed |
| Uvicorn + six loopback GET requests | Passed | All pages/fixtures returned HTTP 200 |
| `npm.cmd --prefix frontend run verify:sources` | Passed | 24 source files and exact Fragment Mono SHA-256 verified |
| `npm.cmd --prefix frontend run build` | Passed | Vite production build; FastAPI serves the built landing from `/` and assets from `/web/` |
| Hallmark `sloplint --stage hero --render` | 0 FAIL, 0 WARN; 2 documented waivers | Rendered at 1280, 1440, 1920, and 375 CSS px |
| Puppeteer hero smoke | Passed | Headline, canvas, `/app` CTA, upload control, privacy, health, stylesheet and font verified |

## Failing tests / bugs / blockers

- Full CSV workflow has not yet been driven end-to-end in a browser. Starlette TestClient emits an HTTPX deprecation warning. No real Meta request has been made.

## Important files touched

- `app/`, `examples/`, `tests/`, `README.md`, and implementation docs.

## Decisions to preserve

- Follow `AGENTS.md` and `CODEX_CONTINUITY_PROTOCOL.md`.
- Manual mapping and local CSV processing must work without Meta API.
- Do not claim the real Meta API works until verified by a real request.
- Do not push/deploy/publish without approval.

## Environment variables needed (names only; never values)

- `MODEL_API_KEY` (only if configured locally)
- `ALLOW_META_API_CALLS` (must remain false until user explicitly enables real calls)

## Next 1–3 concrete actions

1. Integrate GlassAiButton and the Sable dock from unchanged canonical sources, using documented ImportGuard adapters.
2. Add the persisted dark/light toggle on landing, workspace and privacy; keep the selected hero scene dark.
3. Connect the below-fold workflow preview to a real fixture and run browser upload, mapping, export and recipe replay checks.
4. Run full tests, Hallmark page sweep and accessibility checks. Keep live Meta mapping disabled.

## Copyable instruction for next session

Read `AGENTS.md`, the visual redesign plan and `CODEX_CONTINUITY_PROTOCOL.md`; inspect Git state before edits. Continue with the Glass CTA and Sable dock adapters. Keep `MODEL_API_KEY` server-side and `ALLOW_META_API_CALLS=false`; do not make Meta calls.

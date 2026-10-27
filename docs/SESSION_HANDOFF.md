# ImportGuard Session Handoff

> This file is the first handoff source for any new model/session. Update at each major checkpoint and before ending a session or nearing a context/usage limit.

- Updated at: 2026-10-27
- Session/model: Codex implementation session
- Current branch: master
- Last verified code commit: `52134f9` (`feat(ui): complete Hallmark landing and workflow integration`)
- Working tree state: Implementation checkpoint committed. Pre-existing modified user docs and untracked user references remain untouched; intermediate visual captures remain untracked.
- Checkpoint type: Hallmark redesign, working sample workflow, shared theme, and browser/a11y verification

## Project state

The FastAPI app and deterministic CSV workflow remain in place. The new Vite/React landing entry is served by the same FastAPI app after `npm.cmd --prefix frontend run build`.

## Completed work

- CSV profile/caps, strict schema and transformations, mapping approval, accepted/rejected export package, recipe/report, replay, landing/workspace/privacy pages, fake-provider validation.

## Current work / last action completed

- Core implementation, verification, and implementation checkpoint completed.
- Replaced the old landing page with a dark Predictive Arc hero, the required headline, responsive below-fold sections, and a real sample pipeline using the existing profile/local-suggestion/process APIs.
- Integrated all canonical ThreeUI sources without editing vendor files. `verify:sources` checks all 24 files and the 15,176-byte Fragment Mono font. MIT/OFL notices are under `frontend/src/vendor/threeui/`.
- The Glass source renderer is retained in a sandboxed iframe; a native accessible anchor overlays it and routes to `/app`. This is a documented product adapter and is not byte-identical integration behavior.
- The original Glass source, Sable dock source, and Predictive Arc source hashes match owner-supplied pins. Recheck licenses/attribution before release.
- The animated dock has working home, section, workspace, and privacy navigation. Small screens use a native bottom navigation.
- Dark is the default; a persisted theme switch works on landing, workspace, and privacy. The arc stays dark in light theme.
- The landing preview calls the actual bundled synthetic CSV, profile endpoint, and local mapping endpoint. Visitors can edit and approve mappings, validate, and download a real package.
- Workspace UI browser flow exercised the bundled fixture, manual mapping corrections, approval, process package download, and recipe replay through the existing file controls.
- Before/after and final screenshots were captured and reviewed in `docs/visual-qa/`; browser checks cover 1920, 1440, 1280, 1024, 768, 430, 390, and 360 CSS px.
- Intermediate screenshots from earlier layout iterations (`live-full.png` and the non-`-viewport` files for 1024, 1280, 1920, 360, 430, and 768) remain untracked and untouched. The staged screenshot set contains the final reviewed viewport images plus reviewed 1440/390 full pages and workspace theme captures.

## Tests and commands

| Command | Result | Notes |
|---|---|---|
| `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient HTTPX deprecation warning only |
| `python -m ruff check .` | Passed | All checks passed |
| Uvicorn + six loopback GET requests | Passed | All pages/fixtures returned HTTP 200 |
| `npm.cmd --prefix frontend run verify:sources` | Passed | 24 source files and exact Fragment Mono SHA-256 verified |
| `npm.cmd --prefix frontend run build` | Passed | Vite production build; FastAPI serves the built landing from `/` and assets from `/web/` |
| `npm.cmd --prefix frontend test` | 2 passed | Glass adapter product label/source guard |
| `npm.cmd --prefix frontend run test:browser` | Passed | Full workspace sample and recipe replay, dock, keyboard action, themes, axe on three pages in both themes, WebGL fallback, reduced motion, and eight widths |
| Hallmark rendered page sweep | 0 FAIL, 0 WARN, 2 WAIVED, 1 NOTE | 1280x800, 1440x900, 1920x1080, 1440 and 375 full pages |
| `npm.cmd --prefix frontend audit --omit=dev` | 0 vulnerabilities | Puppeteer Core was updated to 25.16.0 after the first audit identified dev-tool advisories |
| `python -m pytest -q` | 33 passed, 1 warning | Existing Starlette/HTTPX deprecation warning |
| `python -m ruff check .` | Passed | All checks passed |

## Failing tests / bugs / blockers

- Vite reports a large JavaScript chunk (Three.js/WebGL sources; index about 1,003 kB uncompressed, about 268 kB gzip). Build succeeds; consider code splitting if startup performance becomes a concern.
- Starlette TestClient emits an HTTPX deprecation warning. No live Meta API request was made or verified.

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

1. Optional: split/lazy-load Three.js to reduce the initial JavaScript chunk.
2. Optional: update Starlette/TestClient dependencies to remove the HTTPX deprecation warning.
3. Keep Meta disabled and do not deploy, publish, push, or make real API calls without explicit authorization.

## Copyable instruction for next session

Read `AGENTS.md`, `CODEX_CONTINUITY_PROTOCOL.md`, and this handoff; inspect Git status and recent commits. Redesign checkpoint `52134f9` is complete and verified. Preserve pre-existing user instructions/references and intermediate screenshot captures. Optional follow-ups: code splitting and updating the deprecated TestClient dependency. Do not make Meta API calls or publish/deploy/push.

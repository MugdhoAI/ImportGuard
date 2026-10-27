# ImportGuard Session Handoff

> This file is the first handoff source for any new model/session. Update at each major checkpoint and before ending a session or nearing a context/usage limit.

- Updated at: 2026-10-27
- Session/model: Codex implementation session
- Current branch: master
- Last verified commit: `91793d894cbfd138296094b2d2536621600b9cb0` (`feat: build ImportGuard CSV workflow MVP`)
- Working tree state: Code checkpoint committed; this handoff update is being committed separately
- Checkpoint type: Functional MVP implementation checkpoint

## Project state

The starter workspace contained specifications only. A FastAPI app, deterministic CSV workflow, browser UI, exports, replay, optional gated Meta adapter, and synthetic fixtures have been added. Verify against tests and diff before committing.

## Completed work

- CSV profile/caps, strict schema and transformations, mapping approval, accepted/rejected export package, recipe/report, replay, landing/workspace/privacy pages, fake-provider validation.

## Current work / last action completed

- Core implementation and first test/lint iteration completed; final verification and checkpoint remain.

## Tests and commands

| Command | Result | Notes |
|---|---|---|
| Not run | Not verified | Do not assume tests have passed |
| `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient HTTPX deprecation warning only |
| `python -m ruff check .` | Passed | All checks passed |
| Uvicorn + six loopback GET requests | Passed | All pages/fixtures returned HTTP 200 |

## Failing tests / bugs / blockers

- Browser workflow not driven in a real browser. Starlette TestClient emits an HTTPX deprecation warning; API tests pass. No real Meta request has been made.

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

1. Perform a real browser pass at desktop and mobile sizes for upload, manual mapping, approval, download, and recipe replay; no browser automation was available during this session.
2. Keep live Meta mapping disabled until the owner confirms credits/access and explicitly enables `ALLOW_META_API_CALLS`.
3. Before public release, choose a project license and review the privacy/release blockers in the checklist.

## Copyable instruction for next session

Read `AGENTS.md` and `CODEX_CONTINUITY_PROTOCOL.md`, inspect actual Git status and recent commits, rerun pytest and Ruff, then perform browser QA on the current app. Do not enable or call Meta unless explicitly authorized.

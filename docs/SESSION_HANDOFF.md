# ImportGuard Session Handoff

> This file is the first handoff source for any new model/session. Update at each major checkpoint and before ending a session or nearing a context/usage limit.

- Updated at: 2026-10-27
- Session/model: Codex implementation session
- Current branch: master
- Last verified commit: No commit yet; checkpoint pending
- Working tree state: Uncommitted project implementation; staging not verified
- Checkpoint type: Functional MVP implementation in progress

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

1. Run `python -m pytest -q` and `python -m ruff check .`; fix failures.
2. Start Uvicorn bound to 127.0.0.1 and check `/`, `/app`, `/privacy`, and `/health`.
3. Review `git diff --check`, full diff, secrets/private data, update docs with actual outcomes, and commit intended files locally.

## Copyable instruction for next session

Read `AGENTS.md` and `CODEX_CONTINUITY_PROTOCOL.md`, inspect actual Git status, rerun pytest and Ruff, verify local Uvicorn routes, then stage only intended files and create a local checkpoint. Do not enable or call Meta unless explicitly authorized.

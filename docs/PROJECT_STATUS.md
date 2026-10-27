# ImportGuard Project Status

> Update after every major milestone. Only record verified state.

- Current phase: Hallmark landing redesign and local workflow QA complete
- Last updated: 2026-10-27
- Current branch: master
- Last verified implementation commit: `6c4fb76` (hero checkpoint); full-page checkpoint pending
- Working tree: Preserve pre-existing user instructions/references; implementation and generated review captures are being checkpointed locally
- Local app startup command: `npm.cmd --prefix frontend run build` then `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Core workflow status: Pipeline, API, UI, exports, and replay implemented
- Meta API status: Adapter implemented; no Meta call made; live integration not verified
- Latest verified tests: 33 backend tests passed (1 Starlette/HTTPX deprecation warning); 2 frontend unit tests passed; browser end-to-end and axe scans passed; Hallmark page sweep 0 FAIL / 0 WARN

## Milestone status

| Milestone | Status | Evidence / commit | Notes |
|---|---|---|---|
| Workspace and Git bootstrap | Implemented | `91793d8` | Local-only root commit; no remote |
| CSV parsing and profiling | Implemented | `tests/test_csv_pipeline.py` | |
| Schema and mapping | Implemented | Unit/API tests | Manual and local suggestions |
| Validation and transformations | Implemented | Unit tests | Strict configured types and allowlist |
| Exports and recipe replay | Implemented | Unit/API tests | Fixed ZIP member names |
| Meta adapter / fake-provider tests | Implemented | `tests/test_meta_client.py` | Live API not tested |
| Real Meta API request | Pending account access | | Never infer success |
| Frontend end-to-end workflow | Implemented and browser verified | `/`, `/app`, `/privacy` | Workspace sample profile, local mapping, export, and UI recipe replay exercised |
| Landing redesign | Implemented and rendered | `frontend/src/pages/Landing.tsx`; captures under `docs/visual-qa/` | Verified Predictive Arc; Glass CTA adapter; working Sable dock; dark/light persisted themes; real sample pipeline |
| ThreeUI source and licenses | Verified | `frontend/src/vendor/threeui/VERIFICATION.json` | 24 source files and 15,176-byte Fragment Mono asset match supplied SHA-256; ThreeUI Community MIT, font OFL 1.1 |
| Security/privacy and accessibility | Implemented and browser audited | Axe scans on all three pages in both themes; keyboard CTA; WebGL fallback; reduced motion | No automated accessibility violations |
| Documentation/demo | Implemented | README, architecture, test plan, demo script, source notices | Recheck terms and attribution before any public release |

## Next actions

- Review commit and final local tree; preserve user-supplied uncommitted instructions and references.
- If preparing a public release later, recheck current ThreeUI license terms and provide required notices; no publish/deploy is authorized.

## Next action

Next: inspect `git status --short`, verify the local full-page checkpoint commit, and continue only from the exact recorded handoff. Do not make Meta API calls without explicit authorization.

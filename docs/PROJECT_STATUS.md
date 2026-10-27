# ImportGuard Project Status

> Update after every major milestone. Only record verified state.

- Current phase: Hallmark landing repair and browser QA complete
- Last updated: 2026-10-27
- Current branch: master
- Last verified implementation: local Hallmark landing repair checkpoint
- Working tree: Repair committed; pre-existing user instructions/references and intermediate captures remain untouched
- Local app startup command: `npm.cmd --prefix frontend run build` then `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Core workflow status: Pipeline, API, UI, exports, and replay implemented
- Meta API status: Adapter implemented; no Meta call made; live integration not verified
- Latest verified tests: frontend browser workflow passed; axe scans passed on landing, workspace, and privacy in both themes; source verification and build passed; Hallmark page sweep 0 FAIL / 0 WARN

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
| Landing repair | Implemented and rendered | `docs/visual-qa/landing-repair.md` and `landing-repair-*.png` | Reduced overlay, centered stack, single animated responsive dock, repaired theme click target and light contrast; canvas motion measured in browser |
| ThreeUI source and licenses | Verified | `frontend/src/vendor/threeui/VERIFICATION.json` | 24 source files and 15,176-byte Fragment Mono asset match supplied SHA-256; ThreeUI Community MIT, font OFL 1.1 |
| Security/privacy and accessibility | Implemented and browser audited | Axe scans on all three pages in both themes; keyboard CTA; WebGL fallback; reduced motion | No automated accessibility violations |
| Documentation/demo | Implemented | README, architecture, test plan, demo script, source notices | Recheck terms and attribution before any public release |

## Next actions

- Preserve the pre-existing dirty instructions/references and intermediate captures; do not stage them accidentally.
- If preparing a public release later, recheck current ThreeUI license terms and provide required notices; no publish/deploy is authorized.

## Next action

Next: optional performance follow-up is lazy-loading/splitting the Three.js bundle; address the Starlette/HTTPX deprecation when upgrading the test stack. Do not make Meta API calls without explicit authorization.

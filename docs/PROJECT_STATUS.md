# ImportGuard Project Status

> Update after every major milestone. Only record verified state.

- Current phase: Landing redesign in progress; verified Predictive Arc hero checkpoint complete
- Last updated: 2026-10-27
- Current branch: master
- Last verified implementation commit: `91793d894cbfd138296094b2d2536621600b9cb0`
- Working tree: User-provided redesign references remain unmodified; implementation changes are being checkpointed locally
- Local app startup command: `npm.cmd --prefix frontend run build` then `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Core workflow status: Pipeline, API, UI, exports, and replay implemented
- Meta API status: Adapter implemented; disabled by default; no real request made
- Latest verified tests: `python -m pytest -q` — 33 passed, 1 upstream warning; frontend build, source hashes, hero browser smoke, and Hallmark hero sweep passed

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
| Frontend end-to-end workflow | Implemented; browser check pending | `/`, `/app`, `/privacy` | API tested using TestClient; Uvicorn routes returned 200 |
| Landing redesign hero | Implemented and rendered | `frontend/src/pages/Landing.tsx`; desktop/phone captures | Canonical Predictive Arc renderer hash verified; Glass CTA, Sable dock, theme toggle, and lower sections remain in progress |
| ThreeUI source and licenses | Verified | `frontend/src/vendor/threeui/VERIFICATION.json` | 24 source files and 15,176-byte Fragment Mono asset match supplied SHA-256; ThreeUI Community MIT, font OFL 1.1 |
| Security/privacy and accessibility | Implemented; review pending | Bounded uploads, safe rendering/export, focus and reduced motion | No browser audit |
| Documentation/demo | Implemented | README, architecture, test plan, demo script | License choice remains undecided |

## Next actions

- Complete the Glass CTA and Sable dock adapters; keep canonical sources unchanged and test their navigation behavior.
- Integrate the working persisted theme toggle across landing, workspace, and privacy pages; then connect the real sample workflow below the fold.

## Next action

Integrate the Glass CTA and Sable dock, then complete the actual workflow preview and theme parity before full browser and accessibility QA.

# ImportGuard Test Log

Record commands actually run, exact outcomes, and failures. Do not record expected results as completed results.

| Date/time | Commit | Command | Result | Notes / follow-up |
|---|---|---|---|---|
| Initial template | | Not run | Not verified | Start recording after first test run |
| 2026-10-27 | `91793d8` | `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient notes HTTPX deprecation; no test failures |
| 2026-10-27 | `91793d8` | `python -m ruff check .` | Passed | All checks passed |
| 2026-10-27 | `91793d8` | `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` and `Invoke-WebRequest` for six routes | Passed | `/health`, `/`, `/app`, `/privacy`, and both example files returned HTTP 200; bound to loopback |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend run verify:sources` | Passed | Verified all 24 files from canonical Predictive Arc, GlassAiButton, and AnimatedTopDock bundles, supplied component hashes, and 15,176-byte Fragment Mono hash |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend run build` | Passed | TypeScript and Vite production build; FastAPI serves the public vendor stylesheet and verified font from `frontend/dist` |
| 2026-10-27 | redesign working tree | Hallmark `sloplint` with `--stage hero --render` at `http://127.0.0.1:8001/` | 0 FAIL, 0 WARN, 2 WAIVED, 1 NOTE | Four rendered viewports at 1280, 1440, 1920 and 375 CSS px; waivers 44c/79 document the full-screen Poster canvas; required design-plan copy is verbatim |
| 2026-10-27 | redesign working tree | Puppeteer browser smoke at `http://127.0.0.1:8001/` | Passed | Dark default, exact headline, rendered arc pixels, CTA to `/app`, upload control, privacy and health routes, stylesheet/font response and SHA; no page errors or 4xx requests |
| 2026-10-27 | redesign working tree | `python -m pytest -q` | 33 passed, 1 warning | Existing Starlette/HTTPX deprecation warning only |
| 2026-10-27 | redesign working tree | `python -m ruff check .` | Passed | All checks passed |

## Test categories

- Unit tests
- API/route tests
- Fake Meta provider tests
- Real Meta smoke test (separate; never conflate with mocks)
- End-to-end browser workflow (full CSV upload-to-replay browser run remains pending)
- CSV security/data integrity cases
- Lint/type/syntax checks
- Clean-install/startup check

For each failure, include the exact test name and a brief error summary. Do not store keys, raw CSV data, private output, or full sensitive payloads here.

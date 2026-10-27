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
| 2026-10-27 | `52134f9` | Git staged secret-pattern scan and `git diff --cached --check` | Passed | No secret-pattern matches; whitespace check clean |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend test` | 2 passed | Glass adapter unit tests verify product label, navigation message, and source-change guard |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend run test:browser` | Passed | Landing fixture profile/local mapping/manual corrections/approval/downloaded ZIP; existing workspace sample profile/mapping/export and recipe plus CSV file-chooser replay; all Sable routes, keyboard CTA, persisted themes; Axe on landing/workspace/privacy in both themes; WebGL fallback; reduced-motion still frame; no overflow at 1920, 1440, 1280, 1024, 768, 430, 390, 360 px |
| 2026-10-27 | redesign working tree | `node .agents/skills/hallmark/scripts/sloplint.mjs frontend/src/pages/Landing.tsx frontend/src/styles/tokens.css frontend/src/styles/landing.css --genre atmospheric --stage page --render --url http://127.0.0.1:8001/` | 0 FAIL, 0 WARN, 2 WAIVED, 1 NOTE | Rendered 1280x800, 1440x900, 1920x1080, 1440 full page, and 375 full page. Waivers 44c/79 document the full-viewport hero canvas. |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend audit --omit=dev` | 0 vulnerabilities | Full npm install audit also reported 0 after updating Puppeteer Core to 25.16.0 |
| 2026-10-27 | redesign working tree | `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient warns that HTTPX support is deprecated |
| 2026-10-27 | redesign working tree | `python -m ruff check .` | Passed | All checks passed |

## Test categories

- Unit tests
- API/route tests
- Fake Meta provider tests
- Real Meta smoke test (separate; never conflate with mocks)
- End-to-end browser workflow (completed using both landing sample controls and the existing workspace UI)
- CSV security/data integrity cases
- Lint/type/syntax checks
- Clean-install/startup check

For each failure, include the exact test name and a brief error summary. Do not store keys, raw CSV data, private output, or full sensitive payloads here.

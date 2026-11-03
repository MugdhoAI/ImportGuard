# ImportGuard Test Log

Record commands actually run, exact outcomes, and failures. Do not record expected results as completed results.

## Reference-based interior UI — 2026-11-03

| Working tree | Command / check | Result | Notes |
|---|---|---|---|
| interior UI | `py -3 -m pytest -q` | 112 passed, 1 warning | Added account display-name coverage; known Starlette/httpx deprecation and Windows temp cleanup warning remain. |
| interior UI | `py -3 -m ruff check .` | Passed | Protected temporary-directory access warnings only. |
| interior UI | `npm --prefix frontend test` | 2 passed | Landing component tests remain green. |
| interior UI | `npm --prefix frontend run build` | Passed | Landing bundle builds unchanged; existing large-chunk warning remains. |
| interior UI | `npm --prefix frontend run test:browser` | Passed | Existing CSV workflow, landing CTA/dock, themes, accessibility, fallback, reduced motion and responsive checks passed. |
| interior UI | Custom Puppeteer interior QA | Passed | Workspace full-width stage, real sample preview, Continue step, dashboard metrics, honest billing, signup fields/password toggle, theme, direct routes and reloads; no console or request failures. |

## Local startup/reload repair — 2026-11-03

| Working tree | Command / check | Result | Notes |
|---|---|---|---|
| startup repair | `py -3 -m pytest -q` | 111 passed, 1 warning | Final sequential run passed. Warning is the known Starlette/httpx deprecation; pytest also emitted the existing Windows temp cleanup PermissionError after completion. |
| startup repair | `py -3 -m ruff check .` | Passed | Ruff passed; protected temporary directories emitted access-denied scan warnings. |
| startup repair | `npm --prefix frontend test` | 2 passed | Vitest passed. |
| startup repair | `npm --prefix frontend run build` | Passed | Vite build passed with the existing large-chunk warning. |
| startup repair | `npm --prefix frontend run verify:sources` | Passed | 24 ThreeUI source files and the 15,176-byte Fragment Mono asset matched their pinned SHA-256 values. |
| startup repair | `start-local.bat` from a stopped port plus HTTP smoke | Passed | Rebuilt the frontend, started Uvicorn on `127.0.0.1:8000`, and returned HTTP 200 for `/health` and `/`; landing revalidation headers were present. |
| startup repair | `npm --prefix frontend run test:browser` | Passed | Sample profile/local mapping/approval/export/replay, CTA, dock, themes, reduced motion, fallback, axe scans, console errors, and 8 widths all passed. |
| startup repair | Puppeteer direct-route/reload smoke | Passed | `/`, `/app`, `/workspace`, `/privacy`, `/home`, `/dashboard`, `/billing`, and `/payments` each loaded directly and after reload with no page or console errors. |
| startup repair | Parallel pytest + Vite build attempt | Failed then fixed | The concurrent Vite clean of `frontend/dist` made pytest hit the fallback template before fallback cache headers were added; the final sequential pytest run passed. |

## Local URL diagnosis and verification — 2026-11-03

| Working tree | Command / check | Result | Notes |
|---|---|---|---|
| `5d370b9` | `py -3 -m pytest -q` | 111 passed, 1 warning | Full local suite passed. Warning is the known Starlette/httpx deprecation; pytest also reported a Windows temp cleanup PermissionError at interpreter exit after the successful run. |
| `5d370b9` | `py -3 -m ruff check .` | Passed | Ruff passed; the sandbox emitted access-denied warnings while scanning protected temporary directories. |
| `5d370b9` | `npm.cmd --prefix frontend test` | 2 passed | Vitest component tests passed. |
| `5d370b9` | `npm.cmd --prefix frontend run build` | Passed | Vite build passed with the existing large-chunk warning. |
| `5d370b9` | Uvicorn on `127.0.0.1:8000` plus `Invoke-WebRequest` smoke | Passed | `/health`, `/`, `/app`, `/privacy`, built JS/CSS, and both example assets returned HTTP 200. No public deployment URL or deployment configuration is present. |
| Browser-harness working tree | `npm.cmd --prefix frontend run test:browser` before repair | Failed, diagnosed | The script defaulted to obsolete port `8001` while the documented server uses `8000`; after changing the port, Puppeteer also required explicit viewport setup and DOM-ready navigation waits. |
| Browser-harness working tree | `node --check frontend/scripts/browser-check.mjs` | Passed | Browser harness syntax check after the repair. |
| Browser-harness working tree | `npm.cmd --prefix frontend run test:browser` | Passed | Real local flow passed on `http://127.0.0.1:8000`: sample/workspace profile, mapping, approval, export, replay, CTA, Sable routes, themes, axe scans, WebGL fallback, reduced motion, and eight viewport widths. |

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
| 2026-10-27 | landing repair working tree | `npm.cmd run test:browser` | Failed, corrected | First run exposed a test assertion using browser `innerHeight` in Node; fixed to compare against the configured viewport height. |
| 2026-10-27 | landing repair working tree | `npm.cmd run test:browser` | Failed, corrected | Landing theme check initially queried workspace-only `[data-theme-toggle]`; updated it to `.theme-toggle`. |
| 2026-10-27 | landing repair working tree | `npm.cmd run test:browser` | Failed, corrected | Landing theme stayed dark because the fixed full-width dock mount intercepted pointer input; restricted pointer events to the real dock nav. |
| 2026-10-27 | landing repair working tree | `npm.cmd run test:browser` | Failed, corrected | Light-theme axe scan found low contrast on workflow step numbers and the footer mark; darkened the subtle token and adjusted the footer mark. |
| 2026-10-27 | landing repair checkpoint | `npm.cmd run test:browser` | Passed | Landing theme toggle/reload persistence; no axe A/AA violations on landing, workspace, or privacy in either theme; sample/workspace CSV flow, replay, CTA, dock routing/fitting, reduced motion, fallback, and 8 widths. |
| 2026-10-27 | landing repair checkpoint | `npm.cmd run build` | Passed | Final frontend production build; existing >500 kB JavaScript chunk warning. |
| 2026-10-27 | landing repair checkpoint | `npm.cmd run verify:sources` | Passed | Rechecked 24 ThreeUI files and the pinned font asset. |
| 2026-10-27 | landing repair checkpoint | Hallmark page `sloplint --render` | 0 FAIL, 0 WARN, 2 WAIVED, 1 NOTE | 1280, 1440, 1920 viewports and desktop/mobile full pages. Required 13-word copy retained verbatim. |
| 2026-10-27 | `52134f9` | Git staged secret-pattern scan and `git diff --cached --check` | Passed | No secret-pattern matches; whitespace check clean |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend test` | 2 passed | Glass adapter unit tests verify product label, navigation message, and source-change guard |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend run test:browser` | Passed | Landing fixture profile/local mapping/manual corrections/approval/downloaded ZIP; existing workspace sample profile/mapping/export and recipe plus CSV file-chooser replay; all Sable routes, keyboard CTA, persisted themes; Axe on landing/workspace/privacy in both themes; WebGL fallback; reduced-motion still frame; no overflow at 1920, 1440, 1280, 1024, 768, 430, 390, 360 px |
| 2026-10-27 | redesign working tree | `node .agents/skills/hallmark/scripts/sloplint.mjs frontend/src/pages/Landing.tsx frontend/src/styles/tokens.css frontend/src/styles/landing.css --genre atmospheric --stage page --render --url http://127.0.0.1:8001/` | 0 FAIL, 0 WARN, 2 WAIVED, 1 NOTE | Rendered 1280x800, 1440x900, 1920x1080, 1440 full page, and 375 full page. Waivers 44c/79 document the full-viewport hero canvas. |
| 2026-10-27 | redesign working tree | `npm.cmd --prefix frontend audit --omit=dev` | 0 vulnerabilities | Full npm install audit also reported 0 after updating Puppeteer Core to 25.16.0 |
| 2026-10-27 | redesign working tree | `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient warns that HTTPX support is deprecated |
| 2026-10-27 | redesign working tree | `python -m ruff check .` | Passed | All checks passed |
| 2026-10-30 | `22ff452` + CTA tree | `npm --prefix frontend test` | 2 passed | Glass CTA adapter unit tests, before and after the source-check fix |
| 2026-10-30 | `22ff452` + CTA tree | `npm --prefix frontend run build` | Passed | tsc + Vite; known >500 kB chunk warning only |
| 2026-10-30 | `22ff452` + CTA tree | `node --check frontend/scripts/browser-check.mjs` | Passed | Syntax check after CTA assertion updates |
| 2026-10-30 | `22ff452` + CTA tree | CTA browser probe (built bundle + Chrome, 9 assertions) | 9 passed | Single CTA, exact label, IG mark, no demo branding; pointer click → /app; 9-tab keyboard focus + Enter → /app; no-WebGL fallback → /app; foreign postMessage ignored; reduced-motion click → /app; no page/console errors; 1280x800 screenshots reviewed |
| 2026-10-30 | `22ff452` + CTA tree | `test:browser`, pytest, ruff | Not run | No usable Python interpreter in this sandbox; full backend-backed suite must run where Python is available |
| 2026-10-30 | readiness tree | secret-pattern scan of tracked files | Clean | No key/token/private-key patterns outside vendor skill refs; no `.env`, uploads, or exports in tree |
| 2026-10-30 | readiness tree | `npm --prefix frontend test` | 2 passed | CTA adapter unit tests after hygiene edits |
| 2026-10-30 | readiness tree | `npm --prefix frontend run build` | Passed | Known large-chunk warning only |
| 2026-10-30 | readiness tree | `npm --prefix frontend run verify:sources` | Passed | 24 vendor files + 15,176-byte font re-verified; VERIFICATION.json timestamp updated |
| 2026-10-30 | readiness tree | `scripts/test_meta_api.py`, pytest, ruff, `test:browser`, CI | Script not run here | Unrunnable in this sandbox (no Python); pytest/ruff/test:browser later confirmed by owner runs below |
| 2026-10-30 | readiness tree | `python -m scripts.test_meta_api` (owner-run, live) | Passed, exit 0 | Live call to `muse-spark-1.3`: 1 synthetic request succeeded in 18.6s with 3 mappings (student_id←Reg No medium, phone←Mobile high, payment_status←Paid medium). Synthetic headers only; no sample values sent. This verifies the live round trip, not mapping quality on real user CSVs |
| 2026-10-30 | readiness tree | `python -m pytest -q` (owner-run, local shell) | 33 passed, 1 warning | Owner-reported: only the known Starlette/HTTPX deprecation warning |
| 2026-10-30 | readiness tree | `python -m ruff check .` (owner-run, v0.16.10) | Passed | Owner-reported: all checks passed |
| 2026-10-30 | readiness tree | `npm --prefix frontend test` (owner-run) | 2 passed, 1 file | Owner-reported: matches sandbox result |
| 2026-10-30 | readiness tree | `npm --prefix frontend run build` (owner-run) | Passed | Owner-reported: known >500 kB chunk warning only |
| 2026-10-30 | readiness tree | `npm --prefix frontend run test:browser` (owner-run) | Passed, exit 0 | Owner-reported clean run: sample + workspace profile/mapping/export/replay, Glass CTA + WebGL fallback, Sable navigation, persisted themes, dark/light axe scans, reduced motion, 8 viewport widths |

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

## Product completion loop — 2026-10-31

| Date | Working tree | Command / check | Result | Notes |
|---|---|---|---|---|
| 2026-10-31 | product-shell changes | `C:\Users\rojina\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pytest -q` | 34 passed | Includes route/nav/payment-boundary coverage; Starlette HTTPX deprecation and pytest cache warning only. `pytest.exe -q` could not run because its wrapper expected missing `_console_main`; `python` alias could not launch. |
| 2026-10-31 | product-shell changes | `npm.cmd --prefix frontend run build` | Passed | Vite production build; existing >500 kB chunks warning. First sandboxed attempt could not write generated vendor assets; approved local run completed. |
| 2026-10-31 | product-shell changes | Headless Chrome check at `http://127.0.0.1:8002` | Passed | `/home`, `/dashboard`, `/app`, `/billing`, `/payments` render with full nav; dark CSV preview text differs from its background; all five mobile nav links visible and no 390px horizontal overflow. |

## Product completion loop — accounts/history/billing

| Date | Working tree | Command / check | Result | Notes |
|---|---|---|---|---|
| 2026-10-31 | completion tree | `pytest -q` (sandbox) | 52 passed, 20 env-blocked | All 20 failures are TestClient/async socket PermissionError (sandbox denies loopback bind; bare `asyncio.run` fails too). Includes 23 new sync unit tests (store/auth/export/billing), all passing. TestClient suites need an owner/CI run |
| 2026-10-31 | completion tree | `ruff check .` (sandbox) | Passed | Whole repo, including new store/auth/accounts/billing modules and 6 new test files |
| 2026-10-31 | completion tree | `npm --prefix frontend test` + `run build` (sandbox) | Passed | 2/2 vitest; build with known chunk-size warning only |
| 2026-10-31 | completion tree | Rendered-template visual sweep (sandbox Chrome) | Passed | 8 pages × 1280/390: no overflow (fixed one grid blowout with `min-width:0`); dark default + light reviewed with screenshots |
| 2026-10-31 | console tree | `pytest -q` (sandbox) | 91 passed, 20 env-blocked | Same 20 TestClient loopback PermissionErrors. +39 runnable: `tests/test_console.py` (29 direct-call route tests) + 6 store + 4 auth. Covers gates, teams, admin, history filters, sweep of every page |
| 2026-10-31 | console tree | `ruff check .` (sandbox) | Passed | Whole repo; fixed 6 pre-existing store E501s, 3 new-test E501s, 1 import sort, 1 redefined function (deduped) |
| 2026-10-31 | console tree | `node --check app/static/js/app.js` | Passed | Syntax check for preview-table + guest-nudge workspace changes; behavior needs owner browser run |
| 2026-10-31 | console tree | Updated TestClient suites (not run) | Not verified | `test_exports/nav/dashboard/accounts/api` updated for the download gate + new nav; owner/CI must run the full suite |
| 2026-10-31 | console tree | Static QA script (51 routes × templates + app.js) | Passed | Zero dead links/fetches; only 2 unstyled classes, both in unreachable legacy `landing.html` fallback (dist build exists) |
| 2026-10-31 | console tree | Headless Chrome review, 12 shots (`visual-qa/`) | Passed with fixes | 1280 dark/light + 768 + 390-emu reviewed pixel-by-pixel. Fixed mobile stats 2-col truncation (1fr), grid minmax, sidebar min-width guard. Headless-new crops sub-500 viewports, so 390 was verified via body-width emulation (identical media queries); tablet History table scrolls horizontally (spec-permitted) |

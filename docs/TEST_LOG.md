# ImportGuard Test Log

Record commands actually run, exact outcomes, and failures. Do not record expected results as completed results.

| Date/time | Commit | Command | Result | Notes / follow-up |
|---|---|---|---|---|
| Initial template | | Not run | Not verified | Start recording after first test run |
| 2026-10-27 | `91793d8` | `python -m pytest -q` | 33 passed, 1 warning | Starlette TestClient notes HTTPX deprecation; no test failures |
| 2026-10-27 | `91793d8` | `python -m ruff check .` | Passed | All checks passed |
| 2026-10-27 | `91793d8` | `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` and `Invoke-WebRequest` for six routes | Passed | `/health`, `/`, `/app`, `/privacy`, and both example files returned HTTP 200; bound to loopback |

## Test categories

- Unit tests
- API/route tests
- Fake Meta provider tests
- Real Meta smoke test (separate; never conflate with mocks)
- End-to-end browser workflow
- CSV security/data integrity cases
- Lint/type/syntax checks
- Clean-install/startup check

For each failure, include the exact test name and a brief error summary. Do not store keys, raw CSV data, private output, or full sensitive payloads here.

# ImportGuard

ImportGuard is a local-first CSV mapping and validation workspace. Review a source-to-target mapping, validate rows deterministically, export accepted and rejected records, and replay a saved recipe on a later file.

## What works

- UTF-8 and UTF-8 BOM CSV profile with 5 MB, 5,000 row, and 100 column limits.
- Editable target fields with string, integer, decimal, boolean, and strict `YYYY-MM-DD` date validation.
- Manual mapping and clearly labeled local normalized-header suggestions.
- User approval before deterministic `identity`, `trim`, `collapse_whitespace`, `lowercase`, or `uppercase` operations run.
- Accepted CSV, recoverable rejected CSV with row numbers and errors, versioned recipe JSON, and a report JSON in a ZIP.
- Recipe replay without a model call.
- Optional server-side Meta Muse Spark mapping adapter, disabled by default and requiring a deliberate UI request. Sample values are separately opt-in.

The default workflow does not contact Meta. No live Meta API request has been verified. Fake-provider tests exercise response validation only.

## Run on Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. If `py -3` is unavailable, use `python -m venv .venv`.

## Tests and checks

```powershell
python -m pytest -q
python -m ruff check .
```

## Data handling and limitations

CSV content and downloads are processed in memory by the local server and are not intentionally persisted. Manual mapping and validation stay local. If Meta mapping is explicitly enabled and invoked, source headers and target schema are sent to Meta's API. Up to three values per column are included only when the separate unchecked option is selected. Do not send confidential data without authorization. See `/privacy` for the current disclosure.

Spreadsheet exports prefix values beginning with `=`, `+`, `@`, tab, carriage return, and non-numeric `-` with an apostrophe. Ordinary negative numeric values such as `-15` remain unchanged. This is an export-only safeguard; the in-memory values and recipe are not rewritten. Rejected rows retain original values except for this documented export safeguard.

Validation enforces only the selected schema rules. It does not deduplicate, infer date formats, normalize identifiers, or guarantee that accepted records are correct. Mapping suggestions can be wrong and require review.

## Meta configuration (optional)

The Meta Model API adapter follows the current official OpenAI-compatible Chat Completions and structured-output documentation, uses `muse-spark-1.3`, and accepts `MODEL_API_KEY` only on the server. To enable the UI action, configure local `.env` after verifying account/credit access:

```dotenv
MODEL_API_KEY=your-local-key
ALLOW_META_API_CALLS=true
```

Restart the app, review the on-screen disclosure, then invoke Meta explicitly. Never put the key in frontend code. The real integration remains **not tested**. The app does not claim that a mock response is live.

Official references: [Meta Chat Completions quickstart](https://dev.meta.ai/docs/cookbook/quickstart-chat-completions), [structured output](https://dev.meta.ai/docs/structured-output), and [models](https://dev.meta.ai/docs/models).

## Project status

This is an MVP under active development. The project license has not yet been selected. See [project status](docs/PROJECT_STATUS.md), [architecture](docs/ARCHITECTURE.md), and [test plan](docs/TEST_PLAN.md).

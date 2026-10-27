# ImportGuard: Codex Execution Plan

> **Purpose:** Build a complete, locally runnable ImportGuard MVP for the Meta Global AI Developer Hackathon 2026. This file is the working specification for Codex. Read it fully before editing code, then execute the phases in order, implement the product, run tests, fix failures, and leave a clear status report.
>
> **User's goal:** Submit a working project. Do not optimize for winning, invent unnecessary features, or spend time endlessly comparing ideas. Favor a small, reliable, understandable application.

## 0. Instructions for Codex

1. Read `AGENTS.md`, this entire file, `CODEX_DESIGN_REFERENCE_GUIDE.md`, `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md`, and `CODEX_CONTINUITY_PROTOCOL.md` before changing anything. Inspect the current project directory, installed Python, Git status, and available commands.
2. If the folder is empty, create the project. If files already exist, inspect them and preserve useful work. Do not overwrite files blindly.
3. Implement the app locally end to end. Do not stop after producing a plan or a design mockup.
4. Work in phases, but continue through all phases that are possible without the user's account credentials or other unavailable dependencies. Do not ask the user to approve ordinary implementation decisions.
5. Use sensible defaults and record meaningful decisions in `docs/DECISIONS.md`. Ask the user only when a decision is genuinely necessary and cannot safely be inferred.
6. The Meta API credits may still be pending. Build and test the application without spending on real API calls. Only make a real Meta Model API request when `ALLOW_META_API_CALLS=true` is explicitly configured by the user. Never infer that credits have arrived just because a payment card is present.
7. Never display, print, log, commit, or expose `MODEL_API_KEY`. Do not read secret values aloud in tool output. Keep `.env` ignored by Git. Never send credentials to the browser.
8. Never claim a live Meta response was tested if it was not. Clearly separate automated tests using a fake provider from a real API integration test.
9. Do not deploy the app, publish the repository, push Git branches, create paid resources, or incur non-credit charges without the user's explicit permission.
10. Do not delete user files, reset Git history, run destructive cleanup, or use force operations.
11. Prefer one small Python application over multiple services. Do not add Supabase, Redis, Celery, Docker, a vector database, an agent framework, a separate Node frontend, or authentication unless a verified requirement makes one necessary.
12. After every phase, run the relevant tests or checks and fix failures before proceeding. Never report tests as passing without actually running them.
13. At completion, report: implemented features, exact commands run, test results, known limitations, whether a real Meta call was verified, and the command to start the app.

## 1. Product definition

### 1.1 What ImportGuard does

ImportGuard helps a user convert an unfamiliar CSV export into a chosen target schema without silently changing ambiguous data.

Example:

- Source CSV columns: `Reg No`, `Mobile`, `Paid`
- Target columns: `student_id`, `phone`, `payment_status`
- Meta Muse Spark may propose the semantic column mappings.
- The user reviews and approves mappings.
- Local Python code runs only allowlisted transformations and validates every row.
- The app creates an accepted CSV, a rejected-rows CSV with reasons, a reusable JSON recipe, and a run summary.
- The approved recipe can be applied to another CSV without another model call.

The core product is the review workflow, deterministic transformation engine, validation, and repeatability. It must not be merely a chat interface or an AI-generated explanation.

### 1.2 Target user

Start with a university club administrator, researcher, or small operator who regularly imports CSV data into a fixed format. This is an initial target hypothesis, not a claim that users have already been interviewed.

### 1.3 MVP scope: build these only

- A polished, responsive landing page.
- A functional CSV import workspace.
- CSV upload and local profiling.
- A simple target-schema builder.
- Manual column mapping so the application is useful without model access.
- Optional Meta Muse Spark mapping suggestions, when enabled by the user.
- A review screen where every mapping and transformation can be changed before execution.
- Deterministic transformations and row-level validation.
- Accepted/rejected CSV exports and a report.
- A JSON mapping recipe and recipe replay against another CSV.
- Helpful errors, tests, README, and a reproducible local startup command.

### 1.4 Explicitly out of scope

Do not build these in the MVP:

- XLS/XLSX support, PDF/OCR, image processing, or multi-table joins.
- External database imports, live integrations, GitHub integrations, or third-party data APIs.
- Automatic entity/person deduplication.
- Autonomous edits, code execution, or agentic workflows.
- User accounts, paid plans, billing UI, or Supabase.
- Complex background jobs, queues, or microservices.
- Fancy charts that do not improve the workflow.
- Claims of guaranteed data correctness, privacy, market demand, or time savings.

If time remains after the required workflow passes tests, improve usability and error messages rather than expanding scope.

## 2. Hackathon requirements and timing

The user-provided participant guide states:

- The project must fit one of the themes: **Build for Your World** or **Push the Frontier**.
- The project must meaningfully incorporate eligible Meta model tooling.
- The repository must be public for submission.
- The three-minute demo must show the specific features, code, and functionality built during the hackathon; new contributions must be clearly identifiable.
- The guide lists anti-project examples including basic RAG applications, simple image analyzers, simple AI education chatbots, job screeners, nutrition coaches, personality analyzers, sports analyzers/coaches, and political/war-related projects.
- Solo participants are permitted.
- Deadline listed in the guide: November 4, 2026 at 9:00 PM Eastern Time. That is November 5, 2026 at 8:00 AM Bangladesh time because the US has returned to standard time by then.

The internal goal is to have everything ready and submit by **November 4, 2026 at 8:00 PM Bangladesh time**, approximately twelve hours before the published deadline. Check current official announcements before submission because event schedules can change.

Do not present pre-existing work as newly built. Record what is created in this project during the event. Do not copy implementation code from other projects without checking the license and preserving attribution.

## 3. Source of truth and official references

Use official documentation first. If a URL has changed, find the equivalent page on the same official domain and note the correction in `docs/DECISIONS.md`.

### Hackathon

- Official event listing: https://events.cerebralvalley.ai/e/meta-ai-developer-hackathon
- Event details and rules: https://cerebralvalley.ai/e/meta-ai-developer-hackathon/details
- Discord instructions: https://cerebralvalley.ai/e/meta-ai-developer-hackathon/discord
- Meta Model API event portal: https://dev.meta.ai/events/global-hackathon

### Meta Model API

- Overview: https://dev.meta.ai/docs/overview
- Quickstart: https://dev.meta.ai/docs/quickstart
- Python Chat Completions quickstart: https://dev.meta.ai/docs/cookbook/quickstart-chat-completions
- Structured output: https://dev.meta.ai/docs/structured-output
- Structured-output cookbook: https://dev.meta.ai/docs/cookbook/structured-output
- Model list: https://dev.meta.ai/docs/models
- Pricing and limits: https://dev.meta.ai/docs/pricing-rate-limits
- Geographic-use policy: https://dev.meta.ai/legal/geographic-use-policy
- Dashboard / API key / billing: https://dev.meta.ai/

### Framework references

- FastAPI file uploads: https://fastapi.tiangolo.com/tutorial/request-files/
- FastAPI templates and static files: https://fastapi.tiangolo.com/advanced/templates/
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/
- Codex iterative development guidance: https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex

### Existing solutions examined during research

- OpenRefine: https://openrefine.org/ and https://github.com/OpenRefine/OpenRefine
- Frictionless Python: https://github.com/frictionlessdata/frictionless-py
- GitHub Open Source Projects topic: https://github.com/topics/open-source-projects
- Public APIs catalog: https://github.com/public-apis/public-apis
- Hackathon project topic: https://github.com/topics/hackathon-project
- Hackathon-Tools repository: https://github.com/rahavshukla/Hackathon-Tools

Use these as research references only. Do not use the Hackathon-Tools ZIP or any unexplained binary. Research concluded its README had inconsistent download links; there is no need for it in this project.

## 4. Technology choices

Keep the stack small and local-first.

- **Language:** Python 3.11 or newer; use the locally available supported version if it is compatible.
- **Backend:** FastAPI + Uvicorn.
- **Frontend:** Server-rendered HTML with Jinja2 templates, plain CSS, and vanilla JavaScript.
- **CSV handling:** Python standard-library `csv`, `io`, `json`, `decimal`, `datetime`, and `hashlib` as appropriate. Do not install pandas for this bounded CSV workflow unless a proven need appears.
- **Meta integration:** Official OpenAI-compatible Python SDK, using the `openai` package and Meta's documented base URL.
- **Validation:** Pydantic models for request structures and recipe/mapping validation.
- **Tests:** pytest, FastAPI TestClient/httpx, and tests using an injected fake model provider.
- **Code quality:** Ruff for linting and formatting where practical.
- **Storage:** No database for MVP. Process input in memory, do not retain uploaded files by default, and stream downloadable outputs.
- **Frontend assets:** `app/static/` and `app/templates/` served by FastAPI.

Do not introduce Next.js, React, TypeScript, Tailwind, or a separate npm toolchain by default. A single Python app reduces installation and deployment risks. Build a good-quality website with real HTML/CSS/JS instead of a static mockup.

## 5. Required project structure

Create a clean structure close to this. Adjust only when there is a clear implementation reason.

```text
importguard/
├── CODEX_EXECUTION_PLAN.md
├── AGENTS.md
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── pyproject.toml
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── csv_service.py
│   │   ├── schema_service.py
│   │   ├── mapping_service.py
│   │   ├── transformation_service.py
│   │   ├── export_service.py
│   │   └── meta_client.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── landing.html
│   │   └── app.html
│   └── static/
│       ├── css/styles.css
│       ├── js/app.js
│       └── examples/registrations.csv
├── examples/
│   ├── registrations.csv
│   └── registrations_schema.json
├── tests/
│   ├── test_csv_service.py
│   ├── test_schema_service.py
│   ├── test_mapping_service.py
│   ├── test_transformation_service.py
│   ├── test_exports.py
│   ├── test_api.py
│   └── test_meta_client.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── TEST_PLAN.md
│   └── DEMO_SCRIPT.md
└── .github/
    └── workflows/ci.yml
```

The final code does not need to match every file exactly. Avoid empty abstraction layers. If a service is too small to justify a separate file, it may remain in a related module, but keep responsibilities understandable.

## 6. User experience and website requirements

The website must be a working product, not a landing page with nonfunctional buttons. Make the app reachable at `/app`; the landing page is `/`.

### 6.1 Visual direction

Reference for visual inspiration: https://threeui.com/landing-pages/kage-landing-page

Borrow the polished, cinematic landing-page qualities: confident typography, deliberate spacing, a strong hero, controlled motion, and visual depth. Adapt these principles to a trustworthy data utility; do not copy Kage's branding, imagery, temple concept, source code, or page layout.

Do not recreate its full Three.js/WebGL world or complex scroll scenes. That is unnecessary for this project and adds implementation and performance risk. Prefer HTML/CSS and subtle transitions.

Use a distinctive dark/ink-toned landing-page hero, a restrained accent color, and a clean, highly readable workspace for the actual CSV workflow. Keep tables, validation issues, and review controls easy to scan. The app must be responsive, accessible, keyboard-usable, and coherent on desktop and mobile. Do not create an icon wall, fake logos, fake testimonials, fabricated metrics, or decorative controls that do not work.

### 6.2 Landing page `/`

Include:

1. **Header:** ImportGuard wordmark, links for How it works and Privacy, and a visible `Open workspace` CTA.
2. **Hero:**
   - Headline: `Import CSVs with confidence.`
   - Supporting line: `Map columns, review changes, validate every row, and keep a repeatable import recipe.`
   - Primary CTA: `Start an import` linking to `/app`.
   - Secondary CTA: `See how it works` scrolling to the workflow section.
3. **Product visual:** Create an authentic UI preview using HTML/CSS, showing sample source columns, a reviewed mapping, and validation totals. Mark it as an illustrative example; do not pretend it is a real customer or live run.
4. **How it works:** Upload CSV → map and review → validate and export.
5. **Core capabilities:** Explicit mapping approval, row-level validation, accepted/rejected exports, recipe replay.
6. **Trust/limitations note:** Uploaded CSVs are processed transiently by the local app; optional example values may be sent to Meta only after the user opts in. Do not claim that all data stays local if AI mapping is enabled.
7. **Footer:** Project name, links to README/source only when valid URLs exist, and `Built with Meta Muse Spark` only after the actual integration has been implemented. It must not imply successful live API calls before one has been verified.

### 6.3 Workspace `/app`

Build a complete responsive step-by-step workflow with clear progress:

**Step A — Upload**
- Drag-and-drop and browse-file controls for `.csv`.
- State maximum file size (5 MB) and maximum data rows (5,000).
- Show filename and clear removal/replacement action.
- Provide a `Load example` option that loads synthetic project fixtures.
- Detect invalid encoding, empty files, duplicate headers, blank headers, malformed rows, and oversized files with actionable messages.

**Step B — Define target schema**
- Let user add, rename, remove and reorder required output fields.
- For each field: field name, type, and required toggle.
- Allowed types: `string`, `integer`, `decimal`, `boolean`, and `date_iso`.
- `date_iso` means strict `YYYY-MM-DD`. Do not guess formats such as `03/04/2026`.
- Validate schema names and prevent duplicate target field names.
- Include a clearly labeled example schema and allow loading `examples/registrations_schema.json`.

**Step C — Profile the CSV**
- Show row count, source columns, empty counts, duplicate header status, and up to three sample values per column in the browser.
- Compute simple local column summaries only; do not infer or display sensitive content unnecessarily.
- Explain that sample values are displayed locally and are not sent to Meta unless the user opts in for the mapping request.

**Step D — Suggest and review mappings**
- Provide two modes: `Suggest with Meta AI` and manual mapping.
- Also offer local normalized-header baseline suggestions. Label them as local suggestions, not AI output.
- Before sending example values to Meta, show an unchecked opt-in checkbox with clear language such as: `Include up to 3 example values per column in the Meta request. These examples may contain personal or confidential data.`
- Default to sending only headers and target field definitions. Send sample values only if the user explicitly checks the box.
- Never send the whole CSV or all its rows to Meta for mapping.
- Show a review table with target field, selected source column, transformation, confidence/notes from the model, and whether the user must review it.
- Allow the user to change every suggested mapping. Never apply a model suggestion without user approval.
- Make unmapped target fields visible. If a required field has no mapping, warn clearly before processing.
- If the Meta key/credits are unavailable, disable the Meta action with an explicit reason; manual mapping must still work. Do not silently substitute mock responses and call them AI.

**Step E — Validate and export**
- Display accepted count and rejected count, with a clear explanation that a row is accepted only when mapped target fields pass the schema checks.
- Give a brief preview of accepted output and rejected records/errors without exposing data unnecessarily.
- One download: ZIP containing `accepted.csv`, `rejected.csv`, `recipe.json`, and `report.json`.
- Also offer individual downloads if simple to implement without duplicate business logic.
- Explain transformations and the specific reasons rows failed.

**Step F — Replay a recipe**
- Allow users to upload a prior `recipe.json` and a new CSV.
- Apply only the recipe's allowlisted, previously approved operations; do not call Meta during replay.
- Validate source columns and schema before execution. If the recipe is incompatible, show which columns are missing or changed.
- Export the same accepted/rejected/recipe/report package.

### 6.4 Frontend behavior

- Build real interactions, not decorative controls.
- Show loading state while processing, disable duplicate submissions, and display errors near the relevant control.
- Preserve the user's reviewed mappings when the form reports a recoverable error.
- Use `fetch` to call same-origin FastAPI endpoints.
- Build downloads using Blob/object URLs and revoke object URLs after use.
- Ensure all controls are keyboard-operable and have visible focus indicators.
- Never include API keys in JavaScript, HTML, network payloads sent to the browser, or client-visible errors.

## 7. CSV processing and safety rules

The CSV pipeline is the most important code. Keep it deterministic and thoroughly tested.

### 7.1 Input limits and parsing

- Accept only `.csv` files for the MVP; do not trust extension alone, validate bytes/content as well.
- Default limits: 5 MB, 5,000 data rows, and 100 columns. Store these in configuration.
- Decode UTF-8 and UTF-8 with BOM (`utf-8-sig`). If decoding fails, explain that the file must be exported as UTF-8; do not silently replace invalid bytes.
- Use `csv.reader` or equivalent logic that detects duplicate headers before converting rows to dictionaries. Duplicate column names must not silently overwrite one another.
- Reject empty files, header-only files if the workflow needs at least one data row, duplicate/blank headers, and structurally malformed rows with useful error messages.
- Keep row numbers referring to physical data rows, with header on line 1. Document the convention.
- Do not write uploaded files to a persistent server directory. Process within bounded memory and discard request data after response.
- Never log raw CSV content, full sample values, or personal records.

### 7.2 Target schema and mapping model

Use validated Pydantic request types. A target field should have:

- `name`: non-empty, trimmed, unique.
- `type`: one of the five allowed types above.
- `required`: boolean.

A mapping entry should have:

- `source_column`: existing source header or `null` for unmapped.
- `target_field`: existing target field name.
- `operation`: an allowlisted operation.
- `confidence`: optional enum such as `high`, `medium`, `low` for AI suggestions only.
- `needs_review`: boolean.
- `note`: short string, never treated as verified truth.

Operations allowed in the MVP:

- `identity`
- `trim`
- `collapse_whitespace`
- `lowercase`
- `uppercase`

Do not let the model invent Python code, regex instructions, SQL, shell commands, or arbitrary transformation expressions. The server must reject unknown operations and source/target references.

Mapping constraints:

- A target field may have at most one selected source column.
- A source column may map to at most one target field in the MVP.
- Unmapped optional fields can be blank; missing required output fields must lead to clear errors/rejected rows.
- Reject mapping plans with duplicate source/target references rather than silently choosing one.

### 7.3 Deterministic type validation

- `string`: preserve content apart from the explicitly selected operation; blank is empty after the selected operation.
- `integer`: strict base-10 integer parsing; do not silently drop punctuation or decimal portions.
- `decimal`: parse with Python `Decimal`; do not use binary float for financial-looking or precision-sensitive values.
- `boolean`: accept a short explicit allowlist such as `true/false`, `yes/no`, `1/0` case-insensitively; reject other values as ambiguous.
- `date_iso`: accept only valid calendar dates formatted as `YYYY-MM-DD`; never infer ambiguous date formats automatically.
- Treat blank/whitespace-only values as missing for required-field checks, but do not rewrite values unless an approved operation calls for it.
- Preserve original source row and values for rejected output.
- No automatic deduplication.
- No implicit unit, currency, locale or timezone conversion.

### 7.4 Output contract

- `accepted.csv`: target-schema columns only, in target-schema order, containing rows that pass all configured validations.
- `rejected.csv`: `_source_row_number`, `_errors`, and original source columns so rejected data is recoverable. Escape structured errors consistently, e.g. JSON text in `_errors`.
- `recipe.json`: versioned approved target schema, source-to-target mappings, and allowlisted operations. No uploaded row values, API key, model prompt, or secret.
- `report.json`: timestamp, row counts, mapping summary, validation counts, input file hash, app/recipe version and any non-sensitive processing summary. Do not include raw row data.
- Row accounting invariant: `input_data_rows == accepted_rows + rejected_rows`.
- Output row order must be stable and match source order within accepted/rejected files.
- Validate all generated data structures before serialization.
- CSV files can be interpreted as formulas by spreadsheet software. Include an explicit spreadsheet-safe export policy for values beginning with formula-triggering characters (`=`, `+`, `-`, `@`, tab or carriage return). Do not silently mutate source input. If neutralizing such values in a download, document the behavior and test it. Keep original raw values in the rejected export where appropriate, with a clear warning.
- Return a ZIP download using safe filenames and an explicit `application/zip` content type. Never include the user's original filename as an unchecked filesystem path.

## 8. Meta Muse Spark integration

### 8.1 Official connection values

Use the currently documented values and verify them against official docs:

- Base URL: `https://api.meta.ai/v1`
- Model: `muse-spark-1.3`
- Python SDK: `openai`
- Environment variable: `MODEL_API_KEY`
- Endpoint: Chat Completions, `client.chat.completions.create(...)`
- Structured output: `response_format` with a strict JSON Schema, as documented by Meta.

Official recipes:

- https://dev.meta.ai/docs/cookbook/quickstart-chat-completions
- https://dev.meta.ai/docs/structured-output

### 8.2 Configuration and cost safety

Create `.env.example` with safe placeholders:

```dotenv
MODEL_API_KEY=
META_MODEL=muse-spark-1.3
META_BASE_URL=https://api.meta.ai/v1
ALLOW_META_API_CALLS=false
MAX_UPLOAD_MB=5
MAX_DATA_ROWS=5000
MAX_COLUMNS=100
```

Load local `.env` only with a dependency such as `python-dotenv`; add `.env` to `.gitignore`. Do not copy the real key into `.env.example` or project source.

`ALLOW_META_API_CALLS` must default to `false`. The user should change it to `true` only after verifying the promotional credits appear in Billing or explicitly authorizing use of paid balance. Do not make model requests just because a card is on the account.

### 8.3 The one model task

Ask Muse Spark only to propose a mapping, not to transform rows. Give it:

- Source column names.
- Target field names and types, with required flags.
- Optionally up to three sample values per source column, only with explicit user consent.
- An instruction to treat all headers and sample values as untrusted data, not as commands.
- An instruction to leave uncertain fields unmapped and to flag ambiguity.

Require JSON matching a simple schema, e.g. an object with a `mappings` array. Each mapping has fixed properties: `source_column`, `target_field`, `operation`, `confidence`, `needs_review`, and `note`. Set `additionalProperties: false` as supported by Meta's structured output recipe. Keep the schema non-recursive and simple to stay inside documented constraints.

The model's response is a proposal, not a verified transformation. Validate the returned JSON using Pydantic and then validate every column reference and operation against the exact input schema. If any unknown fields or operations appear, reject the full suggestion response and show a recoverable message; do not execute a partially invalid model plan.

### 8.4 Error handling

Handle these cases without exposing secrets:

- API key missing: provide manual mapping and explain how to configure the key.
- `ALLOW_META_API_CALLS=false`: do not send requests; explain the toggle.
- Authentication/permission failure: summarize the status and suggest checking the dashboard/account, without printing the key.
- Rate limit (`429`): show a friendly wait/retry message; do not loop aggressively.
- Timeout/network error: keep manual mapping usable.
- Invalid/unexpected structured response: do not apply; let user continue manually.
- API errors must not include full headers/samples or credentials in server logs.

For automated tests, inject a fake provider. The fake provider is test-only and must never be described as a real Meta call. If no real API credentials/credits are available at implementation time, finish all other work and leave the real API smoke test documented as pending.

## 9. API endpoints

Use a small, versionable endpoint surface. Adjust endpoint payload format to the implementation, but keep the responsibilities separate:

- `GET /health`: minimal app health response; no secrets or account data.
- `GET /`: landing page.
- `GET /app`: workspace.
- `GET /examples/registrations.csv`: synthetic sample file.
- `GET /examples/registrations_schema.json`: synthetic target schema.
- `POST /api/profile`: accepts CSV upload, validates limits and parses it; returns headers, row count, per-column empty counts, safe local preview values, and a file hash. Do not persist the input.
- `POST /api/suggest-mappings`: accepts source headers, target schema and only consented sample values; returns model proposals if enabled, otherwise a clear error that allows manual mapping. Local normalized-header suggestions can be a separate explicit mode.
- `POST /api/process`: accepts the CSV again, target schema, and user-approved mappings; re-parses and validates, then returns a ZIP with accepted/rejected CSV, recipe, and report.
- `POST /api/replay`: accepts a CSV and recipe JSON; validates recipe version and applies it without a model call, returning the same ZIP format.

If the frontend requires a different request flow, keep the API design simple and stateless. Do not introduce database-backed sessions merely to avoid re-uploading a bounded 5 MB file.

Use FastAPI response models or explicit response types. Provide clear HTTP status codes for invalid input, invalid mappings, missing model configuration, and upstream API failures.

## 10. Test and quality requirements

Create tests before or alongside implementation. Use synthetic fixtures only; do not commit personal data.

### 10.1 Unit tests

- Empty file, only header, malformed CSV, invalid UTF-8/BOM handling.
- Duplicate/blank headers and mismatched row lengths.
- Size/row/column limit enforcement.
- Column profiling and sample handling.
- Invalid schema types, duplicate target names and invalid source references.
- Each allowlisted transformation.
- Type validation for strings, integers, decimals, booleans and strict ISO dates.
- Missing required fields, invalid values and optional blanks.
- Row accounting invariant and stable source order.
- Recipe serialization, version check and replay without AI.
- Unknown recipe operation rejection.
- Formula-safe export behavior.
- ZIP contains exactly the expected files with safe filenames.

### 10.2 API tests

- Health and pages return successfully.
- CSV profiling accepts valid input and rejects bad input clearly.
- Manual mapping can produce valid exports without a Meta key.
- Meta mapping disabled/missing key returns a safe explanatory error.
- Fake provider returns a valid mapping proposal and the app validates it.
- Fake provider returning invalid fields/operations is rejected.
- Processing returns a valid ZIP and correct row-count headers/summary.
- Recipe replay does not call the Meta provider.
- API error messages do not reveal environment variables or submitted row values.

### 10.3 Real API smoke test

Create a separate opt-in command, e.g. `python -m scripts.test_meta_api`, that:

- Does nothing unless `ALLOW_META_API_CALLS=true` and `MODEL_API_KEY` is configured.
- Sends a small, non-sensitive request such as a few synthetic column headers.
- Requests a structured mapping response.
- Reports success/failure, latency and returned usage if available, without printing the API key.
- Does not run as part of default pytest or CI.

Do not count fake-provider tests as live API verification.

### 10.4 CI

Add a GitHub Actions workflow that installs dependencies and runs pytest and Ruff on a supported Python version (prefer a small matrix if practical). CI must not require `MODEL_API_KEY`. Do not add paid services.

## 11. README and project documentation

Create a factual, concise README with:

- Project name and one-sentence description.
- What it does and the user workflow.
- Features and screenshots/GIF placeholders only if genuine captures exist.
- Architecture/data flow.
- Exact Meta Model API role and fallback behavior.
- Local setup, environment variables, run command and tests.
- CSV/schema restrictions and safe handling behavior.
- Privacy note explaining that optional sample values are sent to Meta only after opt-in; be clear that data sent to the API is externally processed.
- Known limitations and a statement that model suggestions require user review.
- License and dependency notices.
- Real demo and product links only when they exist.

Also maintain:

- `docs/ARCHITECTURE.md`: modules, data flow, major invariants.
- `docs/DECISIONS.md`: small decision log, including the chosen MVP scope.
- `docs/TEST_PLAN.md`: test cases and observed results.
- `docs/DEMO_SCRIPT.md`: final 3-minute video script.

Do not claim the project is production-ready, enterprise-grade, fully private, or perfectly accurate.

## 12. Local environment and developer experience

Support Windows PowerShell first, while keeping Python code cross-platform where reasonable.

README setup should resemble:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

If the machine only has `python` rather than `py`, document that alternative. Do not assume a Unix shell. Test startup using the actual environment available to Codex.

Provide a Windows-friendly `run.ps1` only if it reduces friction. Avoid making the project depend on `make`, Docker, or Linux shell commands.

## 13. Implementation phases and acceptance gates

### Phase 1 — Workspace inspection and bootstrap

- Inspect directory, Python version, Git state, and available shell.
- Create `AGENTS.md` containing the key instructions in this document: scope, test requirements, no secret leaks, and no deployment/push without permission.
- Initialize or verify local Git safely, confirm `.gitignore` excludes secrets/private data, and create/maintain `docs/PROJECT_STATUS.md`, `docs/SESSION_HANDOFF.md`, `docs/DECISIONS.md`, `docs/TEST_LOG.md`, and `docs/THIRD_PARTY_NOTICES.md` according to `CODEX_CONTINUITY_PROTOCOL.md`.
- Make a local checkpoint commit after the bootstrap tests pass; never push without permission.
- Create dependencies, configuration, application entrypoint and a health endpoint.
- Add `.gitignore`, `.env.example`, project license file and `docs/DECISIONS.md`.
- Create sample CSV/schema fixtures containing synthetic data.

**Gate:** App imports, `/health` works, dependencies install, and tests start running.

### Phase 2 — Deterministic CSV pipeline

- Implement parser, input caps, profile, schema validation, transformations, rejected/accepted rows, recipe and report.
- Add unit tests for all parsing/validation invariants.
- Do not build the complete UI before the service layer works.

**Gate:** Tests demonstrate stable outputs, correct row accounting and no silent destructive conversion.

### Phase 3 — Meta mapping adapter and manual fallback

- Implement a Meta client isolated from core processing.
- Implement simple constrained JSON mapping responses.
- Add local manual/header-similarity mapping so the whole product works before credits arrive.
- Require explicit user approval before processing.
- Keep real API calls disabled unless the configuration flag is enabled.

**Gate:** Fake-provider tests pass; invalid model proposals cannot reach the deterministic executor unchecked. Real API status is explicitly marked pending unless a genuine request is run.

### Phase 4 — FastAPI endpoints and exports

- Implement profile, suggestion, process and replay endpoints.
- Return consistent errors and safe ZIP exports.
- Add route tests.

**Gate:** Endpoints work with TestClient and manual mode without API access.

### Phase 5 — Landing page and workspace UI

- Build shared base template, landing page, responsive styles and functional workspace.
- Implement all state transitions and error/loading states.
- Connect frontend to real endpoints.
- Ensure manual workflow and recipe replay work with the synthetic example.

**Gate:** A developer can complete the primary workflow through the browser, not merely through API tests.

### Phase 6 — End-to-end testing and polish

- Run all tests and Ruff.
- Launch the app locally and test the full user workflow with sample files.
- Test invalid files, ambiguous values, rejected rows, recipe replay and file downloads.
- Fix visible layout problems and keyboard accessibility issues.
- Review all error messages and logs for sensitive information.

**Gate:** One complete manual-mode import runs in a browser and produces the expected downloadable files; test suite passes.

### Phase 7 — Optional real Meta verification

Only if credits have appeared or the user explicitly authorizes spend:

- Confirm `ALLOW_META_API_CALLS=true` and `MODEL_API_KEY` are set locally without displaying key contents.
- Run the opt-in smoke test with synthetic headers.
- Test one actual mapping request.
- Verify response parsing, error behavior, and usage where available.
- Record in the README/docs whether live integration was successfully tested.

**Gate:** A true live response has been captured and verified, or the real integration is clearly marked unverified while manual functionality remains complete.

### Phase 8 — Release preparation

- Finish README and required docs.
- Run clean-install instructions as far as the environment allows.
- Confirm no secrets, personal CSVs, temporary exports, or `.env` are tracked.
- Verify license and dependency notices.
- Prepare screenshots only from the actual running app.
- Write the 3-minute demo script.
- Do not deploy, publish, or push unless the user approves that external action.

**Gate:** Local app, tests, documentation and demo plan are ready for the user's final review and submission steps.

## 14. Realistic build schedule

Use this schedule as guidance, not an excuse to stop if one calendar day has passed. Prioritize the order of dependencies.

- **October 27:** Bootstrap and deterministic CSV pipeline; configure API safely.
- **October 28:** Schema/mapping review, mapping recipe, exports and tests.
- **October 29:** API routes and fully usable manual-mode workflow.
- **October 30:** Landing page and integrated workspace UI.
- **October 31:** Recipe replay, error handling, and end-to-end testing.
- **November 1:** Fix correctness issues, verify sample and edge-case files, freeze scope.
- **November 2:** Clean-install checks, README, CI, deployment plan if needed.
- **November 3:** Final UI checks, record/demo preparation, confirm submission requirements.
- **November 4:** Final review, verify public repository/video access and submit well before 9:00 PM ET.

If time slips, cut polish—not validation, manual functionality, the meaningful Meta integration, or the submission video.

## 15. Three-minute demo outline

Write the final script in `docs/DEMO_SCRIPT.md`, aiming for three minutes total:

- `0:00–0:20`: State the CSV import problem and the intended user.
- `0:20–0:45`: Upload the synthetic source CSV and show its mismatched columns.
- `0:45–1:20`: Show Meta-generated or manual mappings and the review/approval step. Be explicit about whether the displayed suggestions came from a real Meta call.
- `1:20–1:55`: Show a deliberately ambiguous/invalid row being flagged instead of silently changed.
- `1:55–2:25`: Process and download accepted/rejected CSVs plus the report and recipe.
- `2:25–2:45`: Replay the recipe on a second synthetic export without another model call.
- `2:45–3:00`: Summarize what was built and show repository/product information if suitable.

Never substitute mock output while claiming it is live. If a cached/saved run is used as backup footage, label it honestly.

## 16. Definition of done

The project is considered locally complete when all required checks below pass:

- [ ] Landing page loads and CTA opens workspace.
- [ ] User can load example and upload a real CSV.
- [ ] Invalid/oversized files show clear errors.
- [ ] Target schema can be edited and validated.
- [ ] Manual mapping works without Meta credentials.
- [ ] Meta mapping code is implemented with constrained structured output and safe configuration.
- [ ] No mapping is executed until the user approves it.
- [ ] Deterministic operations are allowlisted and type validation is tested.
- [ ] Ambiguous dates/invalid types are not silently coerced.
- [ ] Accepted rows, rejected rows, recipe and report are downloadable.
- [ ] Recipe replay works without a model call.
- [ ] Row accounting and row order invariants are tested.
- [ ] Automated tests pass and Ruff is clean (or any exception is documented).
- [ ] README explains install/run/test and limitations.
- [ ] No API keys, private files, or generated output files are tracked.
- [ ] Real Meta API smoke-test status is reported truthfully.
- [ ] Three-minute demo script exists.
- [ ] Submission materials can be made public and verified before the deadline.

## 17. Final report Codex must return

When implementation stops, report in a short, factual format:

1. **Built:** key features implemented.
2. **Run locally:** exact PowerShell commands.
3. **Verification:** exact test/lint commands and real results.
4. **Meta API:** `LIVE TEST PASSED`, `NOT TESTED — CREDITS/KEY UNAVAILABLE`, or a similarly precise status. Do not use ambiguous wording.
5. **Known limitations:** only genuine remaining issues.
6. **Next user action:** only the necessary next action, such as enabling the Meta API after credits arrive or reviewing/publishing the repository.

The main objective is a working project that can be submitted. Keep scope controlled, build the deterministic core first, and never fake verification.

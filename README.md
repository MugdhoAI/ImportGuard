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
- Planned billing display: Free $0/month, Pro $6.99/month, and Business $19.99/month. These are not active payment offers until a provider is configured; checkout and payment history remain unavailable.

The default workflow does not contact Meta. One live smoke request was verified on 2026-10-30 (see Meta configuration below). Fake-provider tests exercise response validation only.

## Run on Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
.\start-local.bat
```

`start-local.bat` rebuilds the frontend and starts Uvicorn on loopback port
8000. Keep that terminal open, then open `http://127.0.0.1:8000`. If `py -3`
is unavailable, use `python -m venv .venv` and the manual fallback below.

The launcher rebuilds the frontend before each start, so changes under
`frontend/src` are reflected after restarting it. To build without starting
the server, run `npm --prefix frontend run build`.

Without a frontend build, `/` falls back to a basic server-rendered page;
`/app`, `/privacy`, and all API routes work either way.

### If the local URL does not open

ImportGuard does not currently have a public deployment URL. Start Uvicorn from
the repository root and open the exact local address shown below:

```powershell
npm --prefix frontend run build
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` rather than port `8001`. The browser workflow
check uses the same default and accepts `IMPORTGUARD_URL` when a different
local port is intentional.

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

Restart the app, review the on-screen disclosure, then invoke Meta explicitly. Never put the key in frontend code. A live smoke test against `muse-spark-1.3` passed on 2026-10-30 (one synthetic-headers request, 3 mappings returned in 18.6s; see `docs/TEST_LOG.md`). That verifies the live round trip only; mapping quality on real user CSVs still requires review for every suggestion, and the app never presents mock or local output as a live result.

To verify with exactly one minimal request (synthetic headers only, no sample
values), after configuring `.env` as above:

```powershell
python -m scripts.test_meta_api
```

The script does nothing unless `ALLOW_META_API_CALLS=true` and `MODEL_API_KEY`
are both configured. It never runs under pytest or CI, never prints the key,
and reports only success/failure, latency, and the returned mapping summary.

Official references: [Meta Chat Completions quickstart](https://dev.meta.ai/docs/cookbook/quickstart-chat-completions), [structured output](https://dev.meta.ai/docs/structured-output), and [models](https://dev.meta.ai/docs/models).

## Optional Google and GitHub sign-in

Email/password authentication works without external credentials. Google and
GitHub OAuth options remain visibly unavailable until each provider is fully
configured on the server. The integration uses server-side authorization-code
exchange, PKCE, one-time expiring state, verified email identities, and an
explicit link flow from Settings. Configure these names in `.env` (never in
frontend code):

```dotenv
OAUTH_STATE_TTL_SECONDS=600
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
GOOGLE_OAUTH_REDIRECT_URI=http://127.0.0.1:8000/auth/oauth/google/callback
GITHUB_OAUTH_CLIENT_ID=
GITHUB_OAUTH_CLIENT_SECRET=
GITHUB_OAUTH_REDIRECT_URI=http://127.0.0.1:8000/auth/oauth/github/callback
```

The redirect URI must exactly match the URI registered with the provider.
Existing password accounts are not silently merged with an OAuth identity;
the provider email must be verified and matching for an explicit Settings link.

## Abuse and resource limits

The local server applies configurable in-process sliding-window limits to login
and signup failures and the profile, mapping, process, and replay endpoints.
Processing concurrency is bounded, uploads are capped before parsing, recipes
are capped at 64 KB, SQLite uses a busy timeout, and OAuth state expires after
the configured TTL. Defaults and environment variable names are listed in
`.env.example`. These protections are intended for a single local server and
are not a substitute for a deployment-specific proxy, distributed limiter, or
security review.

## Accounts, history, and billing

Guests can run the full CSV workflow without signing in. Each validated run is
recorded (filename, row counts, recipe, report, and the ZIP package) for
`EXPORT_RETENTION_DAYS` (default 7) so downloads stay restorable from history.
Signing up or signing in claims the current browser's guest exports.

- Accounts live in a local SQLite file (`IMPORTGUARD_DB`, default
  `data/importguard.db`, gitignored). Passwords use PBKDF2-HMAC-SHA256;
  sessions are server-side with HttpOnly cookies and CSRF-protected mutations.
- `/login`, `/signup`, `/dashboard`, `/billing`, and `/payments` are
  server-rendered pages in the product shell; `/dashboard` shows per-user or
  per-guest history with download links.
- Deleting your account on `/billing` removes the account, sessions, exports,
  and subscription. See [privacy](http://127.0.0.1:8000/privacy) for retention.
- Billing is provider-neutral: `free`/`pro`/`business` plans with usage
  tracking exist, quotas stay off unless `BILLING_ENFORCE_QUOTAS=true`, and
  checkout/webhooks explicitly refuse until a payment provider is selected and
  approved. No provider is integrated and no charges can occur.

## Project status

This is an MVP under active development, licensed under the [MIT License](LICENSE). Third-party components keep their own licenses; see [third-party notices](docs/THIRD_PARTY_NOTICES.md). See [project status](docs/PROJECT_STATUS.md), [architecture](docs/ARCHITECTURE.md), and [test plan](docs/TEST_PLAN.md).

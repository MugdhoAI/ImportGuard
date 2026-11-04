<p align="center">
  <img src="docs/assets/importguard-hero.svg" alt="ImportGuard workflow: profile a CSV, review source to target mappings, validate rows, and export accepted and rejected records" width="100%">
</p>

<h1 align="center">MugdhoAI / <a href="https://github.com/MugdhoAI/ImportGuard">ImportGuard</a></h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python 3.11 or newer">
  <a href="https://github.com/MugdhoAI/ImportGuard/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
</p>

<p align="center">
  <strong>Live demo:</strong> <a href="https://importguard.onrender.com">importguard.onrender.com</a>
</p>

ImportGuard turns a messy CSV export into a clean file that matches the format you actually need. You review the column mapping, approve the changes, and validate every row before anything is exported. Nothing is applied silently.

The demo runs on a free tier, so the first load can take a moment after it has been idle.

## What it does

- Profiles your CSV: columns, row count, and sample values.
- Lets you define the target format: field names, types, and which fields are required. Types are string, integer, decimal, boolean, and strict `YYYY-MM-DD` dates.
- Suggests column matches from the header names. You can also map everything by hand.
- Applies only the fixes you approve: `identity`, `trim`, `collapse_whitespace`, `lowercase`, and `uppercase`. No arbitrary code ever runs.
- Validates every row and splits the result into accepted and rejected records.
- Saves the mapping as a recipe, so the next similar file can be processed the same way with no model call.

## How it works

1. **Import and profile.** Upload a CSV and look at what is actually in it.
2. **Define the target.** Choose the output fields, their types, and the required ones.
3. **Map and review.** Match each source column to a target field and check every mapping.
4. **Validate.** Run the approved fixes and check each row against the target format.
5. **Export and replay.** Download a ZIP with `accepted.csv`, `rejected.csv` (with source row numbers and the error for each row), `recipe.json`, and `report.json`. Reuse the recipe on the next file.

## A quick example

The bundled file `examples/registrations.csv` has three rows with the columns Reg No, Full Name, Email, and Payment. Map them to `student_id`, `full_name`, `email`, and `payment_status`, then validate.

Result: 2 rows accepted, 1 row rejected. The third row has the Payment value "maybe", which is not a valid boolean, so it lands in `rejected.csv` with its row number and the reason.

## Run it locally

You need Python 3.11 or newer. Node.js 18 or newer is only needed if you want to rebuild the landing page.

```bash
git clone https://github.com/MugdhoAI/ImportGuard.git
cd ImportGuard
python -m venv .venv
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000`. The built landing page is included in the repo, so it works out of the box.

On Windows, `start-local.bat` does the setup, rebuilds the landing page, and starts the server in one step.

## Limits

Files up to 5 MB, 5,000 rows, and 100 columns. UTF-8 and UTF-8 BOM files are supported.

## Optional extras

- **Meta Muse Spark mapping suggestions.** Off by default and fully optional. If you enable it in `.env` (`MODEL_API_KEY` and `ALLOW_META_API_CALLS=true`), you can ask for mapping suggestions from the server side adapter. Suggestions only run when you request them, and every one still needs your review. Sample values are sent only if you opt in separately.
- **Google and GitHub login.** Email and password login works on its own. OAuth login can be switched on with provider credentials in `.env`.
- **Accounts.** Guests can use the full workflow. An account adds export history with downloads you can restore later.

## Privacy

Uploads are processed in memory and the source files are not saved. Export records (file name, row counts, recipe, report, and the ZIP) are kept in a local SQLite database so the history works, for 7 days by default. In the default setup, nothing is sent to Meta or any other outside service.

## Plans

The app shows three plans: Free at $0/month, Pro at $6.99/month, and Business at $19.99/month. Checkout is not live in the app yet, so no payment can be taken today.

## Project layout

- `app/main.py`: the FastAPI app, pages, and route setup.
- `app/services/csv_service.py`: parsing, profiling, validation, transformations, exports, and recipes.
- `app/services/meta_client.py`: the optional Meta mapping adapter.
- `app/services/store.py`: SQLite storage for accounts, sessions, and export history.
- `frontend/`: landing page source and its production build.

More detail lives in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and dependency credits are in [docs/THIRD_PARTY_NOTICES.md](docs/THIRD_PARTY_NOTICES.md).

## Tests

```bash
python -m pytest -q
python -m ruff check .
npm --prefix frontend test
npm --prefix frontend run build
```

## Status

ImportGuard is an MVP built as a hackathon and portfolio project, currently at v1.0.0. Mapping suggestions can be wrong, which is why a person reviews them before anything runs. Validation checks the rules you pick; it cannot judge whether a record is true. Please do not use it with confidential or regulated data unless your own setup has been reviewed first.

## License

MIT. See [LICENSE](LICENSE).

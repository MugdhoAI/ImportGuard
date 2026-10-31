# Architecture

- `app/services/csv_service.py`: strict in-memory CSV parse/profile; validated schema/mappings; deterministic transforms; per-row validation; ZIP serialization and recipe parsing.
- `app/services/meta_client.py`: optional OpenAI-compatible Meta mapping call; both settings and an explicit endpoint request are required; structured output is validated and checked against exact source/target references.
- `app/api/routes.py`: stateless profile, mapping, process, and replay routes. Uploads are read with bounded byte limits and never written to disk.
- `app/main.py`: FastAPI pages, static assets, API routes, and `/privacy`.
- `app/templates`, `app/static`: accessible server-rendered pages and vanilla JavaScript workflow.
- `app/services/store.py`: SQLite persistence (users, sessions, export records, subscriptions).
- `app/services/auth.py`: PBKDF2 password hashing, session issue/validation, CSRF checks, login throttle.
- `app/services/billing.py`: plan/entitlement model, usage state, and the `BillingProvider` seam (`NullProvider` until a provider is approved).
- `app/api/accounts.py`: signup/login/logout/delete pages and routes, export history/download/claim endpoints.
- `app/main.py`: product shell pages plus the per-user dashboard and billing views.

Core invariants: data rows equal accepted plus rejected; each source and target can appear at most once in an approved mapping; output order follows input order; transformations use a fixed allowlist; every recipe is schema/mapping-only; archive member names are fixed.

The browser re-uploads the selected file per processing request; source files are never stored as files. The server retains account sessions and export records (counts, recipe, report, bounded ZIP bytes) in SQLite with 7-day export expiry for restorable history. The optional Meta request sends headers and schema, and up to three sample values per column only after opt-in.

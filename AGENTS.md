# Codex Instructions for ImportGuard

## Read these files first

Before editing code, read all of these files completely:

1. `CODEX_EXECUTION_PLAN.md` — product specification and implementation phases.
2. `CODEX_DESIGN_REFERENCE_GUIDE.md` — product UI direction and reference decisions.
3. `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md` — privacy, security, data integrity, testing and release expectations.
4. `CODEX_CONTINUITY_PROTOCOL.md` — mandatory Git checkpoints and cross-session handoff rules.

The files are complementary. If a visual or convenience request conflicts with data integrity, security, hackathon rules, or working product behavior, preserve the latter and record the decision.

## Goal

Build and verify a complete, locally runnable ImportGuard MVP that can be submitted to the Meta Global AI Developer Hackathon. The user wants a functional project, not a winning-at-all-costs research exercise. Keep scope small, implement real behavior, test it, and document truthfully what works.

## Mandatory work style

- Inspect the existing workspace and preserve useful work before changing files.
- Work in small, end-to-end phases. Do not stop after a plan, mockup, or landing page.
- After each significant feature or phase: run the relevant tests, inspect the diff, update status/handoff records, and create a local Git checkpoint commit according to `CODEX_CONTINUITY_PROTOCOL.md`.
- Keep `docs/PROJECT_STATUS.md`, `docs/SESSION_HANDOFF.md`, `docs/DECISIONS.md`, `docs/TEST_LOG.md`, and `docs/THIRD_PARTY_NOTICES.md` current. Create them from the included starter files if not present.
- Treat a near usage limit, context limit, or session ending as a handoff event. Stop feature work early enough to save a checkpoint and write precise resume instructions.
- Make routine, reversible decisions independently. Record material decisions in `docs/DECISIONS.md`; ask only when essential information cannot safely be inferred.
- Never claim a command or test ran unless it did. Distinguish passing automated tests, mocked provider tests, and real Meta API verification.

## Git and continuity

- The user explicitly authorized **local Git checkpoints**. If there is no Git repository, inspect the folder and then initialize one. Never overwrite an existing repository or history.
- Use local commits only. Do not push, publish, deploy, create a remote, or open a PR without explicit approval.
- Commit after each coherent major implementation and test milestone. Inspect staged files before committing; never blindly stage everything.
- Never commit `.env`, API keys, real CSV data, uploaded files, private exports, caches, virtual environments, or build artifacts.
- Do not use `git reset --hard`, `git clean`, force push, history rewrite, or other destructive Git operations.
- If a session may end while work is incomplete, preserve the working tree and write `docs/SESSION_HANDOFF.md`; if useful, make a clearly labelled WIP checkpoint commit after confirming no secrets or private data are staged. Report any failing tests rather than hiding them.
- Start each resumed session by reading the latest handoff, project status, Git status, and recent commit history. Continue from actual state, not assumptions.
- Detailed mandatory procedure is in `CODEX_CONTINUITY_PROTOCOL.md`.

## Technical constraints

- Follow the small Python/FastAPI application and server-rendered HTML/CSS/vanilla JavaScript architecture in the execution plan unless the actual workspace or a verified blocker justifies a change.
- Do not add Supabase, React/Next.js, a database, background queues, Docker, microservices, analytics, account systems, or a heavy 3D framework without a verified requirement.
- Manual column mapping and deterministic CSV processing must work without Meta API access.
- Model output is untrusted. Validate it against a strict schema and allowlist. Require user review before transformations; never execute model-generated code.
- Never silently modify identifiers, guess ambiguous dates, discard rows, or overwrite original files.

## Meta API and secrets

- Keep `MODEL_API_KEY` in a local `.env` file or environment variable. Ensure `.env` is ignored by Git.
- Never print, expose, commit, place in frontend code, or send secrets to the browser.
- Keep `ALLOW_META_API_CALLS=false` by default. Make a real/billable call only when the user explicitly enables it and confirms access/credit status.
- A fake provider is permitted for automated tests but must never be described as a real Meta request.
- If credits are pending, finish all non-API work and leave a clear pending status. Do not fake live responses.

## Design

- Use the product-specific direction in `CODEX_DESIGN_REFERENCE_GUIDE.md`, taking inspiration from supplied examples without copying their unrelated branding/content.
- The workspace and data review experience matter more than animation. Every visible control must work.
- ThreeUI components are optional, not requirements. Verify exact source, license/terms, attribution, hashes and assets before integrating copied source. If that takes too long or the rights are unclear, use an original CSS/HTML effect and continue.
- No fake testimonials, customer logos, usage metrics, client lists, or unsupported claims.

## Privacy, safety and release

- Implement an accurate `/privacy` page consistent with actual data flow; do not invent legal contacts or claim compliance without evidence.
- Follow `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md` for file upload validation, CSV formula injection, safe HTML, model-input consent, logs, accessibility, licensing, and test expectations.
- Bind the app to `127.0.0.1` by default. Public deployment requires explicit approval and a separate deployment/privacy review.
- Check dependency licenses and preserve required notices.

## Completion report

When blocked, interrupted, or finished, state: what is implemented; current Git commit; working-tree state; exact tests/commands run and their results; known failures; what is not yet verified; whether a real Meta API request succeeded; exact local run command; and the next concrete task. Keep API keys and private data out of the report.

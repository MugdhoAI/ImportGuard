# Prompt 03 — Handoff Before Usage/Context Limit

Stop adding features and prepare ImportGuard for a reliable handoff to another Codex session/model. Follow `CODEX_CONTINUITY_PROTOCOL.md`.

- Inspect Git status, branch, last commit, and diff check.
- Run the most relevant quick test if feasible; record if not run.
- Update `docs/PROJECT_STATUS.md` and `docs/SESSION_HANDOFF.md` precisely.
- Include the last verified commit hash, modified/staged/untracked files, completed work, tests/commands/results, exact failing tests or blockers, last action completed, next three tasks in order, startup/test commands, required environment variable names only, Meta API/credit status, and warnings against overwriting/deleting anything.
- Update `docs/TEST_LOG.md` and `docs/DECISIONS.md` as needed.
- Review staged files for credentials and private data. Save coherent work in a local checkpoint commit; if work is incomplete or failing, mark any checkpoint WIP and say so. Never discard in-progress work.
- Do not push, deploy, publish or create costs.

Finish with a concise copyable instruction for the next model. State plainly what is not finished. Do not imply a hard termination can preserve edits that have not been saved.

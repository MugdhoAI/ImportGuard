# Prompt 02 — Phase Checkpoint

Pause feature development at the current safe boundary. Follow `CODEX_CONTINUITY_PROTOCOL.md`.

1. Inspect `git status --short`, branch and recent commits.
2. Run all focused tests/lint/syntax checks for the work just completed; report the exact commands and outcomes.
3. Run `git diff --check`; inspect the diff and stage only reviewed files.
4. Confirm no `.env`, API key, real CSV, private export, personal data, cache or build output is staged.
5. Update `docs/PROJECT_STATUS.md`, `docs/TEST_LOG.md`, `docs/DECISIONS.md` if needed, and `docs/SESSION_HANDOFF.md` with the actual state.
6. Create a descriptive local checkpoint commit for coherent work. Do not push. If tests fail, either fix them or record them clearly and use a labelled WIP checkpoint only if safe.
7. Verify the last commit with `git log -1 --oneline`.

Report the milestone, test status, commit hash, remaining issues and next 1–3 steps. Do not claim tests passed unless they ran and passed.

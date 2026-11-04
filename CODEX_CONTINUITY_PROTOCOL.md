# ImportGuard — Git Checkpoint and Session Handoff Protocol

This protocol exists so work can continue across Codex usage limits, context limits, restarts, or a handoff to another coding model. Follow it for every substantial implementation, not only at the very end.

## 1. First actions in every session

Run/check the following before editing (adapt commands to the available shell):

```powershell
git status --short
git branch --show-current
git log -5 --oneline
```

Then read:
- `docs/SESSION_HANDOFF.md`
- `docs/PROJECT_STATUS.md`
- `docs/DECISIONS.md`
- `docs/TEST_LOG.md`
- the relevant phase in `CODEX_EXECUTION_PLAN.md`

If the workspace is not a Git repository, inspect it first and initialize local Git without overwriting any existing work. Confirm `.gitignore` excludes `.env`, virtual environments, cache/build folders, local uploads/outputs, and private data before staging files.

Do not assume the previous model's summary is accurate. Inspect the actual repository, current files, and last commit.

## 2. When to create checkpoints

Create a local Git checkpoint after every coherent major unit, such as:

1. Workspace bootstrap, app startup, configuration, and initial tests.
2. CSV parser/profiler plus edge-case tests.
3. Target-schema and manual mapping workflow.
4. Deterministic transform/validation engine plus tests.
5. Accepted/rejected exports and JSON recipe replay.
6. Meta adapter with fake-provider tests and safe configuration (real request remains separately verified).
7. API routes and browser workflow connected end-to-end.
8. Landing page, responsive workspace, and accessible functional controls.
9. Security/privacy fixes and quality test suite.
10. Documentation, demo readiness, and final audit.

Also checkpoint before a risky refactor and whenever a significant set of tests passes. For long tasks, update the status/handoff files after roughly 30–60 minutes of meaningful work or sooner when a coherent unit is finished. Do not spend time committing every tiny edit.

## 3. Pre-commit procedure

Before a normal checkpoint commit:

1. Run focused tests and appropriate lint/type/syntax checks.
2. Run `git diff --check`.
3. Inspect `git status --short` and `git diff --stat`.
4. Stage only the specific files intended for the checkpoint. Do not use `git add .` blindly.
5. Inspect the staged diff (`git diff --cached --stat` and, when needed, `git diff --cached`).
6. Confirm no `.env`, credentials, real CSV files, private exports, personal data, caches, or build artifacts are staged.
7. Update `docs/PROJECT_STATUS.md`, `docs/TEST_LOG.md`, and `docs/SESSION_HANDOFF.md` with actual results.
8. Commit using a descriptive message, for example:

```text
feat(csv): add bounded CSV profiling
feat(validation): add row-level schema checks
feat(export): add accepted and rejected CSV downloads
test(import): cover ambiguous dates and identifier preservation
fix(ui): handle invalid upload feedback
chore(docs): update continuity checkpoint
```

Use local commits only. Do not push. Never claim a checkpoint commit exists until `git log -1 --oneline` confirms it.

## 4. If tests fail at a checkpoint

- Prefer to fix the failures before declaring the milestone complete.
- If the work must be handed off before all tests pass, record the exact failure, command and output summary in `docs/TEST_LOG.md` and `docs/SESSION_HANDOFF.md`.
- If a partial commit is useful for recovery, make a clearly labelled WIP checkpoint only after reviewing staged files and ruling out secrets/private data. The handoff must state that this is a WIP and name the failing tests.
- Never change a test to make it pass unless the test expectation itself is shown to be wrong; preserve a record of the reasoning.

## 5. Handoff trigger: nearing a usage/context limit or stopping

Do not continue adding features until the end of a session and leave no summary. Stop at the next safe boundary and do all of the following:

1. Run `git status --short`, `git log -1 --oneline`, and `git diff --check` if possible.
2. Run the smallest relevant test command if feasible; otherwise say it was not run.
3. Update `docs/PROJECT_STATUS.md` with the overall stage and gates passed/blocked.
4. Update `docs/SESSION_HANDOFF.md` with:
   - current date/time if available;
   - current branch and last verified commit hash;
   - whether changes are committed, staged, or uncommitted;
   - completed work and important file paths;
   - exact commands run and test results;
   - failing tests or unresolved bugs;
   - the last action completed;
   - the next 1–3 concrete actions in order;
   - exact command(s) to run next, if useful;
   - environment variable *names* needed, never values;
   - whether Meta credits/API were verified and whether any real request succeeded;
   - warnings about files that must not be overwritten or data that must not be deleted.
5. Update `docs/DECISIONS.md` if a meaningful technical or scope decision was made.
6. Create a local checkpoint commit for the handoff docs and coherent working changes if safe. If code is mid-change or failing, either preserve it as a clearly labelled WIP checkpoint or leave it uncommitted and document precisely why. Never discard it.
7. End the session summary with one copyable instruction for the next model.

## 6. Resume prompt contract

The next model must read this protocol and the latest `docs/SESSION_HANDOFF.md`, inspect Git status and recent commits, run or review the listed tests, and continue from the actual state. It must not recreate files, repeat completed work, or overwrite existing implementation just because the prior model stopped.

Resume from `docs/SESSION_HANDOFF.md` and follow the current execution phase in `CODEX_EXECUTION_PLAN.md`.

## 7. Git safety rules

- Never use `git reset --hard`, `git clean -fd`, force push, history rewrite, or destructive cleanup.
- Do not delete branches or untracked files automatically.
- Do not commit secrets or private sample data even for a WIP checkpoint.
- Do not create/push a remote, deploy, publish, create paid resources, or open public PRs without explicit approval.
- Git is a continuity mechanism, not a substitute for tests or a truthful handoff.

## 8. Definition of a good checkpoint

A good checkpoint lets a different model resume without asking the user to repeat the project goal. It includes a meaningful commit or safely preserved working tree, accurate tests, clear project status, decisions, known blockers and the next concrete action. It does not claim that incomplete or mocked functionality is finished.

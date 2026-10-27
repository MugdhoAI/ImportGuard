# Prompt 01 — Start or Continue ImportGuard

Read `AGENTS.md`, `CODEX_CONTINUITY_PROTOCOL.md`, `CODEX_EXECUTION_PLAN.md`, `CODEX_DESIGN_REFERENCE_GUIDE.md`, and `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md` completely before changing code.

Inspect the current workspace, Git status/history, Python environment, and available commands. If the project has existing work, preserve it. If Git is not initialized, initialize it safely and ensure `.gitignore` excludes `.env`, keys, uploaded CSVs, private exports, caches, virtual environments and build artifacts.

Build the actual locally runnable ImportGuard MVP defined in `CODEX_EXECUTION_PLAN.md`. Do not stop after a plan, landing page, static prototype, or mocked UI. Prioritize the complete manual workflow: bounded CSV upload and profiling, target schema, manual mapping, review, deterministic allowlisted transformations, row validation, accepted/rejected downloads, report and recipe replay. Add the Meta Muse Spark adapter and mocked-provider tests, but keep real API calls disabled until `ALLOW_META_API_CALLS=true` is explicitly configured by the user.

Follow the design guide, but core workflow and tests come before optional effects. Inspect licensing before copying source/assets from ThreeUI; if source or rights are unclear, use a native product-specific CSS/HTML effect instead. Implement the accurate privacy page and security checklist items.

Work in coherent phases, run tests, fix failures, update `docs/PROJECT_STATUS.md`, `docs/SESSION_HANDOFF.md`, `docs/DECISIONS.md`, `docs/TEST_LOG.md`, and `docs/THIRD_PARTY_NOTICES.md`, and create local Git checkpoint commits according to `CODEX_CONTINUITY_PROTOCOL.md` after significant completed work. Do not blindly stage all files. Never commit secrets or real user data. Do not push, deploy, publish, create a remote, or incur non-credit costs without approval.

Continue through all feasible tasks. If blocked by credentials, credits, missing inputs, or a genuinely necessary owner decision, finish all independent work and document the blocker rather than pretending it passed.

At the end of this work session, report exact features implemented, current commit, working-tree state, tests and outcomes, known failures, Meta API status, and the next concrete action. Do not claim untested behavior is verified.

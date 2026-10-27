# ImportGuard Codex Kit — Start Here

This kit contains the product specification, design guidance, privacy/security quality checklist, mandatory Git checkpoint/handoff protocol, and ready-to-use Codex prompts.

## Put these files in `C:\ImportGuard`

Extract the ZIP **into the existing `C:\ImportGuard` folder**, keeping the structure exactly as shown. Do not extract into a second nested project folder.

```text
C:\ImportGuard\
  AGENTS.md
  CODEX_EXECUTION_PLAN.md
  CODEX_DESIGN_REFERENCE_GUIDE.md
  CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md
  CODEX_CONTINUITY_PROTOCOL.md
  README_START_HERE.md
  prompts\
    01_START_OR_CONTINUE.md
    02_PHASE_CHECKPOINT.md
    03_HANDOFF_BEFORE_LIMIT.md
    04_RESUME_FROM_HANDOFF.md
    05_FINAL_AUDIT.md
  docs\
    PROJECT_STATUS.md
    SESSION_HANDOFF.md
    DECISIONS.md
    TEST_LOG.md
    THIRD_PARTY_NOTICES.md
```

If files already exist, compare and replace with care; keep the latest execution plan and design/security guides. The kit includes updated versions of `AGENTS.md` and `CODEX_EXECUTION_PLAN.md` that reference Git continuity.

## First Codex action

Open `C:\ImportGuard` in Codex and submit the contents of `prompts/01_START_OR_CONTINUE.md` as the initial task. `AGENTS.md` is automatically useful as workspace guidance in Codex-compatible workflows; still explicitly ask Codex to read the other files.

## Ongoing use

- After a major implementation, use `prompts/02_PHASE_CHECKPOINT.md`.
- Before ending a session or approaching a usage/context limit, use `prompts/03_HANDOFF_BEFORE_LIMIT.md`.
- In a new session/model, use `prompts/04_RESUME_FROM_HANDOFF.md`.
- Before considering submission ready, use `prompts/05_FINAL_AUDIT.md`.

## What this does and does not guarantee

Local Git commits plus the handoff files greatly reduce lost context and make model handovers easier. No workflow can guarantee that an abrupt process termination saves the very last in-progress edit; this is why Codex must checkpoint frequently and update the handoff at safe boundaries. Never push or deploy without approval. Never commit keys, `.env`, or private CSV data.

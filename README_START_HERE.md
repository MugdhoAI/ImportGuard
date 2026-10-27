# ImportGuard Visual Redesign Kit

This kit replaces conflicting old visual instructions with one current direction and provides the owner-supplied source references to Codex.

## Before running Codex

1. Extract/merge these files into `C:\ImportGuard`, replacing the older `AGENTS.md` and `CODEX_DESIGN_REFERENCE_GUIDE.md` with the versions in this kit. The ZIP contains instruction and reference files only; it does not contain your `app/` implementation.
2. Keep `CODEX_EXECUTION_PLAN.md`, `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md`, and `CODEX_CONTINUITY_PROTOCOL.md` aligned with the current project.
3. In a terminal inside `C:\ImportGuard`, install Hallmark for Codex:
   ```powershell
   npx skills add nutlope/hallmark --agent codex
   ```
   If the installer asks which project/harness, choose Codex and local/project install. Inspect the prompt before approving terminal actions.
4. Reopen/restart Codex if needed so it discovers the skill.
5. Submit `prompts/03_VISUAL_REDESIGN.md`.

## Why the old screenshot missed

The earlier guide still favored a light Lumora-style presentation. The latest design choices (Predictive Arc dark background, Sable Dock, GlassAiButton, Hallmark redesign) had not been consolidated into one authoritative specification. This kit resolves that conflict. The screenshot alone cannot prove which files Codex read; it proves the rendered result did not meet the latest intended design.

## What is and isn't included

- Included: supplied GlassAiButton and AnimatedTopDock source text bundles, current screenshot, and separate Aegis visual sample.
- Not included: the complete canonical Predictive Arc JSON source bundle. Codex must fetch the exact source and verify its hashes; if that fails, report it, do not approximate.
- ThreeUI's original GlassAiButton contains “GPT 6 Sol” in its canvas label. The application adapter needs ImportGuard copy and a real CTA action; keep the unmodified original file in references and document the adapter divergence.
- The `awesome-codex-skills` repository is a catalogue, not one design skill. Hallmark is the chosen anti-slop design skill. Its rendered linter should be run on actual local output.

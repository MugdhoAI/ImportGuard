# ImportGuard Design Reference Guide — Current Direction

**Use this version as the current visual source of truth.** It supersedes earlier references to a light Lumora-style layout or Kage/Sylva worlds for the next redesign.

Read:
- `design.md` — locked design thesis, tokens and page anatomy.
- `CODEX_VISUAL_REDESIGN_PLAN.md` — detailed source, integration, anti-slop and acceptance requirements.
- `CODEX_EXECUTION_PLAN.md` — product behavior and architecture.
- `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md` — safety and quality.
- `CODEX_CONTINUITY_PROTOCOL.md` — checkpoints and handoff.

## Selected effects

1. **Background:** PredictiveArcCanvas from https://threeui.com/hero/predictive-arc using the source bundle at https://threeui.com/source-code/predictive-arc.json. Use exact source, verify hashes. The full source bundle itself has not been included as an attachment; fetch it before integration. Do not substitute `references/visual/aegis-remixed-bento-reference.html`.
2. **Navigation:** AnimatedTopDock / Sable from https://threeui.com/css/animated-top-dock. Owner-supplied source reference is `references/threeui/animated-top-dock-source.md`; its required binary font is separate and must be fetched/hash-verified.
3. **CTA:** GlassAiButton from https://threeui.com/buttons/glass-ai-button. Owner-supplied source is `references/threeui/glass-ai-button-source.md`. The original says “GPT 6 Sol”; keep the original source in vendor references, but make a minimal documented app adapter with ImportGuard label and real action before shipping.

## Install and run Hallmark

Hallmark is the actual anti-slop design skill; `awesome-codex-skills` is a catalogue and should not be treated as a single design skill.

From `C:\ImportGuard`:
```powershell
npx skills add nutlope/hallmark --agent codex
```

Use Hallmark's redesign procedure on the current app (not fresh-build). Keep existing behavior and routes, run `sloplint --before` and later `sloplint --kept` as supported, build/review the hero first, then run rendered `sloplint --render` and fix Floor failures. Its rendered checks need Node 18+, Puppeteer Core and Chrome; report blockers honestly.

The catalogue https://github.com/composio-community/awesome-codex-skills contains a relevant `webapp-testing` skill for Playwright, but do not install the whole catalogue. Use the skill only after inspecting its instructions/license or run equivalent Playwright QA directly.

## Current reference sources provided to Codex

- `references/threeui/glass-ai-button-source.md`: full source bundle supplied by the owner.
- `references/threeui/animated-top-dock-source.md`: full text source bundle supplied by the owner; binary font not included.
- `references/visual/current-landing-before.png`: current homepage screenshot.
- `references/visual/aegis-remixed-bento-reference.html`: separate security-themed visual sample, not the Predictive Arc source.

Do not combine every past reference into one design. The current direction is dark arc + functional navigation + glass CTA, with a restrained product UI that passes Hallmark.

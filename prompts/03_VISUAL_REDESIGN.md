# Codex prompt: Redesign ImportGuard with Hallmark

Read the following files fully before editing:
- `AGENTS.md`
- `CODEX_DESIGN_REFERENCE_GUIDE.md`
- `CODEX_VISUAL_REDESIGN_PLAN.md`
- `design.md`
- `CODEX_EXECUTION_PLAN.md`
- `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md`
- `CODEX_CONTINUITY_PROTOCOL.md`

Then act on the existing app, not a new scaffold.

1. Inspect the current Git state, app routes, and project handoff files. Preserve all working CSV logic.
2. Verify/install the Hallmark skill project-locally with `npx skills add nutlope/hallmark --agent codex` if missing. Read the installed `SKILL.md`. This is a redesign: use Hallmark's redesign workflow and record the current wiring before changes.
3. Inspect the attached source bundles in `references/threeui/`.
4. Retrieve `https://threeui.com/source-code/predictive-arc.json` and verify its files against the hashes in the supplied specification. The local Aegis HTML is not that source. If the bundle cannot be retrieved or source/license verified, do not imitate it; report the exact blocker.
5. Build the hero alone first: full-bleed Predictive Arc background, accessible Sable dock, centered headline “Make every CSV import predictable.”, concise body copy, and an actually working Start an import CTA using a minimal documented adapter of GlassAiButton. Rebrand the original GPT 6 Sol label in the application-specific adapter to “CSV IMPORT”; keep original source unchanged under references and preserve its rendering/motion. Wire the activation to the actual workspace.
6. Add persisted dark/light mode; dark is default. The hero stays dark. All main color values use the tokenized design system.
7. Capture and inspect real screenshots; fix the hero before continuing. Then redesign below-the-fold sections and keep the existing CSV workspace intact.
8. Remove generic AI design tells: eyebrow, colored single-word heading, tracked uppercase micro-labels, decorative dots, fake client/metric claims, “Illustrative example” panel, repeated identical card grids and nonfunctional controls.
9. Run Hallmark rendered lint on the hero and full page. Fix every Floor failure and resolve or document Reflex warnings. Test real UI with Playwright/equivalent at 1920, 1440, 1280, 1024, 768, 430, 390 and 360 px widths.
10. Test navigation and theme toggle; start import; upload a real fixture CSV; review mappings; process; download accepted/rejected rows and report; replay a recipe; check console; verify reduced motion and WebGL fallback.
11. Run backend tests, lint and `git diff --check`; inspect staged changes for secrets/private data; update visual screenshots, project status, test log, decisions and handoff; create a descriptive local commit.
12. Do not make real Meta API calls unless `ALLOW_META_API_CALLS=true` is explicitly set by the owner. Do not deploy or push.

Work in small phases and keep going until the acceptance criteria in `CODEX_VISUAL_REDESIGN_PLAN.md` are satisfied or a real blocker is reached. Do not make claims about visual quality without screenshots and test output. At the end, report evidence rather than general assurances.

# Codex Task: Repair the ImportGuard Landing Page to Match the Approved Visual Direction

**This is a visual reconstruction task, not another broad redesign.** The existing workspace works and must remain intact. The current landing page is visibly wrong despite successful tests. Do not declare completion based on build/test success alone.

## Authority and conflict resolution

For the landing-page visual direction, this prompt is the current source of truth. First inspect `AGENTS.md`, `CODEX_DESIGN_REFERENCE_GUIDE.md`, `CODEX_VISUAL_REDESIGN_PLAN.md`, `design.md`, current component source references, and the actual running page. Identify and resolve contradictory instructions. In particular, older instructions favoring a Lumora-style/light/left-aligned hero or rejecting `GlassAiButton` do **not** apply to this task. Keep the existing security, privacy, data-integrity, and Git safety rules.

Create `docs/LANDING_VISUAL_SOURCE_OF_TRUTH.md` containing the current design decisions and acceptance criteria in this prompt. Update the landing-design guidance in `AGENTS.md` to point to that document and explicitly mark conflicting older landing-design directions as superseded for this task. Do not delete reference/history documents or alter unrelated instructions.

## Phase 0 — Diagnose before changing code

1. Inspect `git status`, current branch, `HEAD`, recent commits, project routes, and current handoff documents. Preserve all pre-existing user changes. Never reset, clean, or discard unrelated files.
2. Confirm that the screenshot being tested is actually served by the current checkout and latest local commit. Trace the `/` route to its real template/component and styles. Rule out a stale Uvicorn process, stale frontend build, cache, or a route serving a different page before editing.
3. Use the browser and DOM/computed styles to diagnose the actual causes of these visible failures in the current screenshot:
   - The hero content is left aligned instead of centered.
   - The hero background appears as two faint circular outlines rather than the intended prominent Predictive Arc scene.
   - The primary CTA looks like an ordinary solid purple pill, not the supplied glass effect.
   - A static “Illustrative example” mapping panel occupies/overlaps the hero despite the decision to remove it.
   - An entire lower section has a pale background with nearly white text, making it unreadable.
   - The page retains an eyebrow, a single purple word in the headline, and other patterns explicitly prohibited by the current brief.
4. Inspect actual implementation and computed values. Do not guess. Specifically check canvas dimensions, opacity, animation state, positioning, stacking contexts, overlays, and component props; inspect the GlassAiButton iframe/adapter/layers; inspect CSS theme variables and selectors for the low-contrast section.
5. Check the available original component bundles and their verified hashes before reusing them. The Predictive Arc must be the actual supplied source, not a CSS drawing or the Aegis reference. The Glass button’s accessible action must work without an opaque overlay hiding its visual effect. Preserve unrelated source bundles unchanged.
6. Write a short root-cause note to `docs/visual-qa/landing-repair-findings.md` with the observed evidence, files/selectors responsible, and fixes planned. Then continue straight into implementation; do not stop after diagnosis or ask for approval.

If an approved target/reference image exists in the repository or provided files, use it as the visual comparison target. Do not treat the current broken screenshot as the desired target. If no approved target image is available, follow the explicit composition requirements below and report honestly that exact pixel-by-pixel comparison was not possible without that image.

## Required result: hero

The hero must feel deliberately art-directed, immersive, and product-specific—not like a generic SaaS template.

- Use the **verified original `PredictiveArcCanvas`** as a full-bleed, animated background. Follow the supplied configuration: `mode="dark"`, `speed={1.00}`, `hue={0}`, `saturation={1.00}`, `brightness={1.00}` (adjust only if the canonical source’s actual API differs, and document why). The real canvas must fill the hero scene and its actual animation/effect must be visible. Do not substitute two hand-drawn rings or a static picture. Do not hide the effect under an opaque overlay. Use only a restrained contrast vignette if necessary.
- The hero remains dark even when the rest of the site switches to light theme.
- Use the requested **AnimatedTopDock / Sable** source for the top navigation. It must have the intended animated dock behavior, working ImportGuard-specific links, no SABLE//OS demo branding, and no unrelated labels. Include the persisted theme toggle without crowding the dock.
- Center the hero content horizontally and compose it as one vertical stack over/within the background. At desktop widths, place the content around the visual center of the hero rather than in a left-side marketing column. The headline and primary CTA must be visible without scrolling at 1280×800.
- Required headline: **“Make every CSV import predictable.”** Use a coherent, high-contrast treatment for the complete heading. Do not color only “predictable.”
- Required supporting copy: **“Map unfamiliar columns, review every transformation, and export validated data without silent changes.”** Constrain line length for intentional wrapping.
- Primary CTA: **“Start an import”** using the supplied **GlassAiButton** visual treatment. Its glass material/refraction, depth, lighting, and hover/press response must be visually recognizable in the screenshot—not replaced by an ordinary solid pill. Keep the original source unchanged; use a minimal documented ImportGuard adapter. It must navigate to the real workspace through an accessible native link/button. If an overlay is needed for accessibility, make it transparent and correctly layered so it does not obscure the glass effect or break pointer/keyboard behavior.
- Secondary action: **“See the workflow”**, a real link to the workflow section.
- Do not include a tiny uppercase eyebrow, decorative dot, “Illustrative example” window, static fake mapping card, fake metrics, or testimonial logos in the hero.
- Give the hero enough height and breathing room for the full visual scene, roughly 88–100svh at desktop, while avoiding mobile overflow. Keep text legible over the animation.

## Required result: below-the-fold landing page

Redesign these sections only after the hero is corrected and captured in screenshots. Do not redesign the working workspace or rewrite CSV business logic.

1. **Workflow section:** Show the real product story—bring a CSV, review each mapping, validate rows, export accepted/rejected rows and a reusable recipe. Any interactive preview or sample action must use the existing sample fixture/real processing path. Label synthetic sample data honestly. Do not imply that an unverified Meta response is live.
2. **Product explanation:** Explain human review, deterministic validation, rejection reasons, and recipe replay with varied editorial compositions. Avoid repeating the same three-card layout in every section. Use authentic data shapes and useful visual hierarchy rather than generic dashboard charts.
3. **Data-control/privacy section:** Keep all copy readable. Prefer the established dark palette or use deliberate light surfaces with dark, high-contrast text. The current pale-background/near-white-text failure must not recur.
4. **Final CTA and footer:** Keep the main action and privacy link functional. Remove redundant filler.

Use the established tokenized system in `design.md`/the project’s current design tokens. No scattered competing colors, default gradient wallpaper, card-inside-card layouts, excessive all-caps labels, tiny grey-on-grey text, or layout animations. Keep reduced-motion support and sensible WebGL fallback behavior.

## Preserve the working application

The existing workspace is already the accepted implementation baseline. Preserve:

- `/app` workspace and `/privacy` page, route behavior, and theme persistence.
- CSV upload/profile limits, schema editing, local suggestions, mapping review, deterministic validation, accepted/rejected CSV exports, report export, and recipe replay.
- The existing local-first privacy behavior and Meta mapping disabled by default.
- Keyboard behavior, focus visibility, labels, errors, reduced-motion support, and existing automated tests.

Only make shared changes (such as a theme-token fix) when necessary; then explicitly regression-test the workspace and privacy page in both themes. Do not make live Meta API calls. Do not deploy, publish, push, create remotes, or make any external side-effecting operation. Local checkpoint commits are permitted; do not commit secrets, user CSVs, captures containing private data, build output, or unrelated user changes.

## Mandatory visual iteration process

**Do not build everything in one pass and merely capture final screenshots.** Work in this order within this task:

1. Capture the current running page at 1440×900 and 390×844; preserve these as `*-before` evidence and complete Phase 0 diagnosis.
2. Fix only the hero, its canvas and dock, CTA, and relevant shared theme wiring. Run the app. Capture and inspect screenshots at 1440×900, 1280×800, 1024×768, 768×1024, 430×932 (or closest supported), 390×844, and 360×800. Compare the screenshots to the requirements and available approved target image. Fix defects and repeat the screenshot review until the hero passes the criteria below. Do not move on just because the code compiles.
3. Build the below-the-fold sections, then repeat the same screenshot/review loop, including full-page screenshots at desktop and mobile sizes.
4. Check both dark and light themes. The hero remains dark in both. No section may contain unreadable text or incorrect inherited colors.
5. Only after the visual checks pass, run the existing automated and browser tests. Fix regressions and take the final screenshots.

### Hero pass criteria — every item required

- Centered headline, support copy, and CTA; no left-column hero composition.
- The actual verified Predictive Arc source fills the background and the scene looks animated/prominent, not like a static pair of faint outlines.
- Original glass-button appearance is visibly recognizable; real accessible navigation works.
- AnimatedTopDock’s intended behavior is present; all links and theme control work.
- No eyebrow, decorative status dot, colored single word, or “Illustrative example” panel.
- Hero fits within 1280×800 without requiring a scroll to reach the CTA.
- Strong text/background contrast; no overlap, console errors, or horizontal overflow.

### Whole-page pass criteria — every item required

- The below-fold layout feels coherent with the hero and uses varied compositions.
- Every section is readable in dark and light themes; body text must meet WCAG AA contrast (4.5:1 where applicable; 3:1 for large text). Run the available accessibility checker and inspect the contrast failure from the current screenshot directly.
- No fake metrics, fake testimonials, simulated AI claims, or nonfunctional controls.
- The page remains responsive at all listed widths, with no clipped text, collisions, horizontal overflow, or oversized empty gaps.
- Workspace, exports, recipe replay, privacy, and theme persistence still work.

## Verification and completion report

Run the relevant project checks, including available backend tests, Ruff/lint, frontend tests, browser tests, source-hash verification, production build, and dependency audit. Run `git diff --check`. Do not claim a check passed unless it actually ran. Use Hallmark rendered checks if installed and available; Hallmark is a supplementary gate, not a substitute for actual screenshot review.

Save final screenshots under `docs/visual-qa/` with clear filenames by viewport/theme. Update the project status, decisions, test log, and handoff documents as appropriate. Make a local checkpoint commit containing only this coherent landing-repair work after inspecting the diff and staged files.

In the final report, state:
1. The proven root causes of the previous mismatch and the files changed.
2. The hero and below-fold changes made.
3. Exact final screenshot paths and viewport sizes reviewed.
4. Tests actually run and their results.
5. Any remaining limitations, including whether the approved target image was available and whether the Meta API remains unverified.
6. The local commit hash and current `git status`.

**Do not say “done” based on a successful build, green tests, or a Hallmark score alone. Completion requires the rendered screenshots to pass the visual criteria above.**

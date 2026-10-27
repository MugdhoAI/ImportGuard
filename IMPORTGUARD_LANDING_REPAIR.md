# ImportGuard landing repair — implementation brief

Act as a senior product designer and frontend engineer. Optimize for the rendered result, not the amount of code. Make routine design decisions independently and keep the work focused.

## Objective
Repair **the existing landing page only**. The workspace already works; preserve its CSV pipeline, mapping, validation, exports, recipe replay, privacy page, and persisted theme. Do not rebuild the application.

The target is a premium, editorial, dark ImportGuard landing page: **centered hero + the real animated Predictive Arc + the supplied GlassAiButton + the real AnimatedTopDock**, followed by clear, distinctive product sections. Manus previously achieved a closer composition but used a static image; keep that composition direction and replace the image with the actual animation. If a Manus screenshot/export exists in the project or supplied references, use it as a layout reference only—not as a background asset. Do not rebuild or migrate the Manus project. The last Codex version rendered faint static-looking rings and got the composition/contrast wrong. Diagnose, then fix the real causes.

## Authority and efficient workflow
1. This brief supersedes previous landing-repair prompts, including `IMPORTGUARD_LANDING_REPAIR_PROMPT.md` and `IMPORTGUARD_ANIMATED_LANDING_FIX.md`. Follow this brief only for the landing repair; resolve older conflicting layout advice in its favor. Do not merge conflicting prompt files or spend tokens rereading/reprinting every project document.
2. Read `AGENTS.md` for safety/Git constraints, this project's Hallmark `SKILL.md`, and the supplied Predictive Arc `skill.md`. Inspect only the relevant design tokens, landing components, adapters, and source-verification setup.
3. Inspect `git status` and current route first. Preserve all pre-existing edits. Do not reset, clean, broadly reformat, or touch workspace/business logic.
4. Reuse the already verified component sources and lockfile/dependencies. Do not re-download, reprint, or re-hash giant source bundles if `verify:sources` already verifies them. Do not install a second animation library or create another renderer.
5. Diagnose current render before editing. Then implement and verify the page; do not stop at a plan, checklist, or build passing.

## Non-negotiable: real animated background
Use the verified authored Predictive Arc implementation described in the supplied `skill.md`. Prefer the already-integrated, source-verified package/local renderer that is least disruptive. Follow its exact rendering API/configuration:

```tsx
<PredictiveArcCanvas
  mode="dark"
  speed={1.00}
  hue={0}
  saturation={1.00}
  brightness={1.00}
/>
```

The effect must be a live, animated Canvas/WebGL/Three.js renderer with the authored composition—not a JPG/PNG/WebP, CSS background, a hand-drawn approximation, or two static circles. Do not substitute the unrelated Aegis WebGL sample. Fix integration/root causes rather than replacing the renderer: check import and CSS, initialized variant, parent sizing, canvas backing dimensions, opacity and blend modes, stacking/clipping, opaque overlays, render loop, console/WebGL errors, resize/visibility/reduced-motion lifecycle, and cleanup. Keep the actual scene visible enough to recognize while ensuring text stays readable. In the hero, the animated scene fills the background, behind the content, responsively.

**Proof required:** run the page in a real browser and capture the same hero viewport twice, at least 1.5–2 seconds apart. Compare the scene crop or record the animation live. Confirm visible changes in the authored effect—not merely that a `<canvas>` exists. If motion is subtle or not visible, investigate and fix; do not claim success. Honor `prefers-reduced-motion` and provide a graceful fallback only when required; never describe a still fallback as the requested animation.

## Visual target
### Hero
- Full-bleed near-black scene; dramatic but controlled animated arc composition.
- Center the **entire stack**: headline, supporting text, primary glass CTA, secondary link. Not a left-column hero. Keep it visible at 1280×800.
- Headline: **Make every CSV import predictable.** Use one coherent high-contrast treatment; do not color only the final word.
- Supporting copy: **Map unfamiliar columns, review every transformation, and export validated data without silent changes.**
- Primary CTA: **Start an import**. Use the verified GlassAiButton visual source with the smallest documented ImportGuard adapter needed. It must have a real, keyboard-accessible link/button action to the current workspace; no transparent overlay may hide the glass effect or break focus/clicks.
- Secondary CTA: **See the workflow**, linking to the real section anchor.
- Use the actual AnimatedTopDock source and its motion/controller; adapt navigation labels and actions to ImportGuard, remove all SABLE/demo branding, and keep the dock inside the viewport on mobile. Do not replace it with a static imitation.
- Keep the hero dark in both app themes. Avoid eyebrows, tracked uppercase microcopy, decorative status dots, isolated accent words, fake hero mapping mockups, stock image backgrounds, fake metrics/logos/testimonials, and generic gradient wallpaper.

### Sections below the hero
Design a coherent page, not repeated generic SaaS cards. Use intentional spacing, typography, alignment, and varied composition. Explain the real flow: import a CSV → review/approve mappings → validate rows → export accepted/rejected rows and a reusable recipe. A sample preview must use the actual local fixture/logic and be clearly marked as sample data. Explain human review, deterministic checks, rejection reasons, recipe replay, and local-first processing only to the extent supported by the code. Keep privacy/footer links functional.

Fix the known contrast failure in “Know what changed. Know what didn’t.” Audit all text and controls in both themes. No pale background with near-white text, low-contrast fine print, clipped content, horizontal overflow, or dead controls. Keep layout responsive and preserve existing shared theme persistence.

## Hallmark / anti-slop gate
Use the already installed Hallmark skill and its actual instructions for the redesign/review; do not reinstall it unnecessarily. Apply its relevant anti-slop checks: coherent tokenized palette/type, strong hierarchy, no fabricated proof/metrics, no generic purple-blue wallpaper, no `transition: all`, no layout-property animation, visible focus, reduced-motion handling, and deliberate mobile composition. A clean lint result is supplementary; the rendered page is the source of truth. Correct visual failures rather than adding waivers to hide them.

## Execution and acceptance
1. Record the starting Git status and inspect current landing at the browser. Identify the specific cause of the static/ring-like effect and composition mismatch in a short note at `docs/visual-qa/landing-repair.md`.
2. Fix the hero first. Take and inspect screenshots; iterate until the animation, centered stack, CTA, and dock visibly meet this brief. Then correct every lower section and contrast problem.
3. Browser-review desktop `1440×900`, `1280×800` and mobile `390×844`, `360×800`; also check `1024×768` if the layout changes materially. Review the full page in dark and light themes, the mobile dock/hero, browser console, keyboard focus, and reduced motion. Save screenshots under `docs/visual-qa/`.
4. Verify `Start an import`, `See the workflow`, all dock links, theme persistence, `/app`, and `/privacy`. Run source verification and frontend build/browser checks that already exist. Because backend logic must not change, do not rerun unrelated backend suites unless a shared file was changed. Report commands actually run and their results.
5. Inspect `git diff --check`, the focused diff, and staged paths. Do not stage unrelated user files or secrets. Make one local checkpoint commit for this repair only if the changes are coherent and safe. Never deploy, publish, push, make a remote operation, or call the live Meta API.

## Completion gate
Do not report completion unless:
- [ ] The actual Predictive Arc renderer is running and visibly animated in the browser; evidence is two time-separated hero captures or equivalent direct inspection.
- [ ] The hero has the centered composition, genuine glass CTA with working accessible action, and actual AnimatedTopDock motion.
- [ ] The below-hero sections are visually coherent and readable in both themes, including the known contrast defect.
- [ ] Mobile layouts have no overflow/clipping and all links/actions work.
- [ ] Workspace behavior remains unchanged and verified at the relevant route.
- [ ] Screenshots were actually inspected and source verification/build/browser results are reported truthfully.

Final report: brief root cause; files changed; screenshot paths; source verification status; exact checks/results; remaining limitations; Git status and local commit hash if created. Be concise and evidence-based. A passing build, a present canvas, or a Hallmark score alone is not proof of visual completion.

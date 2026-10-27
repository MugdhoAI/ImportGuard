# Codex Task: Fix the ImportGuard Landing Page — Real Animated Predictive Arc

The workspace is already working. **Fix the landing page only. Do not rebuild the app or touch workspace business logic.** The last attempt passed tests but failed visually. The next attempt is not complete until the actual rendered page has been inspected and approved against the criteria below.

## The critical distinction

The hero background must be a **live, animated Predictive Arc renderer**, not a JPG/PNG/WebP background, not a CSS gradient pretending to be the effect, and not two faint static circular outlines. Manus previously got closer to the desired visual composition but used an image for the background. Keep the good centered, immersive composition and replace the image with the real animation. The current Codex page also got the composition wrong, so correct both composition and animation.

Use the supplied usage as the reference API:

```tsx
import { PredictiveArcCanvas } from "@designcodeio/threeui";
import "@designcodeio/threeui/style.css";

export function Scene() {
  return (
    <div className="shader-frame">
      <PredictiveArcCanvas
        mode="dark"
        speed={1.00}
        hue={0}
        saturation={1.00}
        brightness={1.00}
      />
    </div>
  );
}
```

The supplied `add-predictive-arc` skill says to use the verified authored renderer/source, including its Canvas 2D/raw-WebGL/Three.js renderers and proper lifecycle. First inspect the existing package lockfile, current frontend dependencies, all copied Predictive Arc source files, and their source-hash verification. **Use the already-verified canonical component/source if present.** The existing implementation report says the canonical sources were verified; find out why the running page renders only faint rings and fix the cause. Do not hand-draw a replacement, substitute the Aegis example’s unrelated WebGL lines/halftone, or use a static image. Aegis is only a separate visual/code example, not the Predictive Arc source.

If the `@designcodeio/threeui` package is already installed and supported by the app, use the canonical component and stylesheet. If the project intentionally uses copied verified sources instead, import that local `PredictiveArcCanvas` and its styles. Do not invent a third implementation. Do not edit canonical source files just to hide integration bugs; fix the host, sizing, stacking, initialization, and adapter where possible.

## Required landing-page result

### Hero

- A dark, full-bleed hero with the **actual Predictive Arc animation visibly moving** behind the content.
- Center the entire content stack horizontally: headline, supporting copy, primary CTA, and secondary link. This must not become a left-column hero.
- Headline: **“Make every CSV import predictable.”** Keep the whole heading high contrast and stylistically coherent; do not color only the last word.
- Supporting copy: **“Map unfamiliar columns, review every transformation, and export validated data without silent changes.”**
- Primary CTA: **“Start an import”**, using the supplied verified `GlassAiButton` visual effect. It must actually navigate to the existing workspace through an accessible native link/button. The native interaction layer must not visually obscure the glass effect.
- Secondary CTA: **“See the workflow”**, linked to the real workflow section.
- Use the supplied `AnimatedTopDock` source for navigation, with ImportGuard-specific labels/actions and no SABLE//OS/demo branding. Preserve its actual dock animation; a static nav that merely resembles it is not sufficient.
- At desktop sizes, the headline and CTAs are visible without scrolling at 1280×800. Use an approximately 88–100svh hero where suitable, but prevent mobile overflow.
- No tiny uppercase eyebrow, decorative status dot, fake “illustrative” mapping panel in the hero, fake metrics, or testimonial logos.
- Keep the hero dark even when the global theme is switched to light.

### Animation implementation requirements

Investigate the actual running page before editing. Use DevTools/browser inspection and the code to establish why the current canvas appears as rings. Check the live route, console errors, component import, parent dimensions, canvas backing resolution, `opacity`, `z-index`, clipping/overflow, stacking contexts, theme overlays, GPU/WebGL initialization, animation-frame loop, and reduced-motion logic. Confirm that the renderer is drawing the intended authored scene rather than only a decorative fallback.

The canvas/renderer must:
- occupy the intended full hero background area with responsive sizing;
- visibly change over time while the page is active (not just exist as a `<canvas>` element);
- remain behind legible hero content without being covered by opaque layers;
- handle resize and high-DPI screens;
- pause/reduce motion appropriately when the tab is hidden or `prefers-reduced-motion` is enabled;
- clean up animation frames, listeners, observers, WebGL resources, and event handlers on teardown;
- fail gracefully if WebGL is unavailable, without pretending a static image is the requested animation.

For proof, capture two screenshots of the hero at the same viewport after a meaningful delay and compare the animation area, in addition to visually reviewing it live. If animation is too subtle to be apparent in browser review, the implementation has not passed. Do not use CSS pulsing on top of a static image as a substitute.

### Sections below the hero

Fix the remaining landing sections so they feel coherent with the hero. Use varied, deliberate composition rather than the same generic cards repeated throughout. Explain the real workflow: import a CSV, review each mapping, validate rows, export accepted/rejected rows and a reusable recipe. Any sample or interactive preview must use existing local sample/processing behavior and label synthetic sample data honestly. Explain human review, deterministic validation, rejection reasons, recipe replay, and local-first data control without claiming unverified Meta AI results.

Fix the current severe contrast defect where a pale section has almost-white text. Make all copy readable in dark and light themes. Do not introduce a new collection of unrelated colors, gradient wallpaper, card-inside-card UI, tiny grey text, or excessive uppercase labels. Keep the footer and privacy link functional.

## Resolve instruction conflicts

Inspect `AGENTS.md`, design guides, `design.md`, the reference documents, current components, and the running landing page. Older guidance that favors the old Lumora/light/left-aligned layout or rejects GlassAiButton as the primary CTA is superseded for this task. Do not delete these old references; update the authoritative landing direction so subsequent runs do not revert it. Preserve all unrelated project/security/privacy instructions.

## Execution order (do the work, do not stop at a plan)

1. Inspect `git status`, branch, HEAD, routes, current server/build process, and the existing handoff. Preserve all pre-existing user changes. Do not reset, clean, discard, or overwrite unrelated files.
2. Capture current landing screenshots at 1440×900 and 390×844. Reproduce the actual current state and write root-cause findings to `docs/visual-qa/landing-animation-fix.md` with evidence and responsible files/selectors.
3. Fix the hero first: canonical moving Predictive Arc, centered content, GlassAiButton, AnimatedTopDock. Run the app and inspect the actual browser rendering. Iterate until it meets every hero criterion; do not proceed based only on compile/test results.
4. Fix the below-hero sections and contrast. Inspect the full page in dark and light themes.
5. Run browser tests and existing application checks. Confirm the `/app` workspace and `/privacy` page still function.
6. Save before/after/final screenshots in `docs/visual-qa/` at 1440×900, 1280×800, 1024×768, 768×1024, 430×932 (or nearest supported), 390×844, and 360×800. Review the screenshots, not just capture them. Review both themes and at least two time-separated hero frames to prove the scene is animated.
7. Inspect `git diff --check`, `git diff`, and staged paths. Make a local checkpoint commit only for this coherent landing repair if safe. Do not deploy, publish, push, create remotes, or make live Meta API calls.

## Mandatory pass criteria

Do not report completion unless all are true:

- [ ] The hero is centered and matches the stated composition.
- [ ] The real verified Predictive Arc renderer is running and visibly animated; the background is not a still image or static drawn rings.
- [ ] The glass CTA looks recognizably like the supplied source and navigates to the real workspace accessibly.
- [ ] The actual AnimatedTopDock motion and navigation work.
- [ ] No fake hero mapping card, tiny eyebrow, decorative dot, or single colored heading word remains.
- [ ] Every below-hero section is legible in both themes; fix the current contrast defect.
- [ ] No horizontal overflow, clipped dock, broken mobile hero, console error, or obvious empty space caused by layout bugs.
- [ ] Workspace, CSV operations, exports, recipe replay, privacy page, and persistent theme behavior still work.
- [ ] Screenshots were actually inspected at the requested sizes; tests are reported truthfully.

In the final report list the observed root cause, files changed, screenshots reviewed, actual tests/results, source-hash verification status, remaining limitations, `git status`, and local commit hash if one was made. Distinguish verified animation from a mere canvas element. Do not say “done” just because builds/tests pass or Hallmark reports no failures.

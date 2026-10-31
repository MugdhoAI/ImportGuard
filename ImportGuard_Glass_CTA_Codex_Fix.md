# ImportGuard: Focused Glass CTA Repair for Codex

**Scope: fix only the landing-page “Start an import” button.** Approximately **20% of Codex usage remains**. Do not spend the remaining budget on section animations, hero tuning, refactors, new dependencies, or unrelated cleanup.

## Desired result

The landing page has one cohesive, full-size glass CTA:

- Exact visible label: **Start an import**
- A small, restrained **ImportGuard / IG mark on the left**. Reuse the project's existing logo/mark if available. If no suitable asset exists, use a simple inline SVG mark consistent with the current ImportGuard identity. Do not invent a new brand.
- On the right, keep a small brain-like mark only if it fits the existing ImportGuard style and does not compete with the label. Prefer the existing IG mark as the primary brand cue; remove the unrelated GPT/Astra/Sol mark.
- Preserve the current ThreeUI glass appearance, glow, light movement, shader, and animation behavior. This is a branding/content integration fix, not a new animation.
- The CTA must navigate to the existing ImportGuard workspace (`/app`) and remain keyboard accessible.
- No visible text, logo, accessible label, title, tooltip, or hidden branding may say “GPT 6”, “GPT 6 Astra”, “GPT 6 Sol”, “Astra”, or other unrelated demo branding.

## Why the current result is wrong

The supplied Glass AI Button source is a standalone Three.js/GLSL demo. Its source includes a full-page canvas and a transparent `#activate` button, with the demo name in the document title and accessible label. It is not a ready-made branded ImportGuard CTA with a configurable label prop.

The current integration appears to have placed the demo component inside the app's existing “Start an import” CTA. That produces a small, separate GPT/Astra glass button inside the intended button. Do not fix this by shrinking the demo further, hiding its branding with an overlay, or stacking a second button on top.

## Required workflow — keep it efficient

1. Inspect `AGENTS.md`, the existing Hallmark `SKILL.md`, and the Glass AI Button skill/source notes already in the repository. Read only instructions and files relevant to this button.
2. Inspect the current landing CTA implementation and the supplied source:
   - `references/threeui/glass-ai-button-source.md`
   - `src/shaders/glass-ai-button/GlassAiButton.tsx` and `src/shaders/glass-ai-button/sources/glass-ai-button.html` (or their current project equivalents)
   - The current `LandingPage.tsx` and the CSS used by its primary CTA.
3. Identify the smallest correct integration change. Do not reread giant project documents, regenerate source bundles, reinstall tools, or repeat source hashing if the existing `verify:sources` check already covers them.

## Implementation direction

Make the original glass effect the **visual treatment of the one ImportGuard CTA**, not a miniature standalone demo embedded inside another CTA.

- Keep the original Three.js scene, shader source, rendering loop, animation timing, and light/glass behavior unchanged.
- Adapt only the demo's branding and the component boundary needed for the real CTA.
- Put the label **Start an import** and the ImportGuard mark inside the same visual button surface, aligned neatly and legibly.
- There must be exactly one user-facing CTA and one semantic interactive control. Avoid nested `<button>` elements, competing hit targets, duplicate outlines, or an invisible overlay that blocks keyboard focus.
- The real click/keyboard action must navigate to `/app`. If the animation currently reacts to pointer input, preserve that interaction without letting the embedded demo swallow the navigation click. Keep hover/pointer behavior where technically compatible.
- Keep the CTA compact and aligned with the current hero. Do not use the reference demo's full-page layout dimensions as the CTA dimensions.
- Update the source document title and accessible names to ImportGuard-specific values. Remove GPT/Astra/Sol branding from the actual rendered UI and accessibility tree.
- Keep the original supplied vendor source intact as a reference if project conventions require preserving it. Implement custom behavior in the app-owned adapter/source, and document any intentional modification. Do not claim the canonical vendor source itself has been changed if only an adapter is changed.
- Reuse current design tokens and the existing logo. Do not introduce a new icon library or dependency.
- Preserve focus-visible styling, reduced-motion behavior, and responsive sizing.

### Critical integration check

Before editing, establish which layer currently renders the unwanted small GPT/Astra button. Fix that exact layer. Do not blindly edit only the page's outer text while leaving the embedded demo unchanged.

If the reference source draws the glass surface on a canvas and uses a transparent button only as a hit target, retain the canvas/shader. Add the ImportGuard label and mark as a carefully aligned overlay within the same CTA component, and ensure the app's real `/app` action remains the only navigation action. Do not overlay a fake static pill that hides the glass rendering.

## Acceptance checklist

- [ ] One CTA only; no smaller button trapped inside it.
- [ ] Visible label is exactly `Start an import`.
- [ ] ImportGuard/IG mark appears on the left and matches the current brand.
- [ ] No GPT/Astra/Sol branding remains in visible or accessible UI.
- [ ] Glass/glow/light animation remains recognizably the same as the supplied reference.
- [ ] CTA opens `/app` by mouse and keyboard.
- [ ] Focus-visible state works; reduced-motion preferences are respected.
- [ ] No unrelated files or product behavior changed.
- [ ] Frontend production build passes.
- [ ] Run existing targeted source verification only if relevant and already configured; do not spend time setting up new test infrastructure.
- [ ] Review the final diff and report the exact files changed and checks actually run.

## Strict usage budget

Approximately 20% of Codex usage remains. Work in this order:

1. Inspect only the CTA, source adapter, relevant CSS, and relevant skill instructions.
2. Implement the minimal repair.
3. Run the frontend build.
4. Inspect the CTA in the browser if it can be done immediately with the existing setup.
5. Report completion and any remaining limitation.

**Stop after the CTA is fixed and verified.** Do not work on the slow hero animation, lower-page motion, other visual polish, documentation expansion, or unrelated bugs. Do not deploy, publish, push, commit, or spend money. Do not replace a correct visual integration with a fake approximation merely to finish quickly.

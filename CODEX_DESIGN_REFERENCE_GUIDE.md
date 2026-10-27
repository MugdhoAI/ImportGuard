# ImportGuard — Codex Design and Reference Guide

**Purpose:** Build an attractive, polished landing page and a genuinely functional CSV-import workspace without allowing visual effects to delay the product.

**Read first:** `AGENTS.md` and `CODEX_EXECUTION_PLAN.md`. This file supplements those instructions. If instructions conflict, preserve the essential product requirements and data-safety rules in the execution plan. Do not replace working backend logic merely to add a visual effect.

## 1. Product and success criteria

ImportGuard helps a user map an unfamiliar CSV into a target schema, review proposed transformations, validate rows, and download the results.

The application must ultimately support this real workflow:

1. Upload a CSV.
2. Inspect columns and sample values.
3. Choose or define the target schema.
4. Propose source-to-target mappings (Meta Muse Spark when API access is enabled; manual mapping must still work).
5. Review and approve mappings and any transformations.
6. Validate and process the original data deterministically.
7. Download accepted rows, rejected rows with useful reasons, and a reusable mapping recipe.
8. Replay a saved, approved recipe without another model call.

**Priority order:** data integrity and functional processing → clear workspace UX → responsive landing page → subtle interaction polish → optional advanced visual effects.

Do not call the project complete because the landing page looks good. End-to-end CSV processing, downloads, tests, and honest reporting of Meta API status are mandatory.

## 2. Design references supplied by the owner

Use the references for visual direction and investigate the exact source only when an effect is selected. Do not try to combine every reference in one page.

### Primary reference: Lumora layout and motion brief

- GetLayers template: https://www.getlayers.ai/templates?layer=lumora
- Owner-supplied detailed reconstruction prompt: the user provided a long Lumora specification in this conversation. It describes a refined light palette, Onest typography, large editorial headings, warm burnt-orange accent, rounded surfaces, responsive section layout, scroll reveals, and a cursor-revealed hero image.
- Image asset base in the supplied prompt: `https://api.getlayers.ai/storage/v1/object/public/public/assets/lumora-e8b711fc68`

**Use as the primary visual reference, not as a literal copy of the Lumora agency website.** Build ImportGuard's own content and product visual. The references' agency copy, client names, portfolio items and statistics are not facts about ImportGuard and must not be reused as claims.

Visual tokens to adapt:

```css
:root {
  --background: #ffffff;
  --foreground: #111111;
  --ink: #0a0a0a;
  --muted: #8d8d8d;
  --line: #e6e5e2;
  --surface: #f1f0ee;
  --surface-2: #e3e2df;
  --accent: #b15f2c;
  --accent-light: #cf8047;
  --accent-dark: #97501f;
  --radius-pill: 9999px;
  --radius-card: 2rem;
  --radius-control: 0.875rem;
}
```

Use Onest if loaded successfully, with a system sans-serif fallback. Do not make the app unusable when a remote font or image is unavailable.

### Reference: Kage full landing page

- Preview: https://threeui.com/landing-pages/kage-landing-page
- Canonical HTML: https://threeui.com/landing-pages/kage.html
- Source bundle: https://threeui.com/source-code/kage-landing-page.json
- Supplied source revision: `c8e06b90397a`
- Supplied full HTML SHA-256: `c8e06b90397ac246baf0ab6f32f5f6b570acc6fe03c7009f711b579fb72d9f49`
- Runtime: full HTML + DOM/CSS + local Three.js; the experience is a full-page Japanese temple environment with navigation and scroll scenes.

**Decision for ImportGuard:** do not embed the complete Kage page as the product's main landing page. Its temple narrative, full-page interactions, and large asset set do not match a CSV data tool. It may be inspected for craft, animation timing, transitions, and interaction quality. Only integrate its actual component if a clear, product-relevant use is demonstrated and source/license checks pass; otherwise leave it out.

The owner's supplied Kage instructions list these paths:
- `src/shaders/landing-pages/LandingPages.tsx` — SHA-256 `4d379461ad00eb4de7900df312878035383de7e1ed4e13283b8143a2eea9d30a`
- `src/shaders/landing-pages/pageTypography.ts` — SHA-256 `809cc65797d531cd3b3ca5a56815d55d24b3ee8d293e4e4bad6fdfe6c83244cc`
- `src/shaders/landing-pages/pageRecipes.ts` — SHA-256 `c9d9849cc255bac2d1d938d088c50917f84916f1c516d2bbb27fcfd803523233`
- `src/shaders/landing-pages/LandingPageFrame.tsx` — SHA-256 `61de2cc50888aac4ac5557420b07fa47ed3543bb57c1e0055fafdefa53dbaa78`
- `src/shaders/threeui.css` — SHA-256 `efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf`
- The supplied brief describes local `kage.html`, fonts, `three.min.js`, WebP layers, and MP3 files. Fetch the full source manifest and reconcile it with the supplied list before copying anything; do not assume the abbreviated asset list is complete.

### Reference: Sylva hero

- Preview: https://threeui.com/hero/sylva
- Canonical HTML: https://threeui.com/landing-pages/inner-green-3d.html
- Source bundle: https://threeui.com/source-code/sylva-hero.json
- Variant in supplied instructions: `living-green`
- Supplied source revision: `05f359ce157a`
- Supplied canonical HTML SHA-256: `69c3694bd63f44ef9f007ebe4dac57a83e4402e0cdf6b54dd10b96dd4f05e197`
- Runtime: full HTML + DOM/CSS + local Three.js; moss, plants, pollen, butterfly, and liquid-metal controls.

**Decision for ImportGuard:** treat Sylva as a motion/rendering reference, not the default hero. The nature scene is unrelated to the product and may distract from the data-import workflow. Do not add it merely because it is visually impressive.

Supplied source details:
- `src/shaders/landing-pages/LandingPages.tsx` — SHA-256 `4d379461ad00eb4de7900df312878035383de7e1ed4e13283b8143a2eea9d30a`
- `src/shaders/landing-pages/pageTypography.ts` — SHA-256 `809cc65797d531cd3b3ca5a56815d55d24b3ee8d293e4e4bad6fdfe6c83244cc`
- `src/shaders/landing-pages/pageRecipes.ts` — SHA-256 `c9d9849cc255bac2d1d938d088c50917f84916f1c516d2bbb27fcfd803523233`
- `src/shaders/landing-pages/LandingPageFrame.tsx` — SHA-256 `61de2cc50888aac4ac5557420b07fa47ed3543bb57c1e0055fafdefa53dbaa78`
- `src/shaders/threeui.css` — SHA-256 `efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf`
- `public/landing-pages/inner-green-3d.html` — supplied SHA-256 above
- `public/landing-pages/inner-green-assets/three.min.js` — SHA-256 `8a5f7249903b54d30f79f708699d2fed2d6a1d0741a4cd41377d1f01bb5a2271`
- Binary assets named in the supplied prompt: `card-ecostove.jpg` SHA-256 `70ce084084902bc502f00c366405b661ecdff90dee95d363b36a6e146829e433`; `card-ethos.jpg` SHA-256 `337627390f499b3ae272cec9e2f83c817694a82f42e1aa10a7b26a2c7d679dff`; `lexend-latin.woff2` SHA-256 `1ec8f6ee2750554b4bc59ff0b507d316a82a7ba37e0e5bebc41d3bd9b9faad46`.

### Reference: Glass AI Button

- Preview: https://threeui.com/buttons/glass-ai-button
- Source bundle: https://threeui.com/source-code/glass-ai-button.json
- Source revision: `a484571de316`
- Canonical HTML SHA-256: `a484571de316c05ab7fbd2da82da5e028ee1ffe0bd169449fb8a3c7801abd81e`
- Source file `src/shaders/glass-ai-button/GlassAiButton.tsx` — SHA-256 `1a11cd583e856d3be328a0192be4d77184607c64721f3fb646bd6d61436b2104`
- Shared CSS: `src/shaders/threeui.css` — SHA-256 `efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf`
- Runtime: embedded Three.js r170 + custom GLSL + DOM/CSS, galaxy orb, particle burst, and authored lettering `GPT 6 Sol`.

**Decision for ImportGuard:** do not use this button as a main CTA. Its built-in AI branding is unrelated and could misrepresent the project's model. Use a native accessible button with a restrained hover/press effect. The source may be inspected for interaction quality only.

### Reference: Animated Top Dock

- Preview: https://threeui.com/css/animated-top-dock
- Source bundle: https://threeui.com/source-code/animated-top-dock.json
- Source revision: `5a736cd3c1f6f19802f61ebb10e1701b9f7aa26e`
- `AnimatedTopDock.tsx` — SHA-256 `50ddbba7ebc81565f42bd14dda34efb45e7b18c1aa47e97f196256ffedb4478f`
- `topDockController.ts` — SHA-256 `506ab23d4d42cf1b5bc89131e7714586ee107381bb18d9b0302766e9a1dee2bd`
- `retroPixelField.ts` — SHA-256 `54f0469be51dfce2da7ce37c952d42c583cc7996794bf96d1ea0b2bb35d94115`
- `glassParticleField.ts` — SHA-256 `bc9f07ae6da33b28f82303ea937095806f8e3a2ab08bd1301ae8457aaf0c3464`
- Shared CSS: `src/shaders/threeui.css` — SHA-256 `efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf`
- Font `src/shaders/fonts/fragment-mono.woff2` — SHA-256 `4f4dc27f4a770c0d02fde800daa836c8adc0d1e423b28da74baaf0d1cc3ab96c`
- Runtime: DOM + CSS + WebGL + Three.js r128. Variants include Sable dock, modern command bar, pixel terminal, and liquid glass rail.

**Decision for ImportGuard:** this is the most relevant ThreeUI reference for navigation behavior, but do not integrate the exact component unless its menu contents can be configured cleanly for ImportGuard and its additional runtime is justified. Do not leave irrelevant fixed menu labels in the product. If adapting requires rewriting its source or adding disproportionate complexity, build a simple accessible navigation using CSS transitions instead.

## 3. Product-specific visual direction

Build ImportGuard as a calm, precise developer tool. The visual design should signal trust, clarity, and control over data—not a generic AI chatbot.

### Landing page

Use the Lumora reference's hierarchy and restraint, adapted to ImportGuard:

- Top navigation with the ImportGuard wordmark, `How it works`, `Features`, and a clear `Open workspace` CTA.
- Hero headline: **“Make every CSV import predictable.”**
- Supporting text: **“Map unfamiliar columns, review every transformation, and export validated data without silent changes.”**
- Primary CTA: `Open workspace`; secondary CTA: `See how it works`.
- A product-specific hero visual: a real-looking CSV preview flowing into mapped target columns, with one highlighted ambiguous value awaiting review. Label it `Example data` or `Illustrative preview` if it is not generated by the running app.
- A concise three-step explanation: `Map → Review → Export`.
- Feature section covering explicit approval, row-level validation, rejected-row explanations, and recipe replay.
- A final CTA that opens the functional workspace.
- Small footer with project name and useful links. No fake company address, fabricated testimonials, fake client logos, or invented statistics.

Do not reproduce the fictional Lumora studio, its “200+ brands shipped” line, invented partner names, fake metrics, unrelated portfolio cards, contact-request modal, or nature/temple imagery as ImportGuard facts.

### Workspace

The workspace is the main product and should be easier to use than the landing page is to admire.

- Clear step/progress indicators: `1. Source`, `2. Map`, `3. Review`, `4. Export`.
- Drag/drop and browse-file upload, with keyboard-accessible fallback.
- Show filename, row/column count, and validation or parsing errors.
- Display source columns, sample values, target columns, confidence/uncertainty only if the underlying model response supports it, and explicit review controls.
- Visibly distinguish proposed mappings, user-approved mappings, and blocked ambiguities.
- Provide a before/after preview and row-level validation messages.
- Show accepted and rejected counts based on actual processing, not hardcoded demo metrics.
- Download working accepted CSV, rejected CSV with reasons, JSON recipe, and validation summary.
- Include a clear reset/new-file action and useful empty, loading, success, and error states.

Use realistic synthetic example data for screenshots and development, but clearly label it. Do not upload user files to external services except through the explicit, documented Meta API path when enabled.

## 4. Interactive hero: preferred approach

The best interaction for ImportGuard is a product-specific data animation, not a giant unrelated 3D scene.

Preferred implementation:

- Render a compact example table with a handful of source columns.
- Animate mapping lines or chips from source headers to target schema fields.
- Let a user hover or click an example ambiguous field to reveal a small explanation panel.
- Use slow, subtle entry/reveal animations and restrained parallax only if it remains accessible and performant.
- Keep the hero visual illustrative unless it is driven by the actual application pipeline; never portray a canned animation as live AI output.
- On touch devices and under `prefers-reduced-motion: reduce`, keep a stable static visualization.

Do not make a full-screen loader block the user from reaching the app. No effect may prevent core UI interactions.

## 5. Technical integration rules

The current project plan favors FastAPI and a simple frontend. Keep this approach unless the existing code proves a change is necessary.

- Do not introduce React, Vite, Next.js, Tailwind, a component library, Three.js, an iframe host, or a bundler solely to reproduce a reference.
- First inspect the current repository and the implementation plan. Reuse its agreed stack.
- Use a maintainable template and static asset structure (for example FastAPI templates plus CSS/JS) if that is what the execution plan specifies.
- Keep CSS and JS organized in files rather than pasting a huge single-page agency implementation into the backend.
- External fonts/images are progressive enhancements only. Provide local/system fallbacks.
- Do not introduce remote tracking scripts, analytics, third-party form submission, or any live network dependency unrelated to the product.
- All navigation, upload buttons, mapping controls, exports, and modals must actually work. No decorative controls that imply nonexistent functionality.

## 6. Source retrieval, fidelity, and license guardrails

The source bundle URLs and hashes above are supplied by the owner. They are not proof of an unrestricted license.

If you decide to integrate any exact ThreeUI component:

1. Fetch and read the complete source bundle and all referenced files first.
2. Inspect the current license/terms and any attribution obligations before copying source/assets into the repository or distributing them publicly.
3. Verify supplied SHA-256 hashes against the fetched bytes (PowerShell: `Get-FileHash <path> -Algorithm SHA256`). Do not claim a match if not checked.
4. Copy required assets byte-for-byte with their expected relative paths. Reconcile source-manifest paths with the skill notes; if a required asset is missing, do not approximate it.
5. Do not embed the vendor documentation site itself.
6. Do not recreate an exact-source component from a screenshot if source retrieval fails. Report the blocker and continue with the product's native interface instead.
7. Isolate optional effects so they can be removed without breaking ImportGuard.
8. Test desktop, mobile, keyboard navigation, reduced motion, resize, and console errors.

Never represent a copied third-party component as original work. Preserve license/attribution notices required by the terms.

## 7. Motion, accessibility, and performance

- Honor `prefers-reduced-motion: reduce`.
- All controls must have semantic HTML, visible focus, labels, and keyboard behavior.
- Do not convey state through color alone.
- Avoid cursor-only controls; touch/mobile must remain fully usable.
- Avoid continuous heavy animation when the tab is hidden; clean up animation frames, listeners, observers, and WebGL resources if a WebGL component is ever added.
- Target quick initial rendering. Do not delay the real workspace behind an elaborate intro animation.
- Ensure mobile layouts do not overflow horizontally.
- Handle missing fonts/images without breaking layout.

## 8. Required validation before calling the design complete

- [ ] Landing page reflects ImportGuard, not Lumora's fictional studio.
- [ ] `Open workspace` navigates to the real workspace.
- [ ] Workspace can process an actual CSV end-to-end.
- [ ] Mapping, approval, validation, exports, and recipe replay are functional.
- [ ] All visible controls work and have loading/empty/error states.
- [ ] No fake AI response is represented as a real API result.
- [ ] Responsive at narrow/mobile, tablet, and desktop widths.
- [ ] Keyboard focus and reduced-motion behavior verified.
- [ ] Browser console checked for errors and failed assets.
- [ ] Core tests pass.
- [ ] Optional third-party component source and rights checked if used.
- [ ] README explains local run steps and the true Meta API integration status.

## 9. Execution instruction to Codex

Do the work in this order:

1. Read `AGENTS.md`, `CODEX_EXECUTION_PLAN.md`, and this guide.
2. Inspect the existing app and report the current state briefly in the terminal before editing.
3. Implement and test the complete functional workspace first.
4. Build the product-specific landing page using the visual direction above.
5. Add only small interactions that directly improve clarity or polish.
6. Consider ThreeUI source components only after the core workflow and tests pass; choose at most one, and only if source and rights can be verified and it fits ImportGuard.
7. Run the full test suite and exercise the actual app in a browser if the available tools permit.
8. Report completed functionality, exact tests run/results, any unavailable browser/source/license verification, and the exact local start command.

Do not wait for approval on routine implementation decisions. Do not deploy, publish, spend money, or expose credentials without explicit approval. Do not claim any untested outcome as verified.

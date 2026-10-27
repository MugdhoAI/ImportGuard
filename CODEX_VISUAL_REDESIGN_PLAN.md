# ImportGuard Visual Redesign Plan — Current Source of Truth

**Purpose:** Redesign the existing ImportGuard UI so it feels deliberately art-directed, product-specific, interactive, and professionally finished. Preserve the working CSV application. Do not restart the project or replace working product logic.

**This plan supersedes conflicting older visual notes** that favor a light Lumora-style hero, a static illustrative card, Kage/Sylva imagery, or other earlier directions. The selected direction for this iteration is the Predictive Arc background + Sable Dock navigation + a branded GlassAiButton CTA, reviewed through Hallmark.

## 1. Diagnosis of the current screenshot

The current page at `http://127.0.0.1:8000/` is functional as a starting point, but it reads as a generic AI-generated landing-page template:

- A small uppercase eyebrow with a decorative status dot.
- A headline with only one word colored as an accent.
- A large empty two-column hero with a static product mockup marked “Illustrative example”.
- Small, heavily tracked uppercase labels and status dots.
- A bright, restrained marketing palette that does not use the requested dark, animated visual.
- No dark/light theme control.
- The hero mockup is not proof that the actual workflow works.

Do not defend or lightly polish this exact composition. Preserve the product's copy and working links, then redesign its visual system and composition.

## 2. Mandatory reference and skill workflow

### Hallmark anti-slop design skill

Hallmark is the primary design skill for this redesign:
- Repository: https://github.com/Nutlope/hallmark
- License: MIT (verify current repository license when installing)
- Install project-locally from the `C:\ImportGuard` directory:
  ```powershell
  npx skills add nutlope/hallmark --agent codex
  ```
- If the installer says the skill was installed but Codex does not recognize `$hallmark`, read the installed `SKILL.md` and invoke its procedure directly; restart Codex if needed to load metadata.
- This is a redesign of an existing site, so use the Hallmark **redesign** path (not a fresh build): capture/record existing links, forms, headings and handlers first; preserve the wiring; build the hero first; then the rest; run Hallmark `sloplint` on rendered output.
- The skill's documented rendered lint requires Node 18+, Puppeteer Core and Chrome. Check the environment first. If rendered lint cannot run, say so explicitly and still run available static checks and real-browser/manual QA. Do not claim rendered lint passed without running it.

Hallmark sources:
- https://github.com/Nutlope/hallmark
- https://github.com/Nutlope/hallmark/blob/main/skills/hallmark/SKILL.md

### Relevant Codex skill catalog

The repository https://github.com/composio-community/awesome-codex-skills is a catalogue, not a single design skill. Do not install the whole catalogue. Its `webapp-testing` skill can help with Playwright-based browser checks:
- https://github.com/composio-community/awesome-codex-skills/tree/master/webapp-testing

Use it only if its documented install path and license are verified. Hallmark is the design gate; browser testing is the behavioral gate.

## 3. Intended final result

### Page hierarchy

1. A full-height, near-black hero with the Predictive Arc canvas as the actual background.
2. A floating Sable-style animated glass dock near the top, with ImportGuard-specific navigation.
3. Centered hero content over the background:
   - Headline: **“Make every CSV import predictable.”**
   - Supporting copy: **“Map unfamiliar columns, review every transformation, and export validated data without silent changes.”**
   - Primary CTA: **“Start an import”**, rendered using the supplied GlassAiButton visual effect but wired to the real workspace.
   - Secondary text link: **“See how it works”**.
4. A product workflow section below the hero that demonstrates the real application. It must use the existing real workspace or a clearly labeled sample fixture connected to the actual processing pipeline. Remove the fake “Illustrative example” card.
5. A small number of purposeful sections explaining review-before-processing, deterministic validation, rejected-row explanations and recipe replay. Compose these editorially; do not make every section a repeated 3-card grid.
6. A restrained footer with real navigation and the privacy link.

The hero must show its headline, supporting sentence and primary action without scrolling at 1280×800. The visual scene must support the product rather than make the text hard to read.

### Dark/light mode

- Dark theme is the default because the selected Predictive Arc is explicitly configured with `mode="dark"`.
- Add an accessible theme toggle that changes the rest of the landing page and workspace between dark and light themes.
- Persist the chosen theme in `localStorage`.
- Keep the Predictive Arc hero section dark in both themes as an intentional, consistent brand scene; do not invert or recolor its source unexpectedly.
- Define all colors in CSS custom properties. Do not scatter hard-coded colors throughout component styles.
- The violet/purple arc is the one expressive visual accent. Use restrained neutral surfaces and text. Reserve green/red/amber for actual validation states. Retire the old burnt-orange accent unless the implementation proves a specific contrast/state need.
- No purple-to-blue gradient background added on top of the effect. Do not add multiple competing glow gradients, floating orb decorations or noisy glass cards.

Suggested design tokens (adapt after inspecting the exact source effect, but lock them in one `design.md` and token file):
```css
:root {
  color-scheme: dark;
  --bg: #08090e;
  --bg-raised: #10121a;
  --surface: #141722;
  --surface-hover: #1b2030;
  --text: #f3f2f8;
  --muted: #a3a7b7;
  --subtle: #777d91;
  --line: #292d3a;
  --accent: #a78bfa;
  --accent-strong: #c4b5fd;
  --success: #8bc9a3;
  --warning: #edc58b;
  --danger: #f09a9a;
  --radius-sm: 0.75rem;
  --radius-md: 1.1rem;
  --radius-lg: 1.6rem;
}
[data-theme="light"] {
  color-scheme: light;
  --bg: #f4f3ef;
  --bg-raised: #ffffff;
  --surface: #ffffff;
  --surface-hover: #eeedf4;
  --text: #17171d;
  --muted: #5c6070;
  --subtle: #73788a;
  --line: #dfdfe7;
  --accent: #6d4dd2;
  --accent-strong: #5a3eb5;
}
```
The hero remains near-black regardless of the global theme. Ensure status colors meet contrast requirements in both themes.

## 4. Required component usage and integration rules

### A. PredictiveArcCanvas — hero background

Reference page: https://threeui.com/hero/predictive-arc  
Canonical source bundle: https://threeui.com/source-code/predictive-arc.json

Required component and configuration from the owner's brief:
```tsx
<PredictiveArcCanvas
  mode="dark"
  speed={1.00}
  hue={0}
  saturation={1.00}
  brightness={1.00}
/>
```
Use `variant="predictive"` if the collection component requires it.

**Important source availability note:** the current local reference set contains the owner-provided component specification and file hashes, but not the complete `predictive-arc.json` source bundle. The attached `aegis-remixed-bento-reference.html` is a different security-themed demo and is NOT the Predictive Arc component source. Do not use it as a substitute.

Before implementing:
1. Fetch the canonical JSON bundle from the URL above from the local development environment.
2. Read all listed component, renderer and CSS files.
3. Verify SHA-256 hashes against the owner's supplied manifest.
4. Keep the downloaded canonical source under `references/threeui/original/` (or document the local source location) and record license/attribution.
5. If the bundle cannot be fetched, the source is incomplete, a hash does not match, or the source license/terms do not permit the intended use, stop this specific integration and report the precise blocker. Do not approximate this effect and claim it is exact.

Render it as a true behind-content background: full bleed, absolute/inset 0, clipped to the hero, behind the text/dock, with a subtle solid/transparent readability layer if needed. It must not intercept pointer events that should reach the nav/CTA. Use the source's own lifecycle; stop animation when offscreen/hidden; handle resize, reduced motion, mobile and WebGL failure with a non-animated fallback. Do not run duplicate animation loops.

### B. AnimatedTopDock — floating navigation

Reference: https://threeui.com/css/animated-top-dock  
Canonical bundle: https://threeui.com/source-code/animated-top-dock.json  
Owner-provided source reference: `references/threeui/animated-top-dock-source.md`

Use the **Sable** variant with the supplied defaults:
```tsx
<AnimatedTopDock
  variant="sable"
  proximity={122}
  spring={0.19}
  damping={0.70}
  widthGrowth={17}
  heightGrowth={16}
  drop={3.5}
/>
```
Required source font:
`src/shaders/fonts/fragment-mono.woff2`
SHA-256: `4f4dc27f4a770c0d02fde800daa836c8adc0d1e423b28da74baaf0d1cc3ab96c`

The text source is attached, but the binary font is not embedded. Retrieve the font from the authorized ThreeUI package/source and verify the hash. Do not use a substitute font while claiming exact source fidelity.

Integration:
- Preserve the signature spring/proximity behavior.
- Keep original vendor source unchanged as a canonical reference.
- Create a separately named ImportGuard adapter/fork if labels or actions must change. Record any branding changes; do not pretend the adapted file has the original source hash.
- Rebrand the default labels into concise, human-readable ImportGuard navigation, for example Home, How it works, Import, Privacy, and Help/Guide. Avoid all-caps tracked labels to satisfy the design skill.
- Each item must actually navigate to a real section/route. Do not ship controls that only change selected state.
- Keep the dock usable with keyboard focus and a simpler accessible mobile fallback if the dock overflows or becomes hard to use.
- Add a separate theme toggle if necessary; do not fake one inside the dock.

### C. GlassAiButton — primary import CTA effect

Reference: https://threeui.com/buttons/glass-ai-button  
Canonical bundle: https://threeui.com/source-code/glass-ai-button.json  
Owner-provided source reference: `references/threeui/glass-ai-button-source.md`

The supplied source includes a visible canvas label `GPT 6 Sol` and an accessible label for activating the galaxy. This is brand-specific and would be incoherent as an ImportGuard CTA if left unchanged.

Use the actual supplied renderer/effect as the CTA's visual treatment, but make a minimal, documented ImportGuard adapter:
- Preserve the original source file unchanged in the references/vendor-original location.
- In the application-specific copy only, change the rendered label to `CSV IMPORT` (or another short ImportGuard-appropriate label that fits) and update the accessible name to `Start an import`.
- Wire activation to the real `/app` workspace or the existing start-import flow. Add a minimal, validated `postMessage` bridge if it is hosted in a sandboxed iframe; the parent must check `event.source` equals the expected iframe and allow only a known message type. Never send data or secrets through this message.
- Preserve shader, geometry, motion, interaction and lifecycle behavior. Do not blindly paste the original component and call it functional if the click only animates a demo.
- Make the CTA a real keyboard-accessible button with a visible focus state, accessible text, busy/failure behavior where applicable and a usable fallback if WebGL is unavailable.
- If the source license/terms do not permit this adaptation, do not publish it; report the issue rather than assuming permission.

Original source hash for the canonical HTML:
`a484571de316c05ab7fbd2da82da5e028ee1ffe0bd169449fb8a3c7801abd81e`

### D. Frontend architecture

The current app uses FastAPI and server-rendered HTML. The specified ThreeUI React/TypeScript components may require a small Vite + React + TypeScript frontend. That is now an authorized, narrowly scoped exception to the old “no React unless needed” rule because these exact components are authored as React components.

If a frontend build is necessary:
- Keep FastAPI as the backend and preserve its existing endpoints and CSV services.
- Use one minimal Vite frontend bundle; have FastAPI serve the built static files for the single-app run path.
- Add the smallest number of dependencies required by the supplied source.
- Do not add Next.js, Supabase, authentication, databases, microservices, analytics or a separate hosted service.
- Never put the Meta API key in frontend code or send it to the browser.
- Keep a simple, documented local run/build path.

If exact integration can be done with the existing stack without weakening the source or functionality, prefer the simpler option. Do not migrate the backend.

## 5. Anti-slop rules — enforce, do not merely mention

Use Hallmark's Floor and rendered `sloplint` as a hard gate. Specifically:
- No tiny uppercase eyebrow line above the hero headline.
- No single word colored differently inside an otherwise uniform headline.
- No decorative green/orange status dots.
- No tracked-uppercase labels, all-caps nav or fake terminal/status meta.
- No fake testimonials, client/partner logos, numbers, metrics, customer counts or claims.
- No static “illustrative UI” presented as product evidence.
- No generic procession of identical cards; each section needs a job and a different composition.
- No random emoji icons, noisy glow piles, needless nested cards or empty visual containers.
- No every-section animation. Animate the arc and essential nav/CTA effects; make content and data readability primary.
- Do not insert another email sign-up/contact modal into a product that needs users to start an import.
- No invented “local processing” claims. Copy must match the actual app and Meta data flow.
- The page's first screen must show the true headline, one-sentence value proposition and actual start-import action at 1280×800.
- Define design tokens for all colors, fonts, shadows, spacing and motion. Avoid `transition: all`, layout-animation properties, low contrast, horizontal overflow and inaccessible focus states.
- Respect `prefers-reduced-motion`; meaningful content remains visible if animation/script fails.

The user's supplied Lumora brief, Kage, Sylva and Aegis sample are now secondary/older references and must not be mixed with the chosen arc + dock + glass-button system. Do not use their unrelated marketing copy, fake portfolio items, people/brands, metrics, images or other product identities.

## 6. Keep the app functional

Do not replace the working local CSV workflow with a visual demo. Preserve and regression-test:
- `/health`, `/`, `/app`, `/privacy`, and the current example/demo routes.
- CSV upload bounds, profiling, schema editing, mapping review, deterministic validation, accepted/rejected downloads, report export and recipe replay.
- Manual/local mapping when Meta is disabled.
- Meta mapping is disabled by default. No real API call unless `ALLOW_META_API_CALLS=true` is explicitly set by the owner.
- Keyboard access, visible focus, theme toggle and real navigation.
- Helpful error states, loading state, empty state and a working WebGL fallback.

The homepage's live/sample preview, if included, must use a real fixture and honest labels. A click on “Try a sample import” must load or process the actual sample workflow; it cannot be a fake interaction.

## 7. Execution order

1. Inspect Git status/history, current routes and frontend architecture. Read current project status/handoff first. Preserve working code.
2. Install or locate Hallmark; inspect its `SKILL.md`. Record baseline captures and links/forms/handlers using the Hallmark redesign procedure.
3. Fetch and verify Predictive Arc source/licensing. If unavailable, record a source blocker and do not fake the exact background.
4. Build **the hero alone first**: actual arc background, intended text, real CTA, accessible top dock and theme toggle. Do not build the rest of the new marketing sections until the hero is screenshot-reviewed.
5. Run the site locally and capture screenshots at desktop, tablet and mobile sizes. Review the screenshot critically against this plan.
6. Fix the hero until both the visual composition and controls are correct. Get a fresh-context review where possible.
7. Redesign the below-the-fold landing page and workspace shell without reimplementing business logic.
8. Run rendered Hallmark `sloplint --stage hero --render` for the hero, then the page/app. Fix every Floor `FAIL`; fix Reflex results or record a genuine reason for each waiver.
9. Run end-to-end browser tests (Playwright or equivalent), including upload → mapping review → processing → results/downloads → recipe replay; verify theme toggle, nav, CTA, resize, keyboard and console errors.
10. Run all backend tests and lint, inspect `git diff`, confirm no secrets/private data are staged, update status/test/handoff logs and create a local checkpoint commit.

## 8. Required acceptance criteria

The redesign is not done until all applicable items pass:
- [ ] Hero uses the verified PredictiveArc source, not a hand-drawn approximation or the Aegis reference.
- [ ] Headline copy is exactly “Make every CSV import predictable.” with an informative supporting sentence.
- [ ] No eyebrow, no single orange/purple word in the headline, no decorative status dots, no fake metrics or “Illustrative example” product panel.
- [ ] `Start an import` is a real, accessible action opening the functional workspace.
- [ ] AnimatedTopDock uses the Sable motion and every navigation item works.
- [ ] The glass effect's visible label and accessible name match ImportGuard; the canonical source remains preserved and any adapter divergence is documented.
- [ ] Dark theme is default; light theme toggle works and persists, while the selected hero scene remains intentionally dark.
- [ ] At 1280×800, the headline, supporting copy and primary action are visible without scrolling.
- [ ] Layout works at 1920, 1440, 1280, 1024, 768, 430, 390 and 360 CSS-pixel widths without horizontal overflow.
- [ ] Reduced-motion, keyboard focus, mobile and WebGL failure fallbacks work.
- [ ] Existing functional routes and CSV workflows still work.
- [ ] Hallmark rendered lint is run or the exact blocker is reported. No false claims of lint/browser verification.
- [ ] Automated tests pass; current Git and session handoff records are updated.
- [ ] A before/after screenshot comparison and concise test evidence are saved under `docs/visual-qa/`.

## 9. Final report

Report only facts:
1. What changed visually and functionally.
2. Source files used, hash check and licensing status.
3. Screenshots/viewports tested and the actual Hallmark lint output.
4. Browser/end-to-end tests, backend tests and lint results.
5. Any remaining source/licensing/API blockers.
6. Git commit and working-tree state.
7. Local run command.

Do not stop at “design improved”; the rendered screenshots and successful actions are the evidence.

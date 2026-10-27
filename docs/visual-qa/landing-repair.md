# Landing repair notes

## Diagnosis

- The verified Predictive Arc source is an animated 2D canvas renderer (`createPredictiveArcRenderer`), not a WebGL renderer. The React adapter sizes its canvas to the full hero and runs a requestAnimationFrame loop; this was intact. The `hero-shade` overlay then painted another 42% dark layer over its opaque canvas, flattening the authored dotted arch into faint ring-like bands. No console errors occurred.
- `.mobile-nav` was still rendered alongside the real AnimatedTopDock. At desktop it entered the hero grid and displaced the stack; at mobile it appeared as a duplicate line of links above the hero. The dock's label override also targeted nonexistent `[data-nav-label]`, leaving the source's tracked mono styling.
- The dock's full-width fixed mount had pointer events over the header. The theme control looked exposed but could not receive clicks.
- The displayed support sentence and secondary action differed from the supplied brief.

## Repair and browser evidence

- Reduced only the separate hero wash to 14%, preserving the verified renderer's requested `mode="dark"`, `speed=1`, `hue=0`, `saturation=1`, and `brightness=1`. Added tokenized text shadow for contrast.
- Removed the duplicate static navigation and repositioned the real spring-controlled Sable dock to the mobile bottom edge. Corrected its label type override and limited pointer hit testing to its actual nav.
- Restored the exact requested support sentence and “See the workflow” action. Tightened lower-section copy while keeping the sample tied to the real synthetic fixture and API flow.
- Before screenshots: `landing-repair-before-1280-a.png` and `landing-repair-before-1280-b.png`. The 2-second canvas crop comparison found 59,345 changed pixels of 76,800 before repair.
- After hero screenshots: `landing-repair-hero-1440x900.png`, `landing-repair-hero-1280x800.png`, `landing-repair-hero-1280x800-2s.png`, `landing-repair-hero-390x844.png`, `landing-repair-hero-360x800.png`, and `landing-repair-hero-1024x768.png`. The post-repair crop comparison found 49,734 changed pixels of 76,800 over 2 seconds. Browser console had no errors. The animated dock bounds were within all five viewports.
- Full-page dark and light captures are saved as `landing-repair-dark-1440.png` and `landing-repair-light-1440.png`; Hallmark also rendered desktop and 375-pixel full-page views under `frontend/.hallmark/shots/`.
- Final Hallmark page sweep: 0 FAIL, 0 WARN, 2 documented full-bleed hero waivers, 1 NOTE. Its 12-word copy suggestion is intentionally not applied because the brief requires the exact 13-word support sentence.

## Source note

`frontend/src/vendor/threeui/VERIFICATION.json` continues to verify all 24 supplied source files and the font. The requested separate Predictive Arc `skill.md` was not present under the workspace or installed skill roots, so the integration was checked against the already verified canonical component source and API. No vendor source was modified.

# Third-party and supplied reference inventory

This inventory records source material supplied by the project owner. It does not by itself grant permission to redistribute third-party source. Check the current publisher terms/license before public release.

- Hallmark design skill: https://github.com/Nutlope/hallmark (MIT per repository README/metadata; recheck on install).
- Codex skill catalogue: https://github.com/composio-community/awesome-codex-skills (a catalogue, not a single skill; do not clone/install every listed skill).
- Predictive Arc canonical bundle: https://threeui.com/source-code/predictive-arc.json — requires local retrieval + SHA checks; see `PREDICTIVE_ARC_SOURCE_REQUIRED.md`.
- GlassAiButton bundle supplied by owner: `glass-ai-button-source.md`. Canonical HTML SHA listed in the source: `a484571de316c05ab7fbd2da82da5e028ee1ffe0bd169449fb8a3c7801abd81e`. The visible label is “GPT 6 Sol” and needs a documented product-specific adapter.
- AnimatedTopDock bundle supplied by owner: `animated-top-dock-source.md`. Required `fragment-mono.woff2` font SHA: `4f4dc27f4a770c0d02fde800daa836c8adc0d1e423b28da74baaf0d1cc3ab96c`. The binary font itself is not embedded in the source text file.
- `aegis-remixed-bento-reference.html` is a separate cyber-security design sample using external CDNs and external images; it is not the Predictive Arc source and should not be shipped unchanged.
- `current-landing-before.png` is a screenshot of the pre-redesign landing page for comparison.

Canonical source files should remain unchanged in the reference/vendor directory. Any adapted copy should have a separate filename and a note listing every intentional deviation.

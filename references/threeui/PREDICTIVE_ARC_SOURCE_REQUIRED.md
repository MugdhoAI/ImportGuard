# Predictive Arc source acquisition — blocker record

The owner specified:
- Component: `PredictiveArcCanvas`
- Source bundle: https://threeui.com/source-code/predictive-arc.json
- Source revision: `fa86582fc870`
- Renderer component SHA-256: `ebaa5a1b1f785c7772aaedc2b195318fd63bd9c3e5e5d8e175600968b245dae7`
- Renderer source SHA-256: `fc08c66b13c4a8173c8a88845926b72266d1b1a4fc345c84f44ee61fbfaba92b`
- Collection component SHA-256: `b77a845ab2fa8e8ef8d9b6812d71efe6f320d865d97ec97b2e15253b5950fd63`
- Shared style SHA-256: `efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf`
- Config: `variant="predictive"` (if needed), `mode="dark"`, `speed={1.00}`, `hue={0}`, `saturation={1.00}`, `brightness={1.00}`.

The owner message includes source paths and hashes, but the complete `predictive-arc.json` source bundle was not present among the local source attachments inspected in this kit. `references/visual/aegis-remixed-bento-reference.html` is an unrelated security demo and must not be treated as the canonical Predictive Arc implementation.

Required steps:
1. Retrieve the exact bundle from the URL from the local environment.
2. Extract complete registered text files and all dependencies while preserving canonical originals.
3. Calculate SHA-256 for each file and compare to the provided manifest.
4. Inspect license/terms and attribution requirements.
5. If source access or hashes fail, stop effect integration and report the precise missing asset/permission. Do not approximate the scene and claim exact implementation.

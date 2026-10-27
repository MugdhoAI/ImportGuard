# Third party notices

## ThreeUI Community components

The original Predictive Arc, GlassAiButton, AnimatedTopDock sources, and shared stylesheet in this directory were retrieved from the public ThreeUI source bundles. ThreeUI Community application and component code is licensed under the MIT License; see [LICENSE](./LICENSE). Canonical component source files are kept unchanged. Product adapters live outside this vendor directory and are documented separately.

The bundled GlassAiButton HTML contains the Three.js runtime and its MIT license notice. The AnimatedTopDock shader files use the `three128` package alias for Three.js 0.128.0, which is MIT licensed.

## Fragment Mono

`shaders/fonts/fragment-mono.woff2` is the exact 15,176-byte asset published at the ThreeUI source path and verified against SHA-256 `4f4dc27f4a770c0d02fde800daa836c8adc0d1e423b28da74baaf0d1cc3ab96c`. Fragment Mono is Copyright 2022 The Fragment-Mono Project Authors and licensed under SIL Open Font License 1.1. See [FONT-LICENSES.md](./FONT-LICENSES.md).

ThreeUI's current asset and font licensing terms are preserved in [ASSET-LICENSES.md](./ASSET-LICENSES.md) and [FONT-LICENSES.md](./FONT-LICENSES.md). ThreeUI's Community README identifies its application and Community component code as MIT licensed. These files document the current local source review; recheck upstream terms before any public distribution.

## Local source verification

`npm run verify:sources` retrieves all three canonical JSON bundles, verifies every manifest entry against its code bytes, checks the supplied pinned hashes, and verifies the font bytes from the official ThreeUI GitHub source. Results are written to [VERIFICATION.json](./VERIFICATION.json).

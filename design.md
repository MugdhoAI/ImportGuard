# ImportGuard Design System

This is the locked current design system for the ImportGuard visual redesign. The hero must use the owner's selected Predictive Arc source. This file overrides prior light Lumora/Kage/Sylva visual suggestions for this redesign, while preserving product behavior and accessibility.

## Design thesis

An editorial, atmospheric data-workbench: near-black ink, a precise violet signal, restrained type, visible data transformations, and one genuine signature visual—the Predictive Arc. The product should feel like a carefully built import instrument, not a generic AI SaaS template.

## Palette

Use the CSS tokens described in `CODEX_VISUAL_REDESIGN_PLAN.md` (dark default and a light theme). No raw color literals outside the token block except in immutable third-party source documents. The hero scene itself remains dark in both themes.

## Typography

- Main face: Onest, Geist, or the existing project sans-serif if loading another font would add instability; choose one and use it consistently.
- Data/numeric details: a quiet monospace face only where it improves interpretation.
- Large display type should be clear and editorial, not condensed/ultra-heavy by default.
- No eyebrow labels; no all-caps tracked labels; no isolated colored word in the headline.
- Keep readable line-lengths, wrapping and visible hierarchy.

## Motion and effects

- Signature effect: verified PredictiveArcCanvas, full-bleed in the hero background, `mode="dark"`, speed 1, hue 0, saturation 1, brightness 1.
- Navigation effect: AnimatedTopDock Sable; preserve its proximity spring behavior, adapt copy and wire every item.
- CTA effect: GlassAiButton visual treatment with a minimal documented ImportGuard label/action adapter, keeping the canonical source unchanged in references.
- No additional 3D scene, Kage temple world, Sylva forest world, Lumora liquid-image cursor reveal, or Aegis cyber-security scene. One signature animated background is enough.
- Honor reduced-motion, page visibility, offscreen pause and WebGL fallback.

## Page anatomy

1. Top dock and theme control.
2. Dark full-height hero with Predictive Arc, centered headline and actual Start an import CTA.
3. Real workflow demonstration/sample import.
4. Three or four purposeful explanation sections with varied composition.
5. Privacy/limits and footer links.
6. Workspace retains full processing functionality and supports both themes.

## Content rules

No fabricated metrics, testimonials, customer brands, client logos, "trusted by" lists, fake AI output or unconnected controls. Every preview must be real or explicitly labeled sample fixture. Make product claims only when verified in code.

## Product behavior

Every primary CTA enters the actual import workspace. Navigation links resolve to real anchors/pages. Theme preference persists. Canvas effects are decorative and never contain the only meaningful label or control.

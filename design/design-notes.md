# ImportGuard Design Notes (As-Built)

> Figma file `wGy5iloW7T5Fz1b59XxL5i` could not be opened from this session
> (no MCP/Figma tools; host config access-denied). This package documents the
> IMPLEMENTED interior as the review vehicle. No `.fig` export is claimed.
> See `FIGMA_UNBLOCK.md` for the precise host-side steps.

## Design tokens (CSS variables)

Defined in `app/static/css/styles.css` (`:root`), dark overrides in
`app/static/css/theme.css` (`:root[data-theme="dark"]`).

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#f8f8f5` | `#090a10` | Page background |
| `--ink` | `#171a17` | `#f1f0f6` | Primary text |
| `--muted` | `#777d75` | `#b1b...` | Secondary text (see theme.css) |
| `--line` | `#e3e5df` | `#2a2d3a` | Borders, dividers |
| `--surface` | `#fff` | `#151722` | Cards, sidebar |
| `--accent` | `#c56c42` | `#795fca` | Kickers, active rings |
| `--accent-dark` | `#a84d28` | `#c4b5fd` | Links, buttons |
| `--radius` | `18px` | — | Card radius |

Status pastels are fixed (readable on both themes): pending `#fdf3e3/#8a5f1c`,
success `#eff6ec/#456641`, expired `#f1efe9/#6d6759`, notice `#eef3fb/#2f4d7d`.

## Principles applied

- Data first: tables, counts, and statuses are real database values; no
  decorative charts or invented metrics anywhere.
- Same shell everywhere: sidebar + breadcrumb topbar on all app pages;
  pre-auth pages (login, signup, forgot, reset) stay shell-less.
- Honest unavailable states: no provider, no email delivery, and expired
  files are stated in plain words, never faked.
- Motion: none added; existing `prefers-reduced-motion` block preserved.

## Responsive rules

- Desktop (>850px): persistent sidebar, 4-up stats (auto-fit), full tables.
- Tablet (601–850px): persistent sidebar, 2-up stats, tables scroll
  horizontally inside cards (History 6-col table scrolls; permitted by spec).
- Mobile (≤600px): sidebar becomes a wrapping top bar (labels hidden),
  stats stack 1-up, detail lists stack, tables scroll, no page overflow
  (verified via 390 emulation; see TEST_LOG).

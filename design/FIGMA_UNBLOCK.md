# Figma Unblock (Host-Side Steps)

The Figma source-of-truth work (variables, components, desktop/tablet/mobile
screens with states, `.fig` handoff) is BLOCKED in this session:

1. This session's toolset has no MCP or Figma tools, so file
   `wGy5iloW7T5Fz1b59XxL5i` ("ImportGuard — Product Design System") cannot be
   opened, edited, or verified from here.
2. The likely host MCP config path is access-denied to the sandbox user, and
   no project-local MCP config exists.

## To unblock (owner, on host)

1. In the host Muse environment (outside sandbox), add to MCP config:
   `{"mcpServers": {"Figma": {"url": "https://mcp.figma.com/mcp"}}}`.
2. Complete Figma OAuth in the host browser when prompted.
3. Open `https://www.figma.com/design/wGy5iloW7T5Fz1b59XxL5i/…` and confirm
   the `01 Evidence & Direction` page is visible.
4. Re-run this session's Figma stage with MCP tools available. Transfer
   `vispic/` + `visual-qa/*.png` as evidence (verify pixels, not placeholders).

## Interim authority

Until then, the approved interim sources of truth are, in order:
`IMPORTGUARD_APP_INTERIOR_VISUAL_SPEC.md`, this `design/` package,
`visual-qa/*.png`, and the implementation itself. Design approval of the
as-built interior is requested in the session handoff report.

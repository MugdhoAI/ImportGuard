# Prompt 05 — ImportGuard Final Audit Before Submission

Perform an evidence-based final audit against `CODEX_EXECUTION_PLAN.md`, `CODEX_DESIGN_REFERENCE_GUIDE.md`, `CODEX_SECURITY_PRIVACY_QUALITY_CHECKLIST.md`, and the official hackathon participant requirements available in the workspace.

Do not add features unless they fix a genuine release-blocking defect. Do not deploy or publish without approval.

Verify and report:
- Clean install/setup from documented instructions and exact local start command.
- Landing page, workspace, navigation, all visible controls, empty/loading/success/error states, mobile layout, keyboard use and reduced-motion behavior.
- End-to-end actual CSV workflow: upload, schema, mapping review, approved transformations, validation, accepted/rejected outputs, report and recipe replay.
- CSV parsing edge cases, malformed files, size/row/column limits, identifiers, ambiguous dates, formula injection and stable row accounting.
- API endpoint tests, unit tests, fake-provider tests, lint/type/syntax checks, and browser smoke test if browser tools are available. Record tests not run.
- Meta integration status clearly: mocked test vs actual request. Never claim live API validation if pending.
- Privacy page accurately describes local processing and what is sent to Meta; no invented contact details or false compliance promises.
- No secrets, `.env`, private CSVs or exports in Git; review staged and untracked files.
- Dependency and third-party source/asset license notices.
- README, requirements, environment example, `docs/PROJECT_STATUS.md`, `docs/SESSION_HANDOFF.md`, `docs/TEST_LOG.md`, and `docs/THIRD_PARTY_NOTICES.md` agree with reality.
- Git history has meaningful local checkpoint commits and no accidental publication.
- Three-minute demo outline and synthetic sample data are ready.

Run the relevant checks. Fix release-blocking problems and re-run affected tests. Then update all status/handoff records, make a final local checkpoint commit if safe, verify the commit, and provide a concise pass/fail report with exact evidence and remaining limitations. Do not claim that the project is flawless or professionally security-audited.

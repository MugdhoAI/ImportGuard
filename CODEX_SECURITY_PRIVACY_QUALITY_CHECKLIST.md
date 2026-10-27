# ImportGuard: Security, Privacy, and Product Quality Checklist

> Read this alongside `AGENTS.md`, `CODEX_EXECUTION_PLAN.md`, and `CODEX_DESIGN_REFERENCE_GUIDE.md`. This is a practical release checklist for a small hackathon MVP, not a request to turn ImportGuard into an enterprise platform. Keep controls proportional, test them, and do not claim that a checklist guarantees security or legal compliance.

## 1. Non-negotiable working rules

- Build the smallest complete product. Functional correctness and safe data handling matter more than extra effects, dashboards, abstractions, or services.
- Treat all uploaded CSV content, filenames, schema names, imported recipes, and model output as untrusted input.
- Never use `eval`, `exec`, dynamic imports, shell commands, or generated Python/SQL/regex code to process model suggestions or CSV values.
- Keep model output as a proposal. Validate it against a strict schema and allowlist; require user approval before transformations run.
- Do not silently drop rows, rewrite identifiers, guess ambiguous dates, or overwrite the source.
- Do not show a mocked/cached result as a live model response. Label synthetic examples clearly.
- Do not claim the app is secure, private, compliant, production-ready, or fully tested unless the evidence supports the exact claim.
- If a control is not implemented, do not show it as a working feature.

## 2. Privacy page and accurate disclosures

Implement a real `/privacy` page and make the landing-page Privacy link work. Keep the language short, plain, and consistent with the actual implementation. This page is a project transparency notice, not a guarantee of legal compliance.

It must accurately state:

- **Application mode:** The current version is intended to run locally by default. Clearly explain that if a hosted version is later deployed, uploaded files are processed by that host/server; do not describe hosted processing as happening only on the user's computer.
- **Uploaded CSVs:** The application processes CSVs in bounded memory and should not intentionally persist uploaded files after the request. Verify this against code. Do not promise that no underlying platform, operating system, browser, or provider can ever create logs or copies.
- **Meta AI use:** Manual mapping works without Meta. When the user explicitly clicks the Meta mapping action, disclose that the request sends source headers and target-schema information to Meta's API. Send sample row values only when the user deliberately enables a separate, unchecked-by-default option. Never send the whole CSV for mapping.
- **Third-party processing:** Link to the current Meta Model API privacy/legal information. Use the documented Standard model `muse-spark-1.3`, not a Contributor model, unless the user explicitly changes that decision. Official docs say Standard-mode content is not used to train Meta models; do not expand this into a claim of zero retention, local processing, or guaranteed confidentiality.
- **Storage/analytics:** State only what the code does. Do not add analytics, advertising pixels, cookies, telemetry, an external form, or another third-party service without a real need and a corresponding disclosure.
- **User guidance:** Tell users not to upload sensitive/confidential data they are not authorized to share. Recommend synthetic or anonymized sample data for the demo.
- **Limitations:** Mapping suggestions may be wrong; users must review them; validation checks only the configured rules.
- **Contact:** Do not invent a support email, company address, legal identity, or data-protection contact. If public deployment or the applicable rules require a contact, mark it as a blocker for the owner to provide before release.
- **Effective date:** If a date is shown, use the actual date the notice was written or updated.

Do not add a lengthy Terms of Service, account deletion workflow, or cookie banner to the local MVP unless the actual features or deployment require them. If the project becomes publicly hosted, reassess the privacy notice and applicable legal obligations before collecting real user files.

Official references to consult when describing Meta processing:
- Models and Standard/Contributor mode: https://dev.meta.ai/docs/models
- Meta Model API privacy/legal center: https://dev.meta.ai/help/policies-and-privacy/policies-and-terms
- Meta Model API terms: https://dev.meta.ai/legal/terms-of-service

## 3. CSV upload and processing security

- Accept CSV only for this MVP. Enforce the existing configured 5 MB, 5,000-row, and 100-column limits on the server, not just in the browser.
- Do not trust extension or browser-supplied MIME type by itself. Validate file bytes/decoding and parsing; give a clear error for non-CSV or malformed content.
- Handle UTF-8 and UTF-8 with BOM deliberately. Reject invalid encoding rather than silently replacing characters.
- Reject blank/duplicate headers and malformed row lengths without silently overwriting values.
- Process files in memory within the configured limits. Do not write uploaded data or output archives to a public/static directory or retain them after the request.
- Never use the submitted filename as a filesystem path. Sanitize it for display and use a safe, fixed/generated download filename.
- Never log raw CSV rows, sample values, full prompts, API keys, or sensitive request payloads. Avoid sending these in exception messages to the browser.
- Treat values inside the CSV as data, not instructions. Cell contents must never control model tools, application configuration, file paths, or code execution.
- Escape untrusted values in rendered HTML. Use Jinja's normal auto-escaping; in browser JavaScript prefer `textContent` and safe DOM methods over interpolating CSV text into `innerHTML`.
- Protect ZIP/download handling: use fixed member names, explicit content types, and no path traversal. A recipe must contain schema/mapping rules only, not row values or secrets.
- Enforce stable row accounting: input rows = accepted rows + rejected rows. Preserve original values in the rejection report so users can recover data.

References:
- OWASP File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- OWASP Cross-Site Scripting Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

## 4. CSV formula injection and export safety

CSV exports can be opened by spreadsheet programs that interpret values beginning with formula characters as formulas. This is relevant to accepted and rejected exports.

- Follow the spreadsheet-safe export policy in `CODEX_EXECUTION_PLAN.md`.
- Make any neutralization behavior explicit in the UI/README and test it. Never silently change source values in the processing model.
- Preserve recoverability of rejected source data and explain the difference between raw values and spreadsheet-safe exported values if both representations are provided.
- Add tests for values beginning with `=`, `+`, `-`, `@`, tab, and carriage return, including ordinary negative numbers and identifiers, so the safety layer does not corrupt common legitimate values without explanation.

Reference: OWASP CSV Injection: https://owasp.org/www-community/attacks/CSV_Injection

## 5. Secrets, Meta API, and cost control

- `.env` must be ignored by Git. `.env.example` must contain blank/place-holder values only.
- Never print, commit, screenshot, return to the browser, or expose `MODEL_API_KEY` in errors.
- Keep `ALLOW_META_API_CALLS=false` by default. Do not call the live API until the user explicitly enables it and confirms account/credit status.
- Only call Meta from server-side Python. Never put the key in HTML, CSS, JavaScript, a URL, or a browser request.
- Use `muse-spark-1.3` Standard mode unless the user explicitly decides otherwise. Do not silently change to a Contributor model.
- Send headers and target-schema definitions when the user invokes AI mapping. Include up to three sample values per column only after a separate explicit opt-in. Do not transmit all rows or the whole CSV for mapping.
- Set a finite request timeout and bounded retry behavior. Never retry indefinitely, and never turn a 429/error into a hidden loop.
- Record request status and timing without row values, prompts, response bodies containing user data, or secrets. If provider usage is available, record only non-sensitive usage figures.
- In the UI, distinguish manual suggestions, model suggestions, and a genuine successful live Meta response.
- When credentials or credits are unavailable, disable the Meta action with an honest message while leaving manual mapping and local processing functional.

References:
- Meta models and data mode: https://dev.meta.ai/docs/models
- Pricing/rate limits: https://dev.meta.ai/docs/pricing-rate-limits
- Meta privacy/legal center: https://dev.meta.ai/help/policies-and-privacy/policies-and-terms

## 6. Local running versus public deployment

**Default mode is local-only.** The normal development command should bind to `127.0.0.1`, not expose the app to the network. Do not deploy or publish without the user's explicit approval.

Before any public deployment, perform a separate deployment review:

- Confirm the hosted server's data flow, file retention, region, logs, backups, and third-party processors.
- Do not expose an anonymous upload/processing endpoint without reasonable abuse controls. Reassess request limits, rate limits, authentication if needed, concurrency and memory usage.
- Require HTTPS, restrictive same-origin/CORS behavior, safe error responses and appropriate security headers.
- Confirm request-body limits are enforced before expensive parsing and that errors do not include stack traces or secrets.
- Review CSRF risks if cookie-based sessions or state-changing cross-origin interactions are introduced.
- Verify that generated downloadable content is not publicly cached or accessible to another user.
- Make the privacy page accurate for the deployed architecture and obtain any necessary owner-provided contact details.
- Run the tests against the deployed environment and check server/browser logs without exposing sensitive data.

Do not implement authentication, user accounts, databases, complex rate-limiting infrastructure, or deployment infrastructure merely to make the local MVP feel enterprise-grade. Add public-deployment controls only when deployment is actually approved and its architecture is known.

Reference: OWASP REST Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html

## 7. Quality checks expected from responsible AI-assisted coding

Codex must not treat generated code as correct merely because it compiles. For each meaningful change:

1. State the acceptance criteria briefly in the task/commit notes.
2. Implement the smallest change that meets them.
3. Run focused tests; add tests for bug fixes and edge cases.
4. Inspect the diff for unrelated edits, hard-coded secrets, dead code, unsafe parsing, and accidental feature creep.
5. Run the full test suite and lint checks after integration.
6. Launch the app and test the real browser workflow, if the environment supports it.
7. Report exactly which checks ran and their actual result. Do not say "tested" for code that was only inspected.

The acceptance checklist must include:

- Normal import, mapping approval, processing, accepted/rejected exports, and recipe replay.
- Empty file, malformed CSV, wrong encoding, duplicate headers, excessive size/rows/columns, missing required field, duplicate values, Unicode, commas/quotes/newlines inside cells, and ambiguous dates.
- Formula-triggering export values and preservation of identifiers with leading zeros.
- HTML injection strings in headers/cells displayed as text, not executable markup.
- Invalid/unknown model fields and operations rejected by the backend.
- Meta unavailable, timeout, rate limit, malformed structured response, and manual fallback.
- No persistence of uploaded rows, no data in logs, and no secrets in Git.
- Row-accounting invariant, stable order, and repeatable recipe execution.
- Desktop and mobile layouts, keyboard operation, visible focus, labels, readable contrast, and reduced-motion support.
- All visible buttons/links work; empty/loading/error/success states are clear; no fake results are represented as real.
- `README.md`, privacy notice, example files, and current Meta API status agree with actual behavior.

## 8. Dependencies, licensing, and third-party references

- Prefer maintained, minimal dependencies and pin versions where practical. Do not add a package for a small utility that can be implemented safely with the existing stack.
- Review direct dependency licenses and include notices required by the relevant license.
- A source URL, skill file, source hash, preview, or user-provided prompt does **not** by itself grant permission to redistribute code/assets.
- Before copying ThreeUI source, images, fonts, or runtime assets, retrieve the actual files and verify the current license/terms and attribution requirements. If rights or exact source cannot be verified, use it only as design inspiration and build the effect natively with CSS/HTML.
- The Kage, Sylva, Glass AI Button, and Animated Top Dock effects are optional references, not requirements to integrate every component. Do not delay the functional workspace for 3D/WebGL effects.
- Do not add remote analytics, unknown binaries, unexplained install scripts, or downloads from the inconsistent Hackathon-Tools repository.
- Do not include real users' CSV data in test fixtures, screenshots, the Git repository, or the demo. Use synthetic data or data whose use is explicitly authorized.

## 9. Public-release blockers

Before the owner publishes the repository or deploys a hosted version, report any unresolved blockers, including:

- The applicable project license and attribution decisions.
- Whether the privacy notice matches the actual data flow.
- Any required maintainer/contact information that has not been supplied.
- Whether live Meta integration was genuinely tested.
- Any known critical bugs, failing tests, or untested security-sensitive paths.
- Whether external source/assets have verified redistribution rights.
- Whether the hosting/deployment configuration has received a separate security review.

Never silently fabricate contact details, legal guarantees, data retention claims, user testimonials, security certifications, usage metrics, or test results.

## Definition of done

ImportGuard is ready for the user's review when its required local workflow works, tests and lint results are reported honestly, the privacy notice matches its real behavior, high-risk CSV/model-input cases are covered, no secret or personal fixture is committed, and known limitations are documented. This does not mean the app is penetration-tested or legally certified.

# Three-minute demo outline

Record at 1280x800 from a clean local run (`npm --prefix frontend run build`,
then `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`). Use only
the bundled synthetic registrations fixture. Never show an API key, `.env`
contents, or real personal data on screen.

1. **0:00–0:20** — Landing: headline, the problem (unfamiliar headers such as
   `Reg No` / `Payment`, and a `maybe` value that cannot be safely guessed),
   then click **Start an import** to enter the real workspace.
2. **0:20–0:45** — Workspace: **Load synthetic example**, inspect the profile
   (3 data rows, 4 columns, empty counts).
3. **0:45–1:20** — Mapping: run **Suggest locally**, correct `student_id` to
   `Reg No` and `payment_status` to `Payment`, check the approval box. The
   live Meta round trip was verified on 2026-10-30 (one synthetic request via
   `scripts/test_meta_api.py`); with owner authorization you may show one live
   **Suggest with Meta AI** call on the synthetic fixture instead, then review
   and correct its proposals on screen. State plainly which source each shown
   suggestion came from.
4. **1:20–1:55** — Process: **Validate & download package**; open the rejected
   rows to show the ambiguous boolean (`maybe`) and the reason codes.
5. **1:55–2:25** — Results: 2 accepted / 1 rejected counts and the ZIP contents
   (`accepted.csv`, `rejected.csv`, `recipe.json`, `report.json`).
6. **2:25–2:45** — Replay the exported `recipe.json` against the CSV again and
   note that replay makes no model request.
7. **2:45–3:00** — Close: review-before-processing, deterministic validation,
   repeatable recipes — and the truthful Meta API status.

Rules: synthetic data only. Do not present local suggestions or fake-provider
output as a live Meta result. The verified smoke test proves the live round
trip on synthetic headers, not mapping quality on real user CSVs — every
suggestion shown must still be reviewed on screen. If the live call is not
shown, say so and show the disabled Meta button state instead.

## Recording checklist

- [ ] Fresh server on `127.0.0.1:8000` with the rebuilt frontend (`dist/` current)
- [ ] `ALLOW_META_API_CALLS=false` unless the live Meta segment was authorized and verified
- [ ] Browser at 1280x800, dark theme default, no personal tabs/bookmarks visible
- [ ] Fixture files only (`examples/registrations.csv` + schema); no real data
- [ ] Narration matches the outline timings; total under 3:00 as MP4

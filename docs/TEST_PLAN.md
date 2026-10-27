# Test plan

Automated tests use synthetic data. `python -m pytest -q` covers:

- UTF-8/BOM, Unicode, malformed/empty CSV, duplicate/blank headers, row shape, byte/row/column caps, and physical line numbering when a quoted field spans lines.
- Mapping references and uniqueness, approved operations, strict scalar types, ambiguous/invalid dates, leading-zero identifiers, row order/accounting, and repeatable recipe replay.
- Formula-safe CSV output and fixed ZIP members.
- Health/pages, local profile/suggestions, manual processing, ZIP download, replay, and disabled Meta behavior.
- Injected fake Meta provider for valid/invalid structured proposals, unknown references, rate limits, and timeouts; these tests are not live API calls.

Manual release checks still needed: browser workflow across desktop/mobile, keyboard and reduced-motion review, and the opt-in real Meta smoke test (only after explicit account/credit authorization). There is currently no automated browser test.

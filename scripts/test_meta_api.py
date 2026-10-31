"""Opt-in live Meta API smoke test. Never runs under pytest or CI."""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import settings  # noqa: E402
from app.models.schemas import TargetField  # noqa: E402
from app.services.meta_client import MetaUnavailable, suggest_mappings  # noqa: E402

# Synthetic, non-sensitive headers only. No sample values are ever sent here.
HEADERS = ["Reg No", "Mobile", "Paid"]
SCHEMA = [
    TargetField(name="student_id", type="string", required=True),
    TargetField(name="phone", type="string", required=False),
    TargetField(name="payment_status", type="string", required=False),
]


def main() -> int:
    if not settings.allow_meta_api_calls:
        print("Skipped: set ALLOW_META_API_CALLS=true to authorize a live Meta call.")
        return 0
    if not settings.model_api_key:
        print("Skipped: MODEL_API_KEY is not configured.")
        return 0
    print(f"Sending one synthetic mapping request to {settings.meta_base_url} ...")
    started = time.perf_counter()
    try:
        mappings = suggest_mappings(HEADERS, SCHEMA)
    except MetaUnavailable as exc:
        print(f"Live Meta request failed safely: {exc}")
        return 1
    elapsed = time.perf_counter() - started
    summary = [(m["target_field"], m["source_column"], m["confidence"]) for m in mappings]
    print(f"Live Meta request succeeded in {elapsed:.1f}s: {len(mappings)} mappings.")
    for target, source, confidence in summary:
        print(f"  {target} <- {source} ({confidence})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

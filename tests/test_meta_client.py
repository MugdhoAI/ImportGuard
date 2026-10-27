import json
from types import SimpleNamespace

import pytest

from app.models.schemas import TargetField
from app.services import meta_client


class FakeCompletions:
    def __init__(self, content):
        self.content = content

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))]
        )


def test_meta_adapter_uses_fake_provider_and_validates_proposal(monkeypatch):
    monkeypatch.setattr(
        meta_client,
        "settings",
        SimpleNamespace(
            allow_meta_api_calls=True,
            model_api_key="test-only",
            meta_base_url="https://api.meta.ai/v1",
            meta_model="muse-spark-1.3",
        ),
    )
    fake = FakeCompletions(
        json.dumps(
            {
                "mappings": [
                    {
                        "source_column": "ID",
                        "target_field": "id",
                        "operation": "identity",
                        "confidence": "high",
                        "needs_review": True,
                        "note": "Review",
                    }
                ]
            }
        )
    )
    client = SimpleNamespace(chat=SimpleNamespace(completions=fake))
    proposals = meta_client.suggest_mappings(["ID"], [TargetField(name="id")], client=client)
    assert proposals[0]["source_column"] == "ID"
    assert fake.kwargs["model"] == "muse-spark-1.3"


def test_meta_adapter_rejects_invalid_model_output(monkeypatch):
    monkeypatch.setattr(
        meta_client,
        "settings",
        SimpleNamespace(
            allow_meta_api_calls=True,
            model_api_key="test-only",
            meta_base_url="https://api.meta.ai/v1",
            meta_model="muse-spark-1.3",
        ),
    )
    fake = FakeCompletions(
        '{"mappings":[{"source_column":"ID","target_field":"id","operation":"exec"}]}'
    )
    client = SimpleNamespace(chat=SimpleNamespace(completions=fake))
    with pytest.raises(meta_client.MetaUnavailable, match="invalid mapping"):
        meta_client.suggest_mappings(["ID"], [TargetField(name="id")], client=client)


def test_meta_adapter_rejects_unknown_references(monkeypatch):
    monkeypatch.setattr(
        meta_client,
        "settings",
        SimpleNamespace(
            allow_meta_api_calls=True,
            model_api_key="test-only",
            meta_base_url="https://api.meta.ai/v1",
            meta_model="muse-spark-1.3",
        ),
    )
    fake = FakeCompletions(
        json.dumps(
            {
                "mappings": [
                    {
                        "source_column": "Other",
                        "target_field": "id",
                        "operation": "identity",
                        "confidence": "low",
                        "needs_review": True,
                        "note": "",
                    }
                ]
            }
        )
    )
    client = SimpleNamespace(chat=SimpleNamespace(completions=fake))
    with pytest.raises(meta_client.MetaUnavailable, match="outside the supplied schema"):
        meta_client.suggest_mappings(["ID"], [TargetField(name="id")], client=client)


@pytest.mark.parametrize(
    "exception,message",
    [
        (type("RateLimitError", (Exception,), {"status_code": 429}), "rate limit"),
        (type("APITimeoutError", (Exception,), {}), "timed out"),
    ],
)
def test_meta_adapter_handles_rate_limit_and_timeout_safely(monkeypatch, exception, message):
    monkeypatch.setattr(
        meta_client,
        "settings",
        SimpleNamespace(
            allow_meta_api_calls=True,
            model_api_key="test-only",
            meta_base_url="https://api.meta.ai/v1",
            meta_model="muse-spark-1.3",
        ),
    )

    class BrokenCompletions:
        def create(self, **kwargs):
            raise exception("private payload must not be surfaced")

    client = SimpleNamespace(chat=SimpleNamespace(completions=BrokenCompletions()))
    with pytest.raises(meta_client.MetaUnavailable, match=message) as error:
        meta_client.suggest_mappings(["ID"], [TargetField(name="id")], client=client)
    assert "private payload" not in str(error.value)

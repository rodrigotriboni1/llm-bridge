"""The product's core: primary fails -> next provider answers, attempts recorded."""

from __future__ import annotations

import pytest

from llm_bridge.providers import (
    Bridge,
    Provider,
    ProviderError,
    ProviderKind,
    Routing,
)

MSGS = [{"role": "user", "content": "hi"}]


def _providers() -> dict[str, Provider]:
    return {
        "a": Provider(id="a", kind=ProviderKind.OPENAI, label="A", model="gpt"),
        "b": Provider(id="b", kind=ProviderKind.DEEPSEEK, label="B", model="deepseek"),
        "c": Provider(id="c", kind=ProviderKind.MOCK, label="C", model="mock"),
    }


def _completer(fail: set[str]):
    def complete(provider: Provider, messages: list[dict], kwargs: dict) -> str:
        if provider.id in fail:
            raise RuntimeError(f"{provider.id} boom")
        return f"answer from {provider.id}"

    return complete


def test_primary_success_single_attempt():
    bridge = Bridge(_providers(), _completer(fail=set()))
    res = bridge.complete(Routing(primary="a", fallbacks=["b", "c"]), MSGS)
    assert res.served_by == "a"
    assert res.content == "answer from a"
    assert len(res.attempts) == 1 and res.attempts[0].ok


def test_failover_to_next_when_primary_fails():
    bridge = Bridge(_providers(), _completer(fail={"a"}))
    res = bridge.complete(Routing(primary="a", fallbacks=["b", "c"]), MSGS)
    assert res.served_by == "b"
    assert [a.provider_id for a in res.attempts] == ["a", "b"]
    assert res.attempts[0].ok is False and res.attempts[0].error
    assert res.attempts[1].ok is True


def test_failover_walks_whole_chain():
    bridge = Bridge(_providers(), _completer(fail={"a", "b"}))
    res = bridge.complete(Routing(primary="a", fallbacks=["b", "c"]), MSGS)
    assert res.served_by == "c"
    assert [a.provider_id for a in res.attempts] == ["a", "b", "c"]


def test_all_fail_raises():
    bridge = Bridge(_providers(), _completer(fail={"a", "b", "c"}))
    with pytest.raises(ProviderError):
        bridge.complete(Routing(primary="a", fallbacks=["b", "c"]), MSGS)


def test_disabled_provider_skipped():
    providers = _providers()
    providers["a"].enabled = False
    bridge = Bridge(providers, _completer(fail=set()))
    res = bridge.complete(Routing(primary="a", fallbacks=["b"]), MSGS)
    assert res.served_by == "b"  # 'a' disabled, skipped


def test_chain_dedupes_and_preserves_order():
    r = Routing(primary="a", fallbacks=["b", "a", "c", "b"])
    assert r.chain() == ["a", "b", "c"]

"""Default provider registry + routing, seeded from env.

Offline-first: with no API keys, the MOCK provider is always available and
becomes the primary, so the bridge runs and demos failover with zero setup.
"""

from __future__ import annotations

import os

from llm_bridge.providers import PROVIDER_PRESETS, Provider, ProviderKind, Routing

# The four real providers + the offline mock, in a stable display order.
DEFAULT_ORDER = [
    ProviderKind.OPENAI,
    ProviderKind.ANTHROPIC,
    ProviderKind.MOONSHOT,
    ProviderKind.DEEPSEEK,
    ProviderKind.MOCK,
]


def _has_key(kind: ProviderKind) -> bool:
    env = PROVIDER_PRESETS[kind]["env_key"]
    return bool(env and os.getenv(env))


def default_providers() -> dict[str, Provider]:
    providers: dict[str, Provider] = {}
    for kind in DEFAULT_ORDER:
        preset = PROVIDER_PRESETS[kind]
        pid = kind.value
        has_key = _has_key(kind)
        providers[pid] = Provider(
            id=pid,
            kind=kind,
            label=str(preset["label"]),
            model=str(preset["model"]),
            enabled=has_key or kind is ProviderKind.MOCK,
            has_key=has_key,
            status="unknown",
        )
    return providers


def default_routing(providers: dict[str, Provider]) -> Routing:
    """Primary = first enabled real provider with a key; fallbacks = the other
    enabled ones in order; mock is always the last-resort fallback."""
    enabled = [p.id for p in providers.values() if p.enabled]
    reals = [pid for pid in enabled if pid != ProviderKind.MOCK.value]
    if reals:
        return Routing(primary=reals[0], fallbacks=[*reals[1:], ProviderKind.MOCK.value])
    return Routing(primary=ProviderKind.MOCK.value, fallbacks=[])


def offline() -> bool:
    return os.getenv("LLM_BRIDGE_OFFLINE", "0") == "1"

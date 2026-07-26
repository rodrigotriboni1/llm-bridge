"""LLM Bridge core: providers, routing, and the failover chain.

This is the product's heart: many providers (GPT, Claude, Kimi, DeepSeek), one
OpenAI-compatible surface, and an ordered fallback chain — if the primary
provider fails, the next one is tried automatically. The actual model call is a
pluggable ``Completer`` so the failover logic is testable offline and the real
implementation (LiteLLM) slots in behind it.

Ethos (shared with agent-studio): adopt the engine (LiteLLM), build the
governance (routing + fallback + observability).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum


class ProviderKind(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOONSHOT = "moonshot"  # Kimi
    DEEPSEEK = "deepseek"
    MOCK = "mock"


# Presets keep the UI honest and map a kind to its LiteLLM model id + env key.
# All four real providers speak the OpenAI-compatible API through LiteLLM.
PROVIDER_PRESETS: dict[ProviderKind, dict[str, str | None]] = {
    ProviderKind.OPENAI: {
        "label": "OpenAI · GPT",
        "model": "gpt-4o-mini",
        "litellm_model": "gpt-4o-mini",
        "env_key": "OPENAI_API_KEY",
    },
    ProviderKind.ANTHROPIC: {
        "label": "Anthropic · Claude",
        "model": "claude-3-5-sonnet",
        "litellm_model": "claude-3-5-sonnet-20241022",
        "env_key": "ANTHROPIC_API_KEY",
    },
    ProviderKind.MOONSHOT: {
        "label": "Moonshot · Kimi",
        "model": "moonshot-v1-8k",
        "litellm_model": "moonshot/moonshot-v1-8k",
        "env_key": "MOONSHOT_API_KEY",
    },
    ProviderKind.DEEPSEEK: {
        "label": "DeepSeek",
        "model": "deepseek-chat",
        "litellm_model": "deepseek/deepseek-chat",
        "env_key": "DEEPSEEK_API_KEY",
    },
    ProviderKind.MOCK: {
        "label": "Mock · offline",
        "model": "mock",
        "litellm_model": "mock",
        "env_key": None,
    },
}


@dataclass
class Provider:
    """A configured provider. The API key is NEVER stored here — only whether one
    is present (``has_key``), so the value never leaves the process boundary."""

    id: str
    kind: ProviderKind
    label: str
    model: str
    enabled: bool = True
    has_key: bool = False
    api_base: str | None = None
    status: str = "unknown"  # "up" | "down" | "unknown"

    @property
    def litellm_model(self) -> str:
        return str(PROVIDER_PRESETS[self.kind]["litellm_model"])


@dataclass
class Routing:
    """Primary provider + ordered fallbacks (by provider id)."""

    primary: str
    fallbacks: list[str] = field(default_factory=list)

    def chain(self) -> list[str]:
        """The full ordered attempt list (primary first, then fallbacks),
        de-duplicated while preserving order."""
        seen: set[str] = set()
        out: list[str] = []
        for pid in [self.primary, *self.fallbacks]:
            if pid and pid not in seen:
                seen.add(pid)
                out.append(pid)
        return out


@dataclass
class Attempt:
    provider_id: str
    ok: bool
    error: str | None = None
    ms: int = 0


@dataclass
class ChatResult:
    content: str
    served_by: str
    model: str
    attempts: list[Attempt] = field(default_factory=list)


class ProviderError(Exception):
    """Raised by a Completer when a provider call fails (triggers failover)."""


# A Completer performs ONE provider call. Real impl = LiteLLM; tests/offline use
# a scripted one. Signature: (provider, messages, **kwargs) -> content str.
Completer = Callable[[Provider, list[dict], dict], str]


class Bridge:
    """Runs a chat request through the routing chain with automatic failover.

    Tries the primary provider; on ``ProviderError`` (or any exception) it moves
    to the next fallback, recording every attempt. Raises ``ProviderError`` only
    if the whole chain is exhausted.
    """

    def __init__(self, providers: dict[str, Provider], completer: Completer) -> None:
        self._providers = providers
        self._completer = completer

    def complete(
        self,
        routing: Routing,
        messages: list[dict],
        **kwargs: object,
    ) -> ChatResult:
        attempts: list[Attempt] = []
        chain = [pid for pid in routing.chain() if self._eligible(pid)]
        if not chain:
            raise ProviderError("no eligible providers in the routing chain")

        for pid in chain:
            provider = self._providers[pid]
            started = time.perf_counter()
            try:
                content = self._completer(provider, messages, dict(kwargs))
                ms = int((time.perf_counter() - started) * 1000)
                attempts.append(Attempt(provider_id=pid, ok=True, ms=ms))
                return ChatResult(
                    content=content,
                    served_by=pid,
                    model=provider.model,
                    attempts=attempts,
                )
            except Exception as exc:  # any failure -> try the next provider
                ms = int((time.perf_counter() - started) * 1000)
                attempts.append(
                    Attempt(provider_id=pid, ok=False, error=str(exc), ms=ms)
                )

        raise ProviderError(
            "all providers in the fallback chain failed: "
            + ", ".join(f"{a.provider_id} ({a.error})" for a in attempts)
        )

    def _eligible(self, pid: str) -> bool:
        p = self._providers.get(pid)
        return bool(p and p.enabled)

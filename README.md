# LLM Bridge

**A governed, multi-provider LLM gateway with automatic failover.**

Use every model behind one OpenAI-compatible endpoint — **GPT, Claude, Kimi
(Moonshot), DeepSeek** — and set an ordered fallback chain: if the primary
provider fails, the next one answers automatically. Pick your primary, drag your
fallbacks, and never hard-depend on a single vendor.

> Ethos (shared with `agent-studio`): **adopt the engine, build the governance.**
> The multi-provider calls ride on **[LiteLLM](https://github.com/BerriAI/litellm)**
> (which already speaks every provider + supports fallbacks); the Bridge adds the
> routing, failover chain, health, and a builder UI.

## Why not just use X?
Open-source options that already do multi-provider + fallback: **LiteLLM** (adopted
here), **Portkey AI Gateway**, **one-api / new-api**, **BricksLLM**. LLM Bridge is a
thin, self-hostable gateway over LiteLLM with a first-class **failover UI** and a
clean OpenAI-compatible surface — and it drops into `agent-studio`'s
`ModelProvider` seam.

## Features
- **Providers**: GPT, Claude, Kimi, DeepSeek (+ an offline mock). Enable, set model
  + key (write-only, never returned), test health.
- **Routing / fallback**: choose a primary and an ordered list of fallbacks. "If 1
  fails, use another" — automatic, with every attempt recorded.
- **Playground**: send a prompt, see which provider served it and the failover
  trail; a "simulate failure" toggle demonstrates failover live.
- **OpenAI-compatible** `POST /v1/chat/completions`.

## Design
UI adopts the **Open Design** system (Stripe-inspired: deep navy, one purple
accent, Sohne/Source Code Pro) — see `docs/open-design/` and `web/src/system.css`.

## Run
```bash
# Backend (offline, no keys needed)
cd server && uv venv && . .venv/bin/activate && uv pip install -e ".[engine,dev]"
LLM_BRIDGE_OFFLINE=1 uvicorn llm_bridge.app:app --port 8000

# Frontend
cd web && pnpm install && pnpm dev   # http://localhost:5173
```

Add real providers by setting `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` /
`MOONSHOT_API_KEY` / `DEEPSEEK_API_KEY` (or via the Providers UI) and unset
`LLM_BRIDGE_OFFLINE`.

## License
AGPL-3.0-or-later.

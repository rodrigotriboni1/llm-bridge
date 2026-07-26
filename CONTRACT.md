# LLM Bridge — API contract (FIXED)

Backend (FastAPI, `server/`) and frontend (React, `web/`) build to this. Base URL
`http://localhost:8000`. All responses JSON. Offline mode (`LLM_BRIDGE_OFFLINE=1`)
uses the mock provider so everything runs with no keys.

## Types
```
Provider  { id, kind: "openai"|"anthropic"|"moonshot"|"deepseek"|"mock",
            label, model, enabled, has_key, status: "up"|"down"|"unknown" }
Routing   { primary: provider_id, fallbacks: provider_id[] }   # ordered
Attempt   { provider_id, ok, error?, ms }
ChatResult{ content, served_by: provider_id, model, attempts: Attempt[] }
```

## Endpoints
- `GET  /health` → `{ status, offline }`
- `GET  /providers` → `Provider[]`
- `PUT  /providers/{id}` → body `{ enabled?, model?, api_key?, api_base? }` → `Provider`
      (api_key is write-only; never returned — only `has_key` flips true)
- `POST /providers/{id}/test` → pings the provider → `Provider` (updated `status`)
- `GET  /routing` → `Routing`
- `PUT  /routing` → body `Routing` → `Routing`
- `POST /v1/chat/completions` → body `{ messages:[{role,content}], temperature? }`
      → `ChatResult` (routes through the fallback chain; `served_by` = the provider
      that actually answered; `attempts` shows every try incl. failovers)
- `POST /simulate/failure` → body `{ provider_ids: string[] }` → `{ failing: string[] }`
      (demo hook: forces those providers to fail so failover is visible live)

## Failover behaviour (the product)
`complete()` tries `routing.chain()` (primary then fallbacks, de-duped) over only
enabled providers; on any error it records the `Attempt` and moves to the next;
returns the first success with `served_by` set; 502 only if the whole chain fails.
Core logic is `llm_bridge.providers.Bridge` (already implemented + offline mock).

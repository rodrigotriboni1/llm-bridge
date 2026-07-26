# Design — LLM Bridge

The UI adopts the **Open Design** system exported for this product family
(`docs/open-design/brand-spec.md`, ported verbatim to `web/src/system.css`).

## Language (Stripe-inspired)
- **Palette:** bg `#ffffff`, surface `#f8fafd`, fg/navy `#061b31`, muted `#64748d`,
  border `#e5edf5`, accent/purple `#533afd` (one accent per screen), semantic
  success `#16a34a` / warning `#d97706` / danger `#dc2626`.
- **Type:** Sohne (display/body), Source Code Pro (mono).
- **Shape:** 4px grid; radii 4/8/12px; 1px quiet borders; pill = 9999px.
- **Shell:** dark navy sidebar (`#061b31`) + light content; monogram mark.
- **Icons:** Lucide, no emoji. Feature icons in subtle neutral surfaces.

Reuse the exact class names in `system.css` (`.sidebar`, `.nav-link`, `.card`,
`.btn`, `.badge`, `.field`, `.table`, `.stat-card`, `.module-card`, etc.).

## Screens (LLM Bridge)
- **Providers** — cards for GPT / Claude / Kimi / DeepSeek (+ mock): enable, model,
  key (write-only), health dot, "Test" button.
- **Routing** — pick the **primary** provider and an **ordered fallback** list
  (reorderable); the chain reads primary → fallback → fallback.
- **Playground** — chat composer; each answer shows a `served by <provider>` badge
  and the **attempt trail** (which providers were tried / failed). A "Simulate
  failure" toggle forces providers to fail to demonstrate failover.
- **Logs** — recent requests with served-by + failover count.

Brand mark: geometric monogram **"LB"** in navy/purple (per brand-spec: no
Sparkles, no gradient blobs).

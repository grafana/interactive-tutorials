# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 3 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:has(span:contains('productcatalogservice'))` | rca-demo, rca-demo-ops +1 | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_<br>service names are instance data (OTel demo) — the ask is a parameterized `data-testid` (e.g. `service-node-${name}`) on the service-map node / services-table name cell |

### FYI — we'll retarget these ourselves, just don't rename the replacements (1)

- `a[href*="a/grafana-app-observability-app"]` → link is rendered by Grafana core (mega menu / nav registration) — tutorials will retarget to the core `Nav menu item` selector

> [!WARNING]
> 2 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

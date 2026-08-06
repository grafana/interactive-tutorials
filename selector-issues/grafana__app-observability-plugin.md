# Stable selectors for Grafana Pathfinder tutorials (2 anchors, 4 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (2)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:has(span:contains('productcatalogservice'))` | rca-demo, rca-demo-ops +1 | `plugin/cypress/support/fixtures/serviceMap/data/1.json:382`<br>`plugin/cypress/support/fixtures/serviceMap/data/1.json:386`<br>_low confidence (matched `productcatalogservice`)_ |
| `a[href*="a/grafana-app-observability-app"]` | welcome-to-play/main-page | `docs/development/run-app-platform.md:82`<br>`plugin/cypress/support/commands/general/actions.ts:36` |

> [!WARNING]
> 2 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

# Stable selectors for Grafana Pathfinder tutorials (6 anchors, 13 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## ⚠️ Live in production, gone from `main` (3)

These match on production today (checked 2026-08-06) but not in `main` — tutorials break on your next release. Please share replacement selectors before deploying.

| anchor | tutorials | notes |
|---|---|---|
| `input[data-testid='search-input-input']` | connect-prometheus-metrics, grafana-cloud-tour-lj/explore-connect-data +7 | `search-input-input` |
| `a:has([data-testid='datasource-mysql-card'])` | grafana-cloud-tour-lj/explore-connect-data | `src/features/catalog/CardContent/PermissionMissingModalContent/PermissionMissingModalContent.tsx:52`<br>`src/features/catalog/CardContent/FeaturedConnectionsModalContent/MySQLRouterModalContent.tsx:24`<br>_medium confidence (matched `datasource- …(prefix)`)_ |
| `[data-testid='search-input-input']` | kafka-monitoring-lj/install-grafana-alloy | `search-input-input` |

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `[aria-label='Search connections by name']` | haproxy-load-balancer-lj/install-dashboards, iis-web-server-lj/select-integration | `src/features/catalog/Search/SemanticSearch.tsx:167` |
| `[aria-label="Search connections by name"]` | windows-integration/select-platform | `src/features/catalog/Search/SemanticSearch.tsx:167` |

## Anchor gone — renamed or removed? (1)

Not found in source, bundle, or a live stack (2026-08-06). Tell us the new selector, or we'll re-record the step.

| anchor | tutorials | searched for |
|---|---|---|
| `[role='button']:has([data-testid='icon-plus-circle'])` | grafana-cloud-tour-lj/explore-connect-data, grafana-cloud-tour-lj/explore-send-data | `icon-plus-circle` |

> [!WARNING]
> 26 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

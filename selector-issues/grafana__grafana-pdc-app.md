# Stable selectors for Grafana Pathfinder tutorials (3 anchors, 3 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (3)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `[aria-label="Private data source connect"]` | prometheus-lj/select-private-connection | `src/module.tsx:73`<br>`src/feature/datasource-config/components/DataSourceExtensionFieldAgent.tsx:87` |
| `[aria-label='Private data source connect']` | infinity-csv-lj/select-private-connection | `src/module.tsx:73`<br>`src/feature/private-networks/components/PrivateNetworkDetail/PrivateNetworkDetail.tsx:113` |
| `input[aria-label='Private data source connect']` | mysql-data-source-lj/test-connection | `src/module.tsx:73`<br>`src/feature/datasource-config/components/DataSourceExtensionFieldAgent.tsx:87` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

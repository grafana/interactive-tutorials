# Stable selectors for Grafana Pathfinder tutorials (2 anchors, 2 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (2)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `#auth-method-select` | prometheus-lj/config-authentication | `src/components/ConfigEditor/Auth/auth-method/AuthMethodSettings.tsx:147` |
| `#connection-url` | prometheus-lj/add-data-source-url | `src/components/ConfigEditor/Connection/ConnectionSettings.tsx:40`<br>`src/components/ConfigEditor/Connection/ConnectionSettings.tsx:60` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

# Stable selectors for Grafana Pathfinder tutorials (3 anchors, 1 tutorial)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (3)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `input[name='host']` | mysql-data-source-lj/configure-datasource | `src/configuration/ConfigurationEditor.tsx:77`<br>`src/configuration/ConfigurationEditor.tsx:80` |
| `input[placeholder='Password']` | mysql-data-source-lj/configure-datasource | `src/configuration/ConfigurationEditor.tsx:36`<br>`src/configuration/ConfigurationEditor.tsx:113` |
| `input[placeholder='Username']` | mysql-data-source-lj/configure-datasource | `src/configuration/ConfigurationEditor.tsx:104`<br>`src/configuration/ConfigurationEditor.tsx:108` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

# Stable selectors for Grafana Pathfinder tutorials (3 anchors, 4 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (3)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `[aria-label='Query editor owner']` | github-visualize-lj/build-issues-panel, github-visualize-lj/build-pr-panel +1 | `src/components/selectors.ts:12` |
| `[aria-label='Query editor repository']` | github-visualize-lj/build-issues-panel, github-visualize-lj/build-pr-panel +1 | `src/components/selectors.ts:15` |
| `input[placeholder='Personal Access Token']` | github-data-source-lj/config-github-datasource | `src/views/ConfigEditor.tsx:37`<br>`src/views/ConfigEditor.tsx:127` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

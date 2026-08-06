# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 1 tutorial)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (1)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `input[placeholder='https://feed']` | first-dashboard | `src/components/ConfigEditor/ConfigEditor.tsx:51` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

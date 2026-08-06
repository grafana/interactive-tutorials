# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 1 tutorial)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (1)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `label:contains('All spans')` | drilldown-traces-lj/view-distribution | `src/pages/Explore/primary-signals.ts:13`<br>_low confidence (matched `All spans`)_ |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

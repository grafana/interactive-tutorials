# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 1 tutorial)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `div[class*='connectionBanner']` | assistant-self-hosted | `apps/plugin/src/components/config/OSSSettings.tsx:305`<br>`apps/plugin/src/components/config/OSSSettings.tsx:306` |


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

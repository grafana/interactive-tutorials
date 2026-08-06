# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 2 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `a[href="/a/grafana-metricsdrilldown-app/drilldown"]` | prom-remote-write-lj/verify-metrics-query-works, prometheus-lj/verify-ds-connection | `src/App/Onboarding.tsx:52`<br>`src/App/assistant/questions.ts:7` |

> [!WARNING]
> 1 tutorial depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

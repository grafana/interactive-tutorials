# Stable selectors for Grafana Pathfinder tutorials (6 anchors, 3 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (6)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `#generate-alerts` | slo-quickstart | `src/components/Wizard/Alerts.tsx:35`<br>`src/components/Wizard/Alerts.tsx:46` |
| `a[href="/a/grafana-slo-app/wizard/review"]` | create-availability-slo-lj/configure-targets | `src/utils/grafanaExtensions.tsx:73`<br>`src/utils/grafanaExtensions.tsx:125` |
| `input[name="name"]` | create-availability-slo-lj/configure-targets | `src/pages/SloReports/Report.tsx:23`<br>`src/pages/SloReports/Report.tsx:27` |
| `input[name="objective"]` | create-availability-slo-lj/configure-targets | `src/pages/ManageSlos.tsx:25`<br>`src/pages/SloPerformance.tsx:36` |
| `input[name="timeWindow"]` | create-availability-slo-lj/create-availability-slo | `src/components/Alerting/CollapseAlertRuleLabels.tsx:23`<br>`src/components/Alerting/CollapseAlertRuleLabels.tsx:24` |
| `textarea[name="description"]` | create-availability-slo-lj/configure-targets | `src/pages/SloReports/Report.tsx:24`<br>`src/pages/SloReports/Report.tsx:27` |

> [!WARNING]
> 2 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

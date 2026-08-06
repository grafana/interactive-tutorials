# Stable selectors for Grafana Pathfinder tutorials (4 anchors, 4 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.

## Add a `data-testid` (3)

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:text('Next')` | otel-fleet-management | `src/feature/remote-configuration/components/edit/ConfigurationWizard.test.tsx:125`<br>_low confidence (matched `Next`)_ |
| `#collector-status-filter` | fleet-mgt-monitor-health-lj/check-health-status, fleet-mgt-monitor-health-lj/determine-config | `src/feature/collector-list/components/CollectorListStatusFilter.tsx:50`<br>`src/feature/collector-list/components/CollectorListStatusFilter.tsx:55`<br>**✅ live** 2026-08-06: present on the fleet inventory tab |
| `[aria-label="Search collectors"]` | fleet-mgt-monitor-health-lj/determine-config | `src/feature/collector-list/components/CollectorListBar/SearchInput.tsx:114`<br>`src/feature/remote-configuration/components/drawer/MatchedCollectorsTab.tsx:173` |

## Anchor gone — renamed or removed? (1)

Not found in source, bundle, or a live stack (2026-08-06). Tell us the new selector, or we'll re-record the step.

| anchor | tutorials | searched for |
|---|---|---|
| `div[data-testid='alloy-advanced-integrations-block']+button` | mongodb-integration-lj/configure-alloy | `alloy-advanced-integrations-block` |

> [!WARNING]
> 13 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

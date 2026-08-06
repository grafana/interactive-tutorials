# Stable selectors for Grafana Pathfinder tutorials (4 anchors, 4 tutorials)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:text('Next')` | otel-fleet-management | _component not located by search — the value only appears in test/fixture files or is built dynamically; you'll know the component_ |
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

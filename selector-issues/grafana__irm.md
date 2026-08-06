# Stable selectors for Grafana Pathfinder tutorials (1 anchor, 1 tutorial)

[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor their steps to DOM selectors. We've identified that the guides mentioned below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes in your plugin however data-testids give us a more robust path forwards.

## Add `data-testid`s to the following JSX

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at 2026-08-04/05) |
|---|---|---|
| `button:text("Acknowledge")` | grafana-irm-configuration-lj/run-end-to-end-test | `packages/@plugins/grafana-irm-app/src/pages/Integrations/Apps/OnCallSlackAdditionalFields.tsx:18`<br>`packages/@plugins/grafana-oncall-app/src/pages/incidents/Incidents.tsx:376`<br>_low confidence (matched `Acknowledge`)_ |

### FYI — we'll retarget these ourselves, just don't rename the replacements (3)

- `div:text("Wait")` → existing hook `data-pathfinder="wait-delay-select"` — packages/@grafana-irm/features/src/escalation-chains/components/Policy/EscalationPolicy.tsx:483
- `div:text("Notify users from on-call schedule")` → existing hook `data-pathfinder="notify-users-select"` — packages/@grafana-irm/features/src/escalation-chains/components/Policy/EscalationPolicy.tsx:335
- `div:text("Notify users")` → existing hook `data-pathfinder="notify-users-select"` — packages/@grafana-irm/features/src/escalation-chains/components/Policy/EscalationPolicy.tsx:335

> [!WARNING]
> 5 tutorials depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.


---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.

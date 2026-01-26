# Selector Issue Tracker

Issues with selectors that need developer attention (e.g., missing `data-testid` attributes, tiny highlight areas).

---

## Issue 1: Integration Tiles - Multiple Elements Share Same `href`

**Learning Journey:** Linux Server Integration

### Description
Integration tiles on the "Add new connection" page don't have unique `data-testid` attributes. Multiple elements share the same `href`, requiring `:nth-match(1)` workaround.

### Details
- **Instance:** learn.grafana.net
- **Page URL:** /connections/add-new-connection
- **Steps to reproduce:** Navigate to Connections > Add new connection, search for an integration

### Affected Selectors
```
a[href='/connections/add-new-connection/linux-node']:nth-match(1)
```

### Observed Behavior
Without `:nth-match(1)`, the highlight jumps around or targets the wrong element. The list scrolls unexpectedly.

### Expected Behavior
Each integration tile should have a unique `data-testid` like `data-testid='integration-tile-linux-node'`.

### Severity
- [ ] Blocking (cannot complete LJ)
- [x] Degraded (works with workaround but fragile)
- [ ] Minor (cosmetic)

---

## Issue 2: OS Distribution Dropdown - Tiny Highlight Area

**Learning Journey:** Linux Server Integration

### Description
The OS distribution dropdown (`collector-os-selection`) has `data-testid` on the container, but the clickable area requires targeting the `input` inside, resulting in a tiny highlight.

### Details
- **Instance:** learn.grafana.net
- **Page URL:** /connections/add-new-connection/linux-node
- **Steps to reproduce:** Navigate to Linux Server integration setup page

### Current Selector
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='collector-os-selection'] input",
  "requirements": ["exists-reftarget"],
  "doIt": false
}
```

### Observed Behavior
Highlight appears as a tiny area around the input field, not the full dropdown.

### Expected Behavior
`data-testid` should be on the clickable dropdown element itself, or highlight should encompass the full dropdown container.

### Severity
- [ ] Blocking (cannot complete LJ)
- [x] Degraded (works but looks wrong)
- [ ] Minor (cosmetic)

---

## Issue 3: Architecture Dropdown - Tiny Highlight Area

**Learning Journeys:** Linux Server Integration, macOS Integration

### Description
The architecture dropdown (`collector-arch-selection`) has `data-testid` on the container, but the clickable area requires targeting the `input` inside, resulting in a tiny highlight.

### Details
- **Instance:** learn.grafana.net
- **Page URL:** /connections/add-new-connection/linux-node, /connections/add-new-connection/macos-node
- **Steps to reproduce:** Navigate to Linux Server or macOS integration setup page

### Current Selector
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='collector-arch-selection'] input",
  "requirements": ["exists-reftarget"],
  "doIt": false
}
```

### Observed Behavior
Highlight appears as a tiny area around the input field, not the full dropdown.

### Expected Behavior
`data-testid` should be on the clickable dropdown element itself.

### Severity
- [ ] Blocking (cannot complete LJ)
- [x] Degraded (works but looks wrong)
- [ ] Minor (cosmetic)

---

## Issue 4: Installation Method Dropdown - Tiny Highlight Area

**Learning Journey:** macOS Integration

### Description
The installation method dropdown (`collector-installation-method`) has `data-testid` on the container, but targeting the `input` inside results in a tiny highlight.

### Details
- **Instance:** learn.grafana.net
- **Page URL:** /connections/add-new-connection/macos-node
- **Steps to reproduce:** Navigate to macOS integration setup page

### Current Selector
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='collector-installation-method'] input",
  "requirements": ["exists-reftarget"],
  "doIt": false
}
```

### Observed Behavior
Highlight appears as a tiny area around the input field, not the full dropdown.

### Expected Behavior
`data-testid` should be on the clickable dropdown element itself.

### Severity
- [ ] Blocking (cannot complete LJ)
- [x] Degraded (works but looks wrong)
- [ ] Minor (cosmetic)

---

*Last updated: January 26, 2026*

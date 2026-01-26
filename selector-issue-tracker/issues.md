# Selector Issue Tracker

> Track selectors that need dev team fixes (missing testIDs, tiny highlight areas, etc.)
> 
> **Workflow:** Add issues here → Create GitHub issues from this file → Remove when fixed

---

## Open Issues

### Issue 1: OS Distribution Dropdown - Tiny Highlight Area

**Title:** Unable to record OS distribution dropdown in Linux Server integration

**Instance:** Grafana Cloud (any stack)

**Page URL:** `/connections/add-new-connection/linux-node`

**Steps to record:**
1. Navigate to Connections > Add new connection
2. Search for "Linux Server" and click the tile
3. Try to record clicking the OS distribution dropdown (Debian/RedHat)

**Observed behavior:**
Recording produces selector `div[data-testid='collector-os-selection'] input` which highlights only a tiny area (the hidden input element) instead of the full dropdown component. The "Show me" highlight is barely visible to users.

**Interactive JSON:**
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='collector-os-selection'] input",
  "content": "Select the **operating system** that matches your Linux distribution.",
  "tooltip": "Select your Linux distribution (Debian for Ubuntu/Debian, RedHat for RHEL/Fedora/CentOS).",
  "requirements": ["exists-reftarget"],
  "doIt": false
}
```

**Console logs:** N/A

**Severity:** Medium - Affects user experience but guide still functions

**Additional context:**
- Learning Journey: `linux-server-integration`
- Milestone: `select-platform`
- The parent `div[data-testid='collector-os-selection']` exists but targeting it doesn't highlight the clickable dropdown area properly
- **Suggested fix:** Add a `data-testid` to the visible/clickable dropdown element itself, not just the wrapper div

---

### Issue 2: Architecture Dropdown - Tiny Highlight Area

**Title:** Unable to record Architecture dropdown in Linux Server integration

**Instance:** Grafana Cloud (any stack)

**Page URL:** `/connections/add-new-connection/linux-node`

**Steps to record:**
1. Navigate to Connections > Add new connection
2. Search for "Linux Server" and click the tile
3. Try to record clicking the Architecture dropdown (Amd64/Arm64)

**Observed behavior:**
Recording produces selector `div[data-testid='collector-arch-selection'] input` which highlights only a tiny area (the hidden input element) instead of the full dropdown component. The "Show me" highlight is barely visible to users.

**Interactive JSON:**
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "div[data-testid='collector-arch-selection'] input",
  "content": "Select the **architecture** that matches your system.",
  "tooltip": "Select Amd64 for x86_64 systems or Arm64 for aarch64 systems.",
  "requirements": ["exists-reftarget"],
  "doIt": false
}
```

**Console logs:** N/A

**Severity:** Medium - Affects user experience but guide still functions

**Additional context:**
- Learning Journey: `linux-server-integration`
- Milestone: `select-platform`
- Same issue as OS dropdown - the testID is on wrapper div, not the clickable element
- **Suggested fix:** Add a `data-testid` to the visible/clickable dropdown element itself

---

### Issue 3: Linux Server Tile - Requires Index-Based Selector

**Title:** Unable to record Linux Server tile without `:nth-match(1)`

**Instance:** Grafana Cloud (any stack)

**Page URL:** `/connections/add-new-connection`

**Steps to record:**
1. Navigate to Connections > Add new connection
2. Search for "Linux Server"
3. Try to record clicking the Linux Server tile

**Observed behavior:**
Recording produces selector `a[href='/connections/add-new-connection/linux-node']` but without `:nth-match(1)`, the page exhibits strange scrolling behavior (list scrolls up then down) and highlights the wrong element. This indicates multiple elements share the same `href`, requiring an index-based selector which is fragile.

**Interactive JSON:**
```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[href='/connections/add-new-connection/linux-node']:nth-match(1)",
  "content": "Click on the **Linux Server** tile to select it.",
  "requirements": ["exists-reftarget"]
}
```

**Console logs:** N/A

**Severity:** Low - Works with `:nth-match(1)` but fragile if tile order changes

**Additional context:**
- Learning Journey: `linux-server-integration`
- Milestone: `select-platform`
- Multiple `<a>` elements have `href='/connections/add-new-connection/linux-node'` on the page
- **Suggested fix:** Add a unique `data-testid` to the integration tile, e.g., `data-testid="integration-tile-linux-node"`

---

## Resolved Issues

_Move issues here once fixed, with the PR/commit that resolved them._

| Issue | Resolution | PR/Commit | Date |
|-------|------------|-----------|------|
| _Example_ | _Added data-testid to dropdown_ | _#1234_ | _2026-01-15_ |

---

## Quick Reference: Issue Severity

| Severity | When to use |
|----------|-------------|
| **Low** | Minor inconvenience - guide works, just not ideal |
| **Medium** | Affects user experience but guide still functions |
| **High** | Guide is broken or produces incorrect results |
| **Critical** | Blocks publishing or causes errors |

---

*Last updated: January 26, 2026*

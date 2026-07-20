# Selector discovery notes — interactive-dashboards-lj

Selectors verified live at **learn.grafana.net** (Grafana 12.4+ sidebar dashboard options flow).

## Verification status

| Milestone | Status |
|-----------|--------|
| create-query-variable | Live tested — sidebar flow verified |
| create-custom-variable | Live tested — sidebar + Custom Variable modal verified |
| use-variables-queries | Live tested — panel menu noop, doIt on Run/Save/Exit; Back to dashboard skippable |
| chain-variables | Live tested — Classic query note added; Regex placeholder is not a value |
| configure-display-options | Live tested — Label/Display/Multi as noop (Pathfinder flaky); Sort copy fixed |
| test-variable-interactions | Live tested — Share uses `new share button`; doIt on variable/Share; view mode required for Share |

## Key selectors — sidebar dashboard options flow (Grafana 12.4+)

| UI element | Selector |
|------------|----------|
| Edit / Exit edit | `[data-testid='data-testid Edit dashboard button']` |
| Dashboard options (right sidebar gear) | `button[data-testid='data-testid Dashboard Sidebar options button']` |
| Add variable (sidebar Variables section) | `button[data-testid='data-testid add variable button']` |
| Variable type: Query | `[data-testid='data-testid variable type query'] button` |
| Variable type: Custom | `[data-testid='data-testid variable type custom'] button` |
| Variable name | `input[data-testid='data-testid variable name input']` |
| Variable label (sidebar) | `input[data-testid='data-testid variable label input']` — correct testid (verified in Safari Inspect); Pathfinder `exists-reftarget` still flaky → guide uses `noop` |
| Variable Display select | Testid exists (`Variable editor Display select`) but Pathfinder `exists-reftarget` fails on combobox — guide uses `noop` |
| Multi-value / Include All | Same Pathfinder visibility failures on switches — guide uses `noop`; inspect later if restoring highlights |
| Open query variable editor | `button[data-testid='data-testid Query Variable editor open button']` |
| Data source picker | `[data-testid='data-testid Select a data source']` |
| Query refresh | `[data-testid='data-testid Variable editor Form Query Refresh select']` |
| Query preview | `button[data-testid='data-testid Query Variable editor preview button']` |
| Close query editor | `button[data-testid='data-testid Query Variable editor close button']` |
| Save dashboard | `[data-testid='data-testid Save dashboard button']` |
| Panel menu (any title) | `button[data-testid*='Panel menu']` |
| Panel menu → Edit | `a[data-testid='data-testid Panel menu item Edit']` |
| Share (view mode, Grafana 11.1+) | `[data-testid='data-testid new share button']` — not legacy `share-button` |
| Open custom variable editor | `button[data-testid='data-testid custom-variable-options-open-button']` |
| Custom CSV options input (in modal) | `[data-testid='data-testid custom-variable-input']` |
| Custom Apply (modal) | `button[data-testid='data-testid custom-variable-apply-button']` |

## Deprecated — full settings page flow

**Do not use** for variables on learn.grafana.net. The Variables tab shows:
"Variable settings have moved to the dashboard's sidebar."

| Deprecated element | Old selector |
|--------------------|--------------|
| View all settings → Variables tab | `a[data-testid='data-testid Tab Variables']` |
| Add variable (empty list CTA) | `[data-testid='data-testid Call to action button Add variable']` |
| Variable type dropdown | `[data-testid='data-testid Variable editor Form Type select']` |
| Apply / Back to list | Full-page variable editor buttons |

## Known risks

1. **Variables section collapsed** — if **Add variable** isn't visible after **Dashboard options**, expand the **Variables** section in the pane.
2. **Query editor** — PromQL query entry uses a Monaco editor without a stable single-field test id; left as markdown instruction.
3. **Query Variable modal blocks docked sidebar** — `create-query-variable` pops out before the section and docks back after it (`renderer:pathfinder` conditional), matching `fleet-mgt-monitor-health-lj`. Pop out at start only; mid-flow popout resets step completion. Broader LJ popout norm is parked for a separate PR. **Open variable editor** has **Do it** enabled after popout.
4. **Variable list row click** — editing an existing variable requires clicking a row in the variables table; no stable generic selector — uses `noop` step.
5. **No Configure button (Grafana 12.4+)** — in dashboard edit mode, open the panel via **⋮ → Edit**, not a **Configure** button. Panel menu is often hover-only and title-specific, so `use-variables-queries` uses a `noop` for that step (guided highlight failed with Pathfinder's "hidden due to screen size" even on large viewports).
6. **Demo metrics may lack `environment`** — filtering with `environment="$environment"` can correctly return **No data** if the label is absent; Custom variables still work for teaching `$variable` syntax.
7. **Back to dashboard vs Exit edit** — **Back to dashboard** only exists in the panel editor. After **Save**, you may already be on the dashboard canvas; make that step `skippable` and follow with **Exit edit** (`Edit dashboard button` testid — same control, label toggles).

## Block Editor testing (`?dev=true`)

Pop out and Dock are **unnumbered** meta-steps outside the section (same as fleet LJs). Learners never see them on the website renderer.

### Known Pathfinder bug — Preview resets on pop out / dock

In Block Editor dev mode, **Pop out and Dock remount the BlockEditor** in the other surface (sidebar ↔ floating). Each new instance defaults `viewMode` to **`edit`** — only guide JSON is persisted to localStorage, not the active view mode. Result: switching from **Preview (eyeball)** to **Edit (pencil)** after pop out or dock.

- **Affects:** authors testing guides in Block Editor (`?dev=true`)
- **Does not affect:** learners (no Block Editor; pop out shows the guide renderer only)
- **Workaround:** click **Preview** again after pop out or dock
- **Fix (Pathfinder):** persist `viewMode` across panel-mode handoffs, or share editor state between sidebar/floating BlockEditor mounts — [grafana-pathfinder-app#1290](https://github.com/grafana/grafana-pathfinder-app/issues/1290)

### Known Pathfinder bug — floating panel scroll jumps on large highlights

On **Refresh** (and similar modal steps), clicking **Show me** draws a highlight on `[data-testid='data-testid Variable editor Form Query Refresh select']`, which wraps the whole **Refresh** row — the orange box is intentionally large. If the floating guide overlaps that highlight, Pathfinder's `useHighlightDodge` may **reposition** the panel or switch it to **compact** mode (`height: auto`). When the highlight clears or updates (e.g. after selecting **On dashboard load**), the panel restores to **full** and the guide **scroll resets to the top**. Step progress is not lost; scroll back to your step.

- **Workaround:** skip **Show me** on Refresh/Preview; read the instruction and act manually, then mark the step complete.
- **Authoring option:** convert optional modal config steps (Refresh, Preview) to markdown-only like the Query step — avoids dodge entirely.
- **Fix (Pathfinder):** preserve floating-panel scroll position across compact ↔ full transitions; consider tighter highlight targets for radio/toggle groups — [grafana-pathfinder-app#1291](https://github.com/grafana/grafana-pathfinder-app/issues/1291)

## Pathfinder test order

1. Import `interactive-dashboards-lj/create-query-variable/content.json`
2. Then `create-custom-variable`, `use-variables-queries`, `chain-variables`, `configure-display-options`, `test-variable-interactions`

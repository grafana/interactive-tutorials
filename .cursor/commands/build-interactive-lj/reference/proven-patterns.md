# Proven Patterns - Appendix

Reusable JSON structures for common Grafana UI elements. These were validated through real testing.

> ⚠️ **IMPORTANT:** These are **templates**, not copy-paste solutions. You MUST use Playwright 
> browser tools to verify each selector exists on the actual page before using it. Selectors 
> can change between Grafana versions.

---

## Navigation Patterns

### Multi-Level Menu Navigation

Use `multistep` with `data-testid` nav links for **2-level navigation** (parent → child). Multisteps highlight each step, then click, allowing the nav section to expand before the next step.

```json
{
  "type": "multistep",
  "content": "Navigate to **Drilldown > Logs** from the main menu.",
  "requirements": ["navmenu-open"],
  "steps": [
    { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/drilldown']" },
    { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/a/grafana-lokiexplore-app/explore']" }
  ]
}
```

> ✅ **Why this pattern works:**
> - Uses `data-testid` (stable, intentional test hook)
> - Uses `href` (predictable routes)
> - Works whether menu sections are expanded or collapsed
> - Multisteps are inherently highlight-only; Pathfinder handles the click timing

### Multi-Level Navigation Works Reliably

Even deeply nested paths like **Administration > Plugins and data > Plugins** work with multisteps:

```json
{
  "type": "multistep",
  "content": "Navigate to **Administration > Plugins and data > Plugins**.",
  "steps": [
    { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/admin']" },
    { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/admin/plugins']" },
    { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/plugins']" }
  ],
  "requirements": ["navmenu-open"]
}
```

> ❌ **Don't use expand button selectors** (`button[aria-label*='section:']`)
> 
> Expand buttons **toggle** state — they collapse if already expanded. This breaks navigation when the section is already in the "wrong" state. Always use link selectors instead.

### Common Navigation Selectors

| Destination | href | Full Selector |
|-------------|------|---------------|
| Connections | `/connections` | `a[data-testid='data-testid Nav menu item'][href='/connections']` |
| Add new connection | `/connections/add-new-connection` | `a[data-testid='data-testid Nav menu item'][href='/connections/add-new-connection']` |
| Data sources | `/connections/datasources` | `a[data-testid='data-testid Nav menu item'][href='/connections/datasources']` |
| Dashboards | `/dashboards` | `a[data-testid='data-testid Nav menu item'][href='/dashboards']` |
| Explore | `/explore` | `a[data-testid='data-testid Nav menu item'][href='/explore']` |
| Drilldown | `/drilldown` | `a[data-testid='data-testid Nav menu item'][href='/drilldown']` |
| Alerts & IRM | `/alerts-and-incidents` | `a[data-testid='data-testid Nav menu item'][href='/alerts-and-incidents']` |
| Alerting | `/alerting` | `a[data-testid='data-testid Nav menu item'][href='/alerting']` |
| Alert rules | `/alerting/list` | `a[data-testid='data-testid Nav menu item'][href='/alerting/list']` |
| Observability | `/observability` | `a[data-testid='data-testid Nav menu item'][href='/observability']` |
| Application (App O11y) | `/a/grafana-app-observability-app` | `a[data-testid='data-testid Nav menu item'][href='/a/grafana-app-observability-app']` |

---

## Form Patterns

### Search/Filter Input

ALWAYS use `aria-label` for search inputs, NOT `placeholder`:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label=\"Search [description]\"]",
  "targetvalue": "[search term]",
  "content": "In the search box, type **[term]** to filter the results.",
  "requirements": ["exists-reftarget"]
}
```

**Why:** `placeholder` text can change; `aria-label` is more stable.

### Text Input Fields

For labeled form fields:

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label=\"[Field label]\"]",
  "targetvalue": "[value]",
  "content": "Enter **[value]** in the [field name] field.",
  "requirements": ["exists-reftarget"]
}
```

---

## Button Patterns

### Button by Text (Stable Text)

When a button has consistent, visible text:

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "[Button Text]",
  "content": "Click **[Button Text]** to [action].",
  "requirements": ["exists-reftarget"]
}
```

**Examples:** "Install", "Save", "Create", "Add", "Apply"

### Button by data-testid (Preferred)

When a button has a `data-testid` attribute:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid=\"[testid-value]\"]",
  "content": "Click **[Button name]** to [action].",
  "requirements": ["exists-reftarget"]
}
```

### Icon-Only Button

For buttons with only an icon (no text), use `aria-label`:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[aria-label=\"[Action description]\"]",
  "content": "Click the **[icon name]** icon to [action].",
  "requirements": ["exists-reftarget"]
}
```

---

## Link/Tile Patterns

### Card or Tile Selection

For clickable cards/tiles with href:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[href=\"/[path]\"]",
  "content": "Click the **[Tile name]** tile to select it.",
  "requirements": ["exists-reftarget"]
}
```

---

## Markdown Patterns

### Conditional UI (Multiple Paths)

When user must choose between options:

```json
{
  "type": "markdown",
  "content": "**Choose your option:**\n\n- **Option A**: [description]\n- **Option B**: [description]"
}
```

**Why:** Can't predict user's choice.

### External Actions

When user must do something outside the browser:

```json
{
  "type": "markdown",
  "content": "**On your machine:**\n\n1. [Step 1]\n2. [Step 2]\n3. [Step 3]"
}
```

**Why:** Can't automate outside the browser.

### Conditional Buttons

When a button only appears after user completes a prior action:

```json
{
  "type": "markdown",
  "content": "After [completing the action], click **[Button]** to continue."
}
```

**Why:** Button may not exist when automation runs.

### Verification/Confirmation Steps

When user needs to verify something worked:

```json
{
  "type": "markdown",
  "content": "If successful, you'll see: **[success message]**"
}
```

---

## Integration Setup Patterns

These patterns are specific to integration/data source setup learning paths (Linux, Windows, macOS, MySQL, etc.):

### Alloy Installation Expand Button

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid=\"agent-config-button\"]",
  "content": "Click **Run Grafana Alloy** to expand the installation options.",
  "requirements": ["exists-reftarget"]
}
```

### Token Creation → Use Markdown

Token dialogs have multiple paths (create new vs use existing):

```json
{
  "type": "markdown",
  "content": "**Create or select a token:**\n\n- **Create new token**: Click \"Create new token\", enter a name, then click \"Create token\".\n- **Use existing token**: Click \"Use an existing token\" and enter your token."
}
```

### Test Connection → Use Markdown

Conditional on real-world installation:

```json
{
  "type": "markdown",
  "content": "After installation completes, click **Test connection** to verify."
}
```

---

## Connections / Data Source Patterns

### Add New Data Source Button

The "Add new data source" button has a stable `data-testid`. Always prefer it over button text:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "[data-testid='data-testid data-source-add-button']",
  "content": "Click **Add new data source**."
}
```

### Data Source Name Input

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[data-testid='data-testid Data source settings page name input field']",
  "targetvalue": "My Data Source",
  "content": "Enter a name for the data source.",
  "doIt": false
}
```

> Use `"doIt": false` here since the user should enter their own name.

### Filter Data Sources by Name/Type

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[placeholder='Filter by name or type']",
  "targetvalue": "Infinity",
  "content": "In the filter box, type **Infinity** to find the data source."
}
```

### Search Connections by Name

```json
{
  "type": "interactive",
  "action": "formfill",
  "reftarget": "[aria-label='Search connections by name']",
  "targetvalue": "Infinity",
  "content": "In the search box, type **Infinity** to filter the connections."
}
```

### Connection/Plugin Tile Link

Use the `href` for the specific data source plugin page:

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[href='/connections/datasources/yesoreyeram-infinity-datasource/']",
  "content": "Click the **Infinity** tile to select it."
}
```

---

## Dashboard Patterns

### Create New Dashboard

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "New",
  "content": "Click **New** to open the creation menu."
},
{
  "type": "interactive",
  "action": "button",
  "reftarget": "New dashboard",
  "content": "Click **New dashboard** to create a dashboard."
}
```

### Add Visualization Panel

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Panel",
  "content": "Click **Panel** to add a new visualization."
}
```

---

## Section and Noop Patterns

### Section with Mixed Automated and Manual Steps

Use `section` to group steps that should be numbered sequentially. Mix `interactive`, `multistep`, and `noop` blocks inside:

```json
{
  "type": "section",
  "blocks": [
    {
      "type": "interactive",
      "action": "noop",
      "content": "Sign in to your Grafana Cloud account."
    },
    {
      "type": "multistep",
      "content": "Navigate to **Connections > Data sources**.",
      "requirements": ["navmenu-open"],
      "steps": [
        { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/connections']" },
        { "action": "highlight", "reftarget": "a[data-testid='data-testid Nav menu item'][href='/connections/datasources']" }
      ]
    },
    {
      "type": "interactive",
      "action": "highlight",
      "reftarget": "[data-testid='data-testid data-source-add-button']",
      "content": "Click **Add new data source**."
    }
  ]
}
```

### Observation/Verification (Use Markdown, Not Noop)

Observations are not directives — they should be `markdown`, not `noop`:

```json
{
  "type": "markdown",
  "content": "You should receive a **Health check successful** message."
}
```

### Instructional Manual Step as Numbered Step

When a step describes a manual action within a procedure:

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "Enter a title and description for your dashboard, select a folder if applicable, and click **Save**."
}
```

---

## Supplementary Content Patterns

### More to Explore

```json
{
  "type": "markdown",
  "content": "---\n\n### More to explore (optional)\n\n- [Grafana Dashboards](/docs/grafana/latest/dashboards/)"
}
```

### Related Paths

```json
{
  "type": "markdown",
  "content": "---\n\n### Related paths\n\nConsider taking the following paths after you complete this journey.\n\n- [Explore metrics using Metrics Drilldown](/docs/learning-paths/drilldown-metrics/)"
}
```

### Troubleshooting

```json
{
  "type": "markdown",
  "content": "---\n\n### Troubleshooting\n\nExplore the following troubleshooting topics if you need help:\n\n- [There are no patterns](/docs/grafana-cloud/visualizations/simplified-exploration/logs/troubleshooting/#there-are-no-patterns)"
}
```

---

## Quick Decision Guide

| UI Element | Pattern to Use |
|------------|----------------|
| Navigate through menus | `multistep` with `navmenu-open` |
| Search/filter input | `formfill` with `aria-label` or `placeholder` |
| Button with stable text | `button` action |
| Button with data-testid | `highlight` with data-testid |
| Clickable card/tile | `highlight` with `a[href="..."]` |
| Non-interactive numbered step | `noop` inside a `section` |
| Manual step (show but don't auto-do) | interactive with `doIt: false` |
| User chooses between options | `markdown` |
| Action outside browser | `markdown` |
| Button that may not exist yet | `markdown` |
| Supplementary links section | `markdown` with `---` divider + H3 heading |

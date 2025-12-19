# Requirements Reference

This comprehensive guide covers all supported requirements for interactive guide elements. Requirements control when interactive elements become enabled.

## Core Concepts

- **Requirements**: Specified as arrays: `"requirements": ["req1", "req2"]`
- **Validation**: All requirements must pass for the element to become enabled
- **Live checking**: Requirements are continuously monitored and re-evaluated
- **User feedback**: Failed requirements show helpful explanations with "Fix this" or "Retry" buttons

---

## Navigation and UI State Requirements

### `navmenu-open`

**Purpose**: Ensures the navigation menu is open and visible.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "a[data-testid='data-testid Nav menu item'][href='/connections']",
  "requirements": ["navmenu-open"],
  "content": "Click Connections in the left-side menu."
}
```

**Explanation when failed**: "The navigation menu needs to be open and docked. Click 'Fix this' to automatically open and dock the navigation menu."

**Note**: This requirement is auto-fixable—a "Fix this" button can automatically open the menu.

### `exists-reftarget`

**Purpose**: Verifies the target element specified in `reftarget` exists on the page.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Save dashboard",
  "requirements": ["exists-reftarget"],
  "content": "Save your dashboard changes."
}
```

**Explanation when failed**: "The target element must be visible and available on the page."

### `form-valid`

**Purpose**: Ensures the current form on the page passes validation.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Save",
  "requirements": ["form-valid"],
  "content": "Save your configuration."
}
```

**Explanation when failed**: "Please fix form validation errors before proceeding."

---

## Page and Navigation Requirements

### `on-page:<path>`

**Purpose**: Ensures the user is on a specific page or URL path.

```json
{
  "type": "interactive",
  "action": "highlight",
  "reftarget": "button[data-testid='add-panel-button']",
  "requirements": ["on-page:/dashboard"],
  "content": "Add a new panel to your dashboard."
}
```

**Examples**:
- `on-page:/dashboard` - User must be on any dashboard page
- `on-page:/connections` - User must be on the connections page
- `on-page:/admin` - User must be on any admin page

**Explanation when failed**: "Navigate to the '{path}' page first."

---

## User Authentication and Permissions

### `is-logged-in`

**Purpose**: Ensures the user is authenticated.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/dashboards",
  "requirements": ["is-logged-in"],
  "content": "View your dashboards."
}
```

**Explanation when failed**: "You must be logged in to perform this action."

### `is-admin`

**Purpose**: Requires the user to have Grafana admin privileges.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/admin/users",
  "requirements": ["is-admin"],
  "content": "Open the user management page."
}
```

**Explanation when failed**: "You need administrator privileges to perform this action. Please log in as an admin user."

### `is-editor`

**Purpose**: Requires the user to have at least Editor role.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Save dashboard",
  "requirements": ["is-editor"],
  "content": "Save your dashboard changes."
}
```

**Explanation when failed**: "You need Editor permissions or higher to perform this action."

### `has-role:<role>`

**Purpose**: Checks if the user has a specific organizational role.

**Supported roles**:
- `admin` or `grafana-admin` - Grafana admin privileges
- `editor` - Editor permissions or higher
- `viewer` - Any logged-in user

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Create dashboard",
  "requirements": ["has-role:editor"],
  "content": "Create a new dashboard."
}
```

**Explanation when failed**: "You need {role} role or higher to perform this action."

### `has-permission:<permission>`

**Purpose**: Verifies the user has a specific Grafana permission.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/datasources/new",
  "requirements": ["has-permission:datasources:create"],
  "content": "Create a new data source."
}
```

**Explanation when failed**: "You need the '{permission}' permission to perform this action."

---

## Data Source Requirements

### `has-datasources`

**Purpose**: Ensures at least one data source is configured.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/dashboard/new",
  "requirements": ["has-datasources"],
  "content": "Create your first dashboard."
}
```

**Explanation when failed**: "At least one data source needs to be configured."

### `has-datasource:<identifier>`

**Purpose**: Checks for a specific data source by name or type.

**Search behavior**:
- Searches both name AND type fields (case-insensitive)
- First match wins (checks name first, then type)

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "prometheus-datasource",
  "requirements": ["has-datasource:prometheus"],
  "content": "Select your Prometheus data source."
}
```

**Examples**:
- `has-datasource:prometheus-main` - Matches name OR type "prometheus-main"
- `has-datasource:prometheus` - Matches any Prometheus data source
- `has-datasource:loki` - Matches any Loki data source

**Explanation when failed**: "The '{identifier}' data source needs to be configured first."

---

## Plugin and Extension Requirements

### `has-plugin:<pluginId>`

**Purpose**: Verifies a specific plugin is installed and enabled.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/a/volkovlabs-rss-datasource",
  "requirements": ["has-plugin:volkovlabs-rss-datasource"],
  "content": "Configure the RSS data source plugin."
}
```

**Examples**:
- `has-plugin:grafana-clock-panel` - Clock panel plugin
- `has-plugin:volkovlabs-rss-datasource` - RSS data source plugin
- `has-plugin:grafana-piechart-panel` - Pie chart panel plugin

**Explanation when failed**: "The '{pluginId}' plugin needs to be installed and enabled."

---

## Dashboard and Content Requirements

### `dashboard-exists`

**Purpose**: Ensures at least one dashboard exists in the current organization.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/dashboards",
  "requirements": ["dashboard-exists"],
  "content": "View your existing dashboards."
}
```

**Explanation when failed**: "At least one dashboard must exist. Create a dashboard first."

### `has-dashboard-named:<title>`

**Purpose**: Ensures a dashboard with a specific title exists.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/d/monitoring-overview",
  "requirements": ["has-dashboard-named:System Monitoring"],
  "content": "Open your monitoring dashboard."
}
```

**Explanation when failed**: "The dashboard '{title}' needs to exist first."

---

## System and Environment Requirements

### `has-feature:<toggle>`

**Purpose**: Checks if a Grafana feature toggle is enabled.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Query splitting",
  "requirements": ["has-feature:queryLibrary"],
  "content": "Use the query library feature."
}
```

**Explanation when failed**: "The '{feature}' feature needs to be enabled."

### `in-environment:<env>`

**Purpose**: Restricts functionality to specific Grafana environments.

```json
{
  "type": "interactive",
  "action": "navigate",
  "reftarget": "/admin/settings",
  "requirements": ["in-environment:development"],
  "content": "Access development settings."
}
```

**Examples**:
- `in-environment:development` - Development environment only
- `in-environment:production` - Production environment only
- `in-environment:cloud` - Grafana Cloud only

**Explanation when failed**: "This action is only available in the {env} environment."

### `min-version:<version>`

**Purpose**: Ensures Grafana version meets minimum requirements.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Scene app",
  "requirements": ["min-version:9.0.0"],
  "content": "Open the new scene-based application."
}
```

**Explanation when failed**: "This feature requires Grafana version {version} or higher."

---

## Variable Requirements

### `var-<variableName>:<expectedValue>`

**Purpose**: Checks if a guide variable has a specific value. Variables are set by `input` blocks.

```json
{
  "type": "section",
  "title": "Advanced configuration",
  "requirements": ["var-termsAccepted:true"],
  "blocks": []
}
```

**Syntax**: `var-{variableName}:{expectedValue}`

**Examples**:
- `var-termsAccepted:true` - Boolean variable must be `true`
- `var-experienceLevel:advanced` - Text variable must equal "advanced"
- `var-datasourceName:prometheus` - Variable must match specific value

**Explanation when failed**: "The variable '{variableName}' must be set to '{expectedValue}'."

---

## Sequential and Dependency Requirements

### `section-completed:<sectionId>`

**Purpose**: Creates dependencies between tutorial sections.

```json
{
  "type": "section",
  "id": "create-dashboard",
  "title": "Create Dashboard",
  "requirements": ["section-completed:setup-datasource"],
  "blocks": []
}
```

**Explanation when failed**: "Complete the '{sectionId}' section before continuing."

---

## Combining Multiple Requirements

Requirements can be combined in arrays. **All requirements must pass** for the element to be enabled.

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Delete user",
  "requirements": ["is-admin", "on-page:/admin/users", "exists-reftarget"],
  "content": "Remove the selected user."
}
```

### Common Combinations

**Navigation actions**:
```json
"requirements": ["navmenu-open", "exists-reftarget"]
```

**Admin actions**:
```json
"requirements": ["is-admin", "on-page:/admin", "exists-reftarget"]
```

**Data source actions**:
```json
"requirements": ["has-datasource:prometheus", "on-page:/explore", "exists-reftarget"]
```

---

## Objectives System

Objectives use the same syntax as requirements but serve a different purpose:

- **Requirements**: Gate when step CAN execute
- **Objectives**: Gate whether step NEEDS to execute (auto-completion)

```json
{
  "type": "interactive",
  "action": "button",
  "reftarget": "Install plugin",
  "requirements": ["exists-reftarget"],
  "objectives": ["has-plugin:grafana-clock-panel"],
  "content": "Install the clock panel plugin."
}
```

**Key behaviors**:
- If objectives are met, the step is auto-completed
- Objectives always take priority over requirements
- "Already done!" message is shown for auto-completed steps

---

## Validation Rules

### Limits

- **Maximum 10 requirements** per element

### Syntax Rules

- Fixed types (`is-admin`, `is-logged-in`, `is-editor`, `exists-reftarget`, `navmenu-open`, `has-datasources`, `dashboard-exists`, `form-valid`) cannot have arguments
- Parameterized types require an argument after the colon
- Path arguments (e.g., `on-page:`) should start with `/`
- Version arguments should be semver format (e.g., `11.0.0`)
- Variable arguments use format `var-{variableName}:{expectedValue}`

### Common Errors

| Invalid              | Error                  | Fix                                     |
|----------------------|------------------------|-----------------------------------------|
| `is-admin:true`      | Unexpected argument    | `is-admin`                              |
| `has-datasource:`    | Missing argument       | `has-datasource:prometheus`             |
| `has-datasource`     | Unknown type           | `has-datasource:X` or `has-datasources` |
| `on-page:dashboard`  | Invalid path format    | `on-page:/dashboard`                    |
| `min-version:latest` | Invalid version format | `min-version:11.0.0`                    |
| `var-myVar`          | Missing value          | `var-myVar:true`                        |

---

## Troubleshooting

### Common Issues

**"Requirements never pass"**:
- Check browser console for error messages
- Verify requirement syntax matches examples
- Ensure required elements/data actually exist

**"Requirements pass but shouldn't"**:
- Requirements may be cached—try refreshing
- Check for typos in requirement names
- Verify case sensitivity for identifiers

**"Fix this button doesn't work"**:
- Only certain requirements support automatic fixing (`navmenu-open`)
- Some fixes require specific user permissions

### Debug Tools

Enable development mode logging:
```javascript
localStorage.setItem('grafana-docs-debug', 'true');
// Reload page to see detailed logs
```

---

## See Also

- [JSON Guide Format](json-guide-format.md) - Root structure overview
- [Interactive Types](interactive-types.md) - Block and action types
- [JSON Block Properties](json-block-properties.md) - Complete property reference

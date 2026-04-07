# Request: Add data-testid to GitHub Data Source Plugin Query Editor

## Status: Resolved (workaround selectors provided)

Robby Milo provided alternative selectors that allow `highlight` actions without new `data-testid` attributes. The PR Time Field and Repositories Time Field use a custom dropdown from Grafana core (not plugin-specific), so proper `data-testid` attributes would need to be added there to benefit all plugins.

## Workaround Selectors (from Robby)

| Element | Selector |
|---------|----------|
| Query Type dropdown | `div[data-testid='query-editor-row'] div[aria-label='Query Type container'] input` |
| PR Time Field | `div[data-testid="query-editor-row"] div:nth-of-type(4) input` |
| Repositories Time Field | `div[data-testid="query-editor-row"] div:nth-of-type(2) input` |

**Note:** The Issues Time Field already has `data-testid="Query editor issues time field-input"`.

**Caveat:** The `nth-of-type` selectors for PR and Repositories Time Fields are positional and may break if the query editor layout changes. Proper `data-testid` attributes on the Grafana core dropdown would be a more stable long-term solution.

## Original Request

The `github-visualize` Pathfinder interactive guide needed stable selectors on the GitHub data source plugin's query editor dropdowns.

### Elements Originally Missing `data-testid`

| Element | Query Type | Original State | Suggested `data-testid` |
|---------|-----------|---------------|------------------------|
| Query Type dropdown | All | No testid, no aria-label | `Query editor query type` |
| Time Field dropdown | Pull Requests | No testid | `Query editor pull requests time field-input` |
| Time Field dropdown | Repositories | No testid | `Query editor repositories time field-input` |

### Affected Guides

- `github-visualize-lj/build-repository-panel` (Query Type, Time Field)
- `github-visualize-lj/build-issues-panel` (Query Type)
- `github-visualize-lj/build-pr-panel` (Query Type, Time Field)

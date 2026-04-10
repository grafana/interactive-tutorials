# Step 3: Create Recommender Mapping

Create a recommender mapping so the learning path appears in Pathfinder.

---

## When to Run This Step

Only run this step if Step 2 reported: **Recommender mapping: ❌ Not found**

If the mapping was found (✅), skip to Step 4.

---

## Autonomous Mapping Creation

**Automatically analyze the learning path and create the mapping without asking questions.**

### Decision Logic

1. **Recommender file** - Infer from the learning path's primary context:
   - Data source setup/connection → `connections-cloud.json` or `connections-oss.json`
   - Dashboard creation/visualization → `dashboards-cloud.json` or `dashboards-oss.json`
   - Query/exploration → `explore-cloud.json` or `explore-oss.json`
   - Alerting → `alerting-cloud.json` or `alerting-oss.json`
   - Observability features → `observability-cloud.json` or `observability-oss.json`

2. **URL pattern** - Infer from the learning path content:
   - If it mentions specific data source type → `/connections/datasources/[type]`
   - If it's about dashboards → `/dashboards`
   - If it's about exploration → `/explore`
   - If it's about a specific app plugin → `/a/[plugin-id]`
   - Default for dashboards → `/dashboards`

3. **Target platform** - Determine from the learning path:
   - Mentions "Grafana Cloud" throughout → Cloud only
   - Mentions "self-hosted" or "OSS" → OSS only
   - Generic/works for both → Both platforms

---

## Create Mapping Entry

Automatically create the mapping JSON:

**For Cloud:**
- File: `grafana-recommender/internal/configs/state_recommendations/[area]-cloud.json`

**For OSS:**
- File: `grafana-recommender/internal/configs/state_recommendations/[area]-oss.json`

**For Both:**
- Add to both `-cloud.json` and `-oss.json` files

**Mapping JSON structure:**

```json
{
  "title": "[Learning path title from _index.md]",
  "url": "https://grafana.com/docs/learning-paths/[slug]/",
  "description": "Step-by-step guide: [Learning path title].",
  "type": "learning-journey",
  "match": {
    "and": [
      {
        "urlPrefix": "[url-pattern]"
      },
      {
        "targetPlatform": "cloud" // or "oss"
      }
    ]
  }
}
```

---

## Insert Mapping

1. Read the target recommender file(s)
2. Parse the JSON
3. Find an appropriate location in the `rules` array (group with similar learning paths)
4. Insert the new mapping entry
5. Write the updated JSON back to the file
6. Validate JSON syntax

---

## Update Path Manifest with Targeting

After the recommender mapping is created (or an existing mapping is found), check whether a path-level `manifest.json` exists at `interactive-tutorials/[slug]-lj/manifest.json`. If it does, update it with targeting data derived from the recommender rule's `match` expression.

### Fields to Populate

1. **`startingLocation`** — Traverse the `match` expression depth-first, left-to-right and pick the first URL-bearing leaf:
   - `urlPrefix` value
   - First entry of `urlPrefixIn` array
   - If no URL can be derived, omit the field.

2. **`targeting.match`** — Copy the `match` object from the recommender rule verbatim.

3. **`testEnvironment.tier`** — Apply these inference rules:
   - `match` contains `"targetPlatform": "cloud"` → `"tier": "cloud"`
   - `match` contains `"targetPlatform": "oss"` → `"tier": "local"`
   - `match` contains `source: "play.grafana.org"` → `"tier": "cloud"`, `"instance": "play.grafana.org"`
   - Otherwise → `"tier": "cloud"` (default)

### Example

Given this recommender rule:

```json
{
  "match": {
    "and": [
      { "urlPrefixIn": ["/connections/add-new-connection/haproxy", "/connections/infrastructure"] },
      { "targetPlatform": "cloud" }
    ]
  }
}
```

Update the manifest:

```json
{
  "startingLocation": "/connections/add-new-connection/haproxy",
  "targeting": {
    "match": {
      "and": [
        { "urlPrefixIn": ["/connections/add-new-connection/haproxy", "/connections/infrastructure"] },
        { "targetPlatform": "cloud" }
      ]
    }
  },
  "testEnvironment": {
    "tier": "cloud"
  }
}
```

### When No Manifest Exists

If `manifest.json` does not exist (for example, when this step is run from `/build-interactive-lj` on a path that has not been migrated to the package format), skip this section and proceed to the completion summary.

---

## Completion

Display a summary showing: the recommender file modified, mapping title, URL pattern, platform, context, and whether the path manifest was updated with targeting. Ask the user if they're ready for the next step.

---

## Important Notes

- **JSON formatting:** Maintain consistent indentation (2 spaces) and formatting
- **Placement:** Insert learning-journey entries near other learning paths in the file
- **Validation:** After editing, validate JSON syntax before proceeding
- **Multiple platforms:** If "Both" is selected, ensure entries are identical except for `targetPlatform`

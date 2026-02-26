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
3. Find an appropriate location in the `rules` array (group with similar learning journeys)
4. Insert the new mapping entry
5. Write the updated JSON back to the file
6. Validate JSON syntax

---

## Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step 3 complete: Recommender Mapping Created

Added mapping to:
├── grafana-recommender/internal/configs/state_recommendations/[file].json

Mapping details:
├── Title: [title]
├── URL pattern: [pattern]
├── Platform: [cloud/oss/both]
└── Context: [area]

⏳ Next: Step 4 - Scaffold Content Files
   Ready to proceed? (Y/N)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Important Notes

- **JSON formatting:** Maintain consistent indentation (2 spaces) and formatting
- **Placement:** Insert learning-journey entries near other learning journeys in the file
- **Validation:** After editing, validate JSON syntax before proceeding
- **Multiple platforms:** If "Both" is selected, ensure entries are identical except for `targetPlatform`

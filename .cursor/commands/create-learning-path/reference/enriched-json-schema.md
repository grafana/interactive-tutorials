# Enriched JSON Schema (v2.0.0)

This document defines the structure for enriched `content.json` files that serve as the single source of truth for both the interactive Pathfinder experience and the Hugo website.

---

## What Changed from v1.0.0

Schema v2.0.0 adds a `website` key that contains Hugo front matter metadata. This eliminates the need to maintain separate markdown files — the generator script (`scripts/generate-hugo.mjs`) produces Hugo `index.md` files from the JSON.

| Field | v1.0.0 | v2.0.0 |
|-------|--------|--------|
| `schemaVersion` | `"1.0.0"` | `"2.0.0"` |
| `website` | Not present | Contains Hugo front matter metadata |
| `blocks` | Same | Same |

---

## Root-Level Schema

```json
{
  "schemaVersion": "2.0.0",
  "id": "[learning-path-slug]-[milestone-slug]",
  "title": "[Milestone Title]",
  "website": { ... },
  "blocks": [ ... ]
}
```

### Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schemaVersion` | string | Yes | `"2.0.0"` for enriched format |
| `id` | string | Yes | `[learning-path-slug]-[milestone-slug]` (kebab-case) |
| `title` | string | Yes | Milestone title (used by both Pathfinder and Hugo) |
| `website` | object | No | Hugo front matter metadata. If absent, the generator skips this file. |
| `blocks` | array | Yes | Content blocks (unchanged from v1.0.0) |

---

## The `website` Key

The `website` object maps directly to Hugo front matter fields. The generator converts it to YAML. Keys use snake_case to match Hugo's expected field names.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `menuTitle` | string | Short nav title (under 20 chars) |
| `description` | string | 1-2 sentence description starting with action verb |
| `weight` | number | Ordering weight (increments of 100) |
| `step` | number | Step number in the learning path sequence |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `keywords` | string[] | SEO keywords (3-5 terms) |
| `grafana` | object | Grafana-specific metadata (e.g., `{ "skip": true }`) |
| `cta` | object | Call-to-action configuration |
| `side_journeys` | object | Optional exploration links |
| `related_journeys` | object | Related learning paths (typically conclusion only) |
| `troubleshooting` | object | Standalone troubleshooting (outside CTA) |

### Auto-Generated Fields (do NOT include)

The generator adds these automatically:

| Field | Source |
|-------|--------|
| `layout: single-journey` | Always added |
| `pathfinder_data` | Derived from file path |
| `title` | Copied from root-level `title` |

---

## CTA Configuration

### Continue (default for intermediate steps)

```json
"cta": { "type": "continue" }
```

### Success (verification milestones)

```json
"cta": {
  "type": "success",
  "troubleshooting": {
    "title": "Explore the following troubleshooting topics if you need help:",
    "items": [
      {
        "title": "Problem description",
        "link": "/docs/grafana-cloud/.../troubleshoot/#specific-issue"
      }
    ]
  }
}
```

### Conclusion (final milestone)

```json
"cta": {
  "type": "conclusion",
  "image": {
    "src": "/media/docs/learning-journey/journey-conclusion-header-1.svg",
    "width": 735,
    "height": 175
  }
}
```

---

## Side Journeys

```json
"side_journeys": {
  "title": "More to explore (optional)",
  "heading": "At this point in your journey, you can explore the following paths:",
  "items": [
    { "title": "Link title", "link": "/docs/..." }
  ]
}
```

---

## Related Journeys (Conclusion Milestones)

```json
"related_journeys": {
  "title": "Related paths",
  "heading": "Consider taking the following paths after you complete this journey.",
  "items": [
    { "title": "Path title", "link": "/docs/learning-paths/path-name/" }
  ]
}
```

---

## Complete Example (Verification Milestone)

```json
{
  "schemaVersion": "2.0.0",
  "id": "linux-server-integration-install-alloy",
  "title": "Install Grafana Alloy",
  "website": {
    "menuTitle": "Install Alloy",
    "description": "Learn how to install Grafana Alloy",
    "weight": 300,
    "step": 4,
    "cta": {
      "type": "success",
      "troubleshooting": {
        "title": "Explore the following troubleshooting topics if you need help:",
        "items": [
          {
            "title": "Common errors when executing Alloy installation script",
            "link": "/docs/grafana-cloud/.../troubleshoot/#common-errors"
          }
        ]
      }
    },
    "side_journeys": {
      "title": "More to explore (optional)",
      "heading": "At this point in your journey, you can explore the following paths:",
      "items": [
        { "title": "What is Grafana Alloy?", "link": "/oss/alloy-opentelemetry-collector" }
      ]
    }
  },
  "blocks": [
    {
      "type": "markdown",
      "content": "Introductory text..."
    },
    {
      "type": "section",
      "blocks": [
        {
          "type": "interactive",
          "action": "highlight",
          "reftarget": "button[data-testid='agent-config-button']",
          "content": "Click **Run Grafana Alloy**."
        }
      ]
    }
  ]
}
```

---

## Complete Example (Conclusion Milestone)

```json
{
  "schemaVersion": "2.0.0",
  "id": "linux-server-integration-end-linux-server",
  "title": "Destination reached!",
  "website": {
    "menuTitle": "Destination reached!",
    "description": "Your journey concludes",
    "weight": 900,
    "step": 10,
    "cta": {
      "type": "conclusion",
      "image": {
        "src": "/media/docs/learning-journey/journey-conclusion-header-1.svg",
        "width": 735,
        "height": 175
      }
    },
    "related_journeys": {
      "title": "Related paths",
      "heading": "Consider taking the following paths after you complete this journey.",
      "items": [
        { "title": "Explore data using Metrics Drilldown", "link": "/docs/learning-paths/drilldown-metrics/" }
      ]
    },
    "side_journeys": {
      "title": "More to explore (optional)",
      "heading": "The world is your oyster! Read more about how you can:",
      "items": [
        { "title": "Monitor alerts", "link": "/docs/grafana-cloud/alerting-and-irm/alerting/monitor-status" }
      ]
    }
  },
  "blocks": [
    {
      "type": "markdown",
      "content": "Congratulations on completing this journey!..."
    }
  ]
}
```

---

## Block Types (Unchanged from v1.0.0)

See `build-interactive-lj/reference/json-schema.md` for full block type reference:

| Type | Purpose | Has "Do it"? |
|------|---------|--------------|
| `markdown` | Explanatory text | No |
| `interactive` | Automated UI actions | Yes |
| `multistep` | Sequential navigation | Yes |
| `guided` | User performs manually | No |

---

## When to Omit the `website` Key

Omit the `website` key for milestones that need hand-written Hugo markdown with shortcodes (`{{< collapse >}}`, `{{< shared >}}`, etc.). The generator skips these files, and you maintain the markdown manually.

Typical examples: dashboard reference pages, alert reference pages — content-heavy milestones that use Hugo-specific rendering features not representable in JSON.

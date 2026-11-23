# Courses

This directory holds course source files: one `course.json` per course and a
single `badges.json`. They are published to the interactive-learning CDN under
`courses/` as-is. No CI step builds platform indexes from them.

## Structure

```
courses/
  badges.json                           ← all badges
  <course-id>/
    course.json                         ← one per course
```

## Adding a course

1. Create `courses/<id>/course.json` using the shape below.
2. If the course awards a new badge, append it to `courses/badges.json`.
3. Open a PR.

### `course.json`

```jsonc
{
  "schemaVersion": "1.0.0",
  "id": "getting-started",
  "title": "Getting started with Grafana",
  "description": "Build your first dashboard.",
  // Each entry is either a bare package ID (resolved via the plugin's
  // package-engine) or an absolute https:// URL (rendered as an external-
  // link guide). Pathfinder distinguishes via `entry.startsWith('http')`.
  "guides": [
    "welcome-to-grafana",
    "first-dashboard-rss",
    "https://grafana.com/docs/learning-paths/getting-started/"
  ],
  "guideMetadata": {
    "welcome-to-grafana": { "title": "Welcome", "estimatedMinutes": 5 },
    "first-dashboard-rss": { "title": "First dashboard", "estimatedMinutes": 10 }
  },
  "badgeId": "grafana-fundamentals",
  "targetPlatform": "oss",     // "oss" | "cloud" — omit for both
  "estimatedMinutes": 25,
  "icon": "grafana"
}
```

### `badges.json`

```jsonc
{
  "schemaVersion": "1.0.0",
  "badges": [
    {
      "id": "grafana-fundamentals",
      "title": "Grafana Fundamentals",
      "description": "Complete the \"Getting started with Grafana\" course",
      "icon": "grafana",
      "emoji": "🎓",                       // optional; preferred over Grafana icon when set
      "trigger": { "type": "path-completed", "pathId": "getting-started" }
    }
    // … one entry per badge
  ]
}
```

Trigger types:

- `{ "type": "guide-completed", "guideId": "<id>" }` — `guideId` optional (any guide if omitted)
- `{ "type": "path-completed", "pathId": "<course-id>" }`
- `{ "type": "streak", "days": <n> }`

## Schema versioning

`schemaVersion` is bumped only on **breaking** changes. Additive fields
are forward-compatible because plugin-side parsing uses Zod `.loose()`.

The authoritative schema lives in the plugin repo:
[`grafana-pathfinder-app/src/types/courses.schema.ts`](https://github.com/grafana/grafana-pathfinder-app/blob/main/src/types/courses.schema.ts).
Breaking schema changes must land in `interactive-tutorials` **before**
the plugin release that requires the new shape, or the CDN will start
serving content that the plugin rejects (and users will fall back to the
bundled offline course).

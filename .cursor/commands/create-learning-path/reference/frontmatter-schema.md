# Front matter schema reference (read-only source)

This document describes the legacy website `index.md` front matter fields for learning path milestones. It is a **read-only source reference**: use it to understand and read the front matter of existing learning path markdown in the `website` repo when converting a path with `/build-interactive-lj`.

Never write website markdown. These commands do not add `pathfinder_data`, insert the `{{< pathfinder/json >}}` shortcode, or otherwise modify the `website` repo. When converting, map the front matter fields described here into a `website.yaml` in the interactive-tutorials repo. Refer to `docs/website-yaml-reference.md` for the `website.yaml` field reference and to `../../learning-path-workflows/workflows.md` for the conversion workflow.

For `content.json` schema (root structure, block types, action types, field reference), see `build-interactive-lj/reference/json-schema.md`.

---

## Mapping front matter to `website.yaml`

When converting a legacy learning path, read each source file and map its front matter into a `website.yaml`:

| Source file | Maps to `website.yaml` |
|-------------|------------------------|
| Path overview `_index.md` | Path-level `<slug>-lj/website.yaml` |
| Milestone `index.md` | Step-level `<slug>-lj/<milestone>/website.yaml` |

Most fields carry over by name (`menuTitle`, `description`, `weight`, `step`, `journey`, `cta`, `related_journeys`, `side_journeys`). Two fields are legacy artifacts of Hugo/Pathfinder rendering and are **not** copied into `website.yaml`:

- `pathfinder_data` — the interactive package is located by directory convention, so this pointer isn't needed.
- `{{< pathfinder/json >}}` (page body) — the body is no longer rendered from the website; conceptual prose is captured in `content.json` markdown blocks instead.

`title` from the source front matter maps to the content package title (`content.json` `title`); `website.yaml` uses `menuTitle` as its title field. Refer to `docs/website-yaml-reference.md` for which fields the website build actually consumes.

---

## Legacy website front matter schema

In the legacy (pre-Pathfinder) format, every page in a learning path has Hugo front matter and `{{< pathfinder/json >}}` as the body. There are two page types: the path overview (`_index.md`) and milestones (`index.md`). The tables below describe the fields you'll read from existing markdown; the `{{< pathfinder/json >}}` body and `pathfinder_data` field are legacy artifacts you read but never write.

### Path Overview (`_index.md`) Fields

The `_index.md` is the landing page. It points to the path-level `content.json` via `pathfinder_data`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `menuTitle` | string | Yes | Short path name for navigation |
| `title` | string | Yes | Full path title (matches path-level content.json `title`) |
| `description` | string | Yes | 1-2 sentence path description |
| `weight` | number | Yes | Ordering weight among all learning paths |
| `journey` | object | Yes | Path metadata: `group`, `skill`, `source`, `logo` |
| `step` | number | Yes | Always `1` for the landing page |
| `layout` | string | Yes | Always `single-journey` |
| `cascade` | object | Yes | Always `{ layout: single-journey }` |
| `cta` | object | Yes | Always `{ type: start, title: "Are you ready?", cta_text: "Let's go!" }` |
| `keywords` | string[] | No | SEO keywords |
| `related_journeys` | object | No | Related prerequisite paths |
| `pathfinder_data` | string | Yes | Always `[slug]-lj` |

### Milestone (`index.md`) Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `menuTitle` | string | Yes | Short nav title (under 20 chars) |
| `title` | string | Yes | Full milestone title (matches content.json `title`) |
| `description` | string | Yes | 1-2 sentence description starting with action verb |
| `weight` | number | Yes | Ordering weight (increments of 100) |
| `step` | number | Yes | Step number in the learning path sequence |
| `layout` | string | Yes | Always `single-journey` |
| `cta` | object | Yes | Call-to-action configuration |
| `pathfinder_data` | string | Yes | Path to content.json directory: `[slug]-lj/[milestone]` |
| `keywords` | string[] | No | SEO keywords (3-5 terms) |
| `grafana` | object | No | Grafana-specific metadata (e.g., `{ skip: true }`) |
| `side_journeys` | object | No | Optional exploration links |
| `related_journeys` | object | No | Related learning paths (typically conclusion only) |

---

## CTA Configuration

### Start (path overview only)

```yaml
cta:
  type: start
  title: Are you ready?
  cta_text: Let's go!
```

### Continue (default for intermediate steps)

```yaml
cta:
  type: continue
```

### Success (verification milestones)

```yaml
cta:
  type: success
  troubleshooting:
    title: 'Explore the following troubleshooting topics if you need help:'
    items:
      - title: Problem description
        link: /docs/grafana-cloud/.../troubleshoot/#specific-issue
```

### Conclusion (final milestone)

```yaml
cta:
  type: conclusion
  image:
    src: /media/docs/learning-journey/journey-conclusion-header-1.svg
    width: 735
    height: 175
```

---

## Side Journeys

```yaml
side_journeys:
  title: More to explore (optional)
  heading: 'At this point in your journey, you can explore the following paths:'
  items:
    - title: Link title
      link: /docs/...
```

---

## Related Journeys (Conclusion Milestones)

```yaml
related_journeys:
  title: Related paths
  heading: Consider taking the following paths after you complete this journey.
  items:
    - title: Path title
      link: /docs/learning-paths/path-name/
```

---

## Complete examples (legacy source markdown)

The examples below show existing website markdown as it appears in the `website` repo. When converting, you read these files — you don't create or edit them. The `pathfinder_data` field and `{{< pathfinder/json >}}` body are legacy artifacts; the front matter fields map into a `website.yaml` (refer to `docs/website-yaml-reference.md`), and the conceptual prose maps into `content.json` markdown blocks.

### Path cover page

**linux-server-integration-lj/content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "linux-server-integration-lj",
  "title": "Monitor a Linux server in Grafana Cloud",
  "blocks": [
    {
      "type": "markdown",
      "content": "Welcome to the Grafana learning path that provides best practices for monitoring your Linux server.\n\nThis path involves implementing an integration that provides helpful alerts and pre-built dashboards to monitor metrics and logs for Linux servers."
    },
    {
      "type": "markdown",
      "content": "## Here's what to expect\n\nWhen you complete this path, you'll be able to:\n\n- Describe the benefits of using Grafana Cloud as your observability solution\n- Set up a Linux server integration and view telemetry data from your Linux server\n- Use pre-built dashboards and alerts to identify and troubleshoot problems in your environment"
    },
    {
      "type": "markdown",
      "content": "## Before you begin\n\nBefore you monitor a Linux server, ensure you have:\n\n- A Grafana Cloud account. To create an account, refer to [Grafana Cloud](https://grafana.com/signup/cloud/connect-account).\n- A Linux server running a supported distribution.\n- Configured your firewall to allow outbound HTTPS (port 443) to `*.grafana.net`."
    },
    {
      "type": "markdown",
      "content": "## Troubleshooting\n\nIf you get stuck, we've got your back! Where appropriate, troubleshooting information is just a click away."
    },
    {
      "type": "markdown",
      "content": "## More to explore\n\nWe understand you might want to explore other capabilities not strictly on this path. We'll provide you opportunities where it makes sense."
    }
  ]
}
```

**_index.md:**
```markdown
---
menuTitle: Monitor a Linux server
title: Monitor a Linux server in Grafana Cloud
description: Welcome to the Grafana learning journey that provides the best practice for setting up your Linux server integration.
weight: 100
journey:
  group: data-availability
  skill: Beginner
  source: Docs & blog posts
  logo:
    src: /media/docs/learning-journey/linux/linux-journey-2.png
step: 1
layout: single-journey
cascade:
  layout: single-journey
cta:
  type: start
  title: Are you ready?
  cta_text: Let's go!
pathfinder_data: linux-server-integration-lj
---

{{< pathfinder/json >}}
```

---

### Verification milestone

**content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "linux-server-integration-install-alloy",
  "title": "Install Grafana Alloy",
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

**index.md:**
```markdown
---
menuTitle: Install Alloy
title: Install Grafana Alloy
description: Learn how to install Grafana Alloy
keywords:
  - Grafana Alloy
  - installation
weight: 300
step: 4
layout: single-journey
cta:
  type: success
  troubleshooting:
    title: 'Explore the following troubleshooting topics if you need help:'
    items:
      - title: Common errors when executing Alloy installation script
        link: /docs/grafana-cloud/.../troubleshoot/#common-errors
side_journeys:
  title: More to explore (optional)
  heading: 'At this point in your journey, you can explore the following paths:'
  items:
    - title: What is Grafana Alloy?
      link: /oss/alloy-opentelemetry-collector
pathfinder_data: linux-server-integration-lj/install-alloy
---

{{< pathfinder/json >}}
```

---

### Conclusion milestone

**content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "linux-server-integration-end-linux-server",
  "title": "Destination reached!",
  "blocks": [
    {
      "type": "markdown",
      "content": "Congratulations on completing this journey!..."
    }
  ]
}
```

**index.md:**
```markdown
---
menuTitle: Destination reached!
title: Destination reached!
description: Your journey concludes
weight: 900
step: 10
layout: single-journey
cta:
  type: conclusion
  image:
    src: /media/docs/learning-journey/journey-conclusion-header-1.svg
    width: 735
    height: 175
related_journeys:
  title: Related paths
  heading: Consider taking the following paths after you complete this journey.
  items:
    - title: Explore data using Metrics Drilldown
      link: /docs/learning-paths/drilldown-metrics/
side_journeys:
  title: More to explore (optional)
  heading: 'The world is your oyster! Read more about how you can:'
  items:
    - title: Monitor alerts
      link: /docs/grafana-cloud/alerting-and-irm/alerting/monitor-status
pathfinder_data: linux-server-integration-lj/end-linux-server
---

{{< pathfinder/json >}}
```

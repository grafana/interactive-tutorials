# Front Matter Schema Reference

This document defines the website `index.md` front matter fields for learning path milestones.

For `content.json` schema (root structure, block types, action types, field reference), see `build-interactive-lj/reference/json-schema.md`.

---

## Website Front Matter Schema

Every page in a learning path has Hugo front matter and `{{< pathfinder/json >}}` as the body. There are two page types: the path overview (`_index.md`) and milestones (`index.md`).

### Path Overview (`_index.md`) Fields

The `_index.md` is the landing page. It points to `welcome/content.json` via `pathfinder_data`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `menuTitle` | string | Yes | Short path name for navigation |
| `title` | string | Yes | Full path title (matches welcome content.json `title`) |
| `description` | string | Yes | 1-2 sentence path description |
| `weight` | number | Yes | Ordering weight among all learning paths |
| `journey` | object | Yes | Path metadata: `group`, `skill`, `source`, `logo` |
| `step` | number | Yes | Always `1` for the landing page |
| `layout` | string | Yes | Always `single-journey` |
| `cascade` | object | Yes | Always `{ layout: single-journey }` |
| `cta` | object | Yes | Always `{ type: start, title: "Are you ready?", cta_text: "Let's go!" }` |
| `keywords` | string[] | No | SEO keywords |
| `related_journeys` | object | No | Related prerequisite paths |
| `pathfinder_data` | string | Yes | Always `[slug]-lj/welcome` |

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

## Complete Example (Welcome Page)

**welcome/content.json:**
```json
{
  "schemaVersion": "1.0.0",
  "id": "linux-server-integration-welcome",
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
pathfinder_data: linux-server-integration-lj/welcome
---

{{< pathfinder/json >}}
```

---

## Complete Example (Verification Milestone)

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

## Complete Example (Conclusion Milestone)

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

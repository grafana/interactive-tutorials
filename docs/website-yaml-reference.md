# Metadata reference for `website.yaml`

Each learning path directory (`<NAME>-lj/`) and each of its step subdirectories contains a `website.yaml` file.
This file carries metadata consumed by the `grafana/website` build.
It's unrelated to `manifest.json`, which controls in-product recommendation targeting.

There are two kinds of `website.yaml`:

- **Path-level**: `<NAME>-lj/website.yaml`. Describes the whole learning path.
- **Step-level**: `<NAME>-lj/<STEP>/website.yaml`. Describes a single step in the path.

## Path-level fields

### Required

| Field                     | Type   | Notes                                                                                                                                                                  |
| ------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `menuTitle`               | string | Short title. Read by breadcrumb, card, path-card, and learning-hub partials.                                                                                           |
| `weight`                  | int    | Hugo page weight. Read explicitly by the content adapter and used as the sort key in `layouts/partials/learning-hub/journey-row.html` (`sort .Pages "Params.weight"`). |
| `step`                    | int    | Always `1` at the path level. `single-journey-main.html` uses `eq .Params.step 1` to render the start CTA and skip pagination.                                         |
| `journey.group`           | string | One of `onboarding`, `data-availability`, `query-and-visualize`, `take-action`. Used by `layouts/learning-hub/home.html` for grouping and filtering.                   |
| `journey.skill`           | string | `Beginner` or `Intermediate`. Rendered on card / card-small / path-card. Defaults to `TBD` if missing.                                                                 |
| `journey.source`          | string | Free-text provenance label. Rendered as-is on the card. Defaults to `TBD` if missing. Convention: `Docs & blog posts`.                                                 |
| `journey.logo.src`        | string | Path to the path icon under `/static/img/menu/`. Read by card and card-small.                                                                                          |
| `journey.logo.background` | string | CSS color for the icon background.                                                                                                                                     |
| `journey.logo.width`      | int    | Icon width in pixels.                                                                                                                                                  |
| `journey.logo.height`     | int    | Icon height in pixels.                                                                                                                                                 |
| `cta.type`                | string | Always `start` at the path level. Selects the `start.html` partial in `single-journey-main.html`.                                                                      |
| `cta.title`               | string | Heading shown on the start CTA. Read by `start.html`.                                                                                                                  |
| `cta.cta_text`            | string | Button label on the start CTA. Read by `start.html`.                                                                                                                   |
| `description`             | string | One-sentence summary. Read explicitly by the content adapter and passed to Hugo as the page description (meta tags, listings).                                         |

### Optional

| Field                            | Type   | Notes                                                                                                                            |
| -------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `show_play`                      | bool   | Set to `false` to hide the play button. Defaults to shown when omitted. Read by `single-journey-main.html` and `path-card.html`. |
| `related_journeys.title`         | string | Heading for the related paths block. Conventionally `Related paths`. Rendered by `related-journeys.html`.                        |
| `related_journeys.heading`       | string | Lead-in sentence above the list.                                                                                                 |
| `related_journeys.items[].title` | string | Display title of the related path.                                                                                               |
| `related_journeys.items[].link`  | string | URL or site-relative path to the related path.                                                                                   |

### Not consumed (candidates for removal)

These fields appear in current `website.yaml` files but are not read by any template under [PR-31372](https://github.com/grafana/website/pull/31372):

| Field            | Notes                                                                                                                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `keywords`       | No template under `/docs/learning-paths/` reads `.Params.keywords`. Not surfaced as meta keywords by the docs layout.                                                                          |
| `cascade.layout` | The content adapter does not implement Hugo's `cascade` mechanism, and each step's `website.yaml` already sets its own `layout: single-journey`. Merged into `.Params.cascade` but never read. |

## Step-level fields

### Required

| Field         | Type   | Notes                                                                                                                                                 |
| ------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `menuTitle`   | string | Step title in the path sidebar. Read by breadcrumb, `nav.html`, and `pagination.html` via the `menuTitle` partial.                                    |
| `step`        | int    | 1-based step number. The path itself is `1`, so the first content step is typically `2`. Drives `single-journey` pagination, sidebar, and CTA gating. |
| `layout`      | string | Always `single-journey`. `layouts/docs/single.html` dispatches on it.                                                                                 |
| `cta.type`    | string | See [CTA types](#cta-types). `continue` is the default branch (no extra partial); `success` and `conclusion` select dedicated partials.               |
| `description` | string | One-sentence summary. Read explicitly by the content adapter and passed to Hugo as the page description.                                              |

### Optional

| Field                               | Type   | Notes                                                                                                                                       |
| ----------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `cta.image.src`                     | string | Optional banner image rendered above the step body by `single-journey-main.html`.                                                           |
| `cta.image.width`                   | int    | Image width in pixels.                                                                                                                      |
| `cta.image.height`                  | int    | Image height in pixels.                                                                                                                     |
| `cta.troubleshooting.title`         | string | Heading for the troubleshooting block shown after a `success` CTA when the user clicks the "not successful" option. Read by `success.html`. |
| `cta.troubleshooting.items[].title` | string | Display title of a troubleshooting link.                                                                                                    |
| `cta.troubleshooting.items[].link`  | string | URL of a troubleshooting link.                                                                                                              |
| `side_journeys.title`               | string | Heading for the side-trip block. Conventionally `More to explore (optional)`. Rendered by `side-journeys.html`.                             |
| `side_journeys.heading`             | string | Lead-in sentence above the list.                                                                                                            |
| `side_journeys.items[].title`       | string | Display title of the side trip.                                                                                                             |
| `side_journeys.items[].link`        | string | URL or site-relative path.                                                                                                                  |
| `side_journeys.items[].anchor`      | string | Optional fragment appended to the link.                                                                                                     |

### Not used by the website and to-be-removed

| Field      | Notes                                                                                                                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `weight`   | The content adapter assigns it as Hugo's page weight, but step navigation is filtered by `Params.step` in `pagination.html` and `nav.html`. No template iterates step children in weight order. |
| `layout`   | The content adapter sets `layout: single-journey` itself and overrides any value in `website.yaml`.                                                                                             |
| `keywords` | No template under `/docs/learning-paths/` reads `.Params.keywords` on step pages.                                                                                                               |

## CTA types

`cta.type` controls the button rendered at the bottom of the page.

| Value        | Used at                                | Meaning                                                           |
| ------------ | -------------------------------------- | ----------------------------------------------------------------- |
| `start`      | Path-level only.                       | Renders the "start the path" entry button.                        |
| `continue`   | Intermediate step.                     | Advances to the next step.                                        |
| `success`    | Intermediate step.                     | Marks a step as a verified checkpoint. Advances to the next step. |
| `conclusion` | Final step (typically `end-journey/`). | Closes the path.                                                  |

## Sourcing global defaults

The `success` and `conclusion` CTA partials do not read their copy from per-path `website.yaml`.
They read from `.CurrentSection.Parent.Params.cta.defaults.success` and `.Params.conclusion`, which live on the website repo's `content/docs/learning-paths/_index.md`.
This applies site-wide and is not configurable per path.

## Relationship to `manifest.json`

`website.yaml` and `manifest.json` are independent.
`manifest.json` controls in-product recommendation targeting and is not consumed by the website build.

### Possible future consolidation

The path-level `manifest.json` carries a `milestones` array that defines the canonical step order for the in-product PathFinder.
The website's `step:` (and `weight:`) fields duplicate this ordering.

The website also renders intro pages (`business-value`, `value-*`, `advantages-*`) that are deliberately excluded from `milestones`, so the two orderings aren't currently exactly the same.

A later change could have the content adapter derive step order from `manifest.milestones` and drop `step:` from step-level `website.yaml`.
That would require:

- Syncing `manifest.json` into `data/docs/interactive-learning/` alongside `content.json` and `website.yaml`.
- Deciding how website-only intro pages are represented (prelude list, manifest "context" milestone type, or directory convention).
- Reconciling any divergences between `step:` order and `milestones` order.

## Conventions

- The final step directory is conventionally named `end-journey/` (some paths use `end-<topic>/`).
  Its `cta.type` is `conclusion`.
- A path's `related_journeys` lives only at the path level.
  A step's analogous block is `side_journeys`.
- Path-level `weight` values are spaced (for example, 100, 200, 300) so paths can be reordered without renumbering.
- `description` should be a single sentence and avoid duplicating `menuTitle`.

## Minimal examples

Path-level, only the fields consumed by PR-31372:

```yaml
menuTitle: Monitor IIS web servers
weight: 255
step: 1
journey:
  group: data-availability
  skill: Beginner
  source: Docs & blog posts
  logo:
    src: /static/img/menu/grafana2.svg
    background: "#FFFFFF"
    width: 80
    height: 80
cta:
  type: start
  title: Are you ready?
  cta_text: Let's go!
description: Set up the IIS integration to monitor request rates, error rates, and worker process health.
```

Step-level, only the fields consumed by PR-31372:

```yaml
menuTitle: Configure IIS integration
step: 6
cta:
  type: success
description: Learn how to configure Grafana Alloy to collect IIS request rates, error codes, and worker process metrics.
```

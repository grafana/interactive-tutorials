---
alwaysApply: true
description: Overview of this repository and task routing for AI agents.
---

# Interactive Guides Repository

This repository contains interactive Grafana guides in JSON format. Each guide lives in its own directory with a `content.json` file defining the guide structure and a `manifest.json` file whose `targeting.match` controls where the guide is recommended. (`index.json` is frozen and no longer edited per guide -- a CI check fails any PR that changes it.)

Full reference documentation lives in `docs/`. AI-oriented references live in `.cursor/`.

## Critical Rules

1. **Use `navmenu-open`** for any step targeting navigation menu elements
2. **Use stable selectors** -- prefer `data-testid`, button text, and semantic attributes over CSS classes
3. **No markdown titles in guides** -- the guide `title` is rendered by the app frame; a leading `## Title` duplicates it
4. **No multistep singletons** -- a `multistep` with one step must be a plain `interactive` block
5. **Include `exists-reftarget` for selector-targeting steps** -- the repo convention is to list `exists-reftarget` in the `requirements` array for any block or step with a `reftarget`.
6. **Use sections, not markdown headers** -- group steps with `section` blocks, not `##` headings
7. **Include page requirements** -- page-specific actions need `on-page:/path`
8. **Verify state changes** -- use `verify` after save/create operations
9. **Keep prose brief** -- guides render in a sidebar; be direct and action-oriented
10. **Action-focused content** -- "Save your configuration" not "The save button can be clicked"
11. **Connect requirements and objectives** -- if section 1 creates a resource, section 2 should require it
12. **Tooltips** -- under 250 characters, one sentence, don't name the highlighted element
13. **`doIt: false` for secrets** -- never automate filling passwords, tokens, or API keys
14. **Section bookends** -- each `section` needs a 1-sentence "what you'll do" intro markdown block and a 1-sentence "what you learned" summary markdown block
15. **Bold only GUI names** -- "Click **Save & test**" not "Click the **Save & test** button"
16. **`skippable: true` for conditional steps** -- use for permission-gated steps and optional/conditional fields
17. **No focus-before-formfill** -- `highlight` on an input with `doIt: true` is a no-op; use `formfill` instead, or set `doIt: false`
18. **`schemaVersion` is optional** -- if included, use `"schemaVersion": "1.1.0"`; the schema defaults to `"1.1.0"` when omitted
19. **`popout` requires `targetvalue`** -- `popout` actions MUST set `targetvalue` to exactly `"sidebar"` or `"floating"`; the schema rejects any other value, and `popout` is not allowed inside `guided` blocks
20. **Use `openGuide`, not `?doc=`** -- to chain a follow-up guide after a `navigate` step, set `openGuide: "bundled:<guide-id>"` on the interactive block; the legacy `?doc=` query param is back-compat only
21. **`lazyRender` for virtualised targets** -- any step targeting a virtualised container (long tables, paginated lists, dashboard rows below the fold) MUST be inside a `guided` block with `lazyRender: true` on the step; plain `interactive` will fail because `exists-reftarget` cannot scroll

## Task Routing

| Task | Read First | Deep References |
|------|-----------|-----------------|
| Author/edit a guide | [authoring-guide.mdc](.cursor/authoring-guide.mdc) | [common-workflows.mdc](.cursor/common-workflows.mdc), [tutorial-patterns.mdc](.cursor/tutorial-patterns.mdc), [proven-patterns.mdc](.cursor/proven-patterns.mdc), [complete-example-tutorial.mdc](.cursor/complete-example-tutorial.mdc), [best-practices.mdc](.cursor/best-practices.mdc), `shared/snippets/`, `docs/` |
| Audit an existing guide | [audit-guide](.cursor/skills/audit-guide/SKILL.md) skill | [/lint](.cursor/commands/lint.md), [/check](.cursor/commands/check.md), [/attack](.cursor/commands/attack.md), [best-practices.mdc](.cursor/best-practices.mdc) |
| Update/modify an existing guide | [update-guide](.cursor/skills/update-guide/SKILL.md) skill | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [best-practices.mdc](.cursor/best-practices.mdc), [review-guide-pr.mdc](.cursor/review-guide-pr.mdc) |
| Review a guide PR | [review-guide-pr.mdc](.cursor/review-guide-pr.mdc) | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [best-practices.mdc](.cursor/best-practices.mdc), [edge-cases-and-troubleshooting.mdc](.cursor/edge-cases-and-troubleshooting.mdc), `docs/` |
| Review a learning path PR | [/review-learning-path-pr](.cursor/commands/review-learning-path-pr.md) | [review-learning-path](../skills/review-learning-path/SKILL.md), [audit-guide](../skills/audit-guide/SKILL.md), [review-guide-pr.mdc](.cursor/review-guide-pr.mdc) |
| Decision trees & code smells | [best-practices.mdc](.cursor/best-practices.mdc) | [authoring-guide.mdc](.cursor/authoring-guide.mdc), `docs/` |
| Create new guide | `/new` command | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [complete-example-tutorial.mdc](.cursor/complete-example-tutorial.mdc) |
| Validate guide | `/lint`, `/check`, `/attack` commands | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [best-practices.mdc](.cursor/best-practices.mdc) |
| Make a guide recommended | [how-to-write-recommendations.mdc](.cursor/how-to-write-recommendations.mdc) | `manifest.json`, [docs/manifest-reference.md](docs/manifest-reference.md) |
| Write/edit manifest.json | [docs/manifest-reference.md](docs/manifest-reference.md) | [authoring-guide.mdc](.cursor/authoring-guide.mdc) |
| Understand the system | [system-architecture.mdc](.cursor/system-architecture.mdc) | `docs/` |

## Reference Documentation (`docs/`)

| Document | Purpose |
|----------|---------|
| [json-guide-reference.md](docs/json-guide-reference.md) | Block types, properties, and guide structure |
| [interactive-actions.md](docs/interactive-actions.md) | Action type behavior and button controls |
| [requirements-reference.md](docs/requirements-reference.md) | All requirement types |
| [selectors-and-testids.md](docs/selectors-and-testids.md) | Stable selector patterns |
| [guided-interactions.md](docs/guided-interactions.md) | Detailed guided block documentation |
| [manifest-reference.md](docs/manifest-reference.md) | Manifest field reference and derivation rules |

## Historical Context

| Path | What |
|------|------|
| [`docs/history/`](docs/history/) | Completed project records (package migration, recommendation deduplication). Not needed for day-to-day work — consult only when investigating past design decisions or PR provenance. Do not use material from this directory as a basis for building new features. |

## Shared Content (`shared/`)

| Path | Purpose |
|------|---------|
| [shared/snippets/](shared/snippets/) | Pre-tested JSON blocks for common Grafana UI patterns (nav, save dashboard, datasource picker, tab navigation, drilldown nav, etc.) — copy and adapt rather than writing from scratch |
| [shared/templates/tutorial-datasources.json](shared/templates/tutorial-datasources.json) | Reusable tutorial data source template |

## Commands

| Command | Purpose |
|---------|---------|
| [/new](.cursor/commands/new.md) | Create a new guide from scratch |
| [/lint](.cursor/commands/lint.md) | Validate guide JSON structure |
| [/check](.cursor/commands/check.md) | Check guide quality against best practices |
| [/attack](.cursor/commands/attack.md) | Find issues by simulating confused users |
| [/review-learning-path-pr](.cursor/commands/review-learning-path-pr.md) | Full learning path PR review (audit, consistency, Playwright, Pathfinder, GitHub submit) |
| [/build-interactive-lj](.cursor/commands/build-interactive-lj/README.md) | Multi-phase learning journey builder |

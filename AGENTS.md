---
alwaysApply: true
description: Overview of this repository and task routing for AI agents.
---

# Interactive Guides Repository

This repository contains interactive Grafana guides in JSON format. Each guide lives in its own directory with a `content.json` file defining the guide structure, and an optional `index.json` entry controls where the guide is recommended.

Full reference documentation lives in `docs/`. AI-oriented references live in `.cursor/`.

## Critical Rules

1. **Use `navmenu-open`** for any step targeting navigation menu elements
2. **Use stable selectors** -- prefer `data-testid`, button text, and semantic attributes over CSS classes
3. **No markdown titles in guides** -- the guide `title` is rendered by the app frame; a leading `## Title` duplicates it
4. **No multistep singletons** -- a `multistep` with one step must be a plain `interactive` block
5. **`exists-reftarget` is auto-applied** -- never add it manually to requirements
6. **Use sections, not markdown headers** -- group steps with `section` blocks, not `##` headings
7. **Include page requirements** -- page-specific actions need `on-page:/path`
8. **Verify state changes** -- use `verify` after save/create operations
9. **Keep prose brief** -- guides render in a sidebar; be direct and action-oriented
10. **Connect requirements and objectives** -- if section 1 creates a resource, section 2 should require it

## Task Routing

| Task | Read First | Deep References |
|------|-----------|-----------------|
| Author/edit a guide | [authoring-guide.mdc](.cursor/authoring-guide.mdc) | [common-workflows.mdc](.cursor/common-workflows.mdc), [tutorial-patterns.mdc](.cursor/tutorial-patterns.mdc), `docs/` |
| Review a guide PR | [review-guide-pr.mdc](.cursor/review-guide-pr.mdc) | [authoring-guide.mdc](.cursor/authoring-guide.mdc), `docs/` |
| Create new guide | `/new` command | [authoring-guide.mdc](.cursor/authoring-guide.mdc) |
| Validate guide | `/lint`, `/check`, `/attack` commands | [authoring-guide.mdc](.cursor/authoring-guide.mdc) |
| Write index.json entry | [how-to-write-recommendations.mdc](.cursor/how-to-write-recommendations.mdc) | `index.json` |
| Understand the system | [system-architecture.mdc](.cursor/system-architecture.mdc) | `docs/` |

## Reference Documentation (`docs/`)

| Document | Purpose |
|----------|---------|
| [json-guide-format.md](docs/json-guide-format.md) | Root structure and block overview |
| [interactive-types.md](docs/interactive-types.md) | All block and action types |
| [json-block-properties.md](docs/json-block-properties.md) | Complete property reference |
| [requirements-reference.md](docs/requirements-reference.md) | All requirement types |
| [selectors-and-testids.md](docs/selectors-and-testids.md) | Stable selector patterns |
| [guided-interactions.md](docs/guided-interactions.md) | Detailed guided block documentation |

## Commands

| Command | Purpose |
|---------|---------|
| [/new](.cursor/commands/new.md) | Create a new guide from scratch |
| [/lint](.cursor/commands/lint.md) | Validate guide JSON structure |
| [/check](.cursor/commands/check.md) | Check guide quality against best practices |
| [/attack](.cursor/commands/attack.md) | Find issues by simulating confused users |

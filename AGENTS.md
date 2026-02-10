---
alwaysApply: true
description: Overview of this repository and guide authoring documentation.
---

# Interactive Guides Documentation

This repository contains interactive Grafana guides in JSON format, along with comprehensive documentation for AI systems to generate and assist with guide authoring.

## Documentation Structure

### Primary Documentation (`docs/`)

Comprehensive reference documentation:

| Document | Purpose |
|----------|---------|
| [json-guide-format.md](docs/json-guide-format.md) | Root structure and block overview |
| [interactive-types.md](docs/interactive-types.md) | All block and action types |
| [json-block-properties.md](docs/json-block-properties.md) | Complete property reference |
| [requirements-reference.md](docs/requirements-reference.md) | All requirement types |
| [selectors-and-testids.md](docs/selectors-and-testids.md) | Stable selector patterns |
| [guided-interactions.md](docs/guided-interactions.md) | Detailed guided block documentation |

### AI Quick References (`.cursor/`)

Slim references for AI assistance:

| File | Purpose |
|------|---------|
| [ai-guide-reference.mdc](.cursor/ai-guide-reference.mdc) | **Start here** - Quick reference with links |
| [action-types-reference.mdc](.cursor/action-types-reference.mdc) | Action type decision tree |
| [requirements-quick-reference.mdc](.cursor/requirements-quick-reference.mdc) | Requirement patterns |
| [selector-library.mdc](.cursor/selector-library.mdc) | Common selectors |
| [review-guide-pr.mdc](.cursor/review-guide-pr.mdc) | Reviewing PRs of Guides |
| [best-practices.mdc](.cursor/best-practices.mdc) | Authoring best practices |

### Patterns and Examples (`.cursor/`)

| File | Purpose |
|------|---------|
| [common-workflows.mdc](.cursor/common-workflows.mdc) | Reusable workflow templates |
| [tutorial-patterns.mdc](.cursor/tutorial-patterns.mdc) | Guide structure patterns |
| [complete-example-tutorial.mdc](.cursor/complete-example-tutorial.mdc) | Full guide example |
| [edge-cases-and-troubleshooting.mdc](.cursor/edge-cases-and-troubleshooting.mdc) | Handling complex scenarios |

### Commands (`.cursor/commands/`)

Agent commands for common tasks:

| Command | Purpose |
|---------|---------|
| [new.md](.cursor/commands/new.md) | Create new guide |
| [lint.md](.cursor/commands/lint.md) | Validate guide JSON |
| [check.md](.cursor/commands/check.md) | Check guide quality |
| [attack.md](.cursor/commands/attack.md) | Find issues in guide |

## Quick Start for AI

1. **Read** [ai-guide-reference.mdc](.cursor/ai-guide-reference.mdc) for essential patterns
2. **Reference** [docs/json-guide-format.md](docs/json-guide-format.md) for structure
3. **Use** [docs/requirements-reference.md](docs/requirements-reference.md) for requirements
4. **Follow** [best-practices.mdc](.cursor/best-practices.mdc) for quality

## JSON Guide Format

All guides use JSON format exclusively:

```json
{
  "id": "guide-id",
  "title": "Guide Title",
  "blocks": [
    { "type": "markdown", "content": "Introduction text" },
    { "type": "section", "id": "section-1", "title": "First Section", "blocks": [] }
  ]
}
```

## Essential Rules

1. **Use `navmenu-open`** for navigation menu elements
2. **Include page requirements** for page-specific actions
3. **Use stable selectors** - prefer `data-testid` over CSS classes
4. **Add tooltips** for educational value
5. **Make steps skippable** where appropriate

> **Note**: `exists-reftarget` is automatically applied for all DOM interactions—you don't need to add it manually.

## Block Types

| Category | Types |
|----------|-------|
| Content | `markdown`, `html` (use sparingly), `image`, `video` |
| Interactive | `interactive`, `multistep`, `guided` |
| Structural | `section`, `conditional`, `assistant` |
| Assessment | `quiz`, `input` |

## Action Types

| Action | Use Case |
|--------|----------|
| `highlight` | Click by CSS selector |
| `button` | Click by button text |
| `formfill` | Enter text in fields |
| `navigate` | Change pages |
| `hover` | Reveal hover-dependent UI |
| `noop` | Informational step (no DOM action) |

## Quick Reference Cards

### Action Selection
```
Click button with stable text → button action
Click element with stable selector → highlight action
Fill form field → formfill action
Navigate to page → navigate action
Reveal hover-hidden UI → hover action
Informational pause (no DOM action) → noop action
Multiple related actions → multistep action
User performs manually → guided action
Explain interface → highlight with doIt: false
AI-customizable content → assistant block
```

### Requirements Selection
```
Navigation element → navmenu-open
Page-specific → on-page:/path
Admin feature → is-admin
Data source exists → has-datasource:type
Data source connected → datasource-configured:type
Plugin installed → has-plugin:id
Plugin enabled → plugin-enabled:id
Rendering context → renderer:pathfinder
Sequential dependency → section-completed:id
```

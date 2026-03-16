# Interactive Tutorials — Claude Context

This repo contains Pathfinder interactive guide content for Grafana. Guides are JSON files (`content.json`) that drive a React-based interactive learning framework embedded in Grafana.

---

## Always Read First

Before working on any guide content, read these reference files — they are the authoritative source for all authoring rules, block types, selectors, and patterns:
- `.cursor/authoring-guide.mdc` — block types, action types, requirements, best practices, code smells
- `.cursor/selector-library.mdc` — CSS selector patterns and grading (Green/Yellow/Red)
- `.cursor/system-architecture.mdc` — architecture overview, content pipeline, block hierarchy

When reviewing a guide or doing QA, also read:
- `.cursor/review-guide-pr.mdc` — complete review protocol (sections 1-4 are blocking)
- `.cursor/edge-cases-and-troubleshooting.mdc` — known failure modes and fixes

For authoring new content, also read:
- `.cursor/tutorial-patterns.mdc` — reusable structural patterns
- `.cursor/common-workflows.mdc` — workflow templates for common Grafana operations
- `.cursor/complete-example-tutorial.mdc` — full worked example

---

## Slash Commands

These commands are defined in `.cursor/commands/`. When the user invokes one, read the corresponding file and follow its instructions.

| Command | File | What it does |
|---------|------|--------------|
| `/new` | `.cursor/commands/new.md` | Scaffold a new guide |
| `/check` | `.cursor/commands/check.md` | QA checklist: requirements, objectives, editorial review |
| `/attack` | `.cursor/commands/attack.md` | Simulate an inept/confused user; surface failure modes |
| `/lint` | `.cursor/commands/lint.md` | Lint guide JSON for structural issues |
| `/build-interactive-lj` | `.cursor/commands/build-interactive-lj/README.md` | Multi-phase learning journey builder |

---

## Skills

These are complex multi-phase workflows. When the user's request matches a skill, read the `SKILL.md` file listed and follow its workflow exactly. Skills use sub-agents and write intermediate artifacts to `assets/`.

### autogen-guide
**Trigger**: User provides GitHub links to React/TypeScript UI source code and wants a guide generated from it.

Read `.cursor/skills/autogen-guide/SKILL.md` — multi-phase pipeline: acquire → extract → plan → generate (per-section) → review → manifest.

Supporting files the sub-agents load:
- `.cursor/skills/autogen-guide/extraction-patterns.md`
- `.cursor/skills/autogen-guide/selector-strategies.md`

### autogen-guide-dashboard
**Trigger**: User provides a Grafana dashboard JSON (file, pasted, or URL) and wants a guide generated from it.

Read `.cursor/skills/autogen-guide-dashboard/SKILL.md` — same multi-phase pipeline adapted for dashboard JSON.

Supporting files the sub-agents load:
- `.cursor/skills/autogen-guide-dashboard/dashboard-extraction-patterns.md`
- `.cursor/skills/autogen-guide-dashboard/dashboard-selector-strategies.md`
- `.cursor/skills/autogen-guide-dashboard/dashboard-guide-rules.md`
- `.cursor/skills/autogen-guide-dashboard/dashboard-maintenance-flow.md`

### migrate-guide
**Trigger**: User wants to migrate a guide or learning path (`*-lj`) to the Pathfinder package format (add `manifest.json`).

Read `.cursor/skills/migrate-guide/SKILL.md` — generates `manifest.json` (and path-level `content.json` for LJs) from `content.json`, `index.json`, recommender rules (`grafana-recommender` repo), and website markdown.

Supporting reference: `docs/manifest-reference.md`

---

## Skill Memory Convention

Skills write intermediate analysis artifacts to `{output_dir}/assets/`. These are auto-generated and should not be edited. See `.cursor/skills/skill-memory.md` for the shared convention (manifest schema, frontmatter, Phase 0 drift detection).

---

## Key Files

- `docs/json-guide-format.md` — complete JSON format reference (remind users when they create new guides)
- `index.json` — guide targeting rules (read-only; used by migrate-guide)
- `docs/manifest-reference.md` — authoritative field derivation rules for manifests

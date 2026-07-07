# Claude Code Guide — interactive-tutorials

## Source of truth

This repository's authoring intelligence lives in [`.cursor/`](.cursor/) and [`docs/`](docs/). Both Claude Code and Cursor read these files; references use standard markdown links so both tools resolve them natively.

The canonical critical rules list (21 rules; all blocking) lives in [`AGENTS.md`](AGENTS.md#critical-rules). Cursor reads `AGENTS.md` as its entry point; Claude reads this file. **Read those rules before authoring or reviewing any guide — every rule there is blocking.**

When a doc here disagrees with the upstream schema, the schema wins. Authoritative schemas come from [`grafana-pathfinder-app`](https://github.com/grafana/grafana-pathfinder-app) (`src/types/json-guide.types.ts` and `src/types/json-guide.schema.ts`).

## Task Routing

| Task | Read first | Deep references |
|------|------------|-----------------|
| Author / edit a guide | [.cursor/authoring-guide.mdc](.cursor/authoring-guide.mdc) | [common-workflows.mdc](.cursor/common-workflows.mdc), [tutorial-patterns.mdc](.cursor/tutorial-patterns.mdc), [proven-patterns.mdc](.cursor/proven-patterns.mdc), [complete-example-tutorial.mdc](.cursor/complete-example-tutorial.mdc), [best-practices.mdc](.cursor/best-practices.mdc), [docs/](docs/) |
| Audit an existing guide | [audit-guide](.cursor/skills/audit-guide/SKILL.md) skill | [/lint](.cursor/commands/lint.md), [/check](.cursor/commands/check.md), [/attack](.cursor/commands/attack.md), [best-practices.mdc](.cursor/best-practices.mdc) |
| Update / modify an existing guide | [update-guide](.cursor/skills/update-guide/SKILL.md) skill | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [best-practices.mdc](.cursor/best-practices.mdc), [review-guide-pr.mdc](.cursor/review-guide-pr.mdc) |
| Review a guide PR | [.cursor/review-guide-pr.mdc](.cursor/review-guide-pr.mdc) | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [best-practices.mdc](.cursor/best-practices.mdc), [edge-cases-and-troubleshooting.mdc](.cursor/edge-cases-and-troubleshooting.mdc) |
| Review a learning path PR | [/review-learning-path-pr](.cursor/commands/review-learning-path-pr.md) | [review-learning-path](.cursor/skills/review-learning-path/SKILL.md), [audit-guide](.cursor/skills/audit-guide/SKILL.md) |
| Decision trees & code smells | [.cursor/best-practices.mdc](.cursor/best-practices.mdc) | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [docs/](docs/) |
| Create a new guide | [/new](.cursor/commands/new.md) command | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [complete-example-tutorial.mdc](.cursor/complete-example-tutorial.mdc) |
| Validate a guide | [/lint](.cursor/commands/lint.md), [/check](.cursor/commands/check.md), [/attack](.cursor/commands/attack.md) | [authoring-guide.mdc](.cursor/authoring-guide.mdc), [best-practices.mdc](.cursor/best-practices.mdc) |
| Make a guide recommended | [.cursor/how-to-write-recommendations.mdc](.cursor/how-to-write-recommendations.mdc) | `manifest.json`, [docs/manifest-reference.md](docs/manifest-reference.md) |
| Write / edit manifest.json | [docs/manifest-reference.md](docs/manifest-reference.md) | [authoring-guide.mdc](.cursor/authoring-guide.mdc) |
| Understand the system | [.cursor/system-architecture.mdc](.cursor/system-architecture.mdc) | [docs/](docs/) |
| Generate / migrate from source | [autogen-guide](.cursor/skills/autogen-guide/SKILL.md), [autogen-guide-dashboard](.cursor/skills/autogen-guide-dashboard/SKILL.md), [migrate-guide](.cursor/skills/migrate-guide/SKILL.md) | [shared/critical-rules.md](.cursor/skills/shared/critical-rules.md) |

## Reference Documentation (`docs/`)

| Document | Purpose |
|----------|---------|
| [docs/json-guide-reference.md](docs/json-guide-reference.md) | All 17 registered block types and their properties (plus `challenge`, a runtime-only block type in the `JsonBlock` union — 18 total in the union) |
| [docs/interactive-actions.md](docs/interactive-actions.md) | Action type behavior: `highlight`, `button`, `formfill`, `navigate`, `hover`, `noop`, `popout` |
| [docs/requirements-reference.md](docs/requirements-reference.md) | All requirement types (fixed + parameterized) |
| [docs/selectors-and-testids.md](docs/selectors-and-testids.md) | Stable selector patterns and pseudo-selectors |
| [docs/guided-interactions.md](docs/guided-interactions.md) | Guided block deep dive |
| [docs/manifest-reference.md](docs/manifest-reference.md) | Manifest field reference and derivation rules |

## Skills

Multi-phase workflow skills with their own `SKILL.md` files. Skills write intermediate artifacts to `{output_dir}/assets/`; see [.cursor/skills/skill-memory.md](.cursor/skills/skill-memory.md) for the shared convention.

- [.cursor/skills/autogen-guide/](.cursor/skills/autogen-guide/SKILL.md) — generate a guide from React/TypeScript source
- [.cursor/skills/autogen-guide-dashboard/](.cursor/skills/autogen-guide-dashboard/SKILL.md) — generate from a Grafana dashboard JSON
- [.cursor/skills/audit-guide/](.cursor/skills/audit-guide/SKILL.md) — comprehensive read-only audit (structural + semantic + adversarial) producing one prioritised report
- [.cursor/skills/update-guide/](.cursor/skills/update-guide/SKILL.md) — modify an existing guide with a planning checkpoint, review pass, and CLI-validated rollback
- [.cursor/skills/migrate-guide/](.cursor/skills/migrate-guide/SKILL.md) — migrate a guide or learning path to the Pathfinder package format

## Shared Content

- [shared/snippets/](shared/snippets/) — pre-tested JSON blocks for common Grafana UI patterns
- [shared/templates/tutorial-datasources.json](shared/templates/tutorial-datasources.json) — reusable data source template

## Historical Context

[`docs/history/`](docs/history/) — completed project records (package migration, recommendation deduplication). Not needed for day-to-day work — consult only when investigating past design decisions or PR provenance. Do **not** use material from this directory as a basis for new feature work.

## Pathfinder source

This repo's content is rendered by the Grafana Pathfinder app. Authoritative schemas, action handlers, and block parsers live in [`grafana-pathfinder-app`](https://github.com/grafana/grafana-pathfinder-app):

- `src/types/json-guide.types.ts` — TypeScript types for all blocks
- `src/types/json-guide.schema.ts` — Zod schemas (current `schemaVersion: "1.1.0"`)
- `src/types/requirements.types.ts` — requirement vocabulary
- `src/interactive-engine/action-handlers/` — action handlers (button, formfill, navigate, hover, popout, guided)
- `src/cli/utils/block-registry.ts` — `CLI_EXCLUDED_BLOCK_TYPES` (e.g., `grot-guide` is hand-authored in the block editor)

If a doc here disagrees with the schema, the schema wins. Validate locally from a Pathfinder CLI checkout:

```bash
node {pathfinder-app}/dist/cli/cli/index.js validate --packages .
```

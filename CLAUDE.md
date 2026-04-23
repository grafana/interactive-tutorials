@AGENTS.md

## Cursor Skills

This repo uses Cursor-format skills in `.cursor/skills/`. Each skill is a multi-phase workflow defined in a `SKILL.md` file. Available skills:

- `.cursor/skills/autogen-guide/` — generate a guide from React/TypeScript source code
- `.cursor/skills/autogen-guide-dashboard/` — generate a guide from a Grafana dashboard JSON
- `.cursor/skills/migrate-guide/` — migrate a guide or learning path to the Pathfinder package format

When a user's request matches a skill trigger, read the skill's `SKILL.md` and follow its workflow. Skills write intermediate artifacts to `{output_dir}/assets/`; see `.cursor/skills/skill-memory.md` for the shared convention.

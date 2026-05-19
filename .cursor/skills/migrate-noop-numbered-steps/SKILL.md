---
name: migrate-noop-numbered-steps
description: Migrate one published interactive learning path from noop workaround steps to Pathfinder numbered section content. Use when converting LPs away from `action: "noop"` or preparing one path-at-a-time PRs for numbered section step testing.
---

# Migrate Noop Numbered Steps

Use this skill to migrate one published interactive learning path at a time from `interactive` blocks with `action: "noop"` to `markdown` blocks that Pathfinder numbers inside sections.

This workflow is intentionally one-path-per-run. Stop for human testing before creating a PR.

## Invoke This Skill

Use this skill when the user asks to migrate a learning path away from `noop` steps, convert noops to numbered section steps, or continue the numbered-steps migration.

Example prompts:

- "Use the migrate-noop-numbered-steps skill on `prom-remote-write-lj`."
- "Migrate `mysql-data-source-lj` away from noop steps."
- "Continue the numbered section step migration for `visualization-metrics-lj`."
- "Create the PR for the tested `infrastructure-alerting-lj` noop migration."

If the user asks to "do the next one" or "continue the migration," first list the remaining published path packages that still contain `action: "noop"` and ask which path to migrate next.

## Scope

Only migrate a root learning path package with `manifest.json` containing `"type": "path"`.

For each run, the user must provide or approve:

- The path directory, for example `infrastructure-alerting-lj`.
- The branch name, or permission to create a branch named `migrate-<path>-numbered-steps`.

Do not batch multiple learning paths in one PR unless the user explicitly asks.

## Migration Rule

Convert only exact passive workaround blocks:

```json
{
  "type": "interactive",
  "action": "noop",
  "content": "..."
}
```

to:

```json
{
  "type": "markdown",
  "content": "..."
}
```

Preserve all other fields if present, except remove `action: "noop"`. Preserve block order and learner-facing content.

Do not change:

- Real interactive actions such as `highlight`, `button`, `formfill`, `navigate`, `hover`, or `popout`.
- Selectors, `reftarget`, `targetvalue`, `requirements`, `objectives`, IDs, manifests, path ordering, or prose.
- `noop` examples in docs, snippets, or non-target paths.

## Workflow

1. Verify the repo and branch state.
   - Work in `/Users/taylorcole/repos/interactive-tutorials`.
   - Check `git status --short --branch`.
   - If not already on a suitable branch, create a new branch before edits.

2. Inventory the target path.
   - Confirm `<path>/manifest.json` has `"type": "path"`.
   - Count `action: "noop"` in `<path>/**/content.json`.
   - Show the user the affected files and total count.
   - Ask for approval before applying edits.

3. Apply the migration surgically.
   - Edit only `<path>/**/content.json` files that contain `action: "noop"`.
   - Prefer a text-preserving transform so unrelated JSON formatting does not change.
   - Replace adjacent lines `"type": "interactive"` and `"action": "noop"` with `"type": "markdown"` only for matched blocks.

4. Validate before testing.
   - Parse all `<path>/**/content.json` files as JSON.
   - Confirm zero remaining `action: "noop"` in the target path.
   - Confirm every changed block is exactly an allowed conversion.
   - Run `git diff --check`.
   - Run Pathfinder CLI validation if available:

     ```bash
     node pathfinder-app/dist/cli/cli/index.js validate --package <path>
     ```

   - If the CLI is unavailable, report that clearly and continue to the manual test checkpoint.

5. Stop for human Pathfinder testing.
   - Tell the user what changed and what to test.
   - Ask the user to verify that numbered section steps render correctly.
   - Do not commit, push, or create a PR until the user approves.

6. After approval, create the PR.
   - Commit only the target path content files.
   - Do not include temporary snapshots, analysis files, or generated planning artifacts.
   - Push the branch.
   - Create a PR with a short body that summarizes the migration.

## Manual Test Checklist

Ask the user to verify:

- Former `noop` instructions appear in the right place.
- Section numbering is continuous across markdown and interactive blocks.
- Real interactive steps still show and work as expected.
- Sections with only former `noop` steps complete in a sensible way.

## PR Body Template

Use a short PR body:

```markdown
Migrates the <PATH_NAME> learning path from noop workaround steps to markdown content blocks so Pathfinder can render them as sequentially numbered section steps.
```

## Validation Script Pattern

Use this kind of semantic check before asking the user to test:

```python
import json
from pathlib import Path

root = Path("<path>")
remaining = 0

for content in [root / "content.json", *sorted(root.glob("*/content.json"))]:
    if not content.exists():
        continue
    data = json.loads(content.read_text())

    def count_noop(node):
        if isinstance(node, dict):
            return (1 if node.get("action") == "noop" else 0) + sum(count_noop(v) for v in node.values())
        if isinstance(node, list):
            return sum(count_noop(v) for v in node)
        return 0

    remaining += count_noop(data)

if remaining:
    raise SystemExit(f"remaining noop actions: {remaining}")
```

## Failure Handling

If validation finds unexpected changes, stop and restore the target path before continuing. Do not create a PR with partial or unverified conversions.

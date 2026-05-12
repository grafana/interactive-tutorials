# Change Request Schema

The `update-guide` skill accepts change requests in two forms: **free-text** (a natural-language description) or **structured** (a JSON spec matching one of the shapes below). Phase 2 resolves either into the same canonical `change-plan.md`.

Free-text is fine for most use. The structured shapes exist for callers (other skills, scripts, batch jobs) that want predictable parsing.

---

## Free-text examples

These resolve cleanly in Phase 2:

- "Add a markdown block at the end that says 'Thanks for trying this!'"
- "Add a Loki section after the Prometheus one. It should cover installing the Loki data source, writing a basic LogQL query, and viewing logs in Explore."
- "Add `lazyRender: true` to the step at `blocks[3].blocks[2]` and wrap it in a `guided` block."
- "Swap `has-datasource:prometheus` for `has-datasource:loki` in the section with id `query-editor`."
- "Remove the legacy `?doc=` query param from the navigate step at `blocks[5]` and replace it with `openGuide: \"bundled:next-steps\"`."

Phase 2's plan sub-agent infers `what / where / why` from the prose and from `assets/guide-structure.json`.

---

## Structured shapes

### `add-block`

Insert a new block at a specific path.

```json
{
  "action": "add-block",
  "at": { "parent": "blocks[2]", "position": "after-last-child" },
  "block": {
    "type": "markdown",
    "content": "..."
  },
  "rationale": "Section needs a summary bookend."
}
```

`at.position`: `before-first-child` | `after-last-child` | `before:<existing-id>` | `after:<existing-id>` | `index:<N>` (within `parent`'s `blocks` / `steps` / `whenTrue` / `whenFalse` array).

For new section blocks, the orchestrator generates a kebab-case `id` and adds it to `guide-structure.json` for uniqueness checks. The caller may specify `block.id` explicitly to override.

### `edit-block`

Modify fields of an existing block. Field replacement is shallow — to deep-merge, use multiple `edit-block` requests or fall back to `replace-block`.

```json
{
  "action": "edit-block",
  "at": "blocks[3].blocks[2]",
  "set": {
    "lazyRender": true,
    "scrollContainer": "div[data-testid='dashboards-table'] .scrollbar-view"
  },
  "unset": ["tooltip"],
  "rationale": "Targets a virtualised row; rule 21 retrofit."
}
```

`set`: fields to write (or overwrite). `unset`: fields to remove. Both optional but at least one must be present.

### `remove-block`

Delete a block at a specific path. Phase 2 must walk the tree for IDREFs to the removed block and surface them in the plan's `IDREFs Affected` section.

```json
{
  "action": "remove-block",
  "at": "blocks[4]",
  "rationale": "Section is obsolete; superseded by the new Loki section."
}
```

If removing the block would leave a dangling `section-completed:<id>` or `var-<name>` reference elsewhere, Phase 2 must either (a) propose a paired edit to remove the dangling reference, or (b) escalate the dangling reference to the plan's `Risks` section for user resolution before approval.

### `replace-section`

Replace a whole section block. Equivalent to `remove-block` + `add-block` at the same path, but atomic — the plan presents them together so the user sees the swap as one decision.

```json
{
  "action": "replace-section",
  "at": "blocks[3]",
  "new_section": {
    "type": "section",
    "id": "query-editor",
    "title": "Write your first PromQL query",
    "blocks": [/* ... */]
  },
  "rationale": "Rewrite the query-editor section for clarity."
}
```

If `new_section.id` differs from the removed section's id, Phase 2 must list every `section-completed:<old-id>` referrer in `IDREFs Affected` so the user can decide whether to renumber them too.

### `add-requirement`

Add a requirement (or objective) to one or more blocks. The plan resolves selectors and surfaces any that already have the requirement (idempotent — skip).

```json
{
  "action": "add-requirement",
  "to": ["blocks[2].blocks[*]", "blocks[3].blocks[*]"],
  "requirement": "navmenu-open",
  "kind": "requirements",
  "rationale": "Step targets navigate but missing navmenu-open."
}
```

`to`: array of paths or glob-ish patterns (`blocks[N]` for one, `blocks[N].blocks[*]` for all children, `blocks[*]` for all top-level). `kind`: `requirements` | `objectives`. `requirement`: the canonical string from `docs/requirements-reference.md`.

For `objectives`, Phase 2 must surface the requirement-vs-objective distinction in the plan's `Risks` section — adding an objective changes completion semantics, which is a higher-impact change than adding a requirement.

---

## Mixed requests

The `change_request` can also be a JSON array of structured changes, applied in order:

```json
[
  { "action": "add-block", "at": { "parent": "blocks[2]", "position": "after-last-child" }, "block": { "type": "markdown", "content": "..." } },
  { "action": "edit-block", "at": "blocks[3].blocks[0]", "set": { "skippable": true } }
]
```

Phase 2 resolves the array into a single `change-plan.md` with one `Edits` entry per array element, in order. Phase 3 applies them in order. Phase 5 validates the cumulative result.

For a sequence that depends on intermediate state (e.g., "add a new section, then add a step inside it"), use the new section's *id* (not its path) in subsequent entries — paths shift as adjacent blocks are inserted.

---

## What this schema does NOT support

- **Reorder blocks within a parent**. Use `remove-block` + `add-block` instead, or hand-edit.
- **Cross-guide changes**. Each invocation operates on one `guide_dir`.
- **Schema migrations**. If a guide is on `schemaVersion: "1.0.0"` and needs `"1.1.0"` features, use a separate migration pass first.
- **Manifest-only changes**. To change `manifest.json` without touching `content.json`, hand-edit the manifest and re-run `migrate-guide` to revalidate.

For these cases, fall back to free-text and let Phase 2 surface a `Risks` warning that the request is beyond schema scope.

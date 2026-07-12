# Severity Rubric

This rubric is the canonical definition of **blocking**, **warning**, and **info** severities for the audit-guide skill. All three audit phases (structural, semantic, adversarial) classify findings into these three buckets so Phase 5 can merge them consistently.

---

## Blocking

A blocking finding means the guide either **fails at runtime** or **violates a critical rule** in [AGENTS.md](../../../AGENTS.md). Block the merge until it is fixed.

| Phase | Examples |
|-------|----------|
| Structural | Invalid JSON; unknown block type; unknown action; missing required field (`reftarget` on non-noop/non-popout, `targetvalue` on `popout`); `popout` `targetvalue` not `"sidebar"` or `"floating"`; `schemaVersion` set to something other than `"1.1.0"` |
| Structural | Critical rules 4, 17, 19, 21 violations (multistep singleton, focus-before-formfill, `popout` validation, lazy-render missing) |
| Semantic | Critical rules 1, 3, 6, 7, 13 violations (missing `navmenu-open`, leading markdown title, markdown headers in place of sections, missing page requirements, `doIt: true` on secret fields) |
| Semantic | Rule 2 — CSS-class-only or auto-generated class selectors with no semantic fallback |
| Semantic | Dangling `section-completed:<id>` (referenced section does not exist) |
| Semantic | Dangling `var-<name>` requirement (no upstream `input` block defines the variable) |
| Semantic | First-action page anchor missing — first interactive step has no `on-page` requirement and is not a `navigate` action |
| Adversarial | Admin-only step without `skippable` in a mixed-audience guide |
| Adversarial | `popout` step inside a `guided` block (not supported) |
| Adversarial | `navigate` action inside a `guided` block (not supported) |
| Adversarial | A step blocks the entire guide for a user who has already completed the action (missing `objectives`) |

---

## Warning

A warning finding means the guide **degrades user experience** but does not hard-fail. Address before merge if possible; merge with follow-up issue otherwise.

| Phase | Examples |
|-------|----------|
| Structural | `interactive` step targeting a virtualised-looking selector (table row, `[data-cy='wb-list-item']`, `:contains(...)` in a list) without being inside a `guided` block with `lazyRender: true` — heuristic; needs human confirmation |
| Structural | `validateInput: true` without `formHint` (silent rejection on bad input) |
| Structural | Missing `verify` on a state-changing action (save, create, navigate) |
| Semantic | Critical rules 8, 9, 10, 11, 12, 14, 15, 16 violations (missing verify on state changes, prose verbosity, button word usage, weak requirement→objective chain, tooltip naming the element, no section bookends, button-word bolding, non-skippable conditional steps) |
| Semantic | Rule 2 — `:contains()` / `:has()` text-match selectors when [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md) priority 3–4 is the appropriate fallback (no stable `data-testid` in context). LP review skill may downgrade further when Pathfinder passes. |
| Semantic | Tooltip > 250 chars or multi-sentence |
| Semantic | Tooltip names the highlighted element (e.g., "Click the **Save** button" when the button is already highlighted) |
| Semantic | Code smell from best-practices.mdc §6 not already covered above |
| Semantic | Missing section bookends (intro markdown immediately before a `section` and summary immediately after). Do not require intro as the first child inside the section. |
| Semantic | In-section intro markdown that may render as a numbered step (first child is "You'll…" / action-preview markdown before interactives) — confirm in Block Editor; LP review posts inline when confirmed. Prefer moving the intro outside the section. |
| Semantic | False `noop` (learner click/type/open instruction with no `reftarget`) — prefer `markdown` or a real highlight |
| Semantic | Legacy `?doc=` query string used instead of `openGuide` field (rule 20) |
| Adversarial | Step content is technically correct but reads as instructions to a developer, not an end-user |
| Adversarial | Tooltip uses Grafana jargon a beginner won't know |
| Adversarial | Optional step has no clear "you can skip this" affordance |

---

## Info

An info finding is a **suggestion**. The guide is correct and usable as-is, but could be improved. Do not block on these.

| Phase | Examples |
|-------|----------|
| Structural | Cosmetic JSON formatting (trailing whitespace in selectors, mixed quote styles in content) |
| Structural | Selector could be more stable (`button[id='foo']` when `[data-testid='foo']` is also present) |
| Semantic | Could use a `code-block` block instead of a `formfill` for Monaco editors |
| Semantic | Section could benefit from a quiz to test understanding |
| Semantic | `assistantEnabled` could be set on query/config interactive steps |
| Adversarial | Step transition would benefit from a `noop` informational pause |
| Adversarial | Section structure could be reordered for better learning flow |

---

## How Phase 5 merges across reports

Phase 5 deduplicates findings across the three raw reports:

1. **Same block path + same rule cited** → list once, credit all reporting phases. Use the highest severity if they disagree (structural usually wins for rule-based findings; adversarial wins for UX findings).
2. **Same block path, different rules** → list separately under their respective rules.
3. **Cross-block findings** (e.g., dangling `section-completed`) → list under the *referring* block's path.

If `severity_floor` is set:

- `errors` → drop all warning and info; keep only blocking.
- `warnings` → drop all info; keep blocking and warning.
- `all` (default) → keep everything.

---

## When severities disagree

If a sub-agent is unsure whether a finding is blocking or a warning:

- **Default to warning** if the user can still complete the guide (just less smoothly).
- **Escalate to blocking** if the guide hard-fails for any plausible user.

When in doubt, cite the relevant critical rule from [AGENTS.md](../../../AGENTS.md). Rules 1-21 are all blocking; everything else is warning at most.

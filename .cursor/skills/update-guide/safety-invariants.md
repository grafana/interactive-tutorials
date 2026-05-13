# Safety Invariants

These five rules are **inviolable** for the update-guide skill. Phase 5 enforces them; the orchestrator must restore from snapshot and fail the run if any are violated.

---

## 1. Scope discipline

**Never touch a block outside the planned `Edits` list in `change-plan.md`.**

The change-plan is the contract. If Phase 3 modifies a block that wasn't in the plan — even to fix something — that's a violation. Fixes outside scope belong in Phase 4 (review) and only within the review's expanded scope (planned blocks + their immediate neighbours).

If Phase 3 discovers it needs to modify additional blocks to satisfy the user's request, **abort Phase 3, re-dispatch Phase 2 with the additional context, and have the user re-confirm the expanded plan**.

---

## 2. Pre-write snapshot is always taken

**Phase 1 takes a byte-level snapshot of `content.json` to `assets/snapshots/content.json.before` before Phase 3 runs.**

The snapshot is the source of truth for restoration. Use raw `cp` (or equivalent byte copy) — do NOT parse and re-serialise. JSON re-serialisation could change whitespace, key ordering, or encoding in ways that prevent a clean restore.

If the snapshot already exists from a prior aborted run, it stays — do not overwrite. Re-running Phase 1 against a current-state-changed file moves the previous snapshot to `assets/snapshots/history/{prior_timestamp}/content.json.before` before taking a new one.

If Phase 1 cannot take the snapshot (disk full, permissions error), the skill must stop before Phase 2 — never plan a change you cannot roll back.

---

## 3. IDs are preserved unless explicitly renamed

**Block IDs and section IDs must remain stable across the update unless the `change_request` explicitly asks for a rename.**

Why: external references depend on them. Recommender rules in `index.json` reference guide ids. Cross-section navigation depends on section ids. Variable references (`var-<name>`) depend on `input` block `variableName` values.

If Phase 2's plan renames an id, the plan MUST list every external referrer in the `IDREFs Affected` section. If any referrer cannot be updated by this skill (e.g., a rule in `index.json` — which `migrate-guide` is responsible for, not this skill), the plan must include a TODO for the user to update it manually.

For new blocks added in Phase 3, the orchestrator generates new ids in kebab-case, checked for uniqueness against `assets/guide-structure.json`.

---

## 4. IDREFs must resolve after the edit

**Phase 5 walks every reference type and confirms it still resolves. Any newly dangling reference fails the run.**

Reference types to walk:

- `section-completed:<id>` requirements → target section must exist in the updated tree.
- `var-<name>:<value>` requirements → an `input` block with `variableName: <name>` must exist earlier in the tree (DFS pre-order).
- `{{<name>}}` substitutions in markdown content → an `input` block with `variableName: <name>` must exist earlier in the tree.
- `whenTrue` / `whenFalse` in `conditional` blocks → must each be non-empty arrays (the schema requires this).
- `grot-guide` screen `screenId` references → target screen `id` must exist in the same `grot-guide` block.

If any reference is unresolved after Phase 3, the run is failed — restore from snapshot and report which reference broke.

---

## 5. Pathfinder CLI validate is a hard gate

**`node {pathfinder-app}/dist/cli/cli/index.js validate --package {guide_dir}` MUST return exit code 0 before the run is marked successful.**

If the CLI is unavailable (build not present, binary not found, path not configured), the run is marked **incomplete** — `manifest.yaml.validation.cli_validate_passed: false` with a `validation.cli_status: "unavailable"` note. The user can complete validation by building the CLI and re-running the skill (Phase 0 will warm-start).

If the CLI returns non-zero, the run is marked **failed** — `manifest.yaml.validation.cli_validate_passed: false` with the CLI's stderr captured in `review-report.md`. The orchestrator restores `content.json` from snapshot and stops.

This is non-negotiable: a guide that fails CLI validation does not get persisted. Schemas evolve and the CLI is the authoritative check.

---

## What happens on violation

When Phase 5 detects any violation:

1. **Restore `content.json`** from `assets/snapshots/content.json.before` (byte-level `cp`).
2. **Restore `manifest.json`** if Phase 3 modified it (also byte-level, from a snapshot Phase 3 takes before modifying `manifest.json`).
3. **Write `assets/review-report.md`** with a `## CRITICAL: <invariant name> violated` section explaining which invariant failed, which file was restored, and what the user should do next.
4. **Update `assets/manifest.yaml`** with `validation.byte_level_diff_clean: false` (or the matching field) and `status: failed`.
5. **Stop.** Do not retry. Do not partially commit. Do not warn-and-continue.

The user gets a clean rollback and a clear report. That is the contract.

# Mass Migration Execution Plan

This document specifies the process for migrating all remaining guides and learning paths to the Pathfinder package format, one PR per migration, managed as a batch on GitHub.

**Related design documents:**
- [MIGRATION.md](MIGRATION.md) — phased migration design, completed phases 0–4, pilot results
- [DEDUPLICATION.md](DEDUPLICATION.md) — post-migration plan for removing duplicate recommendation rules
- [Migration skill](../../.cursor/skills/migrate-guide/SKILL.md) — the reusable skill that performs each migration

---

## Inventory

Counts as of 2026-03-25. Re-verify before execution — authors may add or remove guides on parallel branches.

### Unmigrated standalone guides (6)

| Directory | Notes |
|-----------|-------|
| `enable-coda` | |
| `fleet-management-onboarding` | |
| `how-to-setup-secrets-tutorial` | |
| `play-carbon-intensity` | |
| `slo-quickstart` | |
| `sm-ping-check-tutorial` | |

### Unmigrated learning paths (19)

| Directory | Steps |
|-----------|-------|
| `adaptive-logs-lj` | 7 |
| `billing-usage-lj` | 5 |
| `detect-outages-synthetic-monitoring-lj` | 6 |
| `drilldown-logs-lj` | 8 |
| `drilldown-metrics-lj` | 5 |
| `drilldown-traces-lj` | 5 |
| `github-data-source-lj` | 5 |
| `grafana-cloud-tour-lj` | 5 |
| `infinity-csv-lj` | 7 |
| `infrastructure-alerting-lj` | 9 |
| `kafka-monitoring-lj` | 10 |
| `linux-server-integration-lj` | 8 |
| `macos-integration-lj` | 8 |
| `mysql-data-source-lj` | 7 |
| `mysql-integration-lj` | 8 |
| `postgresql-integration-lj` | 8 |
| `prom-remote-write-lj` | 5 |
| `visualization-metrics-lj` | 6 |
| `visualization-traces-lj` | 8 |

### Special cases (3)

| Directory | Issue |
|-----------|-------|
| `visualization-logs` | LJ-like structure (7 nested content.json) but no `-lj` suffix. Mode detection should trigger Mode 2 ("directory contains nested directories with content.json"), but website markdown mapping may fail (can't strip `-lj` to find website path). |
| `windows-integration` | LJ-like structure (9 nested content.json) but no `-lj` suffix. Same concern as `visualization-logs`. |
| `welcome-to-play` | Multi-part guide (3 nested content.json). Explicitly deferred in MIGRATION.md as needing hand-migration into a metapackage. |

### Already migrated (not in scope)

`alerting-101`, `explore-drilldowns-101`, `first-dashboard`, `prometheus-lj` (pilot, Phase 2), plus 17 other standalone guides that already have `manifest.json`.

---

## PR Conventions

### Branch naming

`migration/<directory-name>`

### Title

```
Package migration: <directory-name>
```

### Labels

| Label | When |
|-------|------|
| `package` | All migration PRs |
| `migration` | All migration PRs |
| `lj` | Learning paths only |
| `special-case` | `visualization-logs`, `windows-integration`, `welcome-to-play` |

### Body template

```markdown
## Summary

Package migration of `<directory-name>/` to the Pathfinder two-file package format.

**Type:** <standalone guide | learning path (N steps)>
**Source directory:** `<directory-name>/`

## Sources Consulted

| Source | Used? | Notes |
|--------|-------|-------|
| `content.json` | Yes | id, title |
| `index.json` | Yes/No | <rule found? match expression summary?> |
| Recommender rules | Yes/No/N/A | <files consulted, rules matched> |
| Website markdown | Yes/No/N/A | <path checked> |
| `journeys.yaml` | Yes/No/N/A | <entry found?> |

## Files Created

- `<dir>/manifest.json`
- (LJ) `<dir>/content.json` — path-level cover page
- (LJ) `<dir>/<step>/manifest.json` — one per step (list all)
- `<dir>/assets/migration-notes.md`

## Files NOT Modified

- [ ] No existing `content.json` was modified (verified by SHA-256)
- [ ] `index.json` was not modified
- [ ] No files outside `<directory-name>/` were changed

## Validation

- [ ] `validate --package` passed
- [ ] `id` matches between content.json and manifest.json
- [ ] (LJ) `milestones` array matches step content.json IDs
- [ ] (LJ) Step ordering matches website `weight` ordering

## Flags for Manual Review

<from migration-notes.md — any fallbacks, missing data, conflicts>

## Migration Notes

Full details in `<dir>/assets/migration-notes.md`.

## Dedup Linkage

Dedup PR: TBD — will be linked when the corresponding recommender rule removal PR is created.

---

Review checklist: [MIGRATION-REVIEW-CHECKLIST.md](docs/design/MIGRATION-REVIEW-CHECKLIST.md)
```

The "Sources Consulted" table creates the audit trail needed for deduplication. Each dedup PR can reference the migration PR and say "this recommender rule was absorbed into manifest targeting as documented in PR #N."

The "Dedup Linkage" section is a placeholder. When the corresponding deduplication PR is created later, edit the migration PR body to add the link, creating bidirectional traceability.

---

## Review Checklist

This checklist lives in the PR template above as a link, not duplicated in every PR body. Create it once as a standalone document that human reviewers can reference.

### Safety checks (must-pass)

1. **Scope containment.** PR only touches files within the stated directory.
2. **No content.json modifications.** The diff contains only new files — no changes to existing `content.json` files.
3. **index.json untouched.** `index.json` does not appear in the diff.
4. **Valid JSON.** Every generated `.json` file is syntactically valid.
5. **ID consistency.** `id` in `manifest.json` matches `id` in `content.json` in the same directory.

### Correctness checks (high confidence)

6. **Correct type.** `"guide"` for standalone guides and LJ steps; `"path"` for LJ root manifests.
7. **testEnvironment present.** Every manifest has `testEnvironment` with a `tier` value that makes sense for the content.
8. **Targeting fidelity.** `targeting.match` (if present) matches the source — `index.json` rule for standalone guides, recommender rule(s) for learning paths.
9. **Catalog-style description.** One-line summary, not introductory prose.
10. **Author convention.** `"Grafana Documentation"` for paths and path-steps; `"interactive-learning"` for standalone guides.

### LJ-specific checks

11. **Milestone count.** `milestones` array has the correct number of steps.
12. **Dependency chains.** Step N `depends` on step N-1; step N `recommends` step N+1. First step has no `depends`; last step has no `recommends`.
13. **Path-level content.json.** Derived from website markdown `_index.md`, not invented. Hugo shortcodes stripped.
14. **Category source.** `category` comes from `journey.group` in website markdown.

### Audit trail checks (for dedup linkage)

15. **Migration notes exist.** `assets/migration-notes.md` is present and documents field derivation sources.
16. **Recommender rules documented.** The migration notes list which recommender files and match expressions were used, or explicitly note that none were found / repo was unavailable.
17. **Dangling references documented.** Any IDs in `depends`/`recommends`/`suggests` that point to not-yet-migrated packages are recorded in the notes (not silently dropped).

---

## Migration Skill Considerations for Batch Execution

The migration skill (`.cursor/skills/migrate-guide/SKILL.md`) is well-suited for this workflow. Key strengths: safety invariants are explicit, migration notes produce the audit trail the PR body needs, it is parallel-safe by design, and the validation step is mandatory.

### Interactive prompts and batch mode

The skill says "stop and ask the user" for missing descriptions and metadata conflicts. In mass-parallel mode, this creates blocking queues.

**Batch convention:** When running migrations in parallel via sub-agents, the agent should write a `TODO` item in the migration notes instead of blocking on interactive prompts. Mark the migration as incomplete. Do a follow-up pass on incomplete migrations after the batch.

### External repo freshness

The skill reads from the website repo (`/Users/davidallen/hax/website/`) and the recommender repo. In parallel execution, each agent resolves the same absolute paths.

**Pre-batch requirement:** Pull both repos once before starting any wave. Do not rely on per-agent pulls — concurrent `git pull` to the same path will race.

### Special case: non-`-lj` learning paths

`visualization-logs/` and `windows-integration/` trigger Mode 2 via the "directory contains nested directories with content.json" condition. However, the website markdown mapping (strip `-lj` suffix) won't work. These need manual website path mapping or fallback-mode migration. Label them `special-case`.

### Special case: welcome-to-play

Explicitly deferred in MIGRATION.md. Exclude from the batch entirely. Handle as a separate future task.

---

## Execution Strategy

### Do not run all migrations simultaneously

Each worktree is a full working-tree copy with disk I/O. Each agent runs a Node.js CLI (`validate --package`). Concurrent git operations on shared repos (`/tmp/grafana-recommender`) will race. Agent subprocess memory and API token consumption scale linearly.

### Wave-based batching

Dispatch migrations in waves. Between waves, review the previous wave's PRs to catch systemic issues before they replicate.

#### Pre-batch setup (run once)

```bash
# Ensure external repos are fresh
git -C /Users/davidallen/hax/website pull --ff-only
git -C /Users/davidallen/hax/grafana-recommender pull --ff-only 2>/dev/null || \
  git clone --depth 1 git@github.com:grafana/grafana-recommender.git /tmp/grafana-recommender
```

Ensure the Pathfinder CLI is built:
```bash
cd /Users/davidallen/hax/grafana-pathfinder-app && npm run build:cli
```

#### Wave 1: Standalone guides (6 PRs)

Run all 6 in parallel. These are Mode 1 (simple): each creates 2–3 files (`manifest.json`, `assets/migration-notes.md`). Low risk, fast execution. Use this wave to validate the PR template and review process before scaling to learning paths.

| Directory |
|-----------|
| `enable-coda` |
| `fleet-management-onboarding` |
| `how-to-setup-secrets-tutorial` |
| `play-carbon-intensity` |
| `slo-quickstart` |
| `sm-ping-check-tutorial` |

**After wave 1:** Review all 6 PRs. Confirm the PR body template works, the review checklist catches real issues, and no systemic problems exist. Adjust the template or process before continuing.

#### Wave 2: Learning paths, batch A (7 PRs)

| Directory | Steps |
|-----------|-------|
| `adaptive-logs-lj` | 7 |
| `billing-usage-lj` | 5 |
| `drilldown-logs-lj` | 8 |
| `drilldown-metrics-lj` | 5 |
| `drilldown-traces-lj` | 5 |
| `grafana-cloud-tour-lj` | 5 |
| `prom-remote-write-lj` | 5 |

#### Wave 3: Learning paths, batch B (7 PRs)

| Directory | Steps |
|-----------|-------|
| `detect-outages-synthetic-monitoring-lj` | 6 |
| `github-data-source-lj` | 5 |
| `infinity-csv-lj` | 7 |
| `infrastructure-alerting-lj` | 9 |
| `kafka-monitoring-lj` | 10 |
| `linux-server-integration-lj` | 8 |
| `macos-integration-lj` | 8 |

#### Wave 4: Learning paths, batch C (5 PRs)

| Directory | Steps |
|-----------|-------|
| `mysql-data-source-lj` | 7 |
| `mysql-integration-lj` | 8 |
| `postgresql-integration-lj` | 8 |
| `visualization-metrics-lj` | 6 |
| `visualization-traces-lj` | 8 |

#### Wave 5: Special cases (2–3 PRs)

| Directory | Issue |
|-----------|-------|
| `visualization-logs` | Needs manual website path mapping |
| `windows-integration` | Needs manual website path mapping |
| `welcome-to-play` | Multi-part, may need hand-migration — evaluate whether the skill can handle it or defer further |

These need human attention. Run them last, possibly one at a time with interactive review.

### Implementation: Agent + worktree per migration

Each migration runs as a sub-agent with `isolation: "worktree"`. The agent:

1. Checks out a worktree on branch `migration/<directory-name>`
2. Runs the migration skill on the target directory
3. Commits the new files
4. Creates the PR using the body template above
5. Returns the PR URL

Within a wave, all agents run in parallel. The orchestrating agent collects PR URLs and reports them.

### Post-batch validation

After all PRs are merged into main, run aggregate validation:

```bash
node dist/cli/cli/index.js validate --packages .
node dist/cli/cli/index.js build-repository . -o repository.json
node dist/cli/cli/index.js build-graph interactive-tutorials:repository.json
```

This catches cross-package issues (duplicate IDs, broken dependency chains) that per-package validation misses.

---

## Tracking

### GitHub tracking issue

Create a GitHub issue titled **"Package migration: full migration tracking"** with a checklist of all directories. Each checkbox links to its PR once created.

```markdown
## Standalone guides
- [ ] `enable-coda` —
- [ ] `fleet-management-onboarding` —
- [ ] `how-to-setup-secrets-tutorial` —
- [ ] `play-carbon-intensity` —
- [ ] `slo-quickstart` —
- [ ] `sm-ping-check-tutorial` —

## Learning paths
- [ ] `adaptive-logs-lj` —
- [ ] `billing-usage-lj` —
- [ ] `detect-outages-synthetic-monitoring-lj` —
- [ ] `drilldown-logs-lj` —
- [ ] `drilldown-metrics-lj` —
- [ ] `drilldown-traces-lj` —
- [ ] `github-data-source-lj` —
- [ ] `grafana-cloud-tour-lj` —
- [ ] `infinity-csv-lj` —
- [ ] `infrastructure-alerting-lj` —
- [ ] `kafka-monitoring-lj` —
- [ ] `linux-server-integration-lj` —
- [ ] `macos-integration-lj` —
- [ ] `mysql-data-source-lj` —
- [ ] `mysql-integration-lj` —
- [ ] `postgresql-integration-lj` —
- [ ] `prom-remote-write-lj` —
- [ ] `visualization-metrics-lj` —
- [ ] `visualization-traces-lj` —

## Special cases
- [ ] `visualization-logs` —
- [ ] `windows-integration` —
- [ ] `welcome-to-play` —
```

Each line gets the PR link appended once the PR is created (e.g., `- [x] enable-coda — #205`).

### Batch management commands

Consistent labeling enables batch operations:

```bash
# List all migration PRs
gh pr list --label migration

# List only LJ migrations
gh pr list --label migration --label lj

# List incomplete/open migrations
gh pr list --label migration --state open

# Close all migration PRs (if process needs restart)
gh pr list --label migration --state open --json number -q '.[].number' | xargs -I{} gh pr close {}
```

---

## Connecting to Deduplication

Each migration PR's "Sources Consulted" table and `assets/migration-notes.md` create the audit trail needed for deduplication ([DEDUPLICATION.md](DEDUPLICATION.md) Phase 3).

When creating deduplication PRs:

1. For each recommender rule being removed, reference the migration PR that absorbed it: "Rule in `connections-cloud.json` for `learning-journeys/prometheus/` → absorbed by manifest targeting in PR #N."
2. Edit the migration PR body to fill in the "Dedup PR" placeholder with the link to the corresponding dedup PR.
3. This creates bidirectional traceability: migration PR → dedup PR and dedup PR → migration PR.

The "Sources Consulted" table in the migration PR body is the key artifact. It records which recommender files and match expressions were consumed, making it trivial to build the dedup PR's audit table (required by DEDUPLICATION.md Phase 3: "for every rule entry removed, link to a corresponding real file on the main branch of interactive-tutorials").

---

## Success Criteria

The mass migration is complete when:

1. Every directory in the inventory has a merged PR
2. `validate --packages .` passes on main with zero errors
3. `build-repository` produces a `repository.json` containing all migrated packages
4. The CI enforcement step (require `manifest.json` for every `content.json`) can be enabled without failures
5. The tracking issue has all checkboxes checked
6. All `assets/migration-notes.md` files are committed and document the full derivation history

# Reference checks (review-learning-path-pr)

Detailed checklists referenced from [SKILL.md](SKILL.md). The agent uses these during Phases 1–2; findings land in `pr-{n}-findings.md`, not on GitHub until Phase 7. Phase 3 buckets findings using [finding severity routing](#finding-severity-routing); Phase 7 applies that routing plus [GitHub comment policy](#github-comment-policy).

**Note:** [finding severity routing](#finding-severity-routing) supersedes [audit-guide/severity-rubric.md](../audit-guide/severity-rubric.md) for this workflow. audit-guide blocking/warning/info labels from Phase 1 are inputs only — re-tag before Phase 7.

---

## Finding severity routing

Use this table when writing `pr-{n}-findings.md` (Phase 3) and when deciding inline vs body-only comments (Phase 7). When Pathfinder **passes** a step that had a static warning, move that finding from **Defer** to **Review body only** unless it is in the **Always inline** column.

| Always inline (merge blocker) | Defer until Pathfinder (Phase 5–6) | Review body only |
|---|---|---|
| Playwright / Pathfinder runtime fail | Section bookends (rule 14) | Companion website drift |
| Outdated `data-testid` / UI label (valid pattern, wrong target) | `on-page` when step might still run | Passed milestones + deferred nits |
| Broken `depends` chain or framing in path `milestones` | `lazyRender` when target might scroll into view | Fresh-stack retest notes (N/A on credentialed stack) |
| First hands-on `depends` references framing ID | Skippable flag when step is permission-gated and passed | Pathfinder app shell UX |
| Missing `exists-reftarget`, `navmenu-open` | Missing `verify` if save step passed live | Editorial / tooltip / vocabulary |
| Fragile selectors | Admin-only steps without `skippable` if step passed | CODEOWNERS reminder |
| `noop` misuse, multistep singleton, focus-before-formfill | — | — |
| Missing `startingLocation` on interactive milestone | Missing objectives when resource already exists | Audit-guide warnings with no runtime impact |
| Pathfinder CLI validate failure | — | Product UX not fixable in JSON |
| `index.json` modified, invalid `testEnvironment.tier` | — | — |
| Secrets auto-filled (`doIt: true`) | — | — |
| Path root / manifest `id` mismatch | — | — |

**After Pathfinder:** promote deferred items to inline only if live test failed or static issue is clearly wrong regardless of runtime (e.g. fragile selector that happened to match today).

---

## Milestone `content.json` checks

Run via [audit-guide](../audit-guide/SKILL.md) plus confirm every row:

| Check | Block when |
|---|---|
| `schemaVersion` | Set to anything other than `"1.1.0"` (omit field instead) |
| Structure | Markdown `##` / `###` used for grouping instead of `section` blocks |
| Title duplicate | Leading `## Title` duplicates guide `title` |
| Section bookends | Interactive `section` missing in-section intro + summary markdown (critical rule 14) |
| `exists-reftarget` | Any step with `reftarget` missing it in `requirements` |
| `navmenu-open` | Nav menu item steps missing it |
| `on-page` | Page-specific steps missing `on-page:/path` |
| `lazyRender` | Below-fold / virtualized targets in plain `interactive` without `guided` + `lazyRender: true` |
| Multistep singleton | `multistep` with one step — must be plain `interactive` |
| Focus-before-formfill | `highlight` on input with default `doIt: true` — use `formfill` or `doIt: false` |
| `verify` | Save/create actions missing `verify` after state change |
| Skippable | Optional sections described as skippable in prose but no `"skippable": true` |
| `noop` misuse | See [noop rules](#noop-and-non-interactive-steps) |
| Secrets | Automated fill of passwords/tokens/API keys — use `doIt: false` |

Also apply [review-guide-pr.mdc](../../review-guide-pr.mdc) blocking rules.

---

## Framing milestones

Framing packages may exist in the repo for the website Learning Path but must **not** appear in path `manifest.json` `milestones`.

**Common framing:** `business-value`, `advantages`, `welcome`, markdown-only intro milestones.

**Flag when:**

- Framing IDs listed in path `milestones`
- First hands-on milestone `depends` references a framing ID — use `"depends": []`
- Path `milestones` includes non–hands-on packages

**OK:** Framing directories + `website.yaml` remain; `end-journey` and hands-on milestones stay in path `milestones`.

---

## Path root `content.json`

Phase 2 only (not a full audit-guide run). Read `{path_dir}/content.json` alongside path manifest and companion website.

| Check | Fail if |
|---|---|
| Root structure | Missing `id`, `title`, or non-empty `blocks` |
| `id` | Does not match path `manifest.json` `id` |
| Title duplicate | Leading markdown block duplicates `title` (same as milestone rule) |
| Before you begin | Prerequisites missing or contradict first hands-on milestone / website `_index.md` Before you begin |
| Env prerequisites | Cloud tier, tokens, CLI, or integrations required by milestones not listed here |
| Framing in JSON | Path `content.json` duplicates website-only framing that belongs in separate packages |
| Datasource / setup | Path intro claims resources the first milestone creates without saying user needs them first |

Severity: `id` mismatch → **Always inline**. Before you begin drift → **Review body** (inline if PR claims website sync done). Editorial intro prose → **Review body**.

---

## `website.yaml`

Path root `{path_dir}/website.yaml` configures the companion Learning Path on grafana.com. Per-milestone `website.yaml` files configure milestone pages.

| Check | Fail if |
|---|---|
| Path root file | Missing when path has framing milestone dirs (`business-value`, etc.) or website companion slug exists |
| `menuTitle` / `description` | Missing or empty on path root `website.yaml` |
| `journey` metadata | Missing `group`, `skill`, or layout fields peer LPs include |
| Slug alignment | Website path slug ≠ `{path_dir}` minus `-lj` when companion exists |
| Milestone pages | Milestone dir in path `milestones` missing `website.yaml` when peer LPs include one for same step type |

Severity: missing path root `website.yaml` when framing dirs exist → **Review body** (package OK if website PR is separate). Wrong slug or broken journey metadata → **Review body** unless PR bundles website changes.

---

## Valid manifests

```bash
node {pathfinder-app}/dist/cli/cli/index.js validate --packages {path_dir}
```

### Path root (`type: "path"`)

| Check | Fail if |
|---|---|
| `id` | Does not match path `content.json` `id` |
| `type` | Not `"path"` or `"journey"` |
| Required fields | Missing `description`, `category`, `author` |
| `milestones` | Missing, empty, or IDs without package directories |
| Milestone IDs | Any `milestones` entry missing `{path_dir}/{name}/content.json` |
| Targeting | Missing or overly broad `targeting.match` |
| `index.json` | PR modifies frozen `index.json` |

### Each milestone (`type: "guide"`)

| Check | Fail if |
|---|---|
| `id` | Does not match milestone `content.json` `id` |
| `type` | Not `"guide"` |
| `targeting` | Present on step guides (path level only) |
| `depends` / `recommends` | Unknown IDs or wrong chain |
| `startingLocation` | Missing on interactive milestones |
| `testEnvironment.tier` | Invalid (e.g. `"play"` — use `"cloud"`) |

### Dependency chain (peer LP pattern)

- Each hands-on milestone `depends` on prior milestone in path `milestones` order
- First hands-on: `"depends": []`

---

## Targeting / recommender

- `targeting.match` not overly broad (product-specific URL prefixes)
- `targetPlatform: "cloud"` when cloud-only
- No separate recommender PR — package manifest feeds `repository.json` after merge

---

## Companion website (separate repo)

When `website` repo + slug available:

- Milestone pages: `pathfinder_data: {path_dir}/{milestone}` + pathfinder JSON shortcode
- Path `_index.md`: `pathfinder_data: {path_dir}`; Before you begin matches path `content.json`
- Framing: shared snippet vs path package (e.g. `case-for-o11y`)
- Doc drift between website markdown and package content

Gaps → review body, not package inline blockers unless PR claims website sync is done.

---

## noop and non-interactive steps

**Reject `noop` when:**

| Pattern | Use instead |
|---|---|
| Observation / confirmation | `markdown` |
| Outside a `section` | `markdown` |
| Click/save with no `reftarget`, `verify`, or `on-page` | `button` / `highlight` + selector + `verify` |
| Optional without `"skippable": true` | Add skippable or restructure |
| Number padding only | `markdown` or merge steps |

**Accept `noop`:** numbered in-section manual step the product cannot automate.

---

## GitHub comment policy (Phase 7)

Apply [finding severity routing](#finding-severity-routing) first. Only **Always inline** findings and runtime failures from Phases 5–6 become inline comments.

### One comment per root cause

Dedupe before posting. Apply these rules in order:

1. **Same root cause, multiple files** — one inline per file that needs a code change, but each comment references the shared root cause (e.g. both `verify-data-collection` and `explore-data` cite the same missing tab). Do not restate the full diagnosis twice; second comment says "same root cause as `{other-milestone}`."
2. **Same root cause, same file** — exactly **one** inline. Merge the fix and any runtime symptom into a single comment (e.g. `depends: []` fix + "complete previous step / steps paused" UX — do not post separate threads on the same manifest line).
3. **Playwright + Pathfinder** — one comment per line with both evidence sources merged.
4. **Symptom caused by fixable code** — inline the code fix; mention the UX symptom in that comment. Do not add a second inline for app-shell behavior that the code fix resolves.

| Inline comment | Review body | Conversation |
|---|---|---|
| **Always inline** column + Phase 5–6 failures | **Review body only** column | Pathfinder app shell UX not caused by this PR's JSON |
| One comment per root cause (rules above) | Passed milestones, deferred nits, companion website, retest notes | Follow-up issue tracking |
| Code fix in PR (`depends`, manifest, noop, framing) | No fixed template | — |

**Never inline:** pass-only, N/A-only, `FROM AUDIT:` dumps, duplicate threads for the same root cause on the same file, items still in **Defer** that Pathfinder passed.

---

## Verdict selection (Phases 8–9)

The reviewer chooses the GitHub review event at Phase 8. The agent **recommends** a default from findings; the reviewer confirms or overrides before Phase 9 submit.

### Decision tree

```
After Phase 7 — any Always inline finding OR Phase 5–6 runtime failure with inline comment?
  Yes → recommend REQUEST_CHANGES
  No  → any Review body only items (companion website, retest notes, deferred nits, shell UX)?
          Yes → recommend COMMENT
          No  → recommend APPROVE
```

### When to use each verdict

| Verdict | Use when | Inline comments | Body |
|---|---|---|---|
| **REQUEST_CHANGES** | Merge blockers remain in this PR — runtime fails, broken `depends`/manifest, framing in path, Pathfinder CLI validate failure | Yes — one per root cause for **Always inline** items | **Must fix before merge** lists every blocker; companion website / retest notes in separate sections |
| **COMMENT** | No merge blockers in this PR, but useful feedback before or after merge | Usually none; optional for minor non-blocking code notes | Companion website checklist, fresh-stack retest, deferred authoring nits, Pathfinder shell UX follow-ups |
| **APPROVE** | Static + live testing passed; you would merge as-is | None | Brief summary of passed milestones; optional polish follow-ups |

### Rules

1. **Do not recommend APPROVE** if any **Always inline** finding is open or any Phase 5–6 failure was inlined in Phase 7.
2. **Do not recommend REQUEST_CHANGES** with zero inline comments unless the reviewer explicitly waives inline at Phase 8 — **Always inline** items belong on the diff, not body-only.
3. **COMMENT** is correct for “mergeable package PR, website/sync work separate” — common for LP reviews where `website.yaml` is present but learn.grafana.net pages are not wired yet.
4. **N/A with fresh-stack caveat** (e.g. install button missing) does not by itself require REQUEST_CHANGES — put in body under author retest; use REQUEST_CHANGES only if live steps actually failed.
5. Agent states recommended verdict at end of Phase 7 and again at Phase 8 opening; reviewer must confirm explicitly before submit.

### Phase 8 prompt (agent)

> Recommended verdict: **{REQUEST_CHANGES | COMMENT | APPROVE}** — {one-sentence reason}. Confirm or override, then say **submit** when ready.

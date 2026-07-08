# Reference checks

Checklists for [review-learning-path/SKILL.md](SKILL.md) Phases 1–2. Findings land in `pr-{n}-findings.md` first — not on GitHub until Phase 7.

**Note:** [finding severity routing](#finding-severity-routing) supersedes [audit-guide/severity-rubric.md](../audit-guide/severity-rubric.md) for this workflow. Re-tag audit-guide labels before Phase 7. Phase 3 buckets findings; Phase 7 applies [GitHub comment policy](#github-comment-policy-phase-7).

**Selector authority for LP reviews:** Follow [docs/selectors-and-testids.md](../../../docs/selectors-and-testids.md) priority order (`data-testid` > semantic > `:contains()` > `:has()` > CSS classes). Do **not** apply [build-interactive-lj/reference/selector-patterns.md](../../commands/build-interactive-lj/reference/selector-patterns.md) autogen rules ("never `:contains()`") when reviewing hand-authored or live-captured guides — that workflow targets source-to-guide generation, not PR review.

**Publishing model (PR [#416](https://github.com/grafana/interactive-tutorials/pull/416)):** LP PRs are **single-repo** (`interactive-tutorials` only). Metadata in package `website.yaml`; prose in `content.json`. The website repo is **read-only** for conversion — never expect `pathfinder_data` or website markdown updates in the LP PR.

**Learning Hub standards:** [learning-hub-standards.md](learning-hub-standards.md) — adapted from `website/content/internal/docs/learning-hub/reviewing-learning-journeys/`. Phase 2 walks the full doc; Phase 1 applies milestone prose checks and [common pitfalls](learning-hub-standards.md#common-pitfalls).

---

## Finding severity routing

Use this table when writing `pr-{n}-findings.md` (Phase 3) and when deciding inline vs body-only comments (Phase 7). When Pathfinder **passes** a step that had a static warning, move that finding from **Defer** to **Review body only** unless it is in the **Always inline** column.

| Always inline (merge blocker) | Defer until Pathfinder (Phase 5–6) | Review body only |
|---|---|---|
| Playwright / Pathfinder runtime fail | Section bookends (rule 14) | `website.yaml` metadata gaps (non-blocking polish) |
| Outdated `data-testid` / UI label (valid pattern, wrong target) | `on-page` when step might still run | Passed milestones + deferred nits |
| `:contains()` when stable `data-testid` or semantic attr verified in DOM | `lazyRender` when target might scroll into view | `:contains()` fallback per [selectors doc](../../../docs/selectors-and-testids.md) when Pathfinder passed and no stable selector exists |
| Broken `depends` chain or framing in path `milestones` | Skippable flag when step is permission-gated and passed | State-dependent selector (missing on pre-setup stack) |
| First hands-on `depends` references framing ID | Admin-only steps without `skippable` if step passed | Fresh-stack retest notes (N/A on credentialed stack) |
| Missing `exists-reftarget`, `navmenu-open` | Missing `verify` if save step passed live | Pathfinder app shell UX |
| CSS-class-only or auto-generated class selectors | Vague step copy when Pathfinder passed | Editorial / tooltip / vocabulary |
| `noop` misuse, multistep singleton, focus-before-formfill | Missing `success` + troubleshooting on verification (Pathfinder passed) | CODEOWNERS reminder |
| Missing `startingLocation` on **path** manifest when path has interactive milestones | — | Landing boilerplate, logo, screenshot, milestone count |
| Pathfinder CLI validate failure | — | `related_journeys` wording, missing value framing |
| `index.json` modified, invalid `testEnvironment.tier` | — | Product UX not fixable in JSON |
| Secrets auto-filled (`doIt: true`) | — | Audit-guide warnings with no runtime impact |
| Path root / manifest `id` mismatch | — | — |
| Hard cross-path artifact dependency in step copy | — | — |
| Confirmed 404 outbound link in `website.yaml` supplementary fields (verified in Phase 2) | — | Suspected bad outbound link (not yet verified) |

**After Pathfinder:** promote deferred items to inline only if live test failed or static issue is clearly wrong regardless of runtime (e.g. author used `:contains()` when Playwright confirmed a `data-testid` on the same element).

### Selector decision tree

Apply after Phase 5–6 when re-tagging audit-guide rule 2 / "fragile selector" findings:

```
Selector finding from audit
  │
  ├─ Pathfinder or Playwright fail on this step? → Always inline
  │
  ├─ Stable data-testid or semantic attr available in DOM
  │    and author used :contains() instead? → Always inline
  │
  ├─ :contains() on heading/button per docs/selectors-and-testids.md
  │    priority 3, Pathfinder passed, no stable selector in DOM? → Review body only
  │
  ├─ :contains() in virtualised/below-fold context (rule 21)? → Defer;
  │    promote to inline only if Pathfinder fails
  │
  └─ CSS class / nth-only selector? → Defer; promote if Pathfinder fails
```

When the author notes test IDs were tried first and failed, treat `:contains()` as justified fallback unless live testing or DOM inspection proves otherwise.

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

**Learning Hub prose (Phase 1 editorial):** When auditing milestone copy, also scan [learning-hub-standards.md § task milestones](learning-hub-standards.md#task-milestones-hands-on-guides) and [common pitfalls](learning-hub-standards.md#common-pitfalls). Vague instructions and missing section context are **Review body** unless Pathfinder fails on the step.

---

## Framing milestones

Framing packages may exist in the package (with `website.yaml` for Learning Hub publish) but must **not** appear in path `manifest.json` `milestones`.

**Common framing:** `business-value`, `advantages`, `welcome`, markdown-only intro milestones.

**Flag when:**

- Framing IDs listed in path `milestones`
- First hands-on milestone `depends` references a framing ID — use `"depends": []`
- Path `milestones` includes non–hands-on packages

**OK:** Framing directories + `website.yaml` remain; `end-journey` and hands-on milestones stay in path `milestones`.

---

## Path root `content.json`

Phase 2 only (not a full audit-guide run). Read `{path_dir}/content.json` alongside path manifest and package `website.yaml`.

| Check | Fail if |
|---|---|
| Root structure | Missing `id`, `title`, or non-empty `blocks` |
| `id` | Does not match path `manifest.json` `id` |
| Title duplicate | Leading markdown block duplicates `title` (same as milestone rule) |
| Before you begin | Prerequisites missing or contradict first hands-on milestone (compare path `content.json` only — not legacy website `_index.md`) |
| Env prerequisites | Cloud tier, tokens, CLI, or integrations required by milestones not listed here |
| Framing in JSON | Path `content.json` duplicates framing that belongs in separate milestone packages |
| Datasource / setup | Path intro claims resources the first milestone creates without saying user needs them first |
| Prose only in legacy markdown | Conversion PR: milestone body prose exists in website `index.md` but is missing from `content.json` blocks |

Severity: `id` mismatch → **Always inline**. Prose not captured in package → **Always inline** on conversion PRs. Before you begin gaps → **Review body**. Editorial intro prose → **Review body**.

Full prerequisite and boilerplate criteria: [learning-hub-standards.md § path landing](learning-hub-standards.md#path-landing-page) and [§ before you begin](learning-hub-standards.md#before-you-begin-prerequisites).

---

## Learning Hub structure (Phase 2)

Walk [learning-hub-standards.md](learning-hub-standards.md) in path order after manifest/depends checks. **Severity:** tag every finding with [finding severity routing](#finding-severity-routing) only — do not use severity columns in `learning-hub-standards.md`.

| Area | Key checks |
|---|---|
| [Path landing](learning-hub-standards.md#path-landing-page) | `website.yaml` identity, boilerplate sections in path `content.json`, logo |
| [Prerequisites](learning-hub-standards.md#before-you-begin-prerequisites) | Complete, specific, Grafana Cloud first, match milestones |
| [Milestone order](learning-hub-standards.md#milestone-types-and-order) | Value framing exists, 5–10 hands-on milestones typical, `end-journey` with `conclusion` |
| [CTA types](learning-hub-standards.md#cta-types-websiteyaml) | `success` on verification only |
| [Side / related journeys](learning-hub-standards.md#side-journeys) | Valid destinations, no LP links in `side_journeys`, soft `related_journeys` |
| [Troubleshooting](learning-hub-standards.md#troubleshooting-on-verification-steps) | Present when steps verify outcomes |
| [Standalone](learning-hub-standards.md#standalone-principle) | No hard deps on other paths' artifacts |
| [Outbound links](learning-hub-standards.md#outbound-link-verification) | Spot-check `side_journeys`, `related_journeys`, `cta.troubleshooting` on conversion PRs |
| [Videos](learning-hub-standards.md#videos) | Do not flag missing; verify if present |

---

## `website.yaml`

Package `website.yaml` files are the **authoritative** Learning Hub metadata for deploy previews and publish ([docs/website-yaml-reference.md](../../../docs/website-yaml-reference.md)). They replace legacy website front matter — no companion website PR is required.

| Check | Fail if |
|---|---|
| Path root file | Missing when peer LPs include path-level `website.yaml` (including paths with framing dirs like `business-value/`) |
| Required path fields | Missing `menuTitle`, `description`, `weight`, `step`, `journey` (`group`, `skill`, `source`, `logo`), or path-level `cta` per [website-yaml-reference.md](../../../docs/website-yaml-reference.md) |
| Step-level files | Milestone in path `milestones` missing `website.yaml` when peer LPs include one for the same step type |
| Step required fields | Missing `menuTitle`, `description`, `step`, `layout`, or `cta.type` on milestone `website.yaml` |
| Slug convention | `{path_dir}` minus `-lj` should match the legacy website folder name when converting an existing path (for read-only source lookup only) |
| Supplementary metadata | `side_journeys`, `cta.troubleshooting`, or `related_journeys` present in legacy front matter but absent from package `website.yaml` when conversion PR |
| CTA type | Verification milestone missing `cta.type: success` or final step not `conclusion` (see [CTA types](learning-hub-standards.md#cta-types-websiteyaml)) |
| Troubleshooting | `success` milestone without `cta.troubleshooting.items` when step verifies an outcome (see [troubleshooting](learning-hub-standards.md#troubleshooting-on-verification-steps)) |

Severity: missing path or milestone `website.yaml` when peers have them → **Review body** (request in this PR — not a separate website PR). Broken required fields → **Review body**; promote to **Always inline** only if deploy preview or publish would fail. Conversion mapping gaps → **Review body**. Suspected bad supplementary links → **Review body** until Phase 2 confirms 404 → **Always inline**.

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
| `startingLocation` | On **path** manifest when peers include it; **omit on step guides** (path-level only per [manifest-reference.md](../../../docs/manifest-reference.md)) |
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

## Legacy website source (optional, read-only)

When the `website` repo is in the workspace, you may read `content/docs/learning-paths/{website_slug}/` for **conversion context only**. Never flag missing website writes.

| Check | When to apply | Severity |
|---|---|---|
| Prose captured in `content.json` | Conversion or migrate PR | **Always inline** if body prose exists only in legacy `index.md` |
| `website.yaml` vs source front matter | Conversion PR | **Review body** — map per [frontmatter-schema.md](../../commands/create-learning-path/reference/frontmatter-schema.md) |
| Legacy `pathfinder_data` or `{{< pathfinder/json >}}` | Any | **Never flag** — legacy artifacts; LP PRs do not modify website markdown |
| Drift between unchanged legacy markdown and package | Any | **Never flag** as merge blocker — legacy markdown is intentionally unchanged |
| Framing source | Converted path with `business-value/` | **Review body** if legacy used a shared snippet but package has its own milestone dir (or vice versa) |

**Do not** request a companion website PR, `pathfinder_data` wiring, or shortcode insertion as part of LP package review.

---

## PR type (Phase 0)

Infer from PR title, changed files, and presence of legacy website source. Record in `pr-{n}.json` → `pr_type`.

| Type | Signals | Phase 2 emphasis |
|---|---|---|
| **new** | New `{slug}-lj/` directory; no legacy website folder | `website.yaml` completeness; path root `content.json` |
| **conversion** | Touches `website.yaml` + prose-heavy markdown blocks; author used `/build-interactive-lj` | [Legacy website source](#legacy-website-source-optional-read-only); prose captured in `content.json` |
| **update** | Changes existing package milestones/manifests only | Phase 2 emphasizes PR-touched milestones; Phases 5–6 test PR-touched interactive milestones first (full path optional at reviewer request) |

---

## Static-only reviews (Phase 3)

`static-only` skips Phases 5–6. Use sparingly — it does not verify selectors or Pathfinder interactivity.

### When static-only is allowed

| Situation | Allowed? |
|---|---|
| **new** or **conversion** PR with interactive milestones in path `milestones` | **No** — require live testing |
| **update** PR touching only markdown / `website.yaml` with no interactive changes | Yes, with reason |
| Merged or closed PR (practice / archaeology) | Yes, with reason |
| Reviewer lacks stack access but author already live-tested | Yes, with reason — cap verdict at **COMMENT** |

### Required when accepting static-only

1. Record `waive_live_testing: true` and `static_only_reason` (reviewer's stated reason) in `pr-{n}.json`.
2. At Phase 3, reject bare `static-only` on **new** / **conversion** interactive PRs — tell the reviewer live testing is required.
3. Prompt format: `static-only: <reason>` (for example `static-only: merged PR dogfood`).

### Verdict cap

**Never recommend APPROVE** when `waive_live_testing` is true. Cap at **COMMENT**. The review body must include a **Not live-tested** section listing every interactive milestone in path `milestones` that was not run in Phases 5–6.

---

## Live testing prerequisites (Phases 5–6)

Apply before interpreting Playwright or Pathfinder results. See also [workflows.md § Phase 4](../../learning-path-workflows/workflows.md).

### Stack state

| Path pattern | Minimum stack state | False-pass risk |
|---|---|---|
| Install / bootstrap milestone | **Fresh** Grafana Cloud stack | Install button missing when resource already exists (shows **Uninstall**) |
| Connect + configure cloud credentials | **Real** credential saved (not just `doIt: false` highlights) | UI tabs or panels absent in pre-setup state (e.g. Services tab before credential) |
| Permission-gated steps | Stack with required RBAC roles | `exists-reftarget` fails for users without role — use `skippable` |
| Default learn.grafana.net | Shared demo stack | May not match fresh-stack or credentialed flows |

Record in state: `stack_state` (free text, e.g. `learn.grafana.net shared`, `fresh cloud`, `azure credentialed`).

### Pathfinder pass ≠ resource created

Steps with `doIt: false` on secrets or **Create/Save** can **pass** Pathfinder without mutating stack state. A later milestone that assumes post-setup UI is only valid if prior milestones actually ran **Do it** on save steps or the stack was pre-configured.

When a selector is missing on a shared stack but the author claims post-setup UI, note in review body: **retest on stack matching learner state** — do not dismiss as author error without that retest.

### Multi-environment testing

Encourage testing beyond the default learn host when the path touches permissions, install flows, or state-dependent UI ([workflows.md](../../learning-path-workflows/workflows.md)). Record N/A with environment caveat in review body.

### Milestone start URL (Phase 6)

LP step manifests usually **omit** `startingLocation`. Derive the page to open:

1. First `on-page:/path` in the milestone's interactive blocks (preferred)
2. Path manifest `startingLocation`
3. Ask the reviewer if ambiguous

---

## Supplementary content

| Check | Fail if | Severity |
|---|---|---|
| `side_journeys` / troubleshooting duplicated | Same links in milestone `website.yaml` **and** trailing markdown blocks in `content.json` | **Review body** — pick one source; duplication causes drift |
| `side_journeys` only in `website.yaml` | Conversion PR omitted links that learners see in package UI | **Review body** |
| Recap references framing | `end-journey` claims milestones not in path `manifest.json` `milestones` | **Review body** |

---

## CODEOWNERS

| Check | Fail if |
|---|---|
| New path directory | `{path_dir}/` not added to `.github/CODEOWNERS` when PR introduces a new `*-lj/` package |

Severity: **Review body** reminder — not a merge blocker unless repo policy requires it in the same PR.

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
| One comment per root cause (rules above) | Passed milestones, deferred nits, `website.yaml` polish, retest notes | Follow-up issue tracking |
| Code fix in PR (`depends`, manifest, noop, framing) | No fixed template | — |

**Never inline:** pass-only, N/A-only, `FROM AUDIT:` dumps, duplicate threads for the same root cause on the same file, items still in **Defer** that Pathfinder passed, audit-only `:contains()` fallback findings when Pathfinder passed (see [selector decision tree](#selector-decision-tree)).

---

## Verdict selection (Phases 8–9)

The reviewer chooses the GitHub review event at Phase 8. The agent **recommends** a default from findings; the reviewer confirms or overrides before Phase 9 submit.

### Decision tree

```
waive_live_testing is true (static-only)?
  Yes → recommend COMMENT only (never APPROVE)
        review body must list Not live-tested milestones
  No  → continue below

After Phase 7 — any Always inline finding OR Phase 5–6 runtime failure with inline comment?
  Yes → recommend REQUEST_CHANGES
  No  → all Pathfinder milestones passed AND remaining findings are audit-only selector warnings or body-only nits?
          Yes → recommend COMMENT (or APPROVE if nothing worth saying)
          No  → any Review body only items (`website.yaml` gaps, retest notes, deferred nits, shell UX)?
                  Yes → recommend COMMENT
                  No  → recommend APPROVE
```

### When to use each verdict

| Verdict | Use when | Inline comments | Body |
|---|---|---|---|
| **REQUEST_CHANGES** | Merge blockers remain in this PR — runtime fails, broken `depends`/manifest, framing in path, Pathfinder CLI validate failure | Yes — one per root cause for **Always inline** items | **Must fix before merge** lists every blocker; `website.yaml` / retest notes in separate sections |
| **COMMENT** | No merge blockers in this PR, but useful feedback before or after merge | Usually none; optional for minor non-blocking code notes | `website.yaml` completeness, fresh-stack retest, deferred authoring nits, Pathfinder shell UX follow-ups |
| **APPROVE** | Static + live testing passed; you would merge as-is | None | Brief summary of passed milestones; optional polish follow-ups |

### Rules

1. **Do not recommend APPROVE** if any **Always inline** finding is open, any Phase 5–6 failure was inlined in Phase 7, or `waive_live_testing` is true.
2. **Do not recommend REQUEST_CHANGES** with zero inline comments unless the reviewer explicitly waives inline at Phase 8 — **Always inline** items belong on the diff, not body-only.
3. **COMMENT** is correct for “mergeable package PR with `website.yaml` polish or conversion mapping nits” — not because a separate website PR is still needed.
4. **N/A with fresh-stack caveat** (e.g. install button missing) does not by itself require REQUEST_CHANGES — put in body under author retest; use REQUEST_CHANGES only if live steps actually failed.
5. Agent states recommended verdict at end of Phase 7 and again at Phase 8 opening; reviewer must confirm explicitly before submit.

### Phase 8 prompt (agent)

At Phase 8 opening, state the recommendation in plain language:

> Recommended verdict: **{REQUEST_CHANGES | COMMENT | APPROVE}** — {one sentence why}. Confirm or override, then reply **submit** when ready.

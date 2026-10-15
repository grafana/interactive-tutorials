# Claim check (shared learning-path policy)

Adversarial factual check for Pathfinder learning path packages. Adapted from the Learning Hub claim-check skill and the MUST FIX bar in journey audit reports. Goal: catch invented product facts, not Hugo slide structure.

**Canonical policy for** [/create-learning-path](../../commands/create-learning-path.md), [/build-interactive-lj](../../commands/build-interactive-lj.md), [review-learning-path](SKILL.md), and [preflight-learning-path](../preflight-learning-path/SKILL.md). Do not fork a second verdict table. Preflight keeps a thin pointer at `../preflight-learning-path/claim-check.md` that redirects here.

**When to run:**

| Caller | When | Mode |
|---|---|---|
| **create** (`/create-learning-path`, `/build-interactive-lj`) | Wrap-up phase, after Block Editor testing | Full |
| **preflight** | Static pass, after audit-guide and path / Learning Hub checks, before the live gate | Changed since last check (see [Changed-since mode](#changed-since-mode)) |
| **review** | Static pass, after audit-guide and path / Learning Hub checks, before the live gate | Full |

Review always runs in full, so a second person checks every claim no matter what earlier runs found.

**Independence:** Prefer a fresh agent pass that did not author the package prose. Default stance: unproven. A claim is flagged unless a source plainly supports it.

---

## Scope (path package)

Read all prose that learners see:

- Path root `content.json` markdown blocks
- Every milestone `content.json` markdown (including framing dirs not in path `milestones`, if present)
- Interactive step `content` / tooltips that state product facts (skip pure click instructions)
- Path and milestone `website.yaml` `description` / CTA copy when it asserts product behavior

Skip: pure navigation instructions ("Click **Save**"), structural Pathfinder rules, and restatements of UI chrome with no product claim.

Website repo (when in workspace) is **read-only** for sources (`content/docs/...`). Do not require a companion website PR.

---

## What counts as a claim

Falsifiable statements about the product, including:

- What a feature does or does not do
- Feature / product / alert / dashboard names
- Versions, defaults, limits, prerequisites, platform availability
- Absolutes and quantifiers (only, never, all, every, must, N dashboards, N alerts)
- Comparisons that rank or prescribe one Grafana capability over another

### Not claims

- "In this milestone you will…" framing
- UI click paths without a product assertion
- Learning Hub boilerplate that matches standards verbatim

---

## Facts file

Every path package keeps `{slug}-lj/assets/facts.md`, written by the create commands before any prose and committed with the package. Nothing under `assets/` is rendered or shipped. It lists each product fact the path states and where that fact comes from, so a reviewer can check the same source the author used.

```markdown
# Facts: {slug}-lj

| # | Fact | Source | Source type | Verified | Used in |
|---|---|---|---|---|---|
| 1 | Default interval is every 10 minutes (5 minutes to 3 hours) | https://grafana.com/docs/.../watchers/#create-a-watcher | Docs | 2026-10-09 | `create-watcher/content.json` |
| 2 | Calibration questions preselect the recommended answer, marked (Recommended) | `grafana-assistant-app` `apps/plugin/src/pages/watcher-agents/CalibrationQuestions.tsx` `initialDraft` @ `{commit}` | Product source | 2026-10-15 | `calibrate-watcher/content.json` |
```

**Source types, in order of preference:**

1. **Docs.** Local `website` docs, then live grafana.com docs. Use this whenever the docs state the fact.
2. **Product source.** A file path, symbol, and commit in the product repo. Use only when the docs don't state the fact, which is common before GA.
3. **Live UI.** What the author saw, with the stack and date. Use only when neither docs nor source code settle it.

A product source or live UI row is a fact the docs don't back yet, so it's the first thing to recheck if the product changes.

When the docs are being rewritten in an unmerged pull request (common before GA), cite both the published page and the docs PR with its commit, and say in the row when the PR drops the fact. List the PR's merge status at the top of the file. A docs PR row counts as **Docs** for the verdict, but recheck it in changed-since mode until the PR merges.

Packages created before this rule may have no `assets/facts.md`. For those, check claims against the docs as in the procedure below, and treat a missing facts file as a note, not a finding.

## Procedure

1. Extract claims (batch by milestone; include path root).
2. For each claim, find its row in `assets/facts.md`. Open that source and confirm it still says what the row claims. If the claim has no row, look for a source yourself: local `website` docs first, then WebFetch to live grafana.com docs. No row and no docs source → **Unsupported**.
3. Open the source; quote the supporting or contradicting line.
4. Verdict (see below). Sweep phrase + category across the whole package so the same error is one finding with multiple locations.
5. Write the report (path depends on caller; see below). Record the branch head commit the check ran against.

Do not edit package JSON during the claim check. Fixes wait for author request (create, preflight) or reviewer post approval (review).

## Changed-since mode

Preflight re-checks only what changed since the last recorded claim check:

1. Read `Run against:` from the most recent `.cursor/lp-preflight-state/{slug}-claim-check.md`. If the report or the line is missing, or the commit is no longer in the branch history (for example, after a rebase), run in full.
2. `git diff {commit}..HEAD -- {slug}-lj/` and extract claims from added or changed prose only.
3. Also re-check every **Product source** and **Live UI** row in `assets/facts.md`, because those are the facts most likely to drift with the product.
4. Check each claim with the normal procedure and write a fresh report that records the new head commit.

A claim added after the last check with no row in `assets/facts.md` is a finding, even when the claim is true.

---

## Verdicts

| Verdict | Meaning | Shared routing |
|---|---|---|
| **Supported** | Source plainly states the claim | Hide (optional Supported list in the report only) |
| **Contradicted** | Source says something different | Review-level: **post inline** / Fix before PR |
| **Unsupported** | No source, or source does not address it | Review-level: **post inline** / Fix before PR |
| **Overstated** | Source supports a weaker version; claim adds absolute/superlative/framing | Review-level: **post inline** / Fix before PR |
| **Product-sourced** | Docs don't state it, but a **Product source** or **Live UI** row in `assets/facts.md` does, and you confirmed that source | Not a finding. List it in the report so the reviewer knows which facts the docs don't back yet |
| **Author decides** | Product-truth call a human must make | Workbook / readiness open question; do not auto-edit |

Only Contradicted / Unsupported / Overstated count toward review-level findings (dedupe by root cause). Soft style nits stay Internal / out of author chat.

A reviewer who can't open a product-source row (for example, no access to the product repo) leaves an open question that names the row, not a request to drop the sentence.

---

## Catches that matter (linter cannot)

1. Made-up facts
2. Invented terms / alert names / dashboard names
3. Overstatements (counts, "zero impact," "most/all/every")
4. Competitive or prescriptive framing without a source
5. Pre-GA / preview features taught as GA

---

## Report paths

| Caller | Report file |
|---|---|
| **create** | `.cursor/lp-preflight-state/{slug}-claim-check.md` (preflight reads it as its starting point) |
| **preflight** | `.cursor/lp-preflight-state/{slug}-claim-check.md` |
| **review** | `.cursor/pr-review-state/pr-{n}-claim-check.md` |

```markdown
---
disclaimer: Auto-generated by learning-path claim-check. Do not edit manually.
path_dir: {path_dir}
---

# Claim check: {path_dir}

Run against: {branch head commit} ({caller}, {full | changed since {commit}})

**Claims checked: N | Supported: N | Product-sourced: N | Contradicted: N | Unsupported: N | Overstated: N**

## MUST FIX (review-level)

### Contradicted
1. `{file}` - {claim}. Source: {quote or URL}. Fix: {one line}.

### Unsupported
…

### Overstated
…

## Product-sourced
1. `{file}` - {claim}. Facts row {#}: {source}.

## Author decides
…

## Sources used
…
```

MUST FIX first, then author-decides. Do not dump Supported claims into chat. No em dashes in the report body.

---

## Caller-specific chat

### Create (wrap-up)

Prefer a fresh agent pass that didn't write the prose. Report MUST FIX items to the author in plain language (problem, why, file) and fix them only after the author agrees. A claim with no row in `assets/facts.md` gets a row (with a source) or comes out of the path; don't leave it in unsourced. Re-run the check on the fixed sentences before the wrap-up summary.

### Preflight (results menu)

Merge MUST FIX items into the findings that feed the **one results menu** (dedupe). Use plain language (problem + why + file). Do **not** put verdict labels like "Contradicted" in author bullets. Do not open with a "What this check is" primer.

Offer **fix all** / **fix N** / combos for package-fixable claim items per [preflight Author-facing findings](../preflight-learning-path/reference-checks.md#author-facing-findings).

If none, say the claim check found no contradicted or unsupported product facts (as part of What we checked / clean results).

### Review (Phase 1 workbook)

Merge MUST FIX items into `pr-{n}-findings.md` under **Post inline if confirmed** (or **Verify in Block Editor** when live confirmation is needed). Tag **post inline** per [finding routing](reference-checks.md#finding-routing). Do not dump Supported into chat. Author-decides may stay Internal or become a short open question in the draft summary.

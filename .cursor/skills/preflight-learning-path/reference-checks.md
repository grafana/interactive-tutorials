# Reference checks (preflight-learning-path)

Author-side routing and readiness for [preflight-learning-path/SKILL.md](SKILL.md).

**Shared checklists (source of truth):** [../review-learning-path/reference-checks.md](../review-learning-path/reference-checks.md) and [../review-learning-path/learning-hub-standards.md](../review-learning-path/learning-hub-standards.md). Run every checklist the five-phase review coach runs in Phase 1.

**Publishing model (PR [#416](https://github.com/grafana/interactive-tutorials/pull/416)):** Single-repo packages in `interactive-tutorials`. Metadata in package `website.yaml`; prose in `content.json`. Website repo is read-only for conversion. Never plan companion website / `pathfinder_data` / shortcode work.

**Voice bar:** Same as review [comment-style.md](../review-learning-path/comment-style.md). Author chat and readiness only include **post inline** items. No em dashes.

---

## Finding severity (author)

Map review [finding routing](../review-learning-path/reference-checks.md#finding-routing) 1:1:

| Review tier | Author action |
|---|---|
| **Post inline** | **Fix before PR** (surface in chat + readiness) |
| **Internal** | Hide (do not mention in chat or readiness) |
| **Discard** | Hide |

Do not invent an author-only softer bar. Do not surface "Polish / follow-up" lists.

### Must surface (post-inline examples)

Apply the same five-phase coach rules (cite shared reference-checks; do not soften):

- Playwright / Block Editor runtime fail (when live failed or `walk-me` failed)
- **Framing milestones** in path `milestones`, or first hands-on `depends` on a framing ID (must be `depends: []`)
- **Fake steps in sections:** missing bookends outside the section; in-section intro markdown that numbers as a step (e.g. first child "You'll …")
- **False noops:** learner-action copy with `noop` and no `reftarget`
- Missing / broken required `website.yaml` identity; Learning Hub structure the author must change
- Path root / manifest `id` mismatch; Pathfinder CLI validate failure
- Secrets `doIt: true`; confirmed 404s; conversion prose only in legacy markdown
- Fragile / wrong selectors when live fails, or stable `data-testid` exists in DOM and the guide uses a weak selector
- **Claim-check MUST FIX:** Contradicted, Unsupported, or Overstated product facts per [claim-check.md](claim-check.md) (made-up counts, invented names, docs contradictions)

### Never surface

Wording polish, justified `:contains()` when live passed, CODEOWNERS reminders, audit noise, selector polish when live passed, landing screenshot notes, milestone-count guidelines.

---

## Checklists to run (Phase 1)

Apply every section from [../review-learning-path/reference-checks.md](../review-learning-path/reference-checks.md):

- Milestone `content.json` checks
- Section intro markdown numbered as a step
- Framing milestones / framing vs not framing
- Path root `content.json`
- Learning Hub structure + [learning-hub-standards.md](../review-learning-path/learning-hub-standards.md)
- `website.yaml`
- Valid manifests (CLI)
- Targeting / recommender
- Supplementary content
- Legacy website source (conversion, read-only)
- noop and non-interactive steps
- CODEOWNERS (discard for author chat)

Then run [claim-check.md](claim-check.md) across path root + milestone prose. Route Contradicted / Unsupported / Overstated as Fix before PR. Hide Supported from chat. Author-decides items may appear in readiness as open questions.

Tag each finding; keep only post-inline for author-facing output.

---

## Path type

Infer from branch diff, directory age, and legacy website source. Record in `{slug}.json` → `path_type`.

| Type | Signals | Live emphasis |
|---|---|---|
| **new** | New `{slug}-lj/`; no legacy website folder | Full Playwright; `website.yaml` + path root completeness |
| **conversion** | Built via `/build-interactive-lj`; prose-heavy | Legacy prose captured in package; Playwright full path |
| **update** | Changes existing package only | Touched interactive milestones first |

---

## Static-only preflight

`static-only: <reason>` at Phase 1 end skips Phase 2.

| Situation | Allowed? |
|---|---|
| **new** / **conversion** with interactive milestones | **No** |
| **update** touching only markdown / `website.yaml` | Yes, with reason |
| Practice run / no stack access | Yes, with reason (caps readiness) |

Reject bare `static-only`. Record `waive_live_testing` + `static_only_reason`.

When live was skipped or incomplete, readiness must include **Not live-tested** (interactive path `milestones` minus recorded Playwright results). Never recommend **Ready for PR** for new/conversion interactive when Playwright was waived.

---

## Readiness gate

Recommend **Ready for PR** only when all are true:

1. Zero open **Fix before PR** (post-inline) items
2. Pathfinder CLI validate passed, or CLI unavailable was noted and no other blockers
3. Playwright: no unexplained **missing** selectors on claimed-tested milestones (or documented stack prerequisite)
4. Block Editor: `already-tested` or successful `walk-me` (not `skip-smoke`) for new/conversion interactive, **or** author accepts **Open PR with notes**
5. `git status` clean of audit-guide artifacts under `{path_dir}`
6. Not `waive_live_testing` on new/conversion interactive (or outcome is **Open PR with notes**)

| Outcome | When |
|---|---|
| **Ready for PR** | Gate conditions met |
| **Fix then re-preflight** | Open post-inline items or Playwright/walk-me failures |
| **Open PR with notes** | Package mergeable but smoke skipped, or fresh-stack retest notes for the reviewer |

---

## PR opener checklist

Include in `{slug}-readiness.md`:

- [ ] Path `{path_dir}` validates with Pathfinder CLI (or CLI unavailable noted)
- [ ] First hands-on milestone `depends: []`
- [ ] No framing IDs in path `manifest.json` `milestones`
- [ ] `schemaVersion: "1.1.0"` or omitted on milestone `content.json`
- [ ] Playwright DOM checked for scoped interactive milestones
- [ ] Block Editor: already-tested notes, walk-me results, or skip noted for reviewer
- [ ] Path and milestone `website.yaml` complete
- [ ] **Not live-tested** section in PR description if any interactive milestone skipped Playwright
- [ ] Single PR in `interactive-tutorials` only (no companion website PR)

---

## State file schema

Path: `.cursor/lp-preflight-state/{slug}.json`

```json
{
  "path_dir": "monitor-azure-resources-lj",
  "slug": "monitor-azure-resources-lj",
  "website_slug": "monitor-azure-resources",
  "path_type": "conversion",
  "branch": "docs/my-path",
  "head_commit": "abc123",
  "learn_host": "learn.grafana.net",
  "stack_state": "learn.grafana.net shared",
  "waive_live_testing": false,
  "static_only_reason": null,
  "smoke_mode": null,
  "smoke_notes": null,
  "pre_review_assets": {},
  "phase": 3,
  "status": "in_progress",
  "readiness": null,
  "playwright": {},
  "pathfinder": {},
  "frontend_pr_url": null
}
```

| Field | Notes |
|---|---|
| `smoke_mode` | `already-tested` \| `walk-me` \| `skip-smoke` \| null |
| `smoke_notes` | Author notes for already-tested / skip |
| `pathfinder` | Only when `walk-me`; keys = milestone slug |
| `playwright` | DOM results per milestone |
| `phase` | Integer 0–5 |
| `readiness` | `Ready for PR` \| `Fix then re-preflight` \| `Open PR with notes` |

---

## Pathfinder CLI validate

```bash
node {pathfinder-app}/dist/cli/cli/index.js validate --packages {path_dir}
```

CLI failure → Fix before PR. CLI missing → note in readiness; do not abort the whole preflight.

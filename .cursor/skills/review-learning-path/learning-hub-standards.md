# Learning Hub standards

Learning Hub expectations for path reviews — adapted from `website/content/internal/docs/learning-hub/reviewing-learning-journeys/`.

Use in **Phase 1** static pass (milestone prose, path landing, CTAs, links).

**Routing:** tag findings with [reference-checks.md § finding routing](reference-checks.md#finding-routing). **Post inline** when the author must change structure or required fields. Keep pure wording polish in the workbook (**internal**) unless the reviewer promotes it.

**Package model (PR [#416](https://github.com/grafana/interactive-tutorials/pull/416)):** Legacy Hugo `index.md` / `_index.md` front matter maps to package `website.yaml`; body prose maps to `content.json` markdown blocks. Do not expect website-repo markdown updates in the LP PR.

## Package mapping

| Legacy (website repo) | Package (interactive-tutorials) |
|---|---|
| `{slug}/_index.md` front matter | `{slug}-lj/website.yaml` |
| `{slug}/_index.md` body | `{slug}-lj/content.json` markdown blocks |
| `{milestone}/index.md` front matter | `{milestone}/website.yaml` |
| `{milestone}/index.md` body + steps | `{milestone}/content.json` blocks |
| Framing milestone (value intro) | Separate milestone dir (e.g. `business-value/`) — **not** in path `manifest.json` `milestones` |

Field reference: [docs/website-yaml-reference.md](../../../docs/website-yaml-reference.md).

---

## Paths vs documentation

Learning paths teach **by doing** in sequence. Documentation answers lookup questions non-linearly.

**Reviewer question:** Is this helping someone look something up, or learn by doing?

| Signal | Concern |
|---|---|
| Long reference tables with no hands-on steps | Lookup content — belongs in docs |
| Steps without context or motivation | Missing path framing |
| Milestone reads like a doc page pasted into JSON | Editorial — suggest restructuring |

---

## Path landing page

Check path root `content.json` and `website.yaml` together.

### `website.yaml` identity

| Check | Fail if |
|---|---|
| `menuTitle`, `description` | Missing or `description` duplicates `menuTitle` |
| `journey.group` | Not one of `onboarding`, `data-availability`, `query-and-visualize`, `take-action` |
| `journey.skill` | Missing (renders as `TBD`) or clearly wrong for path complexity |
| `journey.logo` | Missing, broken `src`, or generic Grafana logo when a feature icon exists |
| `step` | Not `1` at path level |
| `cta.type` | Not `start` with `title` + `cta_text` |
| `related_journeys` | Legacy landing had soft recommendations but package omits them (conversion PR) |
| `related_journeys` copy | Heading implies **required** prior path ("you must complete…") instead of soft background — conflicts with [standalone principle](#standalone-principle) |

Common logo paths: `/static/img/menu/grafana2.svg` (generic), `/static/img/menu/cloud-dashboards.svg`, `/img/docs/logos/icon-alerting.svg` (verify path exists in website static assets).

### Path `content.json` body

| Section | Required text / structure |
|---|---|
| Introduction | Motivating overview of what the path teaches |
| `## Here's what to expect` | Outcomes list — what user can do after completing |
| `## Before you begin` | See [prerequisites](#before-you-begin-prerequisites) |
| `## Troubleshooting` | Exact boilerplate: "If you get stuck, we've got your back! Where appropriate, troubleshooting information is just a click away." |
| `## More to explore` | Exact boilerplate: "We understand you might want to explore other capabilities not strictly on this path. We'll provide you opportunities where it makes sense." |

Do **not** put milestone-specific troubleshooting or side-path links on the path landing — those belong on step `website.yaml` ([side journeys](#side-journeys) / [troubleshooting](#troubleshooting-on-verification-steps)).

### Landing screenshot

Every path should show a compelling end-result screenshot when possible (dashboard, alert, data flowing). Conversion PRs sometimes drop website-relative images — note in review body rather than blocking merge when prose and steps are otherwise sound.

| Check | Notes |
|---|---|
| No motivating visual at all | Note in review body |
| Image shows outcome the path does not deliver | Misleading — route via [finding routing](reference-checks.md#finding-routing) |
| Outdated UI in screenshot | Note in review body |
| Valid `cta.image` on path `website.yaml` or markdown image with working URL | OK |

---

## Before you begin (prerequisites)

Path root `content.json` `## Before you begin` must set users up for success.

| Prerequisite | Notes |
|---|---|
| Grafana Cloud account | Always first — link to signup |
| Data requirements | Metrics, logs, traces, profiles — be specific ("data flowing" not "some data") |
| Integrations / agents | Name the integration or collector required |
| Permissions | Editor, Admin, or named RBAC roles |
| Network / ports | Firewall, outbound connectivity when install steps need it |
| Familiarity | Concepts user should know beforehand |

**Review checklist:**

- Grafana Cloud account listed first
- All data requirements explicit and match first hands-on milestone
- Required permissions stated
- Network/port requirements when path installs agents or collectors
- No **hard** dependency on completing another learning path (see [standalone principle](#standalone-principle))
- Nothing omitted that would block users mid-path

---

## Milestone types and order

### Milestone count

Broad guidelines (not hard rules):

| Count | Guidance |
|---|---|
| 5 or fewer | OK for focused paths |
| 5–10 | Typical |
| More than 12 | Consider splitting |

Count path `manifest.json` `milestones` entries (hands-on only; exclude framing dirs).

### Value milestone (framing)

Every path should open with **why** before **how**. In packages this is usually a framing directory (`business-value`, `value-*`, `advantages-*`, `welcome`) with markdown-only `content.json` — **not** listed in path `milestones`. See [framing vs not framing](reference-checks.md#framing-vs-not-framing): `end-journey` stays in `milestones`; markdown-only alone does not mean framing.

| Check | Notes |
|---|---|
| No framing milestone and first hands-on jumps straight to steps without intro context | Editorial |
| Framing ID incorrectly listed in path `milestones` | See [framing milestones](reference-checks.md#framing-milestones) |
| Value milestone is generic / no clear problem statement | Editorial |
| Ambiguous prose package (e.g. `understanding-*`) in `milestones` | Internal until reviewer confirms framing vs path step |

### Task milestones (hands-on guides)

Each hands-on milestone in path `milestones` should have:

1. **Introduction** — context for what the user will do and why (opening markdown and/or bookends **outside** each `section`, not “You'll …” as the first in-section child)
2. **Actionable steps** — specific UI instructions in interactive blocks

| Red flag | Notes |
|---|---|
| Steps with no introductory context | Editorial |
| Vague copy ("configure the settings") | Editorial |
| Missing sign-in or navigation when UI assumes logged-in state | Defer until Pathfinder |
| Assumed expertise not listed in path prerequisites | Editorial |

**Good step copy:** "Click **Create alert rule**", "Enter `production` in the **Environment** field".

### Destination milestone (`end-journey`)

Final milestone should close the path.

| Check | Fail if |
|---|---|
| Exists | No `end-journey/` (or `end-<topic>/`) with `cta.type: conclusion` |
| Summary | No recap of what the user accomplished |
| Next steps | No related docs/paths in `side_journeys` or body markdown |
| `menuTitle` | Not "Destination reached!" (or peer-consistent variant) |

`end-journey` recap must reference only milestones in path `manifest.json` `milestones` — not framing packages excluded from the array.

---

## CTA types (`website.yaml`)

| `cta.type` | Use when | Package location |
|---|---|---|
| `start` | Path landing only | Path `website.yaml` |
| `continue` | Most task milestones — success is implicit | Step `website.yaml` |
| `success` | Verification checkpoints — shows "Were you successful?" | Step `website.yaml` |
| `conclusion` | Final milestone | `end-journey/website.yaml` |

**Use `success` sparingly** — only when explicit verification matters (data flowing, connection working, alert fired). Obvious UI confirmations (button clicked, dialog closed) stay `continue`.

| Check | Notes |
|---|---|
| Verification milestone uses `continue` instead of `success` | Editorial |
| Non-verification milestone uses `success` without reason | Editorial |

---

## Side journeys

Defined in step `website.yaml` → `side_journeys` (rendered by website; may also appear as trailing markdown in `content.json` from conversion — prefer **one source**).

**Valid destinations:** documentation pages, blog posts, YouTube videos.

**Not side journeys:** links to other learning paths (use path-level `related_journeys` or destination `side_journeys` for "what's next" docs).

| When to include | When to skip |
|---|---|
| Milestone introduces a concept with deeper docs | No relevant doc exists |
| User might ask "where can I learn more?" | Padding links without value |

**Quantity guideline:**

| Milestone type | Side paths |
|---|---|
| Value / intro | 0–2 |
| Action | 0–1 |
| Verification | 0–1 |
| Conclusion | 1–3 |

Duplication between `website.yaml` `side_journeys` and trailing `content.json` markdown — see [supplementary content](reference-checks.md#supplementary-content).

---

## Related journeys

Path-level `related_journeys` in `website.yaml` = **soft recommendations** on the landing page (helpful background, not required).

Destination `side_journeys` = **next steps** after completing the path (docs or continued learning).

| Acceptable | Problematic |
|---|---|
| "Consider taking X to learn dashboards" | Step prose: "Open the dashboard you created in [other path]" |
| User may already have skills — can skip recommendation | User cannot complete without artifacts from another path |

Hard dependency on another path's artifacts — route via [finding routing](reference-checks.md#finding-routing).

---

## Troubleshooting on verification steps

**Rule:** If a milestone or step asks the user to **verify** something worked, provide troubleshooting links for when it does not.

Verification keywords: verify, confirm, check, "you should see", "data is flowing", "alert fired".

Configure in step `website.yaml`:

```yaml
cta:
  type: success
  troubleshooting:
    title: Need help?
    items:
      - title: Data not appearing in Grafana
        link: /docs/grafana-cloud/send-data/troubleshooting/
```

| Check | Notes |
|---|---|
| Verification step with `cta.type: success` but no `cta.troubleshooting` | Editorial |
| Troubleshooting links point to non-existent pages | Verify URL in Phase 1; route via [finding routing](reference-checks.md#finding-routing) |
| Generic troubleshooting link that does not match the failure mode | Editorial |
| Legacy front matter had troubleshooting but conversion omitted it | Editorial |

Troubleshooting links must point to **existing** documentation. If no doc exists, flag for author to create or pick a real page — do not accept hallucinated URLs.

---

## Standalone principle

Every path must be completable with:

- A Grafana Cloud account
- Required data flowing (if stated in prerequisites)
- Motivation to learn

**No path should require completing another path first.**

| Hard dependency (block) | Soft suggestion (OK) |
|---|---|
| "Edit the alert rule you configured in [other path]" | `related_journeys` recommending background reading |
| `depends` or prose assumes artifact only created in another LP | Destination links to logical next paths |
| Prerequisites list another LP as required | "Consider taking X first" on landing |

Scan milestone `content.json` interactive copy and path root prerequisites for cross-path artifact references. Route via [finding routing](reference-checks.md#finding-routing).

---

## Outbound link verification

Verify links that point **outside** the package: `side_journeys`, `related_journeys`, `cta.troubleshooting`, and documentation URLs in markdown blocks.

| Check | Notes |
|---|---|
| Suspected 404 or wrong product area | Note in workbook; fetch URL in Phase 1 when conversion-heavy or links look AI-generated |
| Confirmed 404 after fetch | Route via [finding routing](reference-checks.md#finding-routing) |
| Page exists but title does not match link text | Editorial |
| Deprecated / archived doc when current page exists | Editorial |

During Phase 1, spot-check high-risk links on **conversion** PRs and any milestone with `cta.troubleshooting` or `side_journeys`. A suspected bad link is not posted until you confirm 404.

---

## Videos

Missing milestone videos is **not** a review issue — the video library is still growing.

If `content.json` or markdown embeds video:

- Relevant to milestone content
- Embed works
- Reflects current UI
- Supplements — does not replace — written steps

---

## Common pitfalls

Quick scan during Phase 1 (route via [finding routing](reference-checks.md#finding-routing)):

| Pitfall | Where to look |
|---|---|
| Missing landing screenshot | Path `content.json` / `website.yaml` |
| Vague instructions | Milestone interactive copy |
| Missing sign-in / first UI step | First hands-on milestone |
| Broken or outdated references | Links, menu labels, feature names |
| Assumed expertise | Steps vs path prerequisites |
| Orphan links (404) | `website.yaml` supplementary fields |
| Scope creep | Milestone tries to teach too much |
| Abrupt ending | Missing or thin `end-journey` |
| Made-up procedures | Steps not verified against product |
| Path reads like docs | Long reference sections, no doing |

---

## Internal course reference

Source slides (website repo, internal):

| Topic | Path under `content/internal/docs/learning-hub/reviewing-learning-journeys/` |
|---|---|
| Course overview | `00-intro/01-course-overview/` |
| Path vs docs | `01-foundations/04-how-ljs-differ-from-docs/` |
| Anatomy | `01-foundations/05-anatomy-of-a-journey/` |
| Landing page | `02-structure-and-format/09-structure-and-format/` through `14-boilerplate-more-to-explore/` |
| Prerequisites | `02-structure-and-format/15-prerequisites/` |
| Milestone types | `03-milestones/18-milestone-count/` through `22-destination-milestone/` |
| CTA types | `03-milestones/21-task-milestone-cta-types/` |
| Side / related journeys | `03-milestones/23-side-journeys-what/` through `26-related-journeys-how/` |
| Troubleshooting | `03-milestones/27-when-troubleshooting/` through `28-troubleshooting-frontmatter/` |
| Link verification | `03-milestones/29-verifying-outbound-links/` |
| Videos | `03-milestones/31-milestone-videos/` |
| Standalone principle | `04-user-experience/35-the-standalone-principle/` |
| Common pitfalls | `04-user-experience/36-common-pitfalls/` |
| Key takeaways | `05-appendix/45-key-takeaways/` |

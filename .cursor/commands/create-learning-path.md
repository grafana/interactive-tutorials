# /create-learning-path

Create a complete interactive learning path from scratch. Produces `content.json`, `manifest.json`, and `website.yaml` files in the interactive-tutorials repo.

> **Adding interactivity to an existing learning path?** Use `/build-interactive-lj` instead.

---

## Input

Before anything else, ask: **"Are you starting a learning path from scratch or picking up a proposed learning path from a learning journey in docs-ai?"**

- **From scratch:** the user provides a **feature or product goal** and **target audience** — proceed with the phases below as written.
- **From a learning journey:** the user provides the **docs-ai PR** (URL or number) for the signed-off journey.
  - `gh pr checkout` it into a local `docs-ai` checkout (same pattern as `review-learning-path`'s PR checkout). If checkout fails because the PR already merged and its branch is gone, fall back to reading the target branch (usually `main`) directly — the content is still there, it's just not on a live PR branch anymore.
  - The slug comes from whichever `journeys/<slug>/` directory the checkout touches — there's no separate ID to ask for.
  - Read `journeys/<slug>/outline/outline.md`. It has a section describing learning paths — heading text and casing vary ("Learning Paths" or "Learning paths"), and the split into what already exists versus what's still needed isn't standardized either: some journeys have no split at all, some need nothing, and entries can describe work already built on another branch, already merged, or explicitly dropped. Read the section for meaning, not for an exact heading or table match.
  - If the outline lists more than one needed path, ask the author which one to build first — build one path per run of this command; the author repeats the process for the others afterward.
  - Before treating the confirmed entry as "the plan," verify it's genuinely new, multi-milestone work — not a single interactive guide (a different, lighter artifact this command doesn't produce), not something already built elsewhere, and not cancelled.
  - The confirmed entry is usually one line describing scope, not a milestone list — derive the milestone breakdown yourself from that line and any accompanying notes (which sometimes point at reusing an existing interactive section from another package verbatim), the same judgment call you'd make with any other input.
  - Also read `journeys/<slug>/outline/reference/jargon-inventory.md`'s "UI elements (canonical labels)" table for terms to use verbatim in the generated content.

  This mode skips phase 3 below; see that phase for what happens instead.

---

## Workflow

Follow these phases in order:

1. **Validate environment.** Confirm the `interactive-tutorials` repo is writable and the `website` repo is readable in the workspace, and that Playwright MCP is available. The `website` repo is a read-only source — it's used only to read canonical docs and any existing source markdown. All generated files are written to interactive-tutorials.
2. **Read feature docs.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch.
3. **Propose path options — or use the imported plan.**
   - **From scratch:** review existing paths in `interactive-tutorials/[slug]-lj` for structural patterns — but do not copy a generic "case for observability" / "value of observability" milestone from an older path; see Critical rule 10. Propose 2-4 path options with milestones. Target 2-5 minutes per milestone, 6-8 milestones per path (max 10). Wait for user approval before proceeding.
   - **From a learning journey:** skip the proposal and the approval wait — the outline entry confirmed in the Input phase already tells you what to cover. Derive milestones from that scope yourself (same targets: 2-5 minutes per milestone, 6-8 per path). Use `jargon-inventory.md`'s terms verbatim wherever the generated content names a UI element. Proceed straight to phase 4 with that plan.
4. **Scaffold content files.** Create `content.json` for every milestone — interactive blocks for UI steps, markdown blocks for conceptual content. Gate any screenshot, embedded video, or markdown image behind a `renderer:website` conditional — see [Screenshots and videos](../../docs/learning-path-authoring.md#screenshots-and-videos-website-only-in-pathfinder) for the wrap / dual-branch mechanics. Don't gate plain YouTube text links or `website.yaml` `cta.image`.
5. **Create website metadata files.** Create `website.yaml` for the path and each milestone. Refer to `docs/website-yaml-reference.md`.
6. **Generate manifests.** Create `manifest.json` for the path (`type: "path"`, milestones array, targeting) and each milestone (`type: "guide"`, depends/recommends chain). Refer to `docs/manifest-reference.md`. Where fields can't be derived, ask the user to provide values before generating.
7. **Discover selectors.** Use Playwright at `learn.grafana.net` to find stable CSS selectors for each interactive element. The user must log in through the Playwright browser window (Okta SAML).
8. **Test in Pathfinder.** Tell the user which `content.json` to import into the Block Editor at `learn.grafana.net/?pathfinder-dev=true`. Wait for their feedback on each "Show me" / "Do it" button. Fix broken selectors based on their reports.
9. **Verify and wrap up.** Cross-check all factual claims against live docs. Update `.github/CODEOWNERS`.
   - **Cross-link.** Add this path to `related_journeys` in `website.yaml` and to `suggests`/`recommends` in `manifest.json` (see `docs/website-yaml-reference.md` and `docs/manifest-reference.md` — existing fields, nothing new to add) for *every* learning journey that surfaces this path, not only the one that triggered its creation.
   - **Label reminder.** Before opening the PR, add the `lh-learning-path` label so it appears on the Learning Hub project board.
   - **Handoff back to docs-ai (mode 2 only).** Using the docs-ai checkout from the Input phase, run `check-journey.py --embed-url <package-dir>` yourself and hand the author the generated shortcode — don't just tell them to go run it. Tell them explicitly what to do with it: paste it into the journey's slide in the `website` repo and open a PR there.
   - **Merge-order callout (mode 2 only).** In that same handoff, state plainly: do not merge the website PR until *this* path's PR is merged (not just opened) on `interactive-tutorials`'s default branch. A website PR that merges while its shortcode still points at an unmerged path leaves readers with a broken, empty embed.
   - Provide a summary of all files created.

For background on how this command relates to `/build-interactive-lj`, refer to `.cursor/learning-path-workflows/workflows.md`.

---

## Critical rules

1. **Never modify the website repo.** The `website` repo is a read-only source. Read canonical docs and any existing source markdown from it, but never add `pathfinder_data`, insert the `{{< pathfinder/json >}}` shortcode, or otherwise write to it. All generated files — `content.json`, `manifest.json`, and `website.yaml` — live in the interactive-tutorials repo.
2. **Read all canonical feature docs before writing content.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch. These docs are the authoritative source — never rely on training data.
3. **Scaffold ALL milestones.** Every milestone needs a `content.json`, including conceptual, intro, and conclusion pages.
4. **Use Playwright for selectors.** Never guess. Always inspect the actual DOM at `learn.grafana.net`.
5. **User handles all Pathfinder testing.** Tell the user which `content.json` to import. Wait for their feedback. Never import JSON or click interactive buttons yourself.
6. **Ask before fixing.** When the user reports a broken selector, explain and propose a fix, then wait for approval.
7. **3-attempt limit per selector.** If a selector fails after 3 tries, mark it `TODO:manual-review` and move on.
8. **Update CODEOWNERS.** Add the new `[slug]-lj/` directory to `.github/CODEOWNERS`.
9. **Verify docs accuracy.** After testing, cross-check all factual claims against live Grafana documentation.
10. **No generic "case for observability" milestone.** Do not scaffold a generic "case for observability" / "value of observability" / "business-value" milestone that just explains what observability is in the abstract. It's redundant boilerplate that duplicates content across every path and teaches nothing specific to this one (see [issue #597](https://github.com/grafana/interactive-tutorials/issues/597)). If the path genuinely needs a value-proposition milestone, make it product-specific from the start (for example "The advantages of Grafana Kubernetes Monitoring"), not a generic observability primer.

---

## Anti-patterns

- In `content.json` blocks, use `content` for instruction text — not `description`. The `description` field belongs in `website.yaml` (see `docs/website-yaml-reference.md`).
- Never use `formvalue` — use `targetvalue`
- Include `exists-reftarget` in requirements for steps with a `reftarget` (repo convention)
- Never use position-based selectors (`:nth-child`, `:first-of-type`)
- Never use non-standard CSS (`:contains()`, `:has-text()`)
- Never use data-dependent selectors — use `^=` starts-with patterns
- Never leave placeholder selectors (`"[selector]"`, `"TODO"`)
- All links in content.json must be absolute URLs (`https://grafana.com/docs/...`), not relative
- Never leave a screenshot, video, or markdown image ungated in `content.json` — wrap it in a `conditional` with `conditions: ["renderer:website"]` (see Step 4)
- Never scaffold a generic "case for observability" / "business-value" milestone — go straight into product-specific value or advantages content instead (see Critical rule 10)

---

## Reference

Consult these during the workflow:

| Document | When |
| --- | --- |
| `docs/website-yaml-reference.md` | Creating website.yaml (field reference, CTA types, examples) |
| `build-interactive-lj/reference/json-schema.md` | Writing content.json (block types, action types, field reference) |
| `build-interactive-lj/reference/selector-patterns.md` | Discovering selectors (priority, stability, anti-patterns) |
| `docs/manifest-reference.md` | Generating manifest.json files |
| `docs/learning-path-authoring.md` | Gating screenshots/videos for website-only rendering |
| `.cursor/proven-patterns.mdc` | Reusable patterns for common Grafana UI elements (auto-loaded) |

---

## Quick reference

### Block types

`markdown` · `interactive` · `multistep` · `section` · `guided` · `conditional`

### Action types

`highlight` · `button` · `formfill` · `hover` · `navigate` · `noop` · `popout`

### Selector priority

`data-testid` > `aria-label` > `href` > `id` > stable class

### Key properties

- `doIt: false` — hides "Do it" button, keeps "Show me"
- `targetvalue` — text to enter for `formfill` actions
- `content` — instruction text for interactive blocks

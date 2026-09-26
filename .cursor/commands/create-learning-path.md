# /create-learning-path

Create a complete interactive learning path from scratch. Produces `content.json`, `manifest.json`, and `website.yaml` files in the interactive-tutorials repo.

> **Adding interactivity to an existing learning path?** Use `/build-interactive-lj` instead.

---

## Input

The user provides:
- **Feature or product goal** — what the learning path should teach
- **Target audience** — who it's for (typically Grafana beginners)

---

## Workflow

Follow these phases in order:

1. **Validate environment.** Confirm the `interactive-tutorials` repo is writable and the `website` repo is readable in the workspace, and that Playwright MCP is available. The `website` repo is a read-only source — it's used only to read canonical docs and any existing source markdown. All generated files are written to interactive-tutorials.
2. **Read feature docs.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch.
3. **Propose path options.** Review existing paths in `interactive-tutorials/[slug]-lj` for structural patterns — but do not copy a generic "case for observability" / "value of observability" milestone from an older path; see Critical rule 10. Propose 2-4 path options with milestones. Target 2-5 minutes per milestone, 6-8 milestones per path (max 10). Wait for user approval before proceeding.
4. **Scaffold content files.** Create `content.json` for every milestone — interactive blocks for UI steps, markdown blocks for conceptual content. Gate any screenshot, embedded video, or markdown image behind a `renderer:website` conditional — see [Screenshots and videos](../../docs/learning-path-authoring.md#screenshots-and-videos-website-only-in-pathfinder) for the wrap / dual-branch mechanics. Don't gate plain YouTube text links or `website.yaml` `cta.image`.
5. **Create website metadata files.** Create `website.yaml` for the path and each milestone. Refer to `docs/website-yaml-reference.md`.
6. **Generate manifests.** Create `manifest.json` for the path (`type: "path"`, milestones array, targeting) and each milestone (`type: "guide"`, depends/recommends chain). Refer to `docs/manifest-reference.md`. Where fields can't be derived, ask the user to provide values before generating.
7. **Discover selectors.** Use Playwright at `learn.grafana.net` to find stable CSS selectors for each interactive element. The user must log in through the Playwright browser window (Okta SAML). If an element has no stable selector after 3 tries, write the instruction as `markdown` (or fold it into the next real interactive step). Do **not** use `action: "noop"` as a selector fallback.
8. **Test in Pathfinder.** Tell the user which `content.json` to import into the Block Editor at `learn.grafana.net/?pathfinder-dev=true`. Wait for their feedback on each "Show me" / "Do it" button. Fix broken selectors based on their reports. If Show me cannot target the control, convert that learner action to `markdown` rather than `noop`.
9. **Verify and wrap up.** Cross-check all factual claims against live docs. Update `.github/CODEOWNERS`. Provide a summary of all files created.

For background on how this command relates to `/build-interactive-lj`, refer to `.cursor/learning-path-workflows/workflows.md`.

---

## Critical rules

1. **Never modify the website repo.** The `website` repo is a read-only source. Read canonical docs and any existing source markdown from it, but never add `pathfinder_data`, insert the `{{< pathfinder/json >}}` shortcode, or otherwise write to it. All generated files — `content.json`, `manifest.json`, and `website.yaml` — live in the interactive-tutorials repo.
2. **Read all canonical feature docs before writing content.** Identify the canonical Grafana docs pages for the feature. Read every doc page in full from the local `website` repo first, then WebFetch. These docs are the authoritative source — never rely on training data.
3. **Scaffold ALL milestones.** Every milestone needs a `content.json`, including conceptual, intro, and conclusion pages.
4. **Use Playwright for selectors.** Never guess. Always inspect the actual DOM at `learn.grafana.net`.
5. **User handles all Pathfinder testing.** Tell the user which `content.json` to import. Wait for their feedback. Never import JSON or click interactive buttons yourself.
6. **Ask before fixing.** When the user reports a broken selector, explain and propose a fix, then wait for approval.
7. **3-attempt limit per selector.** If a selector fails after 3 tries, stop targeting it. Put the learner action in `markdown`, or fold it into the next interactive step's `content`. Never use `action: "noop"` for click, open, type, fill, or select copy. Never leave `TODO:manual-review` as a silent skip.
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
- Never use `action: "noop"` for a learner action (click, open, type, fill, select, turn off) when Pathfinder cannot target the control. Use `markdown`, or fold the instruction into the next real interactive step. `noop` is only for a numbered pause that is **not** a click/type instruction (for example "Wait for the query to finish").
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

# /build-interactive-lj

Convert an existing markdown learning path into a complete interactive package in the interactive-tutorials repo. Reads the learning path markdown in the website repo as the source, then creates all `content.json`, `manifest.json`, and `website.yaml` files in interactive-tutorials. The `website.yaml` files capture the front matter from the existing learning path markdown so the package carries its own website metadata. The website repo is read-only — this command never modifies it, and the existing markdown stays in place.

> **Creating a brand-new learning path?** Use `/create-learning-path` instead.

---

## Input

Ask the user for the **learning path slug** (the folder name from `website/content/docs/learning-paths/`).

---

## Workflow

Follow these phases in order:

1. **Validate environment.** Confirm the `interactive-tutorials` repo is writable and the `website` repo is readable in the workspace (website is a read-only source), and that Playwright MCP is available.
2. **Read existing milestones and feature docs.** Locate the learning path in `website/content/docs/learning-paths/[slug]/`. List every milestone directory. Then read the canonical Grafana docs for every product/feature referenced in the milestones — these are the authoritative source for all factual claims.
3. **Scaffold content files.** Create `content.json` for every milestone in the interactive-tutorials repo — interactive blocks for UI steps, markdown blocks for conceptual content. Because the website markdown is no longer used to render this learning path, capture all conceptual prose from each milestone's `index.md` body as markdown blocks so no content is lost. Extract `side_journeys`, `related_journeys`, and `cta.troubleshooting` from each existing `index.md` and include them as markdown blocks. **Exception: the `business-value` milestone gets markdown blocks only — no interactive blocks, sections, or guided blocks.**
4. **Create website metadata files.** Create a `website.yaml` for the path and each milestone, derived from the front matter of the corresponding website markdown files. Map the path `_index.md` front matter into the path-level `website.yaml` and each milestone `index.md` front matter into that milestone's `website.yaml` (for example, `title` → `menuTitle`, plus `description`, `weight`, step ordering, `cta`, `related_journeys` at the path level, and `side_journeys` at the step level). These files take the place of the markdown front matter as the package's source of website metadata; the website markdown itself stays unchanged. Refer to `docs/website-yaml-reference.md`.
5. **Generate manifests.** Create `manifest.json` for the path (`type: "path"`, milestones array, targeting) and each milestone (`type: "guide"`, depends/recommends chain). Refer to `docs/manifest-reference.md`. **Exception: exclude `business-value` from the path-level `milestones` array.** The `business-value` milestone still gets its own `manifest.json` with `depends: []` and `recommends: ["[slug]-[first-interactive-milestone]"]`, but it is not a registered stop on the path.
6. **Discover selectors.** Use Playwright at `learn.grafana.net` to find stable CSS selectors for each interactive element. The user must log in through the Playwright browser window (Okta SAML).
7. **Test in Pathfinder.** Tell the user which `content.json` to import into the Block Editor at `learn.grafana.net/?pathfinder-dev=true`. Wait for their feedback on each "Show me" / "Do it" button. Fix broken selectors based on their reports.
8. **Verify and wrap up.** Cross-check all factual claims against live docs. Update `.github/CODEOWNERS`. Provide a summary of all files created.

For background on how this command relates to `/create-learning-path`, refer to `.cursor/learning-path-workflows/workflows.md`.

---

## Critical rules

1. **Never modify the website repo.** The `website` repo is a read-only source. Read the learning path markdown, frontmatter, and canonical docs from it, but never add `pathfinder_data`, insert the `{{< pathfinder/json >}}` shortcode, or otherwise write to it. All generated files live in the interactive-tutorials repo.
2. **Read all canonical feature docs before writing content.** Identify every Grafana product/feature referenced in the milestones. Read the docs pages in full from the local `website` repo first, then WebFetch. These docs are the authoritative source for all factual claims — never rely on training data.
3. **Scaffold ALL milestones.** Every milestone needs a `content.json`, including conceptual, intro, and conclusion pages. Pathfinder tracks progress through every milestone.
4. **Capture all content in `content.json`.** Since the website no longer renders this learning path, every milestone's conceptual prose must be carried into its `content.json` as markdown blocks. Nothing should remain only in the website markdown.
5. **`business-value` is markdown-only.** The `business-value` milestone always uses markdown blocks exclusively. Never add interactive, section, guided, or multistep blocks to it.
6. **Exclude `business-value` from the path manifest.** Do not include the `business-value` milestone in the path-level `manifest.json` `milestones` array. It has its own `manifest.json` with `depends: []` and `recommends: ["[slug]-[first-interactive-milestone]"]`, but it is not a path stop. The path's `milestones` array starts with the first interactive milestone.
7. **Include supplementary content from frontmatter.** Extract `side_journeys`, `related_journeys`, and `cta.troubleshooting` from each `index.md` and add them as markdown blocks at the end of the `blocks` array.
8. **Derive `website.yaml` from existing front matter.** Create a `website.yaml` for the path and every milestone that captures the existing markdown front matter (`menuTitle`, `description`, `weight`, `step`, `cta`, `related_journeys`/`side_journeys`). Don't invent metadata — take values from the source front matter or docs, and where a required field is missing from the source, ask the user. Refer to `docs/website-yaml-reference.md`.
9. **Use Playwright for selectors.** Never guess. Always inspect the actual DOM at `learn.grafana.net`.
10. **User handles all Pathfinder testing.** Tell the user which `content.json` to import into the Block Editor. Wait for their feedback. Never import JSON or click interactive buttons yourself.
11. **Ask before fixing.** When the user reports a broken selector, explain the problem and proposed fix, then wait for approval.
12. **3-attempt limit per selector.** If a selector fails after 3 tries, mark it `TODO:manual-review` and move on.
13. **Update CODEOWNERS.** Add the new `[slug]-lj/` directory to `.github/CODEOWNERS`.

---

## Anti-patterns

- In `content.json` blocks, use `content` for instruction text — not `description`. The `description` field belongs in `website.yaml` (see `docs/website-yaml-reference.md`)
- Never use `formvalue` — use `targetvalue`
- Include `exists-reftarget` in requirements for steps with a `reftarget` (repo convention)
- Never use position-based selectors (`:nth-child`, `:first-of-type`)
- Never use non-standard CSS (`:contains()`, `:has-text()`)
- Never use data-dependent selectors — use `^=` starts-with patterns
- Never leave placeholder selectors (`"[selector]"`, `"TODO"`)

---

## Reference

Consult these during the workflow:

| Document | When |
| --- | --- |
| `reference/json-schema.md` | Writing content.json (block types, action types, field reference) |
| `reference/selector-patterns.md` | Discovering selectors (priority, stability, anti-patterns) |
| `../create-learning-path/reference/frontmatter-schema.md` | Reading website front matter fields and CTA types (source only) |
| `docs/website-yaml-reference.md` | Creating website.yaml (field reference, CTA types, examples) |
| `docs/manifest-reference.md` | Generating manifest.json files |
| `.cursor/proven-patterns.mdc` | Reusable patterns for common Grafana UI elements (auto-loaded) |

---

## Quick reference

### Block types

`markdown` · `interactive` · `multistep` · `section` · `guided`

### Action types

`highlight` · `button` · `formfill` · `hover` · `navigate` · `noop` · `popout`

### Selector priority

`data-testid` > `aria-label` > `href` > `id` > stable class

### Key properties

- `doIt: false` — hides "Do it" button, keeps "Show me"
- `targetvalue` — text to enter for `formfill` actions
- `content` — instruction text for interactive blocks

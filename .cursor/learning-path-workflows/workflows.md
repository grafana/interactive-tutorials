# Learning path workflows

The two workflows below create interactive learning paths. Both produce the same outputs — `content.json` and `manifest.json` files in the interactive-tutorials repo, plus website markdown scaffolding — but they start from different places.

| Workflow | Starting point | Command |
| --- | --- | --- |
| **A: Make an existing LP interactive** | Milestone markdown already exists in the website repo | `/build-interactive-lj` |
| **B: Create a new LP from scratch** | No markdown exists — starting from a feature description | `/create-learning-path` |

## Before you start (both workflows)

You need:
- The **website** repository cloned locally
- The **interactive-tutorials** repository cloned locally
- **Playwright MCP** configured in Cursor (for CSS selector discovery)
- Access to `https://learn.grafana.net/` (the test environment for selector discovery and testing)

## What both workflows produce

**interactive-tutorials repo** (`[slug]-lj/`):
- `content.json` — Path-level cover page (intro, objectives, prerequisites)
- `manifest.json` — Path manifest with `type: "path"`, targeting, milestones array
- `[milestone]/content.json` — Each milestone's interactive guide content
- `[milestone]/manifest.json` — Each milestone's manifest with `type: "guide"` and dependency chain

**website repo** (`content/docs/learning-paths/[slug]/`):
- `_index.md` — Path cover page with `pathfinder_data: [slug]-lj` and `{{< pathfinder/json >}}` body
- `[milestone]/index.md` — Each milestone with `pathfinder_data: [slug]-lj/[milestone]` and `{{< pathfinder/json >}}` body

## The one difference between A and B

- **Workflow A**: Milestone markdown already exists. The existing body content is removed entirely and replaced with `{{< pathfinder/json >}}`. The `pathfinder_data` field is added to each file's front matter.
- **Workflow B**: No milestone markdown exists. The `_index.md` and every `[milestone]/index.md` are created from scratch with full Hugo front matter, `pathfinder_data`, and `{{< pathfinder/json >}}`.

Everything else — content.json scaffolding, manifest generation, selector discovery, testing, and verification — is identical.

---

## Shared steps

Both workflows follow the same steps in the same order. The only variation is in the website markdown step.

| Step | What happens | Who does the work |
| --- | --- | --- |
| 1. Environment validation | Verifies both repos are accessible and Playwright is available | AI |
| 2. Learning path validation / planning | **A:** Locates existing website markdown, lists milestones, reads canonical feature docs. **B:** Proposes 2-4 path options with milestones, gets your approval, reads canonical feature docs. | AI (B requires your approval) |
| 3. Scaffold content files | Creates `content.json` for every milestone (interactive blocks for UI steps, markdown blocks for conceptual content), including supplementary content from front matter (`side_journeys`, `related_journeys`, `cta.troubleshooting`) | AI |
| 4. Generate manifests | Creates `manifest.json` for the path (`type: "path"`, milestones array, targeting, startingLocation) and each milestone (`type: "guide"`, depends/recommends chain) | AI |
| 5. Selector discovery | Uses Playwright at `learn.grafana.net` to find stable CSS selectors for each interactive element. You must manually log in through the Playwright browser window (Okta SAML). | AI discovers selectors, **you log in** |
| 6. Test in Pathfinder | Collaborative testing at `learn.grafana.net/?pathfinder-dev=true`. AI tells you which `content.json` to import into the Block Editor, you click through "Show me" / "Do it" buttons and report failures, AI fixes selectors. | **You test**, AI fixes |
| 6b. Verify docs accuracy | Cross-checks all factual claims in the content against live Grafana documentation | AI |
| 7. Report and next steps | Summary of all files created, CODEOWNERS update, and PR guidance | AI |

### Website markdown step (the difference)

**Workflow A** — After scaffolding `content.json` files in Step 3, the AI updates each existing milestone `index.md`:
- Adds `pathfinder_data: [slug]-lj/[milestone]` to the front matter
- Replaces the entire body with `{{< pathfinder/json >}}`
- Same for the path `_index.md` (adds `pathfinder_data: [slug]-lj`, replaces body)

**Workflow B** — In Step 3, the AI creates the milestone `index.md` and path `_index.md` from scratch, with full Hugo front matter and `{{< pathfinder/json >}}` body. Refer to the `learning-hub-learning-paths` skill in the website repo for the complete front matter templates.

### Session planning

For paths with 7+ milestones, plan for two sessions. The natural break point is after Steps 1-4 (all content, manifests, and website markdown on disk). Resume at Step 5 (selector discovery).

### Example prompts

**Workflow A:**
> /build-interactive-lj
>
> (When asked) The learning path slug is `mysql-data-source`.

**Workflow B:**
> /create-learning-path
>
> Feature: Setting up MongoDB monitoring with the Grafana Cloud integration
> Audience: Grafana beginners who have MongoDB running and want metrics in Grafana Cloud

### What to do after

- Review generated files in both repos
- Run the cross-repo checklist (matching IDs, correct dependency chains, `pathfinder_data` values match interactive-tutorials directories)
- The AI updates `.github/CODEOWNERS` with the new `[slug]-lj/` directory
- Commit changes and open PRs: one for `interactive-tutorials`, one for `website`

---

## Quick reference

| Workflow | Command | Repos | Key output |
| --- | --- | --- | --- |
| Make existing LP interactive | `/build-interactive-lj` | interactive-tutorials + website | `content.json` + `manifest.json` files, updated website markdown |
| New LP from scratch | `/create-learning-path` | interactive-tutorials + website | `content.json` + `manifest.json` files, new website markdown |

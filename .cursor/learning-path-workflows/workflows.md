# Learning path workflows

Use the `/create-learning-path` command to build a new interactive learning path from scratch. If you have an existing non-interactive learning path that you need to convert, refer to the [appendix](#appendix-convert-an-existing-learning-path).

## Before you start

Make sure you have:

- The **website** and **interactive-tutorials** repositories cloned locally in the same Cursor workspace
- **Playwright MCP** configured in Cursor (the AI uses this to discover CSS selectors)
- Access to `https://learn.grafana.net/` (the test environment)

## What the command produces

`/create-learning-path` generates files in the **interactive-tutorials** repo under `[slug]-lj/`:

- `content.json` and `manifest.json` at the path level
- `[milestone]/content.json` and `[milestone]/manifest.json` for each milestone

## Run the command

Run `/create-learning-path` and describe what the path should cover:

```
/create-learning-path

Feature: Setting up MongoDB monitoring with the Grafana Cloud integration
Audience: Grafana beginners who have MongoDB running and want metrics in Grafana Cloud
```

The AI reads the canonical Grafana docs for the feature, proposes 2–4 path options with milestones, and waits for your approval before writing any files.

## What happens during a session

Every session follows five phases. The AI handles most of the work — your main responsibility is approving the milestone plan in Phase 1 and testing interactive steps in Phase 4.

### Phase 1: Setup and planning

The AI validates that both repos are accessible, reads the canonical Grafana docs for the feature, and proposes milestones for your approval.

**Your role:** Review and approve the proposed milestones before the AI writes anything.

### Phase 2: Content and manifest generation

The AI creates `content.json` files for every milestone (interactive blocks for UI steps, markdown blocks for conceptual content) and generates `manifest.json` files with the correct dependency chains.

**Your role:** None — this phase is fully automated.

### Phase 3: Selector discovery

The AI uses Playwright to inspect the DOM at `learn.grafana.net` and find stable CSS selectors for each interactive element.

**Your role:** Log in through the Playwright browser window or Cursor tab when prompted. The test environment uses Okta SAML, which the AI can't authenticate through on its own.

### Phase 4: Testing

The AI tells you which `content.json` to import into the Pathfinder Block Editor at `learn.grafana.net/?pathfinder-dev=true`. You click through the "Show me" and "Do it" buttons and report any failures. The AI fixes broken selectors based on your feedback.

**Your role:** This is the most hands-on phase. Test every interactive step and report exactly what fails — for example, "Show me on step 3 highlights the wrong element" or "Do it on step 5 doesn't click anything."

### Phase 5: Wrap-up

The AI verifies factual claims against the docs, updates `.github/CODEOWNERS`, and provides a summary of all files created.

**Your role:** Review the generated files, then open a PR in the `interactive-tutorials` repo.

## Tips

- **Plan for session length.** Paths with 7+ milestones often take two sessions. A natural break point is after Phase 2 (all content and manifests on disk). Resume at Phase 3 (selector discovery) in a new session.
- **Selector fixes have a 3-attempt limit.** If a selector can't be resolved after 3 tries, the AI marks it `TODO:manual-review` and moves on. You can fix these by hand later.

---

## Appendix: Convert an existing learning path

Use `/build-interactive-lj` when milestone markdown already exists in the website repo and you need to add interactivity. This workflow requires both the **website** and **interactive-tutorials** repositories in your Cursor workspace. The AI reads the existing milestones, creates `content.json` files with interactive blocks, and updates each `index.md` to use Pathfinder rendering.

The conversion command follows the same five phases as `/create-learning-path`. The only difference is Phase 1: instead of proposing new milestones, the AI locates the existing ones and uses them as its starting point.

When complete, you'll open PRs in both the `interactive-tutorials` and `website` repos.
Before opening PRs, verify that milestone IDs match between `content.json`, `manifest.json`, and website front matter. The AI runs this check automatically, but a quick manual scan catches edge cases.

Run the command and provide the learning path slug when asked:

```
/build-interactive-lj

The learning path slug is mysql-data-source.
```

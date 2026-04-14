# Learning path workflows

Two Cursor commands create interactive learning paths. Both produce the same outputs but start from different places. This guide explains when to use each command, what to expect during a session, and what you're responsible for.

| Command | When to use it |
| --- | --- |
| `/build-interactive-lj` | A learning path already has milestone markdown in the website repo and you want to add interactivity |
| `/create-learning-path` | You're building a new learning path from scratch, starting from a feature description |

## Before you start

Make sure you have:

- The **website** and **interactive-tutorials** repositories cloned locally in the same Cursor workspace
- **Playwright MCP** configured in Cursor (the AI uses this to discover CSS selectors)
- Access to `https://learn.grafana.net/` (the test environment)

## What the commands produce

Both commands generate files in two repos:

**interactive-tutorials** (`[slug]-lj/`):
- `content.json` and `manifest.json` at the path level
- `[milestone]/content.json` and `[milestone]/manifest.json` for each milestone

**website** (`content/docs/learning-paths/[slug]/`):
- `_index.md` for the path cover page
- `[milestone]/index.md` for each milestone

Every website markdown file uses `pathfinder_data` front matter to link to the interactive-tutorials content, and `{{< pathfinder/json >}}` as the body. The AI handles this automatically.

## Choose your command

### `/build-interactive-lj` — convert an existing learning path

Use this when milestone markdown already exists in the website repo. The AI reads the existing milestones, creates `content.json` files with interactive blocks, and updates each `index.md` to use Pathfinder rendering.

Run the command and provide the learning path slug when asked:

```
/build-interactive-lj

The learning path slug is mysql-data-source.
```

### `/create-learning-path` — build a new learning path

Use this when no milestone markdown exists yet. The AI reads the canonical Grafana docs for the feature, proposes 2-4 path options with milestones, and waits for your approval before writing any files.

Run the command and describe what the path should cover:

```
/create-learning-path

Feature: Setting up MongoDB monitoring with the Grafana Cloud integration
Audience: Grafana beginners who have MongoDB running and want metrics in Grafana Cloud
```

## What happens during a session

Both commands follow the same phases. The difference is only in how the starting content is sourced — everything after that is identical.

### Phase 1: Setup and planning

The AI validates that both repos are accessible, reads the canonical Grafana docs for the feature, and either locates existing milestones (`/build-interactive-lj`) or proposes new ones for your approval (`/create-learning-path`).

**Your role:** For `/create-learning-path`, review and approve the proposed milestones before the AI writes anything.

### Phase 2: Content and manifest generation

The AI creates `content.json` files for every milestone (interactive blocks for UI steps, markdown blocks for conceptual content) and generates `manifest.json` files with the correct dependency chains. It also creates or updates the website markdown.

**Your role:** None — this phase is fully automated.

### Phase 3: Selector discovery

The AI uses Playwright to inspect the DOM at `learn.grafana.net` and find stable CSS selectors for each interactive element.

**Your role:** Log in through the Playwright browser window when prompted. The test environment uses Okta SAML, which the AI can't authenticate through on its own.

### Phase 4: Testing

The AI tells you which `content.json` to import into the Pathfinder Block Editor at `learn.grafana.net/?pathfinder-dev=true`. You click through the "Show me" and "Do it" buttons and report any failures. The AI fixes broken selectors based on your feedback.

**Your role:** This is the most hands-on phase. Test every interactive step and report exactly what fails — for example, "Show me on step 3 highlights the wrong element" or "Do it on step 5 doesn't click anything."

### Phase 5: Wrap-up

The AI verifies factual claims against the docs, updates `.github/CODEOWNERS`, and provides a summary of all files created.

**Your role:** Review the generated files, then open PRs in both repos.

## Tips

- **Plan for session length.** Paths with 7+ milestones often take two sessions. A natural break point is after Phase 2 (all content and manifests on disk). Resume at Phase 3 (selector discovery) in a new session.
- **Selector fixes have a 3-attempt limit.** If a selector can't be resolved after 3 tries, the AI marks it `TODO:manual-review` and moves on. You can fix these by hand later.
- **Review the cross-repo checklist.** Before opening PRs, verify that milestone IDs match between `content.json`, `manifest.json`, and website front matter. The AI runs this check automatically, but a quick manual scan catches edge cases.

## Quick reference

| Command | Starting point | Key output |
| --- | --- | --- |
| `/build-interactive-lj` | Existing milestone markdown in website repo | `content.json` + `manifest.json` files, updated website markdown |
| `/create-learning-path` | Feature description (no existing markdown) | `content.json` + `manifest.json` files, new website markdown |

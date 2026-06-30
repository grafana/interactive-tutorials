# Learning path workflows

Use the `/create-learning-path` command to build a new interactive learning path from scratch. If you have an existing non-interactive learning path that you need to convert, refer to the [appendix](#appendix-convert-an-existing-learning-path).

## Before you start

Make sure you have:

- The **website** and **interactive-tutorials** repositories cloned locally in the same Cursor workspace
- **Playwright MCP** configured in Cursor (the AI uses this to discover CSS selectors)
- Access to `https://learn.grafana.net/` (the test environment)
- Understanding of what a selector is. A selector is a way to identify an element on a webpage so that scripts can interact with it. Think of it like a street address: the more precise and stable it is, the better the directions to get there, even if some landmarks change.
  In the context of interactive learning paths, selectors are used to identify buttons, menu items, text boxes, or other parts of the Grafana Cloud UI so interactive guides can highlight the element ("Show me") or take action on behalf of the user ("Do it").
  The command in this workflow prompts an AI agent to find the necessary selectors in the Grafana Cloud application code, but you need to test what it gives you to make sure the selectors work and are durable across variations in the stack's data.

## What the command produces

`/create-learning-path` generates all files in the **interactive-tutorials** repo under `[slug]-lj/`:

- `content.json`, `manifest.json`, and `website.yaml` at the path level
- `[milestone]/content.json`, `[milestone]/manifest.json`, and `[milestone]/website.yaml` for each milestone

The `website.yaml` files are used to create deploy previews so you can see the non-interactive path before it's published to the Learning Hub.

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

### Phase 2: Content, manifest, and website metadata generation

The AI creates `content.json` files for every milestone (interactive blocks for UI steps, markdown blocks for conceptual content), generates `manifest.json` files with the correct dependency chains, and creates `website.yaml` files with metadata required to publish to the website.

**Your role:** This phase is mostly automated. The agent might ask you to supply some of the `website.yaml` values if it can't derive them on its own.

### Phase 3: Selector discovery

The AI uses Playwright to inspect the DOM at `learn.grafana.net` and find stable CSS selectors for each interactive element.

**Your role:** Log in through the Playwright browser window or Cursor tab when prompted. The test environment uses Okta SAML, which the AI can't authenticate through on its own.

### Phase 4: Testing

Use the Block Builder **PR review tool** (dev tools, pathfinder-app 1.4.5+) to load milestone `content.json` files from the `interactive-tutorials` PR under review — do not copy-paste JSON manually unless the tool is unavailable. Test one milestone at a time at `learn.grafana.net/?pathfinder-dev=true`. Click through every **Show me** and **Do it** step and report failures.

**Your role:** Navigate to each milestone's starting page, open the PR review tool, select the milestone, and test every interactive step. Report exactly what fails — for example, "Show me on step 3 highlights the wrong element" or "Do it on step 5 doesn't click anything."

> [!IMPORTANT]
> Test the `content.json` files or the resulting PR in multiple stacks and environments. If you only test in `learn.grafana.net`, you might miss some gotchas, such as permissions required to access a feature or UI variations if the feature is already configured. Use the `ops` environment, your own staff stack, or any other environment you have access to. Aim to test widely to ensure the guide is as unbreakable as possible.

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

## Quick reference

| Command | Starting point | Key output |
| --- | --- | --- |
| `/build-interactive-lj` | Existing milestone markdown in website repo | `content.json` + `manifest.json` files, updated website markdown |
| `/create-learning-path` | Feature description (no existing markdown) | `content.json` + `manifest.json` + `website.yaml` files |
| `/review-learning-path-pr` | Existing LP PR in `interactive-tutorials` (share PR URL/number) | Guided review: findings doc, live testing, GitHub review with inline blockers and submitted verdict |

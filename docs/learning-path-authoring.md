# Author interactive learning paths

This guide is for Grafana docs writers who add Pathfinder interactivity to learning paths.

You build a package in this repo (`interactive-tutorials`) with Cursor commands, then smoke-test **Show me** / **Do it** steps on a Grafana Cloud stack you can log into (commonly `learn.grafana.net`, or your own personal stack) before opening a PR. All generated files land here; you do not write website markdown for these workflows.

Package directories use an `-lj` suffix (from the legacy "learning journey" name). If the path slug is `mysql-data-source`, the package is `mysql-data-source-lj/`. That naming will change eventually, but packages must use `-lj` for now. The slug usually matches the folder under `website/content/docs/learning-paths/` when you are converting. For a new path, you and the agent agree on it during planning.

## Prerequisites

- Always keep this `interactive-tutorials` repo checked out in Cursor. Packages live here and PRs open here.
- Add the website repo to the same workspace when you need it as a read-only source.
  - Converting an existing path (`/build-interactive-lj`) needs `website/content/docs/learning-paths/[slug]/`.
  - Creating a new path (`/create-learning-path`) reads canonical Grafana docs from the local website checkout when available.
  - Preflight or review of an already-built `[slug]-lj/` package does not need the website repo.
- Enable Playwright MCP in Cursor (see [How to test and review](#how-to-test-and-review)).
- Use a Grafana Cloud stack you can log into for live UI checks. Common options are `learn.grafana.net` or a personal stack.

## Which command to run

| When | Command | Outcome |
| --- | --- | --- |
| New path, no existing website markdown | [`/create-learning-path`](../.cursor/commands/create-learning-path.md) | Full `[slug]-lj/` package |
| Existing website LP markdown to convert | [`/build-interactive-lj`](../.cursor/commands/build-interactive-lj.md) | Same package layout, sourced from website markdown (read-only) |
| Package ready, before opening a PR | [`/preflight-learning-path`](../.cursor/commands/preflight-learning-path.md) | Author self-review: static checks + Playwright, readiness report, optional fixes |
| Reviewing someone else’s LP PR | [`/review-learning-path-pr`](../.cursor/commands/review-learning-path-pr.md) | Guided review, Block Editor smoke test, chat-approved GitHub comments |

### Example: Start a new path

In Cursor chat:

```
/create-learning-path

Feature: Setting up MongoDB monitoring with the Grafana Cloud integration
Audience: Grafana beginners who have MongoDB running and want metrics in Grafana Cloud
```

For convert, run `/build-interactive-lj` and give the website learning-path slug (for example `mysql-data-source`).

## Session shape (create or convert)

You drive decisions and testing; the agent writes files and finds selectors. Typical flow:

1. You run the command and approve the milestone plan (create) or confirm the slug (convert).
2. The agent writes `content.json`, `manifest.json`, and `website.yaml` under `[slug]-lj/`.
3. You log into your stack in the Playwright browser when asked so the agent can discover selectors.
4. You smoke-test each milestone in the Block Editor (**Show me** / **Do it**) and report failures.
5. You run `/preflight-learning-path`, then open a PR in `interactive-tutorials`.

For the full create and convert session playbook, including phase-by-phase roles, see [workflows.md](../.cursor/learning-path-workflows/workflows.md).

## Where files live

```text
interactive-tutorials/          # always required; PR target
  [slug]-lj/                    # package root (-lj = learning journey)
    content.json                # path overview (intro for the whole journey)
    manifest.json               # type: path, milestones list, targeting
    website.yaml                # Learning Hub metadata for the path
    [milestone]/
      content.json              # that milestone’s interactive + markdown steps
      manifest.json             # type: guide, depends/recommends
      website.yaml              # Learning Hub metadata for the step

website/                        # read-only; needed for create/convert, not for preflight/review
  content/docs/learning-paths/[slug]/
    _index.md / …/index.md      # source for /build-interactive-lj; docs lookup for create
```

## Required artifacts

- `content.json` holds what the learner sees and does. The path-level file is the journey overview. Each milestone folder has its own file for that stop’s steps ([json-guide-reference.md](json-guide-reference.md)).
- `manifest.json` controls packaging and recommendations. The path-level file lists milestones. Milestone-level files set depends/recommends ([manifest-reference.md](manifest-reference.md)).
- `website.yaml` holds Learning Hub / website metadata for the path and each milestone ([website-yaml-reference.md](website-yaml-reference.md)).

When converting, the agent maps existing website front matter (including legacy `pathfinder_data` if present) into `website.yaml`. Do not edit the website repo for these workflows. See [frontmatter-schema](../.cursor/commands/create-learning-path/reference/frontmatter-schema.md) if you need the field mapping.

## How to test and review

Interactive milestones store CSS selectors inside each step in `content.json`. Pathfinder uses those selectors to find the right control in the Grafana UI when a learner clicks **Show me** (highlight) or **Do it** (act on their behalf).

Think of a selector as a street address for a button, menu item, or field. A precise, stable address still works when nearby UI changes. A fragile one (for example, position-based or data-dependent) breaks on another stack, after a permission difference, or when the feature is already configured.

You do not write selectors by hand in the happy path. During create and convert, the agent discovers them with Playwright against your live stack. Your job is to log in when asked, then prove the steps work in the Block Editor and report failures so the agent can fix them. Prefer stable selectors such as `data-testid` when the UI provides them. For patterns and anti-patterns, see [selectors-and-testids.md](selectors-and-testids.md).

### When selectors apply

Selectors only apply to interactive UI steps (`interactive`, `multistep`, `guided`, and similar blocks). Conceptual milestones that explain ideas without targeting the Grafana UI are markdown-only and skip Playwright selector discovery.

Rule of thumb:

- Teaching a click, fill, or navigate in the Grafana UI needs selectors. The agent discovers them. You smoke-test **Show me** / **Do it**.
- Explaining concepts with no UI target stays markdown only. No selectors.

The create and convert commands already treat `business-value` as markdown-only (no interactive blocks). Intro and conclusion milestones are often mostly markdown too.

### Playwright MCP

Playwright MCP is how Cursor lets the agent drive a real browser against your Grafana stack.

- During create and convert, the agent uses it for selector discovery.
- During preflight and review, it runs DOM checks to verify those selectors still resolve on a live stack.

Your role:

1. Enable Playwright MCP in Cursor before you start create or convert (Settings → MCP).
2. When prompted, log into the stack in the Playwright browser window (Okta on learn, or normal login on a personal/staff stack). The agent cannot complete SAML/Okta alone.
3. Tell the agent when you are ready so it can continue.

If MCP is missing or broken (browser tools fail, or login never works), stop and fix it before continuing selector work. Once a `[slug]-lj/` package exists, run `/preflight-learning-path` and let it diagnose and restore MCP in chat.

### Block Editor smoke test

After the agent has written milestone `content.json` files (or after you open a PR), click through each milestone yourself:

1. On your stack, enable Pathfinder **dev mode**, then open **Debug** → **Block Editor**.
2. Prefer the **PR review tool** (pathfinder-app 1.4.5+) when you have a PR: it loads each milestone’s `content.json` from the package so you do not paste or import JSON by hand. Use paste or import individual `content.json` files only if that tool is unavailable.
3. For each milestone: start on the correct Grafana page, click every **Show me** and **Do it**, and report exact failures (wrong highlight, no click, missing element).
4. When you can, test on more than one stack. Permissions and “already configured” UI states differ.

Screenshots for opening **dev mode** and the Block Editor are in the [repo README](../README.md).

### Before you open a PR / when reviewing

- Authors: run [`/preflight-learning-path`](../.cursor/commands/preflight-learning-path.md) before opening a PR (static checks + live DOM; optional Block Editor walk).
- Reviewers: run [`/review-learning-path-pr`](../.cursor/commands/review-learning-path-pr.md) after the PR exists.
- Add the `lh-learning-path` label to learning path PRs, and set **Status** on the [Learning Hub board](https://github.com/orgs/grafana/projects/1108/views/2), so the PR appears on the board with the right workflow state.

Preflight reports under `.cursor/lp-preflight-state/` are local and gitignored. Do not force-add them to your PR.

## Go deeper

| Topic | Link |
| --- | --- |
| Full session phases (create / convert) | [`.cursor/learning-path-workflows/workflows.md`](../.cursor/learning-path-workflows/workflows.md) |
| Create from scratch | [`.cursor/commands/create-learning-path.md`](../.cursor/commands/create-learning-path.md) |
| Convert existing markdown | [`.cursor/commands/build-interactive-lj.md`](../.cursor/commands/build-interactive-lj.md) |
| Preflight (author self-review) | [`.cursor/commands/preflight-learning-path.md`](../.cursor/commands/preflight-learning-path.md) |
| Review an LP PR | [`.cursor/commands/review-learning-path-pr.md`](../.cursor/commands/review-learning-path-pr.md) |
| Guide JSON blocks | [json-guide-reference.md](json-guide-reference.md) |
| Manifests | [manifest-reference.md](manifest-reference.md) |
| `website.yaml` fields | [website-yaml-reference.md](website-yaml-reference.md) |
| Selectors | [selectors-and-testids.md](selectors-and-testids.md) |
| Block Editor / dev mode UI screenshots | [README.md](../README.md) |

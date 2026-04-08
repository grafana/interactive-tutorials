# Step 8: Report and Next Steps

Summarize the session and provide guidance for creating PRs.

---

## CODEOWNERS (REQUIRED)

Add the new learning path directory to `.github/CODEOWNERS` with the user as code owner. Insert the entry alphabetically in the "Guide directories" section:

```
/[slug]-lj/ @[github-username]
```

Ask the user for their GitHub username if not already known from the existing CODEOWNERS entries.

---

## Summary

Display a completion summary showing: milestone counts (interactive/markdown-only/hugo-only), all created files across all three repos, and recommender mapping status.

---

## PR Guidance

This workflow creates changes across up to three repositories. Guide the user to create PRs in this order:

1. **interactive-tutorials** — content.json files (`[slug]-lj/`)
2. **website** — milestone markdown + path overview (`content/docs/learning-paths/[slug]/`)
3. **grafana-recommender** — mapping (`internal/configs/state_recommendations/`)

---

## PR Description

When the user asks for a PR description, provide it in a markdown code block. Include: a summary of what the learning path teaches, a table of milestones with block counts and interactivity status, and a note about the JSON-first authoring approach.

# Step 8: Report and Next Steps

Summarize the session and provide guidance for creating PRs.

---

## Summary

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 LEARNING PATH COMPLETE: [slug]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESULTS
├── Total milestones: [N]
├── Fully interactive: [N] ✅
├── Markdown-only: [N] 📝
└── Hugo-only (manual): [N] ✏️

JSON FILES (interactive-tutorials repo)
├── [slug]-lj/welcome/content.json ✅ welcome page
├── [slug]-lj/milestone-1/content.json ✅
├── [slug]-lj/milestone-2/content.json ✅
└── ...

WEBSITE MARKDOWN (website repo)
├── [slug]/_index.md → welcome/content.json ✅
├── [slug]/milestone-1/index.md ✅
├── [slug]/milestone-2/index.md ✅
└── ...

RECOMMENDER (grafana-recommender repo)
└── [area]-cloud.json ✅ mapping added

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PR Guidance

This workflow creates changes across up to three repositories. PRs should be created in this order:

### 1. interactive-tutorials PR (content.json files)

```
git add [slug]-lj/
git commit -m "Add interactive content for [slug] learning path"
git push && gh pr create
```

### 2. website PR (milestone markdown + path overview)

```
git add content/docs/learning-paths/[slug]/
git commit -m "Add [slug] learning path pages"
git push && gh pr create
```

### 3. grafana-recommender PR (mapping)

```
git add internal/configs/state_recommendations/
git commit -m "Add recommender mapping for [slug] learning path"
git push && gh pr create
```

---

## Slack-Ready Summary

Offer to provide a copy-paste summary for Slack:

```
Would you like a Slack-ready summary? (Y/N)
```

If yes, display:
```
🎯 New interactive learning path: [slug]
✅ [N]/[N] milestones interactive
📄 Website markdown written alongside JSON
🔗 Ready for PRs across interactive-tutorials, website, grafana-recommender
```

---

## PR Description

When the user asks for a PR description, provide it in a markdown code block:

````
```markdown
Add interactive content for `[slug]` learning path.

### Summary

[Description of what this learning path teaches]

### Changes

| Milestone | Blocks | Interactive? |
|-----------|--------|-------------|
| [name] | [N] | ✅ / 📝 |
...

### Architecture

- **JSON-first authoring** — content.json files contain the interactive content
- Website markdown (front matter + `{{< pathfinder/json >}}`) written alongside JSON
- Recommender mapping added for Pathfinder contextual suggestions
```
````

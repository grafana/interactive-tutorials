# Step 7: Report and Next Steps

Summarize the session and provide guidance for creating a PR.

---

## Summary

Use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 BUILD COMPLETE: [slug] Interactive Learning Path
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESULTS
├── Total milestones: [N]
├── Fully interactive: [N] ✅
└── Partial (some markdown): [N] 🟡

FILES CREATED
├── [slug]-lj/milestone-1/content.json ✅
├── [slug]-lj/milestone-2/content.json ✅
└── ...

NEXT STEPS
1. Review the content.json files in your editor
2. Stage files: git add [slug]-lj/
3. Commit with message: "Add interactive content for [slug] learning path"
4. Push and create PR

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Slack-Ready Summary

Offer to provide a copy-paste summary for Slack:

```
Would you like a Slack-ready summary? (Y/N)
```

If yes, display:
```
🎯 Interactive learning path complete: [slug]
✅ [N]/[N] milestones interactive
🔗 Ready for PR
```

---

## PR Description

When the user asks for a PR description, ALWAYS provide it in a markdown code block so they can copy it easily:

````
```markdown
## Add interactive content for `[slug]` learning path

### Summary

[Description of what this PR adds]

### Changes

| Milestone | File | Blocks | Description |
|-----------|------|--------|-------------|
| [name] | `[file]` | [N] | [description] |
...

### Interactive features

- [Key features, selectors used, etc.]

### Testing

- ✅ JSON validation passed
- ✅ All highlights working correctly
- ✅ Show me buttons functional

### Related

- Learning path: `/docs/learning-paths/[slug]/`
```
````

**IMPORTANT:** The user should NEVER have to ask "please provide in markdown" — always use the code block format by default.


# Step 2: Learning Path Validation

Locate the learning path and verify it has all the required components.

---

## Tutorial Mode Introduction

```
**Step 2: Learning Path Validation**

I'll locate the "[slug]" learning path and:
- Find all milestones (the steps users complete)
- Check if it's mapped in the recommender (so it appears in Pathfinder)

Ready to proceed? (Y/N)
```

Wait for confirmation, then validate.

---

## Expert Mode

Validate immediately without introduction.

---

## Validate

1. Find source: `website/content/docs/learning-paths/[slug]/`
2. List all milestones found
3. Search `grafana-recommender` for mapping rules
4. **Read all related feature documentation (MANDATORY)** — From the milestone source markdown, identify every Grafana product/feature referenced. Read the canonical docs pages in full (main page, getting started, navigation, configuration, concepts sub-pages) — prefer reading from the local `website` repo first (e.g., `content/docs/grafana-cloud/.../_index.md`); fall back to WebFetch for docs not in the workspace. These docs are the authoritative source for all factual claims in the path. Do NOT rely on training data or memory for feature names, UI navigation, capabilities, platform availability, or prerequisites.

**Display:**
```
Found learning path: [title]

Milestones:
1. [milestone-1-title] (milestone-1-slug)
2. [milestone-2-title] (milestone-2-slug)
...

Recommender mapping: ✅ Found / ❌ Not found
```

**On success:**
```
✅ Learning path validated. Ready to scaffold [N] milestones.
```

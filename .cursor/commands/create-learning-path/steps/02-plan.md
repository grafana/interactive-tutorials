# Step 2: Plan Learning Path

Design the learning path structure before writing any JSON.

---

## Tutorial Mode Introduction

```
**Step 2: Plan Learning Path**

I'll help you design the learning path:
- Propose 2-4 path options based on your feature
- Outline milestones for the chosen option
- Get your approval before writing any files

What feature or product goal should this learning path cover?
```

Wait for the user to provide the feature.

---

## Expert Mode

Ask for the feature, then proceed directly to proposals.

---

## Planning Process

### 1. Gather Context

Before proposing paths:
- Review existing paths in `website/content/docs/learning-paths/` for patterns and gaps
- Understand the feature's complexity and user journey
- Identify which milestone categories apply (see below)
- **Read all related feature documentation (MANDATORY)** — Identify the canonical Grafana docs pages for the feature/product. Read every doc page in full — prefer reading from the local `website` repo first (e.g., `content/docs/grafana-cloud/.../_index.md`); fall back to WebFetch for docs not in the workspace. Read the main docs page, sub-pages for getting started, navigation, configuration, and concepts. These docs are the authoritative source for all factual claims in the path. Do NOT rely on training data or memory for feature names, UI navigation, capabilities, platform availability, or prerequisites. Track the list of all docs pages consulted — these will be added to the `_index.md` front matter as `source_docs` in Step 3.

### 2. Propose 2-4 Learning Path Options

For each option, provide:

```
## Option N: [Path Name]
**Description:** [1-2 sentences]
**Group:** [data-availability | query-and-visualize | take-action | onboarding]
**Skill Level:** [Beginner | Intermediate | Advanced]
**Milestones:**
1. [Title] (weight: XXX) - [brief description]
2. [Title] (weight: XXX) - [brief description]
...
```

### 3. Milestone Categories and Ordering

Follow these patterns when designing milestones:

**Infrastructure monitoring paths:**
1. Business value (100) → Advantages (200) → Installation (300-400) → Configuration (500-600) → Verification (700) → Usage (800) → Conclusion (900)

**Data exploration paths:**
1. Business value (100) → Navigation (200) → Search/filter (300) → Analysis (400-500) → Open in Explore (600) → Add to dashboard (700) → Conclusion (800)

**Data source connection paths:**
1. Business value (100) → Advantages (200) → Install plugin (300) → Add data source (400) → Configure auth (500) → Test (600-700) → Build dashboard (800) → Conclusion (900)

### 4. Detailed Outline (When Requested)

For the chosen path, provide per-milestone detail:

```
### Milestone N: [Title] (weight XXX)
- **Milestone type:** [business-value | navigation | creation | installation | configuration | verification | exploration | conclusion]
- **Interactive?:** [Yes — has UI interactions | No — conceptual/external only]
- **H1 heading:** "[Exact heading text]"
- **Introduction:** [What the intro paragraphs cover]
- **Steps:** [List of specific actions]
- **CTA type:** [continue | success | conclusion]
- **Troubleshooting links:** [If CTA is success, list links]
- **Side journeys:** [Optional exploration links]
```

### 5. Identify Hugo-Only Milestones

Flag milestones that need hand-written Hugo markdown (no `website` key in JSON):
- Dashboard/alert reference pages with `{{< collapse >}}` shortcodes
- Pages using `{{< shared >}}` snippets
- Content requiring Hugo-specific rendering

These milestones get `content.json` with blocks but no `website` key. Their Hugo markdown is maintained separately.

---

## Milestone Scope Rules

**Good scope (single milestone):**
- Navigate to a specific page
- Create one token or configuration
- Copy a code snippet
- Fill out a single form
- View one interface section

**Too broad (split into multiple):**
- "Configure the entire application"
- "Set up monitoring and alerts"
- "Analyze user behavior patterns"

**Target:** 2-5 minute completion time per milestone. Maximum 10 milestones per path (typical: 6-8).

---

## Get Approval

After presenting the detailed outline:

```
Would you like me to proceed with writing the JSON files for this path,
or do you want to adjust the outline first?
```

Wait for explicit approval before proceeding to Step 3.

---

## Output

The approved plan is used directly by Step 3 to write JSON and website markdown files. No intermediate artifacts are created — the plan lives in the conversation context.

---

## Completion

Display a brief summary showing: path name, group, skill level, and milestone count. Ask the user if they're ready for Step 3 (Write Enriched JSON).

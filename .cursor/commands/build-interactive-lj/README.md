# Build Interactive Learning Path

This command automates the creation of interactive content (`content.json` files) for learning paths in Grafana Pathfinder.

---

## Overview

When a writer runs `/build-interactive-lj`, this command guides them through a 7-step process to create fully functional interactive guides:

1. **Environment Validation** - Verify repos, browser automation, and GitHub CLI
2. **Learning Path Validation** - Find the learning path and list milestones
3. **Create Recommender Mapping** - Ensure the learning path appears in Pathfinder (if needed)
4. **Scaffold Content Files** - Create content.json structure for each milestone
5. **Selector Discovery** - Find CSS selectors for interactive elements
6. **Test in Pathfinder** - Collaboratively test each milestone
7. **Report and Next Steps** - Summarize results and provide PR guidance

**Expected time:** 30-60 minutes depending on the number of milestones.

---

## Critical Rules

### 🚨 CRITICAL TESTING RULE

> During Step 6 (Test in Pathfinder), the AI must NOT interact with Pathfinder at all. The AI tells the user which content.json file to import, then WAITS. The USER handles ALL Pathfinder interactions: importing JSON, clicking "Show me", "Do it", and testing.

**Why:** Users can import and test faster and catch visual/UX issues that automation misses. AI interaction with Pathfinder is error-prone and wastes time.

### Core Principles

1. **Be autonomous, not interrogative** - Analyze content and make intelligent decisions. Don't ask questions that can be inferred from context.
2. **Follow steps in order** - Each step has verification built in.
3. **Test ONE milestone at a time** - Tell the user which file to import, wait for their feedback.
4. **ASK before fixing issues** - Explain the problem and proposed fix, wait for approval.
5. **Let the user handle git** - Summarize changes, let them decide when to commit.
6. **Use browser tools for selectors** - ALWAYS inspect the actual DOM with Playwright.

---

## Anti-Patterns (Do NOT)

- ❌ **Do NOT interact with Pathfinder** - No importing JSON, no clicking buttons. User handles all Pathfinder interactions
- ❌ **Do NOT ask questions that can be inferred** - Be autonomous (recommender file, URL patterns, platform)
- ❌ **Do NOT skip any milestones** - EVERY milestone needs a content.json
- ❌ **Do NOT use placeholder selectors** - Never leave `"[selector]"` or `"TODO"`
- ❌ **Do NOT guess at selectors** - Always use Playwright to inspect
- ❌ **Do NOT use `description` field** - Use `content`
- ❌ **Do NOT use `formvalue` field** - Use `targetvalue`
- ❌ **Do NOT use position-based selectors** - `:first-of-type`, `:nth-child()` break with data changes
- ❌ **Do NOT use data-dependent selectors** - Use `^=` starts-with patterns
- ❌ **Do NOT use non-standard CSS** - `:contains()`, `:has-text()` don't work in Pathfinder

---

## File Structure

```
.cursor/commands/build-interactive-lj/
├── README.md                    # This file - main orchestrator
├── reference/
│   ├── selector-patterns.md     # Selector discovery rules & stability patterns
│   ├── json-schema.md           # JSON structure requirements & field reference
│   └── proven-patterns.md       # Appendix of working patterns for common UI
└── steps/
    ├── 01-environment.md        # Environment validation
    ├── 02-validation.md         # Learning path validation
    ├── 03-recommender.md        # Create recommender mapping
    ├── 04-scaffold.md           # Scaffold content files
    ├── 05-selectors.md          # Selector discovery
    ├── 06-testing.md            # Test in Pathfinder
    └── 07-report.md             # Report and next steps
```

---

## Workflow

### Welcome Message

When a writer runs `/build-interactive-lj`, display:

```
👋 Welcome to the Interactive Learning Path Builder!

I'm here to help you create interactive content that powers the "Show me" and 
"Do it" buttons in Grafana Pathfinder. By the end of our session, you'll have 
fully functional content.json files ready for a PR.

Here's what our session will look like:

1. **Environment check** - Verify your setup is ready (30 seconds)
2. **Find your learning journey** - Locate source content and list milestones
3. **Create recommender mapping** - Ensure the journey appears in Pathfinder (if needed)
4. **Scaffold the files** - Create content.json structure for each milestone
5. **Discover selectors** - Find CSS selectors for interactive elements
6. **Test in Pathfinder** - Collaboratively test each milestone
7. **Wrap up** - Summarize results and provide PR guidance

Expect this to take 30-60 minutes depending on how many milestones your 
learning journey has. I'll need your attention during testing so you can 
verify the highlights look right.
```

### Ask: First Time?

```
Is this your first time using /build-interactive-lj? (Y/N)
```

**If YES (Tutorial Mode):**
```
Great! I'll walk you through the process step by step.

Before each step, I'll explain what I'm about to do and ask for your 
confirmation before proceeding. This way you'll understand exactly what's 
happening and can ask questions along the way.

Ready to get started? (Y/N)
```

**If NO (Expert Mode):**
```
Welcome back! I'll move quickly through the steps.

Ready to get started? (Y/N)
```

### Ask: Which Learning Path?

```
Which learning path would you like to make interactive?

Provide the slug (the folder name) from:
website/content/docs/learning-paths/

Examples: prometheus, github-data-source, mysql-data-source
```

Wait for the user to provide the learning path slug, then proceed to Step 1.

---

## Executing Steps

For each step, read the corresponding file from `steps/` directory:

- **Step 1:** Read `steps/01-environment.md`
- **Step 2:** Read `steps/02-validation.md`
- **Step 3:** Read `steps/03-recommender.md` (only if mapping not found)
- **Step 4:** Read `steps/04-scaffold.md` and `reference/json-schema.md`
- **Step 5:** Read `steps/05-selectors.md` and `reference/selector-patterns.md`
- **Step 6:** Read `steps/06-testing.md`
- **Step 7:** Read `steps/07-report.md`

**Reference files** can be consulted at any time:
- `reference/selector-patterns.md` - Selector rules and stability checks
- `reference/json-schema.md` - JSON structure and field requirements
- `reference/proven-patterns.md` - Reusable patterns for common UI elements

---

## Quick Reference

### Key Repositories
- Source: `website/content/docs/learning-paths/[slug]/`
- Output: `interactive-tutorials/[slug]-lj/`
- Mapping: `grafana-recommender/internal/configs/state_recommendations/`

### Block Types
- `markdown` - Explanatory text, no automation
- `interactive` - Automated actions with "Show me" / "Do it"
- `multistep` - Sequential navigation (shows "▶ Run N steps")
- `guided` - User performs manually, no "Do it" button

### Selector Priority
1. `data-testid` (most stable)
2. `aria-label`
3. `href` (for links)
4. `id`
5. Stable class (least stable)

**Avoid:** Generic classes, positional selectors, text content

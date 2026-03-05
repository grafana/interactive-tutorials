# Step 1: Environment Validation

Verify that the user's setup is ready for creating interactive content.

---

## Tutorial Mode Introduction

```
**Step 1: Environment Validation**

I'll check that your setup is ready:
- Three repositories in your workspace (website, interactive-tutorials, grafana-recommender)
- Playwright browser automation working

If anything fails, I'll help you resolve the issue.

Ready to proceed? (Y/N)
```

Wait for confirmation, then run checks.

---

## Expert Mode

Run checks immediately without introduction.

---

## Run Checks

Check these and display results:

- ✅/❌ `website` repo in workspace
- ✅/❌ `interactive-tutorials` repo in workspace
- ✅/❌ `grafana-recommender` repo in workspace
- ✅/❌ Playwright MCP available

**On any failure:** Help the user resolve the issue before continuing.

**On all pass:**
```
✅ Environment ready. Proceeding to Step 2...
```

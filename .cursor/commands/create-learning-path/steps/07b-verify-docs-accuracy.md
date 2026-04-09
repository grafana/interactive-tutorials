# Step 7b: Verify documentation accuracy

Verify that all factual claims in the learning path content match current Grafana documentation.

---

## Tutorial Mode Introduction

```
**Step 7b: Verify documentation accuracy**

I'll cross-check the content you just created against the live Grafana
documentation to make sure all factual claims are accurate:
- Feature names and navigation paths
- Platform availability
- Capability descriptions
- Prerequisites

Ready to verify? (Y/N)
```

Wait for confirmation, then verify.

---

## Expert Mode

Verify immediately without introduction.

---

## Verification Steps

### 1. Identify referenced products and features

Scan all `content.json` files for Grafana product names, feature names, and UI navigation references. Build a list of unique products/features mentioned in the path.

### 2. Collect source documentation URLs

For each product/feature identified, determine the canonical docs page. Check:

- The `end-journey/content.json` (often contains doc links)
- The `welcome/content.json` (may reference products)
- Any `content.json` block that links to `grafana.com/docs/`

Read the docs from the local `website` repo first (e.g., `content/docs/grafana-cloud/.../_index.md`); fall back to WebFetch for docs not in the workspace.

### 3. Cross-check factual claims

Compare the learning path content against the fetched docs for:

| Check | What to verify |
|-------|---------------|
| **Navigation paths** | Where the feature lives in the Grafana UI (menu location, access method) |
| **Feature names** | Current official names (products get renamed between releases) |
| **Capability descriptions** | What the feature actually does, its core workflow |
| **Platform availability** | Cloud-only vs Cloud + self-managed, required Grafana version |
| **Prerequisites** | Required data sources, configurations, or accounts |
| **Sibling features** | Related tools or features the docs mention that the path omits or misrepresents |

### 4. Produce a discrepancy report

For each inconsistency:

| Field | Description |
|-------|-------------|
| **File** | Which `content.json` contains the claim |
| **Claim** | What the content says |
| **Docs say** | What the official documentation says |
| **Severity** | High (factually wrong), Medium (incomplete/misleading), Low (minor omission) |

### 5. Fix high and medium issues

- **High severity** — Must be fixed before proceeding (wrong names, wrong navigation, wrong platform)
- **Medium severity** — Should be fixed (missing capabilities, incomplete descriptions)
- **Low severity** — Note for the author to decide on (acceptable simplifications for teaching)

---

## What this catches

- Outdated UI navigation paths (features move between releases)
- Renamed products or features
- Missing capabilities added after the content was written
- Incorrect platform availability claims
- Stale prerequisite requirements

---

## Completion

Display a summary showing: number of products/features verified, number of discrepancies by severity, and fixes applied. Ask the user if they're ready for Step 8 (Report).

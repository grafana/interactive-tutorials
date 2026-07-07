# GitHub review mechanics (learning path PR)

GraphQL details for [review-learning-path/SKILL.md](SKILL.md) Phases 4, 7, and 9. Reviewer-facing copy uses **draft review**; GitHub's API calls it a pending review until submit.

## Create draft review

GraphQL `addPullRequestReview`:

```graphql
mutation($input: AddPullRequestReviewInput!) {
  addPullRequestReview(input: $input) {
    pullRequestReview { id databaseId state }
  }
}
```

Variables: `pullRequestId` (PR GraphQL node ID from state `pull_request_node_id`, fetched in Phase 0 via `gh pr view --json id`), `body: "Review in progress."` — omit `event`.

## Add inline comment to draft review

Use GraphQL `addPullRequestReviewComment` with diff **`position`** (not REST line attach — unreliable on draft reviews).

Compute `position` from the PR file patch: count lines in the patch hunk until the target new-file line number matches.

```graphql
mutation($input: AddPullRequestReviewCommentInput!) {
  addPullRequestReviewComment(input: $input) {
    comment { databaseId path line }
  }
}
```

Variables: `pullRequestReviewId`, `path`, `position`, `body`.

## Submit (workflow end)

GraphQL `submitPullRequestReview`:

```graphql
mutation($input: SubmitPullRequestReviewInput!) {
  submitPullRequestReview(input: $input) {
    pullRequestReview { state url submittedAt }
  }
}
```

Variables: `pullRequestReviewId`, `event: REQUEST_CHANGES` (or `COMMENT` / `APPROVE`), `body` (full review summary).

## Post-submit inline (new cycle)

REST works for standalone comments after submit:

```bash
gh api -X POST repos/grafana/interactive-tutorials/pulls/{n}/comments \
  -f body='...' -f commit_id='{sha}' -f path='...' -f line=15 -f side=RIGHT
```

## Draft review body UI gap

API-set draft review `body` is stored but **not shown** in GitHub's "Finish your review" textarea. Submitting from the UI without pasting **overwrites** the body with blank. Always submit via GraphQL or paste from `.cursor/pr-review-state/pr-{n}-review-body.md`.

## State file schema

Path: `.cursor/pr-review-state/pr-{n}.json` (replace `{n}` with PR number).

Written at Phase 0; updated through Phase 9. **Never commit to the author's branch.**

```json
{
  "pr_number": 403,
  "pr_url": "https://github.com/grafana/interactive-tutorials/pull/403",
  "pull_request_node_id": "PR_kwDOPf9q6c8AAAAA1234567",
  "repo": "grafana/interactive-tutorials",
  "path_dir": "monitor-azure-resources-lj",
  "website_slug": "monitor-azure-resources",
  "pr_type": "conversion",
  "head_branch": "monitor-azure-interactive",
  "head_commit": "0c11708cf74e306935d2583b97b7e6a4665ab3a5",
  "learn_host": "learn.grafana.net",
  "stack_state": "learn.grafana.net shared — no Azure credentials configured",
  "waive_live_testing": false,
  "pre_review_assets": {
    "navigate-azure-config": ["assets/migration-notes.md"]
  },
  "phase": 7,
  "status": "in_progress",
  "pending_review_node_id": "PRR_kwDOPf9q6c8AAAABERITuA",
  "pending_review_id": 12345678,
  "comment_count": 3,
  "recommended_verdict": "REQUEST_CHANGES",
  "pathfinder": {
    "navigate-azure-config": "pass",
    "connect-azure-account": "pass",
    "configure-metrics": "pass",
    "install-dashboards-and-alerts": "N/A — dashboards already installed",
    "verify-data-collection": "fail step 2 — Tab Services not in DOM",
    "explore-data": "fail step 1 — Tab Services not in DOM"
  },
  "playwright": {
    "verify-data-collection": { "Tab Services": "missing" },
    "explore-data": { "Tab Services": "missing" }
  },
  "verdict": null,
  "submitted_at": null,
  "review_url": null
}
```

### Field reference

| Field | When set | Notes |
|---|---|---|
| `pull_request_node_id` | Phase 0 | PR GraphQL node ID from `gh pr view --json id`; used as `pullRequestId` in Phase 4 |
| `website_slug` | Phase 0 | `{path_dir}` minus `-lj`; optional read-only legacy source lookup when `website` repo is in workspace |
| `pr_type` | Phase 0 | `new`, `conversion`, or `update` — drives Phase 2 emphasis |
| `stack_state` | Phase 3 | Free-text description of host + stack used for Phases 5–6 |
| `waive_live_testing` | Phase 3 | `true` when reviewer replies **static-only** — skip Phases 5–6 |
| `learn_host` | Phase 0 | Default `learn.grafana.net` |
| `pre_review_assets` | Phase 1 (before audit) | Map of milestone slug → list of `assets/` file paths that existed before audit-guide ran |
| `phase` | Each phase completion | Integer 0–10 |
| `status` | Phase 0 → `"in_progress"`; Phase 9 → `"submitted"` | |
| `pending_review_node_id` | Phase 4 | GraphQL node ID for the draft review — inline comments + submit |
| `pending_review_id` | Phase 4 | REST/database ID if needed |
| `pathfinder` | Phase 6 | Keys = milestone slug; values = `pass`, `fail step N — …`, or `N/A — …` |
| `playwright` | Phase 5 | Per-milestone selector results: `exists`, `missing`, `below-fold` |
| `comment_count` | Phase 7 | Inline comments added to pending review |
| `recommended_verdict` | Phase 7 | Agent default: `REQUEST_CHANGES`, `COMMENT`, or `APPROVE` |
| `verdict` | Phase 8–9 | Reviewer-confirmed verdict (may override `recommended_verdict`) |
| `review_url` | Phase 9 | URL returned by `submitPullRequestReview` |

Omit fields until the phase that populates them. On resume (see SKILL.md § Resume), read `phase` and `status` to pick up where the review left off.

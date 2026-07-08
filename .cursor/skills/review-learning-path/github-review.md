# GitHub review mechanics (learning path PR)

GraphQL details for [review-learning-path/SKILL.md](SKILL.md) Phase 3 (post approved comments) and Phase 4 (submit). Reviewer approves comment text in chat before anything posts.

## Flow

1. Phase 3: draft inline comments + summary in **chat**
2. Reviewer approves (`post all`, `post 1,2`, `skip`, edits)
3. Create draft review (if needed) + post approved inline comments
4. Save summary to `pr-{n}-review-body.md`
5. Phase 4: `submitPullRequestReview` with reviewer's verdict

## Create draft review

GraphQL `addPullRequestReview`:

```graphql
mutation($input: AddPullRequestReviewInput!) {
  addPullRequestReview(input: $input) {
    pullRequestReview { id databaseId state }
  }
}
```

Variables: `pullRequestId` from state `pull_request_node_id`, `body: "Review in progress."` — omit `event`.

Create the draft review at start of Phase 3 posting (after chat approval), not before live testing.

## Add inline comment to draft review

Use GraphQL `addPullRequestReviewComment` with diff **`position`**.

```graphql
mutation($input: AddPullRequestReviewCommentInput!) {
  addPullRequestReviewComment(input: $input) {
    comment { databaseId path line }
  }
}
```

Variables: `pullRequestReviewId`, `path`, `position`, `body`.

Follow [comment-style.md](comment-style.md): no em dashes, human voice, max 3 sentences.

## Submit

GraphQL `submitPullRequestReview`:

```graphql
mutation($input: SubmitPullRequestReviewInput!) {
  submitPullRequestReview(input: $input) {
    pullRequestReview { state url submittedAt }
  }
}
```

Variables: `pullRequestReviewId`, `event`, `body` from `pr-{n}-review-body.md`.

## Post-submit inline (new cycle)

REST for standalone comments after submit:

```bash
gh api -X POST repos/grafana/interactive-tutorials/pulls/{n}/comments \
  -f body='...' -f commit_id='{sha}' -f path='...' -f line=15 -f side=RIGHT
```

## Draft review body UI gap

GitHub's UI does not show the draft review body. Always submit via GraphQL or paste from `pr-{n}-review-body.md`.

## State file schema

Path: `.cursor/pr-review-state/pr-{n}.json`

```json
{
  "pr_number": 403,
  "pull_request_node_id": "PR_kwDOPf9q6c8AAAAA1234567",
  "path_dir": "monitor-azure-resources-lj",
  "website_slug": "monitor-azure-resources",
  "pr_type": "conversion",
  "head_branch": "monitor-azure-interactive",
  "head_commit": "0c11708cf74e306935d2583b97b7e6a4665ab3a5",
  "learn_host": "learn.grafana.net",
  "stack_state": "learn.grafana.net shared",
  "waive_live_testing": false,
  "static_only_reason": null,
  "pre_review_assets": {},
  "phase": 3,
  "status": "in_progress",
  "pending_review_node_id": "PRR_kwDOPf9q6c8AAAABERITuA",
  "comment_count": 2,
  "pathfinder": {
    "navigate-azure-config": "pass",
    "verify-data-collection": "fail step 2 — Tab Services not in DOM"
  },
  "playwright": {
    "verify-data-collection": { "Tab Services": "missing" }
  },
  "verdict": null,
  "review_url": null
}
```

### Field reference

| Field | When set | Notes |
|---|---|---|
| `pull_request_node_id` | Phase 0 | For GraphQL mutations |
| `pr_type` | Phase 0 | `new`, `conversion`, `update` |
| `stack_state` | Phase 1 end | Stack used in Phase 2 |
| `waive_live_testing` | Phase 1 end | Skips Phase 2 |
| `static_only_reason` | Phase 1 end | Required when waived |
| `pre_review_assets` | Phase 1 | Map milestone slug → asset paths before audit |
| `phase` | Each phase | Integer **0–4** |
| `pending_review_node_id` | Phase 3 | After chat approval, when posting |
| `pathfinder` | Phase 2 | Block Editor smoke test results per milestone |
| `playwright` | Phase 2 | Required DOM check results per milestone |
| `comment_count` | Phase 3 | Approved inline comments posted |
| `verdict` | Phase 4 | Reviewer-chosen GitHub event |

Omit fields until populated. On resume, read `phase` and `status`.

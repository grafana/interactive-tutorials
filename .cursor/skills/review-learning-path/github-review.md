# GitHub review mechanics (learning path PR)

Used by [review-learning-path/SKILL.md](SKILL.md) Phase 4, 7, and 9.

## Create pending review

GraphQL `addPullRequestReview`:

```graphql
mutation($input: AddPullRequestReviewInput!) {
  addPullRequestReview(input: $input) {
    pullRequestReview { id databaseId state }
  }
}
```

Variables: `pullRequestId` (PR node ID), `body: "Review in progress."` — omit `event`.

## Add inline comment to pending review

Use GraphQL `addPullRequestReviewComment` with diff **`position`** (not REST line attach — unreliable on pending reviews).

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

## Pending review body UI gap

API-set pending review `body` is stored but **not shown** in GitHub's "Finish your review" textarea. Submitting from the UI without pasting **overwrites** the body with blank. Always submit via GraphQL or paste from `.cursor/pr-review-state/pr-{n}-review-body.md`.

## State file

`.cursor/pr-review-state/pr-{n}.json` tracks `pending_review_node_id`, `head_commit`, phase, pathfinder results, and post-submit `status: submitted`.

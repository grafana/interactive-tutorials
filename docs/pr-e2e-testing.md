# Optional E2E tests for pull requests

## Availability

This workflow starts disabled. An unset or false `PR_E2E_ENABLED` repository variable prevents submission.
The coordinator also requires separate admission approval. This test is optional, not a required merge check.

## Request a test

1. Open a same-repository PR in `grafana/interactive-tutorials`.
2. Find the package ID in its `manifest.json`.
3. Post a new PR conversation comment with this whole-body command:

   ```text
   /e2e-test first-dashboard
   ```

4. Read the **Optional PR E2E** run summary in GitHub Actions.
5. Read the App comment for execution results and failure-artifact links.

Replace `first-dashboard` with the manifest ID. Directory paths do not select packages.
IDs contain 1–64 lowercase letters, digits, underscores, or hyphens. The first character must be a letter or digit.

The commenter must be a human with current write, maintain, or admin permission on this repository.
The coordinator checks current permission and the current comment before acceptance.
Bots, ordinary issues, edited comments, quoted commands, and fenced commands do not request execution.
A bare or malformed command receives usage guidance in the Actions summary.

Fork PRs are unsupported, including forks from repository writers.
The helper captures the current PR head SHA. The coordinator rejects a changed head before acceptance.
The runner uses that exact commit, not published tutorial content.

## Results and recovery

Acceptance does not mean that a test passed. The submission workflow does not wait for browser execution.
The App comment identifies the tested SHA, package, outcome, and available evidence.
PR results do not change continuous guide health.

| Response or outcome | Meaning or action |
| --- | --- |
| `ACCEPTED` | The coordinator accepted the request. Read the App comment for results. |
| `DUPLICATE` | This comment already identifies a request. No second browser execution starts. |
| `BUSY` | All three execution slots are occupied. There is no queue. Post a fresh command after capacity becomes available. |
| `HEAD_CHANGED` | The PR head changed after capture. Post a fresh command for the new head. |
| `ADMISSION_DISABLED` | The service does not accept requests. Wait for operator approval. |
| `ACCESS_DENIED` or `WORKFLOW_DENIED` | The requester or workflow identity did not meet the authorization policy. |
| `PR_CLOSED` or `FORK_UNSUPPORTED` | The PR is not eligible. |
| `AUTHORIZATION_UNAVAILABLE` or `INSPECTION_REQUIRED` | An operator must inspect the request or provider state. |
| `passed` | The executed package passed. |
| `failed` | Guide steps failed. Read the report and failure artifacts. |
| `not_executed` | The package did not execute browser steps. This is not a pass. |
| `partial` | Some work executed, but the selected package did not complete. |
| `infrastructure_error` | Execution or report verification failed. This is not a guide-health result. |

If submission times out, inspect the App comment before posting another command.
The coordinator can accept a request before the client loses its response. The helper does not automatically retry.
Feedback updates can also be delayed. Operators can inspect durable state when no comment appears.

The CLI plans dependencies and journey milestones. Authors do not list dependencies in the command.
Local-tier packages and named-instance requirements do not execute on replacement Cloud targets.
The current named-instance rejection can appear as `REPORT_IDENTITY_MISMATCH`, rather than a clean non-execution result.

Failure-artifact links expire after seven days. The bucket remains private.
Anyone with a signed link can read its object until expiration or key revocation.
Treat these links as access credentials. Request refreshed links through an operator when necessary.

## Workflow trust boundary

The submission workflow loads its helper from trusted `main`.
It does not check out PR code, install PR dependencies, or run guide code on the Actions runner.
The coordinator prepares the verified source. A separate CI worker runs the trusted, pinned CLI on an ephemeral Cloud stack.

The submission job has only `contents: read`, `pull-requests: read`, and `id-token: write` permissions.
It uses the short-lived GitHub read token, Google submitter ID token, and a separate GitHub-signed workflow token.
The job receives no App key, artifact-signing key, Grafana token, or pool caller token.
Tokens never enter the prepared submission file or the Actions summary.
Provider response text does not enter logs. Known response codes and validated request metadata enter the summary.

The Google ID token uses audience `https://pathfinder-pr-test-coordinator`.
The GitHub workflow token uses the same audience, but a separate issuer and verification path.
The coordinator checks the exact `e2e-test.yml@refs/heads/main` workflow, repository ID, event, ref, and run ID.
Cloud Run invocation permission alone does not authorize a request.

The separate validation workflow runs helper tests with read-only permissions and no cloud credentials or OIDC permission.
Its mocked requests do not launch tests or consume Cloud leases.

## Operator configuration

| Repository variable | Meaning |
| --- | --- |
| `PR_E2E_ENABLED` | Set `true` to permit submission. Unset or `false` disables the job. |
| `PR_E2E_ALLOWED_ACTORS` | Optional JSON array of commenter logins for controlled acceptance, for example `["operator-login"]`. Unset permits all eligible writers. |

For controlled acceptance, set the actor restriction before temporarily enabling submission and coordinator admission.
The actor restriction does not replace the coordinator's current writer-permission check.
After approved acceptance, remove the actor restriction for general writer access.
Keep submission and coordinator admission disabled until the workflow is merged into `main` and the test window receives approval.

The reviewed deployment settings are public configuration in the workflow and helper.
They identify the dedicated submitter, managed WIF provider, coordinator URL, audience, and immutable repository ID.
No repository secret is required for these settings.

## Local validation

From the repository root, run:

```sh
node --test .github/scripts/e2e-test.test.mjs
actionlint .github/workflows/e2e-test.yml .github/workflows/validate-e2e-workflow.yml
```

The helper uses Node.js 22 and built-in modules. No dependency installation is necessary.
GitHub OIDC/WIF and live coordinator submission still require acceptance from the merged trusted workflow.

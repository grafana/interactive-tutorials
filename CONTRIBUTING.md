# Contributing to interactive-tutorials

This repository holds interactive Grafana guides (`content.json` and `manifest.json` per package). This page explains how outside contributors can help. Grafana employees can also follow the authoring flow in [README.md](README.md).

## Report a problem or request a guide

Use the [Guide problem or request](https://github.com/grafana/interactive-tutorials/issues/new?template=guide-problem-or-request.yml) issue form. You do not need to wait for permission to file an issue. A good problem report names the package or URL, the product version, the exact step, what you saw and what you expected, and how to reproduce it. Do not post secrets, tokens, or private data.

Report security issues through [Grafana's security issue reporting page](https://grafana.com/legal/report-a-security-issue/), not here.

## Implement a fix: only `agent/ready` issues

Maintainers triage every issue. Fix work is open to outside contributors only for issues that carry the `agent/ready` label.

- `agent/ready` is issued by a maintainer. You cannot earn it, and you should not add it yourself.
- If an issue is not labelled `agent/ready`, do not open a PR for it. Comment on the issue if you can add detail.
- Other lifecycle labels:

| Label | Meaning |
|-------|---------|
| `agent/needs-review` | A maintainer must review the prep. |
| `agent/needs-info` | The reporter must add detail. |
| `agent/needs-decision` | Blocked on a maintainer decision. |
| `agent/excluded` | Not open for outside implementation. This covers every non-content and privileged surface. |
| `agent/likely-fixed` | A merged PR appears to fix it. |
| `agent/rotten` | Evidence says it no longer applies. |

### What a ready issue contains

Before a maintainer adds `agent/ready`, the issue records:

- product, version, and environment
- exact package, file, and selector anchors
- user impact
- diagnosis, or a bounded hypothesis
- acceptance checks
- non-goals
- the expected `CODEOWNERS` review owner
- whether privileged E2E was run

The work must be content-only and small enough for one reviewer.

## Rules for a pull request

1. Implement only `agent/ready` issues.
2. One issue, one package-level concern. Do not bundle fixes.
3. Do not change any of the following. If the fix needs one, say so on the issue and stop.
   - `.github/`
   - deployment, or shared publish and build logic
   - `index.json` (frozen; CI fails any PR that changes it)
   - auth, permissions, or secrets
   - dependencies
   - migrations
   - e2e-platform infrastructure
4. Run the exact checks the issue specifies, and paste the results in the PR.
5. Link the issue in the PR description.
6. Sign your commits. PRs with unsigned commits cannot be merged.

CI runs strict guide validation (`validate-json.yml`), and a `CODEOWNERS` review is required before merge.

## Authoring references

Do not duplicate these in your PR. Read them before you edit a guide:

- [AGENTS.md](AGENTS.md#critical-rules): the critical rules. All are blocking.
- [.cursor/authoring-guide.mdc](.cursor/authoring-guide.mdc): how to author and edit guides.
- [docs/](docs/): block, action, requirement, and selector references.

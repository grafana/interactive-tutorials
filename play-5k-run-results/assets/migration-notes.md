---
status: complete
migrated: 2026-04-10
guide: play-5k-run-results
---

# Migration Notes: play-5k-run-results

## Manifest created

`play-5k-run-results/manifest.json` — standalone guide (Mode 1).

## Field derivation

| Field | Source | Value |
|-------|--------|-------|
| `id` | `content.json` | `play-5k-run-results` |
| `type` | Mode 1 default | `guide` |
| `schemaVersion` | Explicit default | `1.1.0` |
| `repository` | Explicit default | `interactive-tutorials` |
| `language` | Explicit default | `en` |
| `description` | `index.json` rule | verbatim from rule |
| `category` | Default (not in -lj) | `general` |
| `author.team` | Standalone guide default | `interactive-learning` |
| `author.name` | `git log` | `Simon Prickett` (sole commit author; no CODEOWNERS entry for this directory) |
| `startingLocation` | `urlPrefix` leaf in `index.json` match | `/d/sixn5pn/analyzing-5k-run-results` |
| `targeting.match` | `index.json` rule | copied verbatim |
| `testEnvironment` | `source` in match is concrete hostname `play.grafana.org` | `{ "tier": "cloud", "instance": "play.grafana.org" }` |
| `conflicts`, `replaces` | Explicit defaults | `[]` |
| `depends`, `recommends`, `suggests`, `provides` | No known relationships | `[]` |

## Validation result

```
✅ play-5k-run-results (play-5k-run-results)
```

No warnings or INFO messages after adding explicit defaults (`schemaVersion`, `repository`, `language`, `conflicts`, `replaces`).

## Notes

- No CODEOWNERS entry for this directory; `author.name` derived from git history only.
- `content.json` was not modified (single existing file, byte-identical after migration).

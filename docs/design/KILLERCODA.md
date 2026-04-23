# KillerCoda to Interactive Guide Migration

This document captures the key references and high-level strategy for translating existing [Grafana KillerCoda](https://github.com/grafana/killercoda) scenarios into Pathfinder interactive guides that leverage the new **Grafana Coda** terminal subsystem.

## Repository References

| Repository | What it provides |
|------------|-----------------|
| [grafana/killercoda](https://github.com/grafana/killercoda) | ~37 existing KillerCoda scenarios across Grafana, Loki, Alloy, Mimir, Tempo, Pyroscope, OTel, and workshops. Each scenario is a directory with `index.json` (config), `intro.md`, `step*.md`, `finish.md`, optional setup scripts, and bundled assets. |
| [grafana/grafana-pathfinder-app](https://github.com/grafana/grafana-pathfinder-app) | Pathfinder plugin source. Contains the **Grafana Coda** integration (`src/integrations/coda/`, `pkg/plugin/coda.go`, `pkg/plugin/terminal.go`) and two new block types: `terminal` and `terminal-connect`. See `AGENTS.md` and `docs/developer/CODA.md`. |
| [grafana/interactive-tutorials](.) (this repo) | Library of interactive guide `content.json` files, shared snippets, authoring docs, and AI skills for guide generation. Does **not** yet document Coda block types. |

## What We Want To Do

Build a repeatable translation pipeline (documented as reference materials and/or AI skills) that converts a KillerCoda scenario into a Pathfinder interactive guide enriched with Coda terminal blocks. The output should be a standard guide package (`content.json` + `manifest.json`) that works within the Pathfinder sidebar.

## Key Concepts Side-by-Side

### KillerCoda Scenario Format

- **`index.json`** -- title, description, ordered step references, backend image (`ubuntu`, `ubuntu-4GB`, `kubernetes-kubeadm-2nodes`), asset copy rules, setup/foreground/background scripts.
- **Step files** (`intro.md`, `step*.md`, `finish.md`) -- Markdown with KillerCoda extensions:
  - `` ```lang ...```{{exec}} `` -- executable code block (runs in terminal on click)
  - `` ```lang ...```{{copy}} `` -- copyable code block
  - `` `text`{{copy}} `` -- inline copyable text
  - `{{TRAFFIC_HOST1_PORT}}` -- dynamic URL placeholder for exposed VM ports
- **Setup scripts** -- `setup.sh` / `foreground.sh` run during intro to install Docker Compose, clone repos, start services.
- **Assets** -- files copied to the VM at specified paths.
- **Two authoring modes**: ~25 scenarios are auto-generated from doc repos via a Go transformer tool; ~12 are hand-authored.

### Pathfinder Interactive Guide Format

- **`content.json`** -- `id`, `title`, `schemaVersion: "1.0.0"`, ordered `blocks` array.
- **Block types**: `markdown`, `html`, `image`, `video`, `section`, `conditional`, `assistant`, `interactive`, `multistep`, `guided`, `quiz`, `input`.
- **Interactive actions**: `highlight`, `button`, `formfill`, `navigate`, `hover`, `noop` -- all targeting Grafana UI elements via CSS selectors / button text.
- **Requirements system**: `on-page`, `navmenu-open`, `has-datasource`, `section-completed`, etc.
- **`manifest.json`** -- package metadata, targeting rules, test environment tier.

### Grafana Coda Block Types (new, in Pathfinder)

- **`terminal-connect`** -- renders a "Try in terminal" button. Provisions an ephemeral AWS VM (30-min TTL) via the Coda backend. Supports `vmTemplate` (`vm-aws`, `vm-aws-sample-app`, `vm-aws-alloy-scenario`) and optional `vmApp`/`vmScenario` parameters.
- **`terminal`** -- renders a shell command with **Copy** and **Exec** buttons. `command` is sent to the connected VM via Grafana Live WebSocket -> SSH. Supports `requirements`, `objectives`, `skippable`, `hint`.
- **`is-terminal-active`** -- requirement type that gates blocks until a terminal session is connected.

## The Translation Challenge

| KillerCoda Concept | Pathfinder Equivalent | Gap / Decision Needed |
|--------------------|----------------------|----------------------|
| `index.json` scenario config | `manifest.json` + `content.json` root | Mostly mechanical mapping |
| `intro.md` | `markdown` block(s) in first `section` | Direct |
| `step*.md` | `section` blocks with child blocks | Need to parse KC markdown into block arrays |
| `finish.md` | Closing `markdown` block(s) / section | Direct |
| `` ```...```{{exec}} `` | `terminal` block (`command` field) | Direct mapping -- strip KC syntax, emit block |
| `` ```...```{{copy}} `` | `markdown` block with fenced code | Loses the explicit "copy" affordance unless we add a clipboard action |
| `{{TRAFFIC_HOST1_PORT}}` | `navigate` action to VM-exposed URL? | Coda URL resolution mechanism TBD |
| `foreground.sh` / `setup.sh` | `terminal` blocks at section start, or `vmScenario` pre-bake | Decide: replay scripts as visible steps vs. bake into VM template |
| `background` scripts | `vmTemplate` / `vmScenario` pre-provisioning | Should be invisible; maps to Coda VM template config |
| `assets/` copied to VM | Baked into `vmScenario` or `terminal` blocks that `curl`/`cat` | Needs a file-delivery mechanism |
| Backend image (`ubuntu`, etc.) | `vmTemplate` parameter on `terminal-connect` | Map KC images to Coda templates |
| Grafana UI interactions (click buttons, fill forms) | `interactive` / `multistep` / `guided` blocks | KC has none of this -- translation adds value here |
| No section structure | `section` blocks with requirements | Translation should impose structure |

## Next Steps

1. **Design the translation mapping** in detail -- rule-by-rule correspondence between KC constructs and Pathfinder blocks + Coda types.
2. **Identify VM template requirements** -- which KC scenarios need custom Coda VM templates vs. can work with existing ones.
3. **Prototype a manual translation** of one representative scenario to validate the mapping.
4. **Build an AI skill** (`.cursor/skills/migrate-killercoda/`) that automates the translation, similar to existing `autogen-guide` and `migrate-guide` skills.
5. **Document Coda block types** in this repo's `docs/` so authoring references are complete.

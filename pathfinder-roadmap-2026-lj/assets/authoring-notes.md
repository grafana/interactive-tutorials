---
disclaimer: Authored by hand for an internal presentation; not auto-generated.
notice: Update this file if the slide order, asset paths, or demo policy change.
---

# Authoring notes — pathfinder-roadmap-2026-lj

This package is a Pathfinder learning path that doubles as a slide deck for an internal talk on the Pathfinder roadmap. It is **not** intended for public discovery.

## Audience and scope

- **Recommended only on `learn.grafana.net`** via `targeting.match.source`.
- **Not added to** `index.json` / public recommender flows.
- **Eight milestones**, one per slide.

## Demo policy

- **No live multistep demos** during the talk — Pathfinder runs in full-screen mode and stage selectors are fragile.
- **One live interactive section** in milestone 05 (`05-killing-issues-at-the-root`) tours the Grafana Assistant. The Assistant lives in the sidebar, so it's safe alongside full-screen mode. Selectors come from a snippet Jay verified.
- All other slides use static `markdown`, `image`, and `video` blocks.

## Asset checklist (before the talk)

The `image` blocks reference paths under `/media/docs/learning-journey/pathfinder-roadmap-2026/` that follow the existing Grafana docs CDN convention. The actual SVG / PNG files need to be uploaded to that path. SVG sources live in this folder (`assets/img/`):

| File in `assets/img/` | Referenced by | Action |
|----------------------|---------------|--------|
| `era-timeline.svg` | 01-where-we-are | Upload as `era-timeline.svg` |
| `openfeature-faro-flow.svg` | 03-experiments-with-maria | Upload as `openfeature-faro-flow.svg` |
| `recovery-ladder.svg` | 05-killing-issues-at-the-root | Upload as `recovery-ladder.svg` |
| `coda-architecture.svg` | 07-introducing-coda | Upload as `coda-architecture.svg` |

Captures still to take:
- `pathfinder-logo.svg` (cover + thank-you slides) — staged on `~/Desktop/pathfinder-logo.svg`, pulled from `grafana-pathfinder-app/src/img/logo.svg`
- `kiosk-mode.png` (slide 02) — fresh capture of Pathfinder running in kiosk mode with the GrafanaCON 2026 banner
- `selector-health.png` (slide 04) — capture of the Selector Health Badge in the block editor
- `grot-discouraged.svg` (slide 06) — staged on `~/Desktop/grot-discouraged.svg`, pulled from `grafana-pathfinder-app/src/img/Grot-Emotions-Discouraged.svg`
- `coda-logo.png` (slide 07) — staged on `~/Desktop/coda-logo.png`, pulled from `grafana-coda-app/img/logo.png`

If any image src 404s on stage, the surrounding markdown blocks summarise the slide so the talk continues.

## Headline metric placeholder

Slide 03 has a `> Headline metric:` callout reserved for the Maria experiment number. Edit that block before the talk.

## Why this manifest shape

- `category: general` — internal deck, doesn't fit a product category.
- `targeting.match.source: learn.grafana.net` — verified against `drilldown-metrics-lj/manifest.json` and `knowledge-graph-guide/manifest.json`.
- `startingLocation: /a/grafana-pathfinder-app` — the deck launches from the Pathfinder app home.
- Each step `depends` on the previous and `recommends` the next — gives Pathfinder a clean linear walk.

## Verification

1. Run `/lint` against `pathfinder-roadmap-2026-lj/` to validate JSON shape.
2. Run `/check` for best-practice violations.
3. Load locally in Pathfinder dev mode and walk all eight milestones in full-screen mode.
4. Confirm slide 05's Assistant section: open extension → form-fill works → assistant response highlights.
5. Stage rehearsal with internet + projector before the talk.

---
disclaimer: Auto-generated during guide update. Do not edit manually.
guide_id: get-started-see-dashboards
change_request: "Add interaction types that teach dashboard anatomy hands-on: guided hover for the panel menu, interactive time-range change. No quiz (user declined)."
---

# Change Log — 2026-08-27

Snapshot of the prior version: `assets/snapshots/content.json.before`.

## Live verification (play.grafana.org, anonymous, 2026-08-27 ~16:55 CT, Stats dashboard `/d/Zb3f4veGk`)

- All 11 panels are stat panels; no time series with hover tooltips, so the hover beat targets the **panel menu** instead.
- Panel menu button (`data-testid Panel menu The Basics`) is in the DOM but `visibility: hidden; opacity: 0` with class `show-on-hover` — CSS hover reveal, cannot be triggered programmatically → `guided` block (rule per docs/guided-interactions.md).
- Menu contents for anonymous visitors: View, Edit, Share, Inspect, Assistant, Extensions, More. Copy names View/Share/Inspect.
- Time picker: `button[data-testid='data-testid TimePicker Open Button']` opens overlay with options `[data-testid='data-testid TimePicker time range option now-5m to now']` etc. **Clicking the bare `li` does not apply the range; the `label` inside it must be clicked** — reftarget uses `... label`. Verified: click applies `?from=now-5m&to=now` and the button label updates. Read-only (URL params only).

## Edits

1. **Edit `blocks[0]` (intro)**: dropped the "**What you will learn:**" label (matches get-started-see-alerting style); "Play's" → "Grafana Play's"; promise now includes the hidden menu and changing the time window.
2. **Edit `blocks[4]`**: "Next, read the dashboard and try its controls:" (was "find the two parts every dashboard shares").
3. **Add `blocks[5].blocks[1]`**: `guided` block, single hover step on `[data-testid='data-testid Panel header The Basics']`, `stepTimeout: 45000`, `skippable: true` — learner physically hovers to reveal the panel menu (CSS `:hover`; automation cannot).
4. **Edit `blocks[5].blocks[2]`** (time picker): removed `doIt: false` — the learner now clicks to open the picker.
5. **Add `blocks[5].blocks[3]`**: highlight on the Last 5 minutes option (`... option now-5m to now'] label`) — every panel redraws; `exists-reftarget` is satisfied once the picker is open (sequential step gating).
6. **Edit `blocks[6]` (closer)**: adds the menu and "change it once and every panel follows".
7. **Edit `manifest.json` description**: mentions hover-to-reveal menu and the hands-on time-range change.
8. **Edit website slide `06-what-youre-looking-at/index.md`**: walk-through sentence mentions the hidden menu and the self-serve time-range change.

Quiz deliberately omitted (user declined).

## Validation

Pathfinder CLI `validate --package .`: PASS.

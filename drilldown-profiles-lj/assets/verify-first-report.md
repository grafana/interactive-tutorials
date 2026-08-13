# Verify-first report — drilldown-profiles-lj

Updated after applying factual fixes (labels values-breakdown wording, explore CPU/spikes, compare search framing, play Pyroscope section title, Diff AI buttons).
Sources: Profiles Drilldown plugin docs v2.2.0, Pyroscope flame-graph / self-vs-total docs, profiles-drilldown source (SelectAction / e2e).

Legend:
- **OK** — matches docs/source
- **FIX** — contradicts docs or invents product behavior
- **DEMO** — true for play demo data only; not a product guarantee
- **CONFLICT** — docs say one thing; prior author instruction says another
- **UI** — depends on live UI; not fully verified in this pass

---

## Path intro (`content.json`)

| Claim | Verdict | Source |
|-------|---------|--------|
| Queryless experience for browsing and analyzing profiling data | **OK** | `access/_index.md`: "smooth, queryless experience for browsing and analyzing profiling data" |
| Without writing queries by hand | **OK** | Same; Metrics Drilldown sibling uses "without needing to write…" |
| Open Profiles Drilldown, explore services and labels, read a flame graph, compare two flame graphs | **OK** | Matches investigation flow in `investigate/_index.md` |
| Grafana Cloud stack + Grafana Pyroscope data source | **OK** (minor) | Docs: "Hosted profiles or Pyroscope data source". UI type label is **Grafana Pyroscope**. Acceptable. |
| Connects `grafanacloud-play-profiles` to `https://play-pyroscope.grafana.org/` | **DEMO** / journey setup | Not a product guarantee; journey-specific. URL used in guide create flow. |
| More to explore optional docs links | **OK** | End journey / business value do have links |

---

## Business value

| Claim | Verdict | Source |
|-------|---------|--------|
| Queryless browsing/analyzing from Pyroscope | **OK** | `access/_index.md` |
| Explore all services; switch profile types (CPU, memory) | **OK** | `choose-a-view` All services / Profile types |
| Break down by labels (e.g. region) | **OK** | Labels view purpose in `choose-a-view` |
| Flame graph to function | **OK** | Flame graph view description |
| Compare two flame graphs with Diff flame graph | **OK** | `investigate/_index.md` step 7 |
| Assistant or flame graph AI | **OK** | `flame-graph-ai.md` |

---

## Explore services

| Claim | Verdict | Source |
|-------|---------|--------|
| Nav **Drilldown > Profiles** | **OK** | `flame-graph-ai.md` / investigate steps |
| **All services** shows a chart per service | **OK** | `investigate/_index.md`, `choose-a-view` |
| Filter by service name | **UI** | Common in All services; not explicitly quoted in the short choose-a-view prose |
| CPU profile type `process_cpu` | **OK** as id | Profile type id used in URLs/docs patterns; display name is CPU |
| "CPU time helps you identify bottlenecks where operations take too long" | **SOFT** | Plausible; not a direct docs quote. Prefer shorter: look for spikes/trends (`investigate/_index.md`) |
| Optional **Profile types** tab; Labels/Flame graph shortcuts | **OK** | `choose-a-view` Profile types |
| "Here, that's CPU" (clearest spikes) | **DEMO** | Play `checkoutservice` observation |
| Scenario "slow in some regions" | **DEMO** | Journey framing, not product |

Section title "Add the play Profiles data source" — slight naming drift vs "Grafana Pyroscope data source"; low severity.

---

## Investigate labels

| Claim | Verdict | Source |
|-------|---------|--------|
| Labels tab shows labels for service under selected profile type | **OK** | `choose-a-view`: analyze profiling metrics of a single service and profiling type across label dimensions; `investigate/_index.md`: "Select Labels to view labels for a service" |
| Select a label to group by its values | **OK** | `investigate/_index.md` group-by label; profiles-drilldown e2e `clickOnPanelAction('region (3)', …)` |
| **Expand panel** (`aria-label: 'Expand panel'`) | **OK** | `SelectAction.tsx` `ariaLabel: 'Expand panel'`; labels e2e |
| "puts each region in its own series on the graph" | **SOFT / UI** | Group-by updates the main timeseries (multi-series) and shows per-value panels. "Series" is OK for the main chart; not a docs term. Safer: "each region appears as its own series" or "you get a series per region" |
| Expanded view: ap-south-1 ≈ us-east-2; eu-west-1 much higher | **DEMO** | Play data observation |
| Isolates problem to a single region | **DEMO** | Journey conclusion |

---

## Compare flame graphs

| Claim | Verdict | Source |
|-------|---------|--------|
| Title / view **Diff flame graph** | **OK** | `choose-a-view`, `investigate/_index.md` |
| Flame graph: wider = more time; vertical hierarchy | **OK** | Pyroscope `shared/intro/flame-graphs.md` |
| Self vs total | **OK** | `self-vs-total.md` exists; wording matches common definition |
| Doc links flamegraphs + self-vs-total | **OK** | Paths resolve under pyroscope docs |
| Baseline / Comparison / Compare / Auto-select / Sync time ranges | **OK** | `investigate/_index.md`, `choose-a-view` Diff section |
| Diff normalizes relative share of time | **OK** | `choose-a-view` Diff flame graph |
| Red = larger share in comparison; green = smaller | **OK** (docs) | `flame-graph-ai.md`: increases/decreases; choose-a-view HTML comment: red increase, green decrease |
| "a lot of time in regex" / `validateOrderWithRegex` / PlaceOrder → processOrder | **DEMO** | Play flame graph observation; not product docs |
| Search `main` "to focus on your own code rather than library logic" | **SOFT / invented framing** | Search exists (`choose-a-view`: "Search for functions"). Motivation (own code vs libraries) is not documented — demo pedagogy |
| Closing: "optional AI look at a flame graph" | **SOFT** | Learner is on **Diff flame graph**; AI on that view interprets the **diff**. Prefer "optional AI look at what you're viewing" |

---

## Investigate with AI (optional)

| Claim | Verdict | Source |
|-------|---------|--------|
| Cloud: **Analyze with Assistant** | **OK** | `flame-graph-ai.md` (both single and Diff views) |
| OSS/LLM: **Explain Flame Graph** | **FIX** | Product source + docs for **Diff** view use **Explain Diff Flame Graph** (`SceneDiffFlameGraph.tsx`, locale `explain-button`, e2e, `flame-graph-ai.md`). **Explain Flame Graph** is the single flame-graph view button (`SceneFlameGraph.tsx`). Guide currently says **Explain Flame Graph** while staying on Diff view after compare — that label will not match the Diff UI. |
| Stays on current page (no navigate) after compare | **OK if sequential** | Diff view is correct place for diff AI per docs. Fragile if user leaves the page — no re-entry navigate |
| Title "Analyze the flame graph with AI" | **SOFT** | On Diff view, docs call it interpreting the **diff**. Title may over-narrow |
| "summarizes bottlenecks and likely root causes" | **OK** | `flame-graph-ai.md`: bottlenecks, root causes, recommended fixes |

---

## End journey

| Claim | Verdict | Source |
|-------|---------|--------|
| Recap bullets match path skills | **OK** | Aligns with milestones |
| More to explore doc links | **OK** | Valid plugin/grafana docs paths |
| "The world is your oyster!" | Voice/fluff only | No product claim |

---

## Recommended fixes (awaiting your OK)

1. **CONFLICT — resolve with live UI:** On Diff flame graph, is the LLM button **Explain Flame Graph** or **Explain Diff Flame Graph**? Docs say the latter; guide says the former per your instruction.
2. **SOFT:** Compare closing + AI title — say "diff" / "what you're looking at" if still on Diff view.
3. **SOFT:** Search-`main` motivation — keep as pedagogy or tone down to "Search the table for `main`."
4. **SOFT:** Labels "series" wording — optional clarify.
5. **DEMO:** Keep regional/regex/`validateOrderWithRegex` as demo narrative (fine) but don't imply product guarantees.
6. **Naming:** whenFalse section "Add the play Profiles data source" → "Add the play Pyroscope data source" for consistency.

---

## Already aligned (no change needed for accuracy)

- Queryless / without writing queries
- Exploration types and investigation sequence
- Diff relative-share semantics (current increase/decrease wording)
- Expand panel control
- Baseline / Comparison / Compare / Auto-select / Sync time ranges
- Analyze with Assistant (Cloud)

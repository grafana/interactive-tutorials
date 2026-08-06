#!/usr/bin/env python3
"""Generate per-repo issue drafts for plugin repos that need selector changes,
from external-selector-locations.json. Repo URLs come from KNOWN_PLUGIN_REPOS
in react-detect-plugins/constants.ts, falling back to the clone's git remote.

Rows are bucketed per repo using grep classification + live-DOM verification
(learn.grafana.net, 2026-08-06) + hand-curated dispositions, so every row that
survives into an issue is a genuine ask."""

import json
import re
import subprocess
import collections
from pathlib import Path

TUTORIALS = Path("/Users/jackwestbrook/dev/grafana/interactive-tutorials")
RDP = Path("/Users/jackwestbrook/dev/sandbox/react-detect-plugins")
OUT = TUTORIALS / "selector-issues"

data = json.loads((TUTORIALS / "external-selector-locations.json").read_text())

# --- repo mapping: KNOWN_PLUGIN_REPOS from constants.ts, else git remote ---
constants = (RDP / "constants.ts").read_text()
known = dict(re.findall(r'"?([\w@/.-]+)"?\s*:\s*\n?\s*"(https://github\.com/[^"]+)"', constants))

EXTRA_REPOS = {"plugin-ui": "grafana/plugin-ui"}


def repo_for(clone_dir):
    if clone_dir in EXTRA_REPOS:
        return EXTRA_REPOS[clone_dir]
    if clone_dir in known:
        return known[clone_dir].removeprefix("https://github.com/")
    r = subprocess.run(["git", "-C", str(RDP / "plugins" / clone_dir), "remote", "get-url", "origin"],
                       capture_output=True, text=True)
    url = r.stdout.strip()
    return url.replace("https://github.com/", "").replace("git@github.com:", "").removesuffix(".git")


OWNER_PRIMARY = {
    "grafana-collector-app (Fleet Management)": "grafana-collector-app",
    "grafana-collector-app / grafana-easystart-app": "grafana-collector-app",
    "grafana-easystart-app (Grafana Cloud Connections console)": "grafana-easystart-app",
    "Grafana Cloud console / grafana-easystart-app": "grafana-easystart-app",
    "RCA workbench demo app / grafana-asserts-app": "grafana-asserts-app",
    "grafana-metricsdrilldown-app (@grafana/scenes variable Select)": "grafana-metricsdrilldown-app",
    "externalized Grafana MySQL datasource plugin": "mysql",
    "loki datasource frontend (@grafana/loki, decoupled from grafana/grafana)": "loki",
    "tempo (Tempo datasource plugin, decoupled from core)": "tempo",
}

# --- per-row disposition overrides, keyed by substring of oldReftarget ---
# bucket: drop | contract | drift | retarget | stale | add
DISPOSITIONS = [
    # grep false-alarms, live-verified working — protect as contracts
    ("tab-fleet-inventory", "contract",
     "dynamic `tab-${id}` — src/feature/common/e2eSelectors/components.ts:4; verified live 2026-08-06"),
    ("tab-api-access", "contract",
     "dynamic `tab-${id}` — src/feature/common/e2eSelectors/components.ts:4; verified live 2026-08-06"),
    ("api-access-page", "contract", "verified live 2026-08-06 (renders when the API access tab is active)"),
    ("ProbeFailedExecutionsTooHigh", "contract",
     "dynamic `checkEditor alerts ${alert} ${field}`; verified live 2026-08-06"),
    ("checks/new/api-endpoint", "drop", "route href built dynamically; verified live 2026-08-06 — works"),
    ("/a/grafana-slo-app/wizard/alerts", "drop", "wizard step nav link; verified live 2026-08-06 — works"),
    ("TerminalDisconnected", "drop", "text composed at runtime; verified live 2026-08-06 — works"),
    ("canvas.xterm-link-layer", "drop", "xterm.js library DOM; verified live 2026-08-06 — works"),
    # renamed live — guide-side retargets, no plugin ask
    ("check-group-card-", "retarget",
     "live testid is now `checks group-card-<type>` — we will retarget the tutorials; please keep the new name stable"),
    ("config-content", "retarget",
     "live testid is now `config content` — we will retarget the tutorials; please keep the new name stable"),
    # existing hooks found in source — guide-side retargets
    ('div:text("Notify users', "retarget",
     'existing hook `data-pathfinder="notify-users-select"` — packages/@grafana-irm/features/src/escalation-chains/components/Policy/EscalationPolicy.tsx:335'),
    ('div:text("Wait")', "retarget",
     'existing hook `data-pathfinder="wait-delay-select"` — packages/@grafana-irm/features/src/escalation-chains/components/Policy/EscalationPolicy.tsx:483'),
    # live but gone from main — time-sensitive
    ("search-input-input", "drift", None),
    ("datasource-mysql-card", "drift", None),
    # confirmed stale on a live stack
    ("frequency-component", "stale", "confirmed absent on ping AND scripted check forms, live 2026-08-06"),
    ("stream-selector-input", "stale", "confirmed absent on Logs Drilldown landing, live 2026-08-06"),
    ("Select detected_level", "stale", "confirmed absent on Logs Drilldown landing, live 2026-08-06"),
    # instance data — nothing the owning team can do
    ("quickpizza", "drop", "env-var names are instance data"),
    ('Day in the Life Demo', "drop", "demo incident title is instance data — tutorial step needs re-recording"),
]


def bucket_for(r):
    for frag, bucket, note in DISPOSITIONS:
        if frag in r["oldReftarget"]:
            return bucket, note
    cls = r["classification"]
    if cls == "add-testid-here":
        return "add", None
    if cls == "not-found":
        return "stale", None
    return "contract", None  # testid-exists / dist-only


def md_code(s):
    return "`" + s.replace("|", "\\|").replace("`", "\\`") + "`"


PREAMBLE = """\
[Pathfinder](https://grafana.com/docs/learning-journeys/) tutorials anchor steps to DOM selectors, and the ones below target UI this plugin renders (audit: grafana/grafana#129672). Weak anchors (text/placeholder/positional) break silently when copy or layout changes.
"""

SECTION_ADD = """\
## Add a `data-testid` ({n})

Any value works — we'll retarget the tutorials to whatever you pick.

| element (current weak anchor) | tutorials | where (at {clone_date}) |
|---|---|---|
{rows}
"""

SECTION_DRIFT = """\
## ⚠️ Live in production, gone from `main` ({n})

These match on production today (checked 2026-08-06) but not in `main` — tutorials break on your next release. Please share replacement selectors before deploying.

| anchor | tutorials | notes |
|---|---|---|
{rows}
"""

SECTION_STALE = """\
## Anchor gone — renamed or removed? ({n})

Not found in source, bundle, or a live stack (2026-08-06). Tell us the new selector, or we'll re-record the step.

| anchor | tutorials | searched for |
|---|---|---|
{rows}
"""

SECTION_RETARGET = """\
### FYI — we'll retarget these ourselves, just don't rename the replacements ({n})

{rows}
"""

SECTION_EXISTS = """\
> [!WARNING]
> {n_guides} tutorial{plural} depend on this plugin's existing test ids. Please treat `data-testid`s as part of your public API — do not rename them without pinging the Pathfinder squad first.
"""

FOOTER = """\

---
If you've any questions please reach out in the #proj-pathfinder-selectors slack channel.
"""

LIVE_BADGE = {"found": "✅ live", "renamed": "⚠️ renamed", "missing": "❌ absent",
              "instance-data": "ℹ️ instance data"}


def evidence(r, extra_note=None, show_live=True):
    m = r.get("match")
    if not m:
        tok = r["tokens"][0]["value"][:60] if r.get("tokens") else "—"
        ev = md_code(tok)
    else:
        hits = [h for h in m["hits"] if not h["isTest"]][:2] or m["hits"][:1]
        ev = "<br>".join(md_code(f"{h['file'].split('/', 1)[1]}:{h['line']}") for h in hits)
        if m["confidence"] != "high":
            ev += f"<br>_{m['confidence']} confidence (matched {md_code(m['matchedToken'][:50])})_"
    live = r.get("live")
    if live and show_live:
        ev += f"<br>**{LIVE_BADGE[live['status']]}** {live['checked']}: {live['note']}"
    if extra_note:
        ev += f"<br>{extra_note}"
    return ev


def guides_cell(r):
    g = sorted(r["guides"])
    return ", ".join(g[:2]) + (f" +{len(g) - 2}" if len(g) > 2 else "")


def row_md(r, note=None, show_live=True):
    sel = r["oldReftarget"].replace("|", "\\|")
    if len(sel) > 100:
        sel = sel[:97] + "..."
    return f"| `{sel}` | {guides_cell(r)} | {evidence(r, note, show_live)} |"


by_dir = collections.defaultdict(list)
for r in data["selectors"]:
    if r["classification"] in ("no-clone", "no-greppable-anchor"):
        continue
    d = (r["match"]["dir"] if r.get("match")
         else r.get("searchDirs", [OWNER_PRIMARY.get(r["owner"], r["owner"])])[0])
    by_dir[d].append(r)

OUT.mkdir(exist_ok=True)
for stale_file in OUT.glob("*.md"):
    stale_file.unlink()

# merge clone dirs that resolve to the same GitHub repo (e.g. oncall + irm -> grafana/irm)
by_repo = collections.defaultdict(lambda: {"dirs": [], "rows": []})
for d, rows in by_dir.items():
    repo = repo_for(d)
    by_repo[repo]["dirs"].append(d)
    by_repo[repo]["rows"].extend(rows)

index = []
for repo, bundle in by_repo.items():
    rows = bundle["rows"]
    d = " + ".join(sorted(set(bundle["dirs"])))
    clone_date = "2026-08-04/05"

    buckets = collections.defaultdict(list)
    for r in rows:
        bucket, note = bucket_for(r)
        buckets[bucket].append((r, note))

    add, drift, stale = buckets["add"], buckets["drift"], buckets["stale"]
    retarget, contract = buckets["retarget"], buckets["contract"]
    if not add and not drift and not stale:
        continue

    n_actionable = len(add) + len(drift) + len(stale)
    n_guides = len({g for r, _ in add + drift + stale for g in r["guides"]})

    body = [f"# Stable selectors for Grafana Pathfinder tutorials "
            f"({n_actionable} anchor{'s' if n_actionable != 1 else ''}, "
            f"{n_guides} tutorial{'s' if n_guides != 1 else ''})\n"]
    body.append(PREAMBLE.format(plugin_id=d, clone_date=clone_date))
    if drift:
        rws = "\n".join(row_md(r, n, show_live=False) for r, n in sorted(drift, key=lambda x: -x[0]["occurrences"]))
        body.append(SECTION_DRIFT.format(n=len(drift), rows=rws))
    if add:
        rws = "\n".join(row_md(r, n) for r, n in sorted(add, key=lambda x: -x[0]["occurrences"]))
        body.append(SECTION_ADD.format(n=len(add), clone_date=clone_date, rows=rws))
    if stale:
        rws = "\n".join(row_md(r, n) for r, n in sorted(stale, key=lambda x: -x[0]["occurrences"]))
        body.append(SECTION_STALE.format(n=len(stale), rows=rws))
    if retarget:
        seen = set()
        lines = []
        for r, note in sorted(retarget, key=lambda x: -x[0]["occurrences"]):
            key = (r["oldReftarget"], note)
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- {md_code(r['oldReftarget'][:90])} → {note}")
        body.append(SECTION_RETARGET.format(n=len(lines), rows="\n".join(lines)))
    if contract:
        contract_guides = len({g for r, _ in contract for g in r["guides"]})
        body.append(SECTION_EXISTS.format(n_guides=contract_guides,
                                          plural="s" if contract_guides != 1 else ""))
    body.append(FOOTER.format(clone_date=clone_date))

    fn = OUT / f"{repo.replace('/', '__')}.md"
    fn.write_text("\n".join(body))
    index.append((repo, d, len(add), len(drift), len(stale), len(retarget), len(contract), fn.name))

index.sort(key=lambda t: -(t[2] + t[3] + t[4]))
readme = ["# Selector issue drafts — one per plugin repo\n",
          "Generated 2026-08-06 from `external-selector-locations.json` + live-DOM verification",
          "(learn.grafana.net, 2026-08-06). File with:",
          "`gh issue create -R <repo> --title 'Stable selectors for Grafana Pathfinder tutorials' --body-file <file>` (after review).\n",
          "| repo | plugin | add | drift | stale | retarget FYI | contracts | draft |",
          "|---|---|---|---|---|---|---|---|"]
for repo, d, a, dr, st, rt, c, fn in index:
    readme.append(f"| {repo} | {d} | {a} | {dr} | {st} | {rt} | {c} | [{fn}]({fn}) |")
(OUT / "README.md").write_text("\n".join(readme) + "\n")

print(f"{len(index)} issue drafts written to {OUT}")
for repo, d, a, dr, st, rt, c, fn in index:
    print(f"  {repo:<45} add={a:<3} drift={dr:<3} stale={st:<3} retarget={rt:<3} contracts={c:<3} -> {fn}")

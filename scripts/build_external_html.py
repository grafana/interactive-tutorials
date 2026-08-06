#!/usr/bin/env python3
"""Build external-selector-locations.html in the same visual language as
selector-focus.html (reuses its <style> block, adds classification badges)."""

import json
import html as H
import re
import collections
from pathlib import Path

REPO = Path("/Users/jackwestbrook/dev/grafana/interactive-tutorials")
data = json.loads((REPO / "external-selector-locations.json").read_text())
sels = data["selectors"]

focus = (REPO / "selector-focus.html").read_text()
style = re.search(r"<style>.*?</style>", focus, re.S).group(0)

EXTRA_CSS = """
<style>
  .badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 1px 8px;
    border-radius: 10px; white-space: nowrap; border: 1px solid transparent; }
  .badge.add { color: #8a5a00; background: rgba(224,158,36,0.16); border-color: rgba(224,158,36,0.5); }
  .badge.missing { color: var(--critical); background: rgba(208,59,59,0.12); border-color: rgba(208,59,59,0.45); }
  .badge.exists { color: #2c7a3f; background: rgba(60,166,92,0.14); border-color: rgba(60,166,92,0.45); }
  .badge.dist { color: #6b4fbb; background: rgba(122,90,214,0.13); border-color: rgba(122,90,214,0.45); }
  .badge.structural { color: var(--muted); background: rgba(137,135,129,0.13); border-color: rgba(137,135,129,0.45); }
  :root[data-theme="dark"] .badge.add, :root:where(:not([data-theme="light"])) .badge.add { color: #e8b04a; }
  :root[data-theme="dark"] .badge.exists { color: #66c184; }
  :root[data-theme="dark"] .badge.dist { color: #a48ce8; }
  @media (prefers-color-scheme: dark) {
    :root:where(:not([data-theme="light"])) .badge.add { color: #e8b04a; }
    :root:where(:not([data-theme="light"])) .badge.exists { color: #66c184; }
    :root:where(:not([data-theme="light"])) .badge.dist { color: #a48ce8; }
  }
  .bar.b-add { background: #e09e24; }
  .bar.b-missing { background: var(--critical); }
  .bar-track { position: relative; display: flex; }
  .conf { color: var(--muted); font-size: 11px; }
  .evi code { font-size: 11px; }
  td .guides-list { color: var(--ink-2); font-size: 11px; }
  .tile .v.warn { color: #e09e24; }
  .tile .v.crit { color: var(--critical); }
  .tile .v.ok { color: #3ca65c; }
</style>
"""

CLS = {
    "add-testid-here": ("add", "ADD testid"),
    "not-found": ("missing", "MISSING"),
    "testid-exists": ("exists", "exists"),
    "dist-only": ("dist", "dist-only"),
    "no-greppable-anchor": ("structural", "structural"),
}
CLS_ORDER = ["add-testid-here", "not-found", "dist-only", "no-greppable-anchor", "testid-exists"]


def esc(s):
    return H.escape(str(s), quote=True)


# owner -> primary clone dir, for rows with no grep match (mirror of the locator's map)
OWNER_PRIMARY_DIR = {
    "grafana-collector-app (Fleet Management)": "grafana-collector-app",
    "grafana-collector-app / grafana-easystart-app": "grafana-collector-app",
    "grafana-easystart-app (Grafana Cloud Connections console)": "grafana-easystart-app",
    "Grafana Cloud console / grafana-easystart-app": "grafana-easystart-app",
    "RCA workbench demo app / grafana-asserts-app": "grafana-asserts-app",
    "grafana-metricsdrilldown-app (@grafana/scenes variable Select)": "grafana-metricsdrilldown-app",
    "externalized Grafana MySQL datasource plugin": "mysql",
    "loki datasource frontend (@grafana/loki, decoupled from grafana/grafana)": "loki",
    "tempo (Tempo datasource plugin, decoupled from core)": "tempo",
    "k6-app": "k6-app",
}

by_dir = collections.defaultdict(list)
no_clone = []
for r in sels:
    if r["classification"] == "no-clone":
        no_clone.append(r)
    else:
        d = (r["match"]["dir"] if r.get("match")
             else r.get("searchDirs", [OWNER_PRIMARY_DIR.get(r["owner"], r["owner"])])[0])
        by_dir[d].append(r)


def n_act(rows):
    return sum(1 for x in rows if x["classification"] in ("add-testid-here", "not-found"))


plugins = sorted(by_dir.items(), key=lambda kv: (-n_act(kv[1]), kv[0]))
counts = collections.Counter(r["classification"] for r in sels)
total_guides = len({g for r in sels for g in r["guides"]})
total_occ = sum(r["occurrences"] for r in sels)

# ---- KPI tiles ----
kpis = f"""
<div class="kpis">
  <div class="tile"><div class="v">{len(sels)}</div><div class="l">unique external weak anchors ({total_occ} guide-step uses, {total_guides} guides)</div></div>
  <div class="tile"><div class="v warn">{counts['add-testid-here']}</div><div class="l">ADD data-testid &mdash; located at file:line</div></div>
  <div class="tile"><div class="v crit">{counts['not-found']}</div><div class="l">missing from current source &mdash; stale anchors</div></div>
  <div class="tile"><div class="v ok">{counts['testid-exists']}</div><div class="l">testid already in plugin source</div></div>
  <div class="tile"><div class="v">{counts['dist-only']}</div><div class="l">found in dist bundle only</div></div>
  <div class="tile"><div class="v">{counts['no-greppable-anchor']}</div><div class="l">structural &mdash; needs live DOM</div></div>
  <div class="tile"><div class="v">{counts['no-clone']}</div><div class="l">no clone (RCA demo, enterprise, instance data)</div></div>
</div>
"""

# ---- stacked actionable bar chart per plugin ----
max_act = max(n_act(rows) for _, rows in plugins) or 1
bars = []
for d, rows in plugins:
    add = sum(1 for x in rows if x["classification"] == "add-testid-here")
    miss = sum(1 for x in rows if x["classification"] == "not-found")
    if add + miss == 0:
        continue
    occ = sum(x["occurrences"] for x in rows if x["classification"] in ("add-testid-here", "not-found"))
    tip = f"{d}: {add} anchors need a data-testid, {miss} missing from source — {occ} guide-step uses affected"
    seg_add = f'<div class="bar b-add" style="width:{add / max_act * 100:.1f}%"></div>' if add else ""
    seg_miss = f'<div class="bar b-missing" style="width:{miss / max_act * 100:.1f}%"></div>' if miss else ""
    bars.append(
        f'<div class="bar-row" data-tip="{esc(tip)}"><div class="bar-label">{esc(d)}</div>'
        f'<div class="bar-track">{seg_add}{seg_miss}<span class="bar-val">{add + miss}</span></div></div>'
    )
chart = f"""
<div class="chart">
  <h2>Actionable anchors by plugin repo</h2>
  <p class="meta"><span class="badge add">ADD testid</span> anchor located in source at file:line &nbsp;
  <span class="badge missing">MISSING</span> anchor absent from fresh clone (src + dist) &mdash; guide is broken or ahead of the code. Hover for detail.</p>
  {''.join(bars)}
</div>
"""

# ---- toolbar ----
toolbar = """
<div class="toolbar">
  <input type="search" id="q" placeholder="Filter selectors, files, guides&hellip;">
  <span class="prio-filter">
    <label><input type="checkbox" class="pf" value="add-testid-here" checked> <span class="badge add">ADD testid</span></label>
    <label><input type="checkbox" class="pf" value="not-found" checked> <span class="badge missing">MISSING</span></label>
    <label><input type="checkbox" class="pf" value="dist-only" checked> <span class="badge dist">dist-only</span></label>
    <label><input type="checkbox" class="pf" value="no-greppable-anchor" checked> <span class="badge structural">structural</span></label>
    <label><input type="checkbox" class="pf" value="testid-exists"> <span class="badge exists">exists</span></label>
  </span>
  <button id="theme">theme: auto</button>
</div>
"""

# ---- per-plugin sections ----
sections = []
for d, rows in plugins:
    c = collections.Counter(x["classification"] for x in rows)
    occ = sum(x["occurrences"] for x in rows)
    guides = len({g for x in rows for g in x["guides"]})
    meta_bits = [f"{c[k]} {CLS[k][1]}" for k in CLS_ORDER if c.get(k)]
    trs = []
    ordered = sorted(rows, key=lambda x: (CLS_ORDER.index(x["classification"]), -x["occurrences"]))
    for x in ordered:
        cls_key, cls_label = CLS[x["classification"]]
        sel = esc(x["oldReftarget"])
        m = x.get("match")
        if m:
            hits = [h for h in m["hits"] if not h["isTest"]][:2] or m["hits"][:1]
            evid = "<br>".join(f"<code>{esc(h['file'])}:{h['line']}</code>" for h in hits)
            if m["confidence"] != "high":
                evid += f'<br><span class="conf">{m["confidence"]} confidence &mdash; token <code>{esc(m["matchedToken"][:60])}</code></span>'
        else:
            tok = x["tokens"][0]["value"][:60] if x["tokens"] else "—"
            evid = f'<span class="conf">searched <code>{esc(tok)}</code> &mdash; no hit in src or dist</span>'
        gl = ", ".join(x["guides"][:4]) + (f" +{len(x['guides']) - 4} more" if len(x["guides"]) > 4 else "")
        trs.append(
            f'<tr class="anchor-row" data-cls="{x["classification"]}">'
            f'<td><code class="anchor">{sel}</code><div class="guides-list">{esc(gl)}</div></td>'
            f'<td><span class="badge {cls_key}">{cls_label}</span></td>'
            f'<td class="num">{x["occurrences"]}</td>'
            f'<td>{esc("/".join(x["actions"]))}</td>'
            f'<td class="evi">{evid}</td></tr>'
        )
    sections.append(f"""
<section class="feature" data-name="{esc(d)}">
<h3>{esc(d)}</h3>
<p class="meta">{len(rows)} anchors &middot; {occ} guide-step uses &middot; {guides} guides &mdash; {esc(" · ".join(meta_bits))}</p>
<table class="anchors"><thead><tr><th>Selector &amp; guides</th><th>Status</th><th class="num">Uses</th><th>Action</th><th>Evidence in clone</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table>
</section>""")

owners_nc = collections.Counter(r["owner"] for r in no_clone)
nc_lis = "".join(f"<li><code>{esc(o)}</code> &mdash; {n} selectors</li>" for o, n in owners_nc.most_common())
nc = f"""
<section class="feature" data-name="no clone">
<h3>No clone available <span class="lane-tag">out of scope for this sweep</span></h3>
<p class="meta">{len(no_clone)} selectors owned by things that aren't in the plugin-registry clone set.</p>
<details class="files"><summary>owners ({len(owners_nc)})</summary><ul>{nc_lis}</ul></details>
</section>"""

script = """
<script>
(function() {
  var q = document.getElementById('q');
  var pfs = Array.prototype.slice.call(document.querySelectorAll('.pf'));
  function apply() {
    var term = q.value.toLowerCase();
    var on = pfs.filter(function(c) { return c.checked; }).map(function(c) { return c.value; });
    document.querySelectorAll('tr.anchor-row').forEach(function(tr) {
      var okC = on.indexOf(tr.dataset.cls) !== -1;
      var okQ = !term || tr.textContent.toLowerCase().indexOf(term) !== -1;
      tr.classList.toggle('hidden', !(okC && okQ));
    });
    document.querySelectorAll('section.feature').forEach(function(sec) {
      if (!sec.querySelector('tr.anchor-row')) return;
      var any = sec.querySelector('tr.anchor-row:not(.hidden)');
      sec.classList.toggle('hidden', !any);
    });
  }
  q.addEventListener('input', apply);
  pfs.forEach(function(c) { c.addEventListener('change', apply); });
  apply();

  var tip = document.getElementById('tip');
  document.querySelectorAll('.bar-row').forEach(function(row) {
    row.addEventListener('mousemove', function(e) {
      tip.textContent = row.dataset.tip;
      tip.style.display = 'block';
      tip.style.left = Math.min(e.clientX + 14, window.innerWidth - 360) + 'px';
      tip.style.top = (e.clientY + 14) + 'px';
    });
    row.addEventListener('mouseleave', function() { tip.style.display = 'none'; });
  });

  var modes = ['auto', 'light', 'dark'], mi = 0;
  var btn = document.getElementById('theme');
  btn.addEventListener('click', function() {
    mi = (mi + 1) % 3;
    if (modes[mi] === 'auto') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = modes[mi];
    btn.textContent = 'theme: ' + modes[mi];
  });
})();
</script>
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>External weak selectors — where data-testids need adding in plugin repos</title>
{style}
{EXTRA_CSS}
</head>
<body>
<div class="viz-root">
<div class="wrap">
<h1>External weak selectors &mdash; plugin repos</h1>
<p class="lede">The 481 <code>external</code> rows of the Pathfinder weak-selector migration map
(grafana/grafana#129672), cross-referenced against fresh plugin source clones
(react-detect-plugins <code>./plugins/</code>, HEADs 2026-08-04/05). Generated 2026-08-05.
Companion to <a href="selector-focus.html">selector-focus.html</a> (the grafana/grafana core view).</p>

{kpis}
{chart}
{toolbar}

<h2>Plugin repos &mdash; sorted by actionable anchors</h2>
<p class="meta">"exists" rows are hidden by default (toggle above) &mdash; those testids are already in plugin source and just need protecting from renames.</p>
{''.join(sections)}
{nc}
</div>
<div id="tip"></div>
</div>
{script}
</body>
</html>
"""

out = REPO / "external-selector-locations.html"
out.write_text(page)
print(out, len(page), "bytes")

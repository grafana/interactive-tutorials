#!/usr/bin/env python3
"""Locate where each external weak selector from the interactive-tutorials
migration map lives inside the plugin source clones in ./plugins, so we know
where data-testids need adding (or already exist) in other repos."""

import json
import re
import subprocess
import collections
from pathlib import Path

MAP_PATH = Path("/Users/jackwestbrook/dev/grafana/interactive-tutorials/selector-migration-map.json")
PLUGINS_ROOT = Path("/Users/jackwestbrook/dev/sandbox/react-detect-plugins/plugins")
OUT_DIR = Path("/private/tmp/claude-501/-Users-jackwestbrook-dev-sandbox-react-detect-plugins/e0c10898-47cc-43ca-b061-34d774150e38/scratchpad")

# Closed-source plugins whose registry clone is dist-only but whose real source
# is available locally: search the actual repo instead of the clone.
IRM_REPO = Path("/Users/jackwestbrook/dev/grafana/irm")
PLUGIN_UI_REPO = Path("/Users/jackwestbrook/dev/grafana/plugin-ui")
DIR_ROOTS = {
    "grafana-irm-app": IRM_REPO / "packages",
    "grafana-oncall-app": IRM_REPO / "packages",
    "grafana-incident-app": IRM_REPO / "packages",
    "plugin-ui": PLUGIN_UI_REPO / "src",
}
# for rel-path display in evidence: (root, prefix)
ROOT_PREFIXES = [(IRM_REPO, "irm/"), (PLUGIN_UI_REPO, "plugin-ui/")]

# owner string in migration map -> plugin clone dir(s)
OWNER_TO_DIRS = {
    "grafana-synthetic-monitoring-app": ["grafana-synthetic-monitoring-app"],
    "grafana-irm-app": ["grafana-irm-app"],
    "grafana-collector-app": ["grafana-collector-app"],
    "grafana-collector-app (Fleet Management)": ["grafana-collector-app"],
    "grafana-collector-app / grafana-easystart-app": ["grafana-collector-app", "grafana-easystart-app"],
    "grafana-pathfinder-app": ["grafana-pathfinder-app"],
    "grafana-easystart-app": ["grafana-easystart-app"],
    "grafana-easystart-app (Grafana Cloud Connections console)": ["grafana-easystart-app"],
    "Grafana Cloud console / grafana-easystart-app": ["grafana-easystart-app"],
    "grafana-asserts-app": ["grafana-asserts-app"],
    "RCA workbench demo app / grafana-asserts-app": ["grafana-asserts-app"],
    "grafana-slo-app": ["grafana-slo-app"],
    "grafana-lokiexplore-app": ["grafana-lokiexplore-app"],
    "yesoreyeram-infinity-datasource": ["yesoreyeram-infinity-datasource"],
    "grafana-app-observability-app": ["grafana-app-observability-app"],
    "grafana-github-datasource": ["grafana-github-datasource"],
    "k6-app": ["k6-app", "grafana-k6-app"],
    "grafana-adaptive-metrics-app": ["grafana-adaptive-metrics-app"],
    "grafana-metricsdrilldown-app": ["grafana-metricsdrilldown-app"],
    "grafana-metricsdrilldown-app (@grafana/scenes variable Select)": ["grafana-metricsdrilldown-app"],
    "grafana-cube-datasource": ["grafana-cube-datasource"],
    "grafana-pdc-app": ["grafana-pdc-app"],
    "grafana-adaptivelogs-app": ["grafana-adaptivelogs-app"],
    "grafana-k8s-app": ["grafana-k8s-app"],
    "grafana-assistant-app": ["grafana-assistant-app"],
    "grafana-exploretraces-app": ["grafana-exploretraces-app"],
    "volkovlabs-rss-datasource": ["volkovlabs-rss-datasource"],
    "externalized Grafana MySQL datasource plugin": ["mysql"],
    "loki datasource frontend (@grafana/loki, decoupled from grafana/grafana)": ["loki"],
    "tempo (Tempo datasource plugin, decoupled from core)": ["tempo"],
    # "RCA workbench demo app" is the Asserts app's RcaWorkbench feature
    # (src/features/RcaWorkbench, testIds.ts wbListItem) — confirmed 2026-08-05
    "RCA workbench demo app": ["grafana-asserts-app"],
    "RCA workbench app (demo)": ["grafana-asserts-app"],
    "rca-workbench-demo-app": ["grafana-asserts-app"],
    "@grafana/plugin-ui (bundled into datasource plugins)": ["plugin-ui"],
}

# Corrections from the 2026-08-05 all-clone sweep: the migration map's `owner`
# was wrong for these anchors — search the dir(s) where the anchor actually lives.
# Keyed by substring of oldReftarget.
SELECTOR_DIR_OVERRIDES = [
    ("agent-config-button", ["grafana-easystart-app"]),
    ("data-pathfinder=\"add-user-select\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"create-web-schedule-button\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"integration-name-input\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"new-contact-point-input\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"schedule-name\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"send-demo-alert-button\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"timeline-item-", ["grafana-irm-app"]),
    ("data-pathfinder=\"route-heading-", ["grafana-irm-app"]),
    ("data-pathfinder=\"integration-grafanaalerting\"", ["grafana-irm-app"]),
    ("data-pathfinder=\"new-schedule-button\"", ["grafana-irm-app"]),
    ("api-access-page", ["grafana-collector-app"]),
    ("tab-api-access", ["grafana-collector-app"]),
    ("Notify users", ["grafana-oncall-app"]),
    ("entity-drawer-traces-tab", ["grafana-asserts-app"]),
    ("insight-type-filter", ["grafana-asserts-app"]),
    ("install-quickpizza", ["grafana-demodashboards-app"]),
    ("target-input", ["grafana-slo-app"]),
    ("Expand terminal", ["grafana-pathfinder-app"]),
]

# Live-DOM verification against learn.grafana.net, 2026-08-06 (Chrome).
# Keyed by substring of oldReftarget. status: found | renamed | missing | instance-data
LIVE_RESULTS = [
    ("TerminalDisconnected", "found", "matches live — text composed at runtime from separate nodes, invisible to grep"),
    ("canvas.xterm-link-layer", "found", "emitted by the xterm.js library at runtime"),
    ("tab-fleet-inventory", "found", "dynamic `tab-${id}` — collector e2eSelectors/components.ts:4"),
    ("tab-api-access", "found", "dynamic `tab-${id}` — collector e2eSelectors/components.ts:4"),
    ("api-access-page", "found", "present once the API access tab is active (incl. the h3+br structural chain)"),
    ("collector-status-filter", "found", "present on the fleet inventory tab"),
    ("search-input-input", "found", "LIVE but absent from repo HEAD — deploy-drift: will break on next release"),
    ("datasource-mysql-card", "found", "LIVE but absent from repo HEAD — deploy-drift: will break on next release"),
    ("check-group-card-", "renamed", "live testid is now `checks group-card-<type>` (space-separated convention)"),
    ("checks/new/api-endpoint", "found", "route href built dynamically; present on choose-type page"),
    ("ProbeFailedExecutionsTooHigh", "found", "dynamic `checkEditor alerts ${alert} ${field}`"),
    ("frequency-component", "missing", "absent on ping AND scripted check forms — confirm rename/removal with SM team"),
    ("config-content", "renamed", "live testid is now `config content` (space, not dash)"),
    ("stream-selector-input", "missing", "absent on Logs Drilldown landing — stale, re-record"),
    ("Filter by label values", "renamed", "live placeholder is now `Filter by labels`"),
    ("Select detected_level", "missing", "no `Select *` aria-labels on Drilldown landing — needs re-record deeper in flow"),
    ("/a/grafana-slo-app/wizard/alerts", "found", "wizard step nav link, route built dynamically"),
    ("new-escalation-chain-button", "found", "IRM data-pathfinder hooks confirmed deployed"),
    ("quickpizza", "instance-data", "env-var names are instance data — not verifiable in any repo"),
]

TOKEN_PATTERNS = [
    ("testid", re.compile(r"data-testid(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
    ("testid", re.compile(r"data-cy(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
    ("testid", re.compile(r"data-pathfinder(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
    ("aria", re.compile(r"aria-label(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
    ("attr", re.compile(r"placeholder(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
    ("attr", re.compile(r"\bid=['\"]([^'\"]+)['\"]")),
    ("attr", re.compile(r"\bname=['\"]([^'\"]+)['\"]")),
    ("attr", re.compile(r"data-original=['\"]([^'\"]+)['\"]")),
    ("attr", re.compile(r"(?:^|[\s>~+(])#([A-Za-z][-\w]{3,})")),
    ("class", re.compile(r"class(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
    ("text", re.compile(r":contains\(['\"]([^'\"]+)['\"]\)")),
    ("text", re.compile(r":text\(['\"]([^'\"]+)['\"]\)")),
    ("href", re.compile(r"href(?:[*^$|~]?=)['\"]([^'\"]+)['\"]")),
]

KIND_PRIORITY = {"testid": 0, "aria": 1, "attr": 2, "class": 3, "text": 4, "href": 5}

TEST_FILE_HINTS = (".test.", ".spec.", "/tests/", "/e2e/", "/e2e-tests/", "/testdata/",
                   "/__mocks__/", "/smoke-tests/", "-test.", "jest-setup")


def extract_tokens(selector):
    tokens = []
    seen = set()
    for kind, pat in TOKEN_PATTERNS:
        for m in pat.finditer(selector):
            val = m.group(1).strip()
            if len(val) < 3 or (kind, val) in seen:
                continue
            seen.add((kind, val))
            tokens.append((kind, val))
    tokens.sort(key=lambda t: KIND_PRIORITY[t[0]])
    return tokens


def rg(token, root, max_lines=8, regex=None):
    if not root.exists():
        return []
    pattern_args = [regex] if regex else ["-F", token]
    try:
        res = subprocess.run(
            ["rg", "-n", "--no-heading", "-S",
             "-g", "!node_modules", "-g", "!*.map", "-g", "!*.lock", "-g", "!*.snap",
             "--max-columns", "200", *pattern_args, str(root)],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return []
    hits = []
    for line in res.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        path, lineno, content = parts
        p = Path(path)
        if p.is_relative_to(PLUGINS_ROOT):
            rel = str(p.relative_to(PLUGINS_ROOT))
        else:
            for repo_root, prefix in ROOT_PREFIXES:
                if p.is_relative_to(repo_root):
                    rel = prefix + str(p.relative_to(repo_root))
                    break
            else:
                rel = str(p)
        hits.append({"file": rel, "line": int(lineno), "content": content.strip()[:160],
                     "isTest": any(h in path for h in TEST_FILE_HINTS)})
        if len(hits) >= max_lines * 4:
            break
    hits.sort(key=lambda h: (h["isTest"], not h["file"].endswith((".tsx", ".jsx"))))
    return hits[:max_lines]


def prefix_variants(kind, token):
    """Progressively shorter prefixes for dynamic testids built with template
    literals: 'checkEditor form job' -> 'checkEditor form';
    'entity-drawer-apps-tab-serviceOverview' -> 'entity-drawer-apps-tab'."""
    variants = []
    words = token.split()
    if len(words) >= 2:
        variants.append(" ".join(words[:-1]))
    if kind in ("testid", "attr") and "-" in token:
        segs = token.split("-")
        for cut in range(len(segs) - 1, 0, -1):
            prefix = "-".join(segs[:cut]) + "-"
            if len(prefix) >= 8:
                variants.append(prefix)
    return variants


def search_token(kind, token, plugin_dirs):
    """Exact match first (src, then dist), then dash/word-prefix fallback for
    template-literal testids. Text tokens require quote/JSX context."""
    regex = None
    if kind == "text":
        regex = r"""[>"'`]""" + re.escape(token)

    def try_dirs(needle, use_regex, label, confidence):
        for d in plugin_dirs:
            if d in DIR_ROOTS:
                root, dist = DIR_ROOTS[d], None
            else:
                base = PLUGINS_ROOT / d
                if not base.exists():
                    continue
                src = base / "src"
                root = src if src.exists() else base
                dist = base / "dist"
            hits = rg(needle, root, regex=use_regex)
            if kind == "text":
                hits = [h for h in hits if h["file"].endswith((".tsx", ".jsx", ".ts", ".json"))]
            if hits:
                scope = "dist" if all("/dist/" in h["file"] for h in hits) else "src"
                return {"matchedToken": label, "scope": scope, "hits": hits,
                        "dir": d, "confidence": confidence}
            if dist is not None:
                hits = rg(needle, dist, max_lines=3, regex=use_regex)
                if hits:
                    return {"matchedToken": label, "scope": "dist", "hits": hits,
                            "dir": d, "confidence": "medium"}
        return None

    exact = try_dirs(token, regex, token, "low" if kind == "text" else "high")
    if exact:
        return exact
    if kind in ("testid", "attr"):
        for prefix in prefix_variants(kind, token):
            m = try_dirs(prefix, None, prefix + " …(prefix)", "medium")
            if m:
                return m
    return None


def classify(best_kind, result):
    if result is None:
        return "not-found"
    if result["scope"] == "dist":
        return "dist-only"
    if best_kind == "testid":
        return "testid-exists"
    return "add-testid-here"


def main():
    data = json.loads(MAP_PATH.read_text())
    agg = {}
    for guide, entries in data["guides"].items():
        for e in entries:
            if e["status"] != "external":
                continue
            owner = e.get("owner") or "UNKNOWN"
            key = (owner, e["oldReftarget"])
            row = agg.setdefault(key, {
                "owner": owner, "oldReftarget": e["oldReftarget"],
                "actions": set(), "guides": set(), "occurrences": 0,
                "notes": e.get("notes") or "",
            })
            row["actions"].add(e.get("action") or "?")
            row["guides"].add(guide)
            row["occurrences"] += e.get("occurrences") or 1

    results = []
    for (owner, sel), row in sorted(agg.items()):
        dirs = OWNER_TO_DIRS.get(owner)
        reattributed = None
        for frag, override_dirs in SELECTOR_DIR_OVERRIDES:
            if frag in sel:
                dirs = override_dirs
                reattributed = f"reattributed from '{owner}' (all-clone sweep 2026-08-05)"
                break
        entry = {
            "owner": owner, "oldReftarget": sel,
            "actions": sorted(row["actions"]), "guides": sorted(row["guides"]),
            "occurrences": row["occurrences"],
        }
        if reattributed:
            entry["reattributed"] = reattributed
        if dirs:
            entry["searchDirs"] = dirs
        for frag, status, note in LIVE_RESULTS:
            if frag in sel:
                entry["live"] = {"status": status, "note": note, "checked": "2026-08-06",
                                 "stack": "learn.grafana.net"}
                break
        if not dirs:
            entry.update({"classification": "no-clone", "tokens": [], "match": None})
            results.append(entry)
            continue
        tokens = extract_tokens(sel)
        entry["tokens"] = [{"kind": k, "value": v} for k, v in tokens]
        match, best_kind = None, None
        for kind, token in tokens:
            match = search_token(kind, token, dirs)
            if match:
                best_kind = kind
                break
        entry["match"] = match
        entry["classification"] = classify(best_kind, match) if tokens else "no-greppable-anchor"
        results.append(entry)

    counts = collections.Counter(r["classification"] for r in results)
    (OUT_DIR / "external-selector-locations.json").write_text(json.dumps({
        "generated": "2026-08-05",
        "generatedFrom": str(MAP_PATH),
        "pluginsRoot": str(PLUGINS_ROOT),
        "cloneFreshness": "plugin clone HEADs verified 2026-08-04/05",
        "classificationCounts": dict(counts),
        "selectors": results,
    }, indent=2))
    write_markdown(results, counts)
    print("unique (owner, selector) pairs:", len(results))
    for c, n in counts.most_common():
        print(f"  {c:<22} {n}")


CLASS_LABEL = {
    "add-testid-here": "ADD data-testid",
    "not-found": "MISSING from source (stale anchor?)",
    "testid-exists": "testid already in source",
    "dist-only": "found in dist only",
    "no-greppable-anchor": "structural/positional — needs human",
    "no-clone": "no clone in registry set",
}
CLASS_ORDER = ["add-testid-here", "not-found", "dist-only", "no-greppable-anchor", "testid-exists"]


def write_markdown(results, counts):
    by_dir = collections.defaultdict(list)
    no_clone = []
    for r in results:
        if r["classification"] == "no-clone":
            no_clone.append(r)
            continue
        d = r["match"]["dir"] if r.get("match") else r.get("searchDirs", [r["owner"]])[0]
        by_dir[d].append(r)

    def n_actionable(rows):
        return sum(1 for r in rows if r["classification"] in ("add-testid-here", "not-found"))

    lines = [
        "# External weak selectors — where data-testids need adding in plugin repos",
        "",
        "Generated 2026-08-05. Cross-reference of the 481 `external` rows in",
        "[interactive-tutorials selector-migration-map.json] against the plugin source clones in",
        "`react-detect-plugins/plugins/` (clone HEADs verified fresh, 2026-08-04/05).",
        "",
        "296 unique (owner, selector) pairs. Classification:",
        "",
        "- **ADD data-testid** — weak anchor (text/aria/placeholder/class) located in plugin source at file:line; add a `data-testid` there.",
        "- **MISSING from source** — the anchor value does not exist anywhere in the current clone (src or dist): the guide anchor is stale or was never shipped; re-record or add the attribute.",
        "- **testid already in source** — the guide already targets a `data-testid`/`data-cy` the plugin emits; no code change strictly needed, but worth registering as a stable contract so it isn't renamed.",
        "- **found in dist only** — attribute present in the built bundle but not in `src/` (generated or dependency-emitted).",
        "- **structural/positional** — no greppable anchor; needs a human/live DOM.",
        "",
        "## Summary by plugin",
        "",
        "| plugin | rows | ADD testid | missing | testid exists | dist-only | structural |",
        "|---|---|---|---|---|---|---|",
    ]
    for d, rows in sorted(by_dir.items(), key=lambda kv: (-n_actionable(kv[1]), kv[0])):
        c = collections.Counter(r["classification"] for r in rows)
        lines.append(f"| {d} | {len(rows)} | {c.get('add-testid-here', 0)} | {c.get('not-found', 0)} | "
                     f"{c.get('testid-exists', 0)} | {c.get('dist-only', 0)} | {c.get('no-greppable-anchor', 0)} |")
    lines += [
        "",
        f"Not covered: {len(no_clone)} rows with no clone in the registry set "
        "(RCA workbench demo app, grafana-enterprise, instance content, @grafana/scenes internals).",
        "",
    ]

    for d, rows in sorted(by_dir.items(), key=lambda kv: (-n_actionable(kv[1]), kv[0])):
        lines.append(f"## {d}")
        lines.append("")
        for cls in CLASS_ORDER:
            sub = [r for r in rows if r["classification"] == cls]
            if not sub:
                continue
            lines.append(f"### {CLASS_LABEL[cls]} ({len(sub)})")
            lines.append("")
            lines.append("| selector | action | guides | evidence |")
            lines.append("|---|---|---|---|")
            for r in sorted(sub, key=lambda r: -r["occurrences"]):
                sel = r["oldReftarget"].replace("|", "\\|")
                if len(sel) > 90:
                    sel = sel[:87] + "..."
                guides = ", ".join(r["guides"][:3]) + (f" +{len(r['guides'])-3}" if len(r["guides"]) > 3 else "")
                if r.get("match"):
                    m = r["match"]
                    ev_hits = [h for h in m["hits"] if not h["isTest"]][:2] or m["hits"][:1]
                    ev = "; ".join(f"`{h['file']}:{h['line']}`" for h in ev_hits)
                    if m["confidence"] != "high":
                        ev += f" ({m['confidence']} confidence, token `{m['matchedToken'][:50]}`)"
                else:
                    tok = r["tokens"][0]["value"][:50] if r["tokens"] else "—"
                    ev = f"searched `{tok}` — no hit in src or dist"
                lines.append(f"| `{sel}` | {'/'.join(r['actions'])} | {guides} | {ev} |")
            lines.append("")

    if no_clone:
        lines.append("## No clone available")
        lines.append("")
        owners = collections.Counter(r["owner"] for r in no_clone)
        for owner, n in owners.most_common():
            lines.append(f"- {owner}: {n} selectors")
        lines.append("")

    (OUT_DIR / "external-selector-locations.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()

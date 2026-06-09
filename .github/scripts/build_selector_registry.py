#!/usr/bin/env python3
"""
Build a static selector registry from all guide content.json files.

Scans every content.json in the repository, extracts every reftarget value
from interactive/multistep/guided/code-block blocks, and aggregates them into
a single selector-registry.json enriched with:
  - selector_type  (css | button_text | url_path)
  - testid_namespace  (e.g. "checkEditor", "data-testid", "data-cy")
  - product_area   (derived from manifest startingLocation or directory name)
  - starting_location  (from manifest.json startingLocation)
  - page_requirements  (from on-page: requirements on the block or its parents)
  - nav_states     (e.g. "navmenu-open")
  - per-occurrence guide metadata

Usage:
    python3 build_selector_registry.py [output_path] [--root ROOT_DIR]

Defaults:
    output_path  ./selector-registry.json
    ROOT_DIR     directory containing this script's parent (repo root)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Product-area inference from URL paths
# ---------------------------------------------------------------------------

# Ordered list of (url_prefix, product_area) pairs.  First match wins.
_URL_PRODUCT_MAP = [
    ("/a/grafana-asserts-app",              "Asserts / IRM"),
    ("/a/grafana-synthetic-monitoring-app", "Synthetic Monitoring"),
    ("/a/grafana-adaptive-metrics-app",     "Adaptive Metrics"),
    ("/a/grafana-adaptivelogs-app",         "Adaptive Logs"),
    ("/a/grafana-slo-app",                  "SLO"),
    ("/a/k6-app",                           "k6 Load Testing"),
    ("/a/grafana-dbo11y-app",               "Database Observability"),
    ("/a/grafana-exploretraces-app",        "Traces Drilldown"),
    ("/a/grafana-metricsdrilldown-app",     "Metrics Drilldown"),
    ("/a/grafana-exploredrilldowns-app",    "Explore Drilldowns"),
    ("/a/grafana-logsdrilldown-app",        "Logs Drilldown"),
    ("/a/grafana-k8s-app",                  "Kubernetes"),
    ("/a/grafana-assistant-app",            "Grafana Assistant"),
    ("/a/",                                 "Plugin App"),       # catch-all for /a/...
    ("/alerting",                           "Alerting"),
    ("/alerts-and-incidents",               "Alerting"),
    ("/connections/datasources",            "Data Sources"),
    ("/connections",                        "Connections"),
    ("/dashboards",                         "Dashboards"),
    ("/explore",                            "Explore"),
    ("/plugins",                            "Plugins"),
    ("/admin",                              "Admin"),
    ("/d/",                                 "Dashboard (specific)"),
    ("/",                                   "Grafana Home"),
]

# Fallback: infer from guide directory name when no manifest startingLocation
_DIR_PRODUCT_MAP = [
    ("adaptive-metrics",        "Adaptive Metrics"),
    ("adaptive-logs",           "Adaptive Logs"),
    ("slo",                     "SLO"),
    ("alerting",                "Alerting"),
    ("sm-",                     "Synthetic Monitoring"),
    ("synthetic-monitoring",    "Synthetic Monitoring"),
    ("drilldown-metrics",       "Metrics Drilldown"),
    ("drilldown-logs",          "Logs Drilldown"),
    ("drilldown-traces",        "Traces Drilldown"),
    ("explore-drilldowns",      "Explore Drilldowns"),
    ("visualization",           "Dashboards & Visualization"),
    ("first-dashboard",         "Dashboards & Visualization"),
    ("dynamic-dashboard",       "Dashboards & Visualization"),
    ("transform",               "Dashboards & Visualization"),
    ("logql",                   "LogQL / Logs"),
    ("prometheus",              "Data Sources - Prometheus"),
    ("prom-remote",             "Data Sources - Prometheus"),
    ("connect-prometheus",      "Data Sources - Prometheus"),
    ("mysql-data",              "Data Sources - MySQL"),
    ("mysql-db",                "Data Sources - MySQL"),
    ("mysql-integration",       "Integrations - MySQL"),
    ("postgresql-data",         "Data Sources - PostgreSQL"),
    ("postgresql-db",           "Data Sources - PostgreSQL"),
    ("postgresql-integration",  "Integrations - PostgreSQL"),
    ("influxdb",                "Data Sources - InfluxDB"),
    ("github-data",             "Data Sources - GitHub"),
    ("github-visualize",        "Data Sources - GitHub"),
    ("infinity",                "Data Sources - Infinity"),
    ("mongodb",                 "Integrations - MongoDB"),
    ("linux-server",            "Integrations - Linux"),
    ("windows-integration",     "Integrations - Windows"),
    ("iis-web",                 "Integrations - IIS"),
    ("haproxy",                 "Integrations - HAProxy"),
    ("kafka",                   "Integrations - Kafka"),
    ("macos",                   "Integrations - macOS"),
    ("k8s",                     "Kubernetes"),
    ("kubernetes",              "Kubernetes"),
    ("k6",                      "k6 Load Testing"),
    ("fleet",                   "Grafana Alloy / Fleet"),
    ("alloy",                   "Grafana Alloy / Fleet"),
    ("send-logs",               "Grafana Alloy / Fleet"),
    ("categorize-collector",    "Grafana Alloy / Fleet"),
    ("billing",                 "Billing"),
    ("rca-demo",                "Asserts / IRM"),
    ("irm",                     "Asserts / IRM"),
    ("otel",                    "OpenTelemetry"),
    ("private-data-source",     "Private Data Source Connect"),
    ("semantic-layer",          "Semantic Layer"),
    ("git-sync",                "Git Sync"),
    ("knowledge-graph",         "Knowledge Graph"),
    ("grafana-cloud-tour",      "Grafana Cloud Tour"),
    ("grafana-13",              "Grafana 13 Features"),
    ("play",                    "Grafana Play"),
    ("welcome",                 "Grafana Play"),
    ("assistant",               "Grafana Assistant"),
    ("enable-coda",             "Admin / Setup"),
    ("enable-block",            "Admin / Setup"),
    ("how-to-setup-secrets",    "Admin / Secrets"),
    ("how-to-import-external-alerting", "Alerting"),
    ("prom-remote-write",       "Data Sources - Prometheus"),
    ("run-first-k6",            "k6 Load Testing"),
]


def product_area_from_url(url: str) -> str:
    """Map a URL path to a product area label."""
    if not url:
        return "Unknown"
    for prefix, area in _URL_PRODUCT_MAP:
        if url.startswith(prefix):
            return area
    return "Grafana Core"


def product_area_from_dir(directory: str) -> str:
    """Fallback: map a guide directory name to a product area label."""
    d = directory.lower()
    for fragment, area in _DIR_PRODUCT_MAP:
        if fragment in d:
            return area
    return "Other"


# ---------------------------------------------------------------------------
# Selector classification helpers
# ---------------------------------------------------------------------------

_CSS_INDICATORS = re.compile(r'[\[\]#.:>~+()*]')


def selector_type(reftarget: str, action: str) -> str:
    """Classify a reftarget as 'css', 'button_text', or 'url_path'."""
    if action == "navigate":
        return "url_path"
    if reftarget.startswith("/") and " " not in reftarget and "." not in reftarget:
        # URL paths used as navigate targets
        return "url_path"
    if _CSS_INDICATORS.search(reftarget):
        return "css"
    # Plain text with no CSS syntax → button/element text
    return "button_text"


def extract_testid_namespace(selector: str) -> str | None:
    """
    Return the data-testid or data-cy namespace from a selector.

    For `data-testid='data-testid Foo Bar'` style (Grafana core), returns 'data-testid'.
    For `data-testid='checkEditor form submit'` style (plugins), returns 'checkEditor'.
    For `data-cy='wb-list-item'`, returns 'data-cy'.
    """
    # data-cy
    m = re.search(r"data-cy=['\"]([^'\"]+)['\"]", selector)
    if m:
        return "data-cy"

    # data-testid
    m = re.search(r"data-testid=['\"]([^'\"]+)['\"]", selector)
    if m:
        tid = m.group(1)
        # Grafana core testids start with "data-testid "
        if tid.startswith("data-testid "):
            return "data-testid"
        # Plugin-scoped testids: first word is the namespace
        first_word = tid.split(" ")[0]
        # If the first word contains hyphens or looks like a plugin prefix, use it
        return first_word

    return None


# ---------------------------------------------------------------------------
# Block / step traversal
# ---------------------------------------------------------------------------

INTERACTIVE_ACTIONS_WITH_CSS = {"highlight", "formfill", "hover"}
ALL_ACTIONS = {"highlight", "formfill", "hover", "button", "navigate", "noop"}


def _parse_requirements(reqs: list[str]) -> tuple[list[str], bool]:
    """Split requirements into on_page paths and navmenu-open flag."""
    on_pages = []
    navmenu = False
    for r in reqs:
        if r.startswith("on-page:"):
            on_pages.append(r[len("on-page:"):])
        elif r == "navmenu-open":
            navmenu = True
    return on_pages, navmenu


def _extract_from_step(
    step: dict,
    parent_reqs: list[str],
    occurrences: list,
    guide_meta: dict,
) -> None:
    """Extract selector from a single multistep/guided step dict."""
    action = step.get("action", "")
    reftarget = step.get("reftarget", "").strip()
    if not reftarget or action == "noop":
        return

    step_reqs = list(parent_reqs) + list(step.get("requirements", []))
    on_pages, navmenu = _parse_requirements(step_reqs)

    occurrences.append({
        **guide_meta,
        "action": action,
        "selector": reftarget,
        "selector_type": selector_type(reftarget, action),
        "on_page": on_pages[0] if on_pages else None,
        "requires_navmenu": navmenu,
    })


def _extract_from_block(
    block: dict,
    parent_reqs: list[str],
    occurrences: list,
    guide_meta: dict,
) -> None:
    """Recursively extract selectors from any block type."""
    btype = block.get("type", "")
    block_reqs = list(parent_reqs) + list(block.get("requirements", []))

    if btype == "interactive":
        action = block.get("action", "")
        reftarget = block.get("reftarget", "").strip()
        if reftarget and action != "noop":
            on_pages, navmenu = _parse_requirements(block_reqs)
            occurrences.append({
                **guide_meta,
                "action": action,
                "selector": reftarget,
                "selector_type": selector_type(reftarget, action),
                "on_page": on_pages[0] if on_pages else None,
                "requires_navmenu": navmenu,
            })

    elif btype in ("multistep", "guided"):
        for step in block.get("steps", []):
            _extract_from_step(step, block_reqs, occurrences, guide_meta)

    elif btype == "code-block":
        reftarget = block.get("reftarget", "").strip()
        if reftarget:
            on_pages, navmenu = _parse_requirements(block_reqs)
            occurrences.append({
                **guide_meta,
                "action": "code-block",
                "selector": reftarget,
                "selector_type": "css",
                "on_page": on_pages[0] if on_pages else None,
                "requires_navmenu": navmenu,
            })

    # Recurse into child-bearing block types
    for child in block.get("blocks", []):
        _extract_from_block(child, block_reqs, occurrences, guide_meta)
    for child in block.get("whenTrue", []):
        _extract_from_block(child, block_reqs, occurrences, guide_meta)
    for child in block.get("whenFalse", []):
        _extract_from_block(child, block_reqs, occurrences, guide_meta)


# ---------------------------------------------------------------------------
# Manifest loading
# ---------------------------------------------------------------------------

def load_manifests(root: Path) -> dict[str, dict]:
    """
    Walk the repo and return {guide_dir_name: manifest_dict} for every
    manifest.json found at the top-level of a guide directory.

    Only top-level manifests are indexed (i.e. manifests exactly one directory
    deep from root).  Sub-guide manifests in learning-journey sub-dirs are
    excluded because their content.json files are attributed to the parent LJ.
    """
    manifests: dict[str, dict] = {}
    for mf in root.glob("*/manifest.json"):
        guide_dir = mf.parent.name
        try:
            manifests[guide_dir] = json.loads(mf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return manifests


# ---------------------------------------------------------------------------
# Registry aggregation
# ---------------------------------------------------------------------------

def build_registry(root: Path) -> dict:
    """Scan the repo and return the complete selector registry dict."""

    _SKIP_DIRS = {"shared", "node_modules", ".cursor", ".github", "docs", "pathfinder-app"}

    # Load all top-level manifests once
    manifests = load_manifests(root)

    # Raw occurrences list (one entry per selector usage in a block/step)
    raw: list[dict] = []

    for cf in sorted(root.rglob("content.json")):
        rel = cf.relative_to(root)
        parts = rel.parts

        # Skip internal / tooling directories
        if parts[0] in _SKIP_DIRS:
            continue

        guide_dir = parts[0]  # always the top-level guide directory
        manifest = manifests.get(guide_dir, {})

        try:
            data = json.loads(cf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  ⚠  Skipping {rel}: {exc}", file=sys.stderr)
            continue

        starting_location = manifest.get("startingLocation") or None
        product_area = (
            product_area_from_url(starting_location)
            if starting_location
            else product_area_from_dir(guide_dir)
        )

        guide_meta = {
            "guide_id": manifest.get("id") or guide_dir,
            "guide_title": data.get("title") or guide_dir,
            "guide_type": manifest.get("type") or "guide",
            "guide_dir": guide_dir,
            "file": str(rel),
            "starting_location": starting_location,
            "product_area": product_area,
        }

        for block in data.get("blocks", []):
            _extract_from_block(block, [], raw, guide_meta)

    # Aggregate occurrences by selector value
    by_selector: dict[str, dict] = {}

    for occ in raw:
        sel = occ["selector"]
        if sel not in by_selector:
            by_selector[sel] = {
                "selector": sel,
                "selector_type": occ["selector_type"],
                "testid_namespace": extract_testid_namespace(sel),
                "action_types": set(),
                "product_areas": set(),
                "starting_locations": set(),
                "page_requirements": set(),
                "requires_navmenu": False,
                "usage_count": 0,
                "occurrences": [],
            }

        entry = by_selector[sel]
        entry["action_types"].add(occ["action"])
        entry["product_areas"].add(occ["product_area"])
        if occ["starting_location"]:
            entry["starting_locations"].add(occ["starting_location"])
        if occ["on_page"]:
            entry["page_requirements"].add(occ["on_page"])
        if occ["requires_navmenu"]:
            entry["requires_navmenu"] = True
        entry["usage_count"] += 1

        # Store per-occurrence context (deduplicated by file + action)
        occ_key = (occ["file"], occ["action"], sel)
        existing_keys = {
            (o["file"], o["action"]) for o in entry["occurrences"]
        }
        if (occ["file"], occ["action"]) not in existing_keys:
            entry["occurrences"].append({
                "guide_id": occ["guide_id"],
                "guide_title": occ["guide_title"],
                "guide_type": occ["guide_type"],
                "guide_dir": occ["guide_dir"],
                "file": occ["file"],
                "action": occ["action"],
                "starting_location": occ["starting_location"],
                "product_area": occ["product_area"],
                "on_page": occ["on_page"],
                "requires_navmenu": occ["requires_navmenu"],
            })

    # Convert sets to sorted lists for stable JSON output
    selectors = []
    for entry in by_selector.values():
        entry["action_types"] = sorted(entry["action_types"])
        entry["product_areas"] = sorted(entry["product_areas"])
        entry["starting_locations"] = sorted(entry["starting_locations"])
        entry["page_requirements"] = sorted(entry["page_requirements"])
        entry["occurrences"] = sorted(
            entry["occurrences"], key=lambda o: (o["guide_dir"], o["file"], o["action"])
        )
        selectors.append(entry)

    # Sort: CSS selectors first, then button text, then url_path; within each group by usage desc
    type_order = {"css": 0, "button_text": 1, "url_path": 2}
    selectors.sort(key=lambda s: (type_order.get(s["selector_type"], 9), -s["usage_count"], s["selector"]))

    # Summary stats
    total_usages = sum(s["usage_count"] for s in selectors)
    by_type = defaultdict(int)
    by_area: dict[str, int] = defaultdict(int)
    for s in selectors:
        by_type[s["selector_type"]] += 1
        for area in s["product_areas"]:
            by_area[area] += 1

    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "selector_count": len(selectors),
        "usage_count": total_usages,
        "summary": {
            "by_type": dict(by_type),
            "by_product_area": {
                k: v for k, v in sorted(by_area.items(), key=lambda x: -x[1])
            },
        },
        "selectors": selectors,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build selector-registry.json from guide content.json files."
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="selector-registry.json",
        help="Output path (default: ./selector-registry.json)",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root directory (default: two levels above this script)",
    )
    args = parser.parse_args()

    # Resolve root: default is <repo-root> = parent of .github/
    script_dir = Path(__file__).resolve().parent
    root = Path(args.root).resolve() if args.root else script_dir.parent.parent

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    print(f"Scanning repository at: {root}")
    print(f"Output path:            {output_path}")

    registry = build_registry(root)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    n_sel = registry["selector_count"]
    n_use = registry["usage_count"]
    print(f"\n✅ Wrote {output_path}")
    print(f"   {n_sel:,} unique selectors · {n_use:,} total usages")
    print("\nBreakdown by type:")
    for stype, count in registry["summary"]["by_type"].items():
        print(f"   {stype:<14} {count:>5}")
    print("\nTop product areas:")
    for area, count in list(registry["summary"]["by_product_area"].items())[:10]:
        print(f"   {area:<35} {count:>4} selectors")

    return 0


if __name__ == "__main__":
    sys.exit(main())

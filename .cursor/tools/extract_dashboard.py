#!/usr/bin/env python3
"""
Deterministic dashboard JSON extraction for autogen-guide-dashboard skill.

Reads a Grafana dashboard JSON file and outputs a structured extraction report
as JSON on stdout. Used by Phase 1/2 of the dashboard autogen pipeline.

Usage:
  python extract_dashboard.py dashboard.json
  python extract_dashboard.py {guide_dir}/assets/dashboard-source.json

Output JSON schema:
  metadata           object   -- uid, title, schemaVersion, tags, urlPath
  panels             array    -- per-panel objects with selector, grade, fold, etc.
  variables          array    -- template variables with panel bindings
  rows               array    -- row groupings
  dataSources        array    -- unique data sources and reference counts
  selectorSummary    object   -- { green, yellow, red } counts
  duplicateTitles    array    -- panels sharing the same title
  variableInterpolatedTitles array -- panel titles containing $variable
  untitledPanels     array    -- panels with empty/missing titles
  driftHash          str      -- SHA-256 of panels+variables structure (drift detection)
"""

import json
import sys
import hashlib
import argparse
import re
from pathlib import Path

# Import grade_selector from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from grade_selector import grade_element


def slugify(title: str) -> str:
    """Convert a title to a URL slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def estimate_fold(panel: dict, panels: list) -> str:
    """
    Estimate whether a panel is above or below the fold.

    Uses cumulative height of panels above this panel's gridPos.y.
    A cumulative height >= 8 grid units = below fold.
    The gridPos.y >= 8 shortcut is also applied as a quick check.
    """
    y = panel.get("gridPos", {}).get("y", 0)
    if y >= 8:
        return "below"
    # Also sum heights of panels strictly above this one
    cumulative = sum(
        p.get("gridPos", {}).get("h", 4)
        for p in panels
        if p.get("gridPos", {}).get("y", 0) < y
        and p.get("type") != "row"
    )
    return "below" if cumulative >= 8 else "above"


def extract_variable_refs(text: str) -> list:
    """Find all $variable references in a string."""
    return re.findall(r"\$([a-zA-Z_][a-zA-Z0-9_]*)", text or "")


def count_title_occurrences(title: str, panels: list) -> int:
    """Count how many panels share this exact title."""
    if not title:
        return sum(1 for p in panels if not p.get("title", "").strip())
    return sum(1 for p in panels if p.get("title", "") == title)


def extract_panels(raw_panels: list, all_panels: list) -> list:
    """Extract and grade each panel."""
    result = []
    title_counts: dict = {}
    for p in all_panels:
        t = p.get("title", "").strip()
        title_counts[t] = title_counts.get(t, 0) + 1

    for panel in raw_panels:
        if panel.get("type") == "row":
            continue

        title = panel.get("title", "").strip()
        panel_type = panel.get("type", "")
        grid_pos = panel.get("gridPos", {})
        fold = estimate_fold(panel, all_panels)
        duplicate = title_counts.get(title, 0) > 1
        variable_in_title = bool(title and "$" in title)
        repeat = panel.get("repeat")

        # Grade the selector
        grading = grade_element({
            "panelTitle": title,
            "duplicateTitle": duplicate,
            "variableInTitle": variable_in_title,
            "fold": fold,
        })

        # Extract variable references from targets
        var_refs: set = set()
        for target in panel.get("targets", []):
            for key in ("expr", "query", "rawSql", "rawQuery", "measurement"):
                val = target.get(key, "")
                if val:
                    var_refs.update(extract_variable_refs(str(val)))
        if title:
            var_refs.update(extract_variable_refs(title))
        if repeat:
            var_refs.add(repeat)

        # Data source
        ds = panel.get("datasource")
        if isinstance(ds, str):
            ds_info = {"type": None, "uid": ds}
        elif isinstance(ds, dict):
            ds_info = {"type": ds.get("type"), "uid": ds.get("uid")}
        else:
            ds_info = None

        result.append({
            "title": title,
            "type": panel_type,
            "gridPos": grid_pos,
            "fold": fold,
            "selector": grading["selector"],
            "selectorGrade": grading["grade"],
            "gradeReason": grading["grade_reason"],
            "variables": sorted(var_refs),
            "datasource": ds_info,
            "hasThresholds": bool(
                panel.get("fieldConfig", {})
                    .get("defaults", {})
                    .get("thresholds", {})
                    .get("steps")
            ),
            "transformationCount": len(panel.get("transformations", [])),
            "repeat": repeat,
        })

    return result


def extract_rows(raw_panels: list) -> list:
    """Extract row groupings from explicit row panels."""
    rows = []
    for panel in raw_panels:
        if panel.get("type") == "row":
            rows.append({
                "title": panel.get("title", ""),
                "collapsed": panel.get("collapsed", False),
                "gridPosY": panel.get("gridPos", {}).get("y", 0),
                "panelCount": len(panel.get("panels", [])),
            })
    return sorted(rows, key=lambda r: r["gridPosY"])


def extract_variables(dashboard: dict, extracted_panels: list) -> list:
    """Extract template variables with panel binding info."""
    templating = dashboard.get("templating", {}).get("list", [])
    result = []

    for var in templating:
        name = var.get("name", "")
        label = var.get("label") or name
        ds = var.get("datasource")
        if isinstance(ds, str):
            ds_info = {"type": None, "uid": ds}
        elif isinstance(ds, dict):
            ds_info = {"type": ds.get("type"), "uid": ds.get("uid")}
        else:
            ds_info = None

        # Find which panels reference this variable
        referenced_by = [
            p["title"] for p in extracted_panels
            if name in p.get("variables", [])
        ]

        # Current value
        current = var.get("current", {})
        current_value = current.get("text") or current.get("value")

        result.append({
            "name": name,
            "type": var.get("type", "query"),
            "label": label,
            "datasource": ds_info,
            "hide": var.get("hide", 0),
            "currentValue": current_value,
            "referencedByPanels": referenced_by,
        })

    return result


def extract_data_sources(dashboard: dict, extracted_panels: list) -> list:
    """Collect unique data sources and reference counts."""
    ds_counts: dict = {}

    # From panels
    for panel in extracted_panels:
        ds = panel.get("datasource")
        if ds:
            key = (ds.get("type"), ds.get("uid"))
            ds_counts[key] = ds_counts.get(key, 0) + 1

    # From variables
    for var in dashboard.get("templating", {}).get("list", []):
        ds = var.get("datasource")
        if isinstance(ds, dict):
            key = (ds.get("type"), ds.get("uid"))
            ds_counts[key] = ds_counts.get(key, 0) + 1

    return [
        {"type": k[0], "uid": k[1], "referencedByCount": v}
        for k, v in sorted(ds_counts.items(), key=lambda x: -x[1])
    ]


def compute_drift_hash(dashboard: dict) -> str:
    """
    Compute SHA-256 of the drift-relevant fields.

    Matches the jq expression used in SKILL.md:
      jq -c '{panels: [.panels[] | {title, type, gridPos}], templating: [.templating.list[] | {name, type}]}'
    """
    panels_key = [
        {"title": p.get("title", ""), "type": p.get("type", ""), "gridPos": p.get("gridPos", {})}
        for p in dashboard.get("panels", [])
    ]
    templating_key = [
        {"name": v.get("name", ""), "type": v.get("type", "")}
        for v in dashboard.get("templating", {}).get("list", [])
    ]
    canonical = json.dumps(
        {"panels": panels_key, "templating": templating_key},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


def extract(dashboard_path: str) -> dict:
    """Run the full extraction pipeline and return a structured report dict."""
    with open(dashboard_path) as f:
        dashboard = json.load(f)

    uid = dashboard.get("uid", "")
    title = dashboard.get("title", "")
    schema_version = dashboard.get("schemaVersion", 0)
    tags = dashboard.get("tags", [])

    # Build URL path
    url_slug = slugify(title) if title else "dashboard"
    url_path = f"/d/{uid}/{url_slug}" if uid else f"/d/unknown/{url_slug}"

    metadata = {
        "uid": uid,
        "title": title,
        "schemaVersion": schema_version,
        "tags": tags,
        "urlPath": url_path,
    }

    # Handle both flat panels and legacy rows format
    raw_panels = dashboard.get("panels", [])
    if not raw_panels and "rows" in dashboard:
        # Legacy format: flatten rows into panels
        for row in dashboard["rows"]:
            raw_panels.append({"type": "row", "title": row.get("title", ""), "collapsed": False, "gridPos": {"y": 0}})
            for p in row.get("panels", []):
                raw_panels.append(p)

    extracted_panels = extract_panels(raw_panels, raw_panels)
    rows = extract_rows(raw_panels)
    variables = extract_variables(dashboard, extracted_panels)
    data_sources = extract_data_sources(dashboard, extracted_panels)

    # Selector summary
    selector_summary = {"green": 0, "yellow": 0, "red": 0}
    for p in extracted_panels:
        grade = p.get("selectorGrade", "red")
        selector_summary[grade] = selector_summary.get(grade, 0) + 1

    # Duplicate titles
    title_groups: dict = {}
    for p in extracted_panels:
        t = p["title"]
        if t not in title_groups:
            title_groups[t] = []
        title_groups[t].append(p)
    duplicate_titles = [
        {"title": t, "count": len(ps), "panels": [p["gridPos"] for p in ps]}
        for t, ps in title_groups.items()
        if len(ps) > 1 and t
    ]

    # Variable-interpolated titles
    variable_interpolated = [p["title"] for p in extracted_panels if "$" in p["title"]]

    # Untitled panels
    untitled = [
        {"gridPos": p["gridPos"], "type": p["type"]}
        for p in extracted_panels
        if not p["title"]
    ]

    drift_hash = compute_drift_hash(dashboard)

    return {
        "metadata": metadata,
        "panels": extracted_panels,
        "variables": variables,
        "rows": rows,
        "dataSources": data_sources,
        "selectorSummary": selector_summary,
        "duplicateTitles": duplicate_titles,
        "variableInterpolatedTitles": variable_interpolated,
        "untitledPanels": untitled,
        "driftHash": drift_hash,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from a Grafana dashboard JSON"
    )
    parser.add_argument("dashboard_json", help="Path to dashboard JSON file")
    parser.add_argument(
        "--pretty", action="store_true", default=True,
        help="Pretty-print output (default: true)"
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="Compact output (overrides --pretty)"
    )
    args = parser.parse_args()

    result = extract(args.dashboard_json)

    if args.compact:
        print(json.dumps(result, separators=(",", ":")))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

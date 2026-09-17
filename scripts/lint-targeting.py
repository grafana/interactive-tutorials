#!/usr/bin/env python3
"""Lint manifest.json `targeting.match` expressions for over-broad matching.

The grafana-recommender scores a match expression and returns anything with
accuracy > 0 -- the `matched` boolean is discarded (cmd/recommender/v1recommend.go).
`and` accuracy is the *fraction* of matched children, so an `and` holding any
child that is true regardless of the current page (targetPlatform, tag,
datasource, userRole, cohort) scores > 0 on every page in the tenant and is
returned everywhere. `or` accuracy is binary, so wrapping the `and` in an `or`
keeps the expression at 1.0-or-absent.

Results are sorted by accuracy alone, with no tie-break and a 10-item cap, so a
precise guide cannot outrank a broad one -- it can only tie it. Reducing how many
guides match a page is the only lever an author has.

Run from the repository root:

    python3 scripts/lint-targeting.py            # lint, exit 1 on findings
    python3 scripts/lint-targeting.py --report   # per-page contention report
"""

import json
import sys
from collections import Counter
from pathlib import Path

# Criterion names the engine understands. Anything else is dropped by non-strict
# json.Unmarshal, leaving `{}` -- which evaluates as matched at accuracy 1.0, so a
# typo becomes a free always-true child.
VALID = {
    "and", "or", "urlRegex", "urlPrefix", "urlPrefixIn",
    "datasource", "datasourceIn", "allDatasources", "noDatasources",
    "userRole", "userRoleIn", "tag", "tagIn", "allTags",
    "cohort", "cohortIn", "targetPlatform", "targetPlatformIn",
    "source", "sourceIn",
}

# Order of the `switch` in internal/recommender/rules.go. Only the first matching
# case in an object is evaluated; sibling keys are silently ignored.
ORDER = [
    "and", "or", "urlRegex", "urlPrefix", "urlPrefixIn",
    "datasource", "datasourceIn", "allDatasources", "noDatasources",
    "userRole", "userRoleIn", "tag", "tagIn", "allTags",
    "cohort", "cohortIn", "targetPlatform", "targetPlatformIn", "sourceIn",
]

URL_KEYS = {"urlPrefix", "urlPrefixIn", "urlRegex"}

# `source`/`sourceIn` are hard pre-filters evaluated before scoring, and bare
# `source` has no case in the switch at all, so it neither constrains the URL nor
# costs anything in the score.
SOURCE_KEYS = {"source", "sourceIn"}


def effective_key(node):
    """The one key the engine will actually evaluate for this object."""
    for key in ORDER:
        if key in node and node[key] not in (None, "", [], {}):
            return key
    return None


def children(node):
    for combinator in ("and", "or"):
        for index, child in enumerate(node.get(combinator) or []):
            yield combinator, index, child


def constrains_url(node):
    if not isinstance(node, dict):
        return False
    if any(key in node for key in URL_KEYS):
        return True
    return any(constrains_url(child) for _, _, child in children(node))


def only_source(node):
    """True for a subtree that carries nothing but source pre-filters."""
    if not isinstance(node, dict):
        return False
    keys = set(node) - {"and", "or"}
    if keys and not keys <= SOURCE_KEYS:
        return False
    kids = [child for _, _, child in children(node)]
    if kids:
        return all(only_source(child) for child in kids)
    return bool(keys)


def lint(package, match):
    findings = []

    def walk(node, path):
        if not isinstance(node, dict):
            return

        for key in node:
            if key not in VALID:
                findings.append(
                    f"{path}: unknown criterion {key!r} -- dropped by the engine, "
                    f"leaving an always-true child"
                )

        scored = [key for key in node if key in ORDER]
        if len(scored) > 1:
            findings.append(
                f"{path}: {len(scored)} criteria in one object {scored} -- only "
                f"{effective_key(node)!r} is evaluated; split into and/or children"
            )

        if node.get("urlPrefix") == "/":
            findings.append(f'{path}: urlPrefix "/" matches every page')

        # An `and` whose children are not all page-dependent scores a partial
        # accuracy everywhere. Wrapping it in `or` restores binary scoring.
        if node.get("and"):
            page_dependent = [constrains_url(c) for c in node["and"]]
            if any(page_dependent) and not all(page_dependent):
                unconstrained = [
                    c for c in node["and"]
                    if not constrains_url(c) and not only_source(c)
                ]
                if unconstrained and path == "match":
                    findings.append(
                        f"{path}: root `and` mixes URL and non-URL criteria -- scores a "
                        f"partial accuracy on every page; wrap it in an `or`"
                    )

        # Every branch of an `or` must constrain the URL, otherwise the
        # unconstrained branch is an easy-out that matches every page.
        for index, child in enumerate(node.get("or") or []):
            if not constrains_url(child) and not only_source(child):
                findings.append(
                    f"{path}.or[{index}]: branch has no URL constraint -- matches every page"
                )

        for combinator, index, child in children(node):
            walk(child, f"{path}.{combinator}[{index}]")

    walk(match, "match")

    if not constrains_url(match):
        findings.append("match: no URL constraint anywhere -- the entry is unmatchable")

    return [(package, finding) for finding in findings]


def load_manifests(root):
    manifests = {}
    for path in sorted(root.glob("**/manifest.json")):
        if "node_modules" in path.parts:
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            print(f"  {path}: invalid JSON -- {exc}", file=sys.stderr)
            continue
        match = (data.get("targeting") or {}).get("match")
        if match:
            manifests[str(path.parent.relative_to(root))] = match
    return manifests


# --- contention report -------------------------------------------------------

import re  # noqa: E402  (only needed by the report path)


def evaluate(node, ctx):
    """Mirror of MatchExpr.EvalWithCriteria; returns (matched, accuracy)."""
    if not isinstance(node, dict):
        return True, 1.0
    key = effective_key(node)
    if key == "and":
        results = [evaluate(c, ctx)[0] for c in node["and"]]
        total = len(results)
        return all(results), (sum(results) / total if total else 1.0)
    if key == "or":
        matched = any(evaluate(c, ctx)[0] for c in node["or"])
        return matched, (1.0 if matched else 0.0)
    if key == "urlRegex":
        pattern = node["urlRegex"]
        pattern = pattern if pattern.startswith("^") else "^" + pattern
        try:
            ok = bool(re.search(pattern, ctx["path"], re.I))
        except re.error:
            ok = False
        return ok, (1.0 if ok else 0.0)
    if key == "urlPrefix":
        ok = ctx["path"].startswith(node["urlPrefix"])
        return ok, (1.0 if ok else 0.0)
    if key == "urlPrefixIn":
        ok = any(ctx["path"].startswith(p) for p in node["urlPrefixIn"])
        return ok, (1.0 if ok else 0.0)
    if key == "tag":
        ok = node["tag"] in ctx["tags"]
        return ok, (1.0 if ok else 0.0)
    if key == "targetPlatform":
        ok = node["targetPlatform"] in ("any", ctx["platform"])
        return ok, (1.0 if ok else 0.0)
    if key == "userRole":
        ok = node["userRole"] == ctx["role"]
        return ok, (1.0 if ok else 0.0)
    if key == "datasource":
        ok = node["datasource"] in ctx["datasources"]
        return ok, (1.0 if ok else 0.0)
    # bare `source` and unrecognised leaves: totalCriteria == 0 -> matched at 1.0
    return True, 1.0


def source_patterns(node):
    found = []
    if isinstance(node, dict):
        if "source" in node:
            found.append(node["source"])
        if "sourceIn" in node:
            found.extend(node["sourceIn"])
        for _, _, child in children(node):
            found += source_patterns(child)
    return found


# Representative pages, drawn from grafana-pathfinder-app/product-knowledge/app-states.mdc
PAGES = [
    ("/dashboards", []),
    ("/dashboards", ["panel-type:timeseries"]),
    ("/d/abc123/my-dashboard", []),
    ("/dashboard/new", []),
    ("/playlists", []),
    ("/explore", []),
    ("/drilldown", []),
    ("/connections", []),
    ("/connections/infrastructure", []),
    ("/connections/add-new-connection", []),
    ("/connections/add-new-connection/kafka", []),
    ("/connections/datasources", []),
    ("/connections/datasources", ["selected-datasource:prometheus"]),
    ("/alerting/list", []),
    ("/admin", []),
    ("/admin/provisioning", []),
    ("/a/k6-app", []),
    ("/a/grafana-k8s-app/home", []),
    ("/a/grafana-irm-app/incidents", []),
]

MAX_RECOMMENDATIONS = 10  # DefaultMaxRecommendations in cmd/recommender/main.go


def report(manifests, host="mystack.grafana.net"):
    over_cap = 0
    appearances = Counter()
    print(f"{'page':<46}{'context tags':<32}{'shown':>6}")
    print("-" * 86)
    for path, tags in PAGES:
        ctx = {
            "path": path, "platform": "cloud", "role": "Editor",
            "datasources": ["prometheus", "loki"], "tags": tags,
        }
        shown = []
        for package, match in manifests.items():
            patterns = source_patterns(match)
            if patterns and not any(re.search(p, host, re.I) for p in patterns):
                continue
            if evaluate(match, ctx)[1] > 0:
                shown.append(package)
                appearances[package] += 1
        flag = "  <== OVER CAP" if len(shown) > MAX_RECOMMENDATIONS else ""
        if len(shown) > MAX_RECOMMENDATIONS:
            over_cap += 1
        print(f"{path:<46}{','.join(tags) or '-':<32}{len(shown):>6}{flag}")
    print(f"\npages over the {MAX_RECOMMENDATIONS}-slot cap: {over_cap}")
    print(f"\nguides matching the most of these {len(PAGES)} pages:")
    for package, count in appearances.most_common(10):
        print(f"   {count:>3}  {package}")
    return over_cap


def main():
    root = Path.cwd()
    manifests = load_manifests(root)
    if not manifests:
        print("No manifests with targeting found. Run from the repository root.", file=sys.stderr)
        return 2

    if "--report" in sys.argv:
        over_cap = report(manifests)
        return 1 if over_cap else 0

    findings = []
    for package, match in manifests.items():
        findings += lint(package, match)

    print(f"Linted {len(manifests)} manifests with targeting.")
    if findings:
        print(f"\n{len(findings)} finding(s):\n")
        for package, finding in findings:
            print(f"  {package}\n      {finding}")
        return 1
    print("No findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

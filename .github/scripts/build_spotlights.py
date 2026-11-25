"""Validate team-authored spotlight files and emit the aggregate CDN index."""
import argparse
import json
import posixpath
import re
import unicodedata
import warnings
from datetime import date, datetime, timezone
from pathlib import Path


# Keep aligned with cmd/recommender/spotlights.go in grafana-recommender.
TEST_CATEGORY = "testing"
TEST_PACKAGES = {"json-guide-demo", "e2e-framework-test"}


def validate(item, catalog, members, owners, source):
    if not isinstance(item, dict) or item.keys() - {"path", "additionalPaths", "heading", "guides", "schedule"}:
        raise ValueError("expected a spotlight object with known fields")
    heading = item.get("heading")
    if not isinstance(heading, str) or not 1 <= len(heading) <= 80 or heading != heading.strip() or any(unicodedata.category(c) == "Cc" for c in heading):
        raise ValueError("expected a heading of 1 to 80 characters")
    additional = item.get("additionalPaths", [])
    if not isinstance(additional, list) or len(additional) > 11:
        raise ValueError("expected at most 11 additional paths")
    for target in [item.get("path"), *additional]:
        if not isinstance(target, str) or not target.startswith("/") or len(target.encode()) > 2048 or re.search(r"[?#\\\s]|//", target) or any(unicodedata.category(c) == "Cc" for c in target):
            raise ValueError(f"invalid Grafana pathname {target!r}")
        key = target.rstrip("/") or "/"
        if key != posixpath.normpath(target):
            raise ValueError(f"invalid Grafana pathname {target!r}")
        if key in owners:
            raise ValueError(f"{target} already claimed in {owners[key]}")
        owners[key] = source
    guides = item.get("guides")
    if not isinstance(guides, list) or not 1 <= len(guides) <= 12 or not all(isinstance(g, str) for g in guides) or len(set(guides)) != len(guides):
        raise ValueError("expected 1 to 12 distinct guide or learning path IDs")
    for guide in guides:
        entry = catalog.get(guide, {})
        if entry.get("type") not in {"guide", "journey", "path"} or guide in members or entry.get("category") == TEST_CATEGORY or guide in TEST_PACKAGES:
            raise ValueError(f"{guide!r} is not a standalone guide or learning path")
    window = item.get("schedule", {})
    if not isinstance(window, dict) or window.keys() - {"startDate", "endDate"}:
        raise ValueError("invalid schedule")
    for value in window.values():
        if not isinstance(value, str) or (value and date.fromisoformat(value).isoformat() != value):
            raise ValueError("dates must use YYYY-MM-DD")
    if window.get("endDate") and window["endDate"] < window.get("startDate", ""):
        raise ValueError("end date precedes start date")
    if window.get("endDate") and window["endDate"] < datetime.now(timezone.utc).date().isoformat():
        warnings.warn(f"{source}: expired spotlight on {item['path']} still reserves its pages", stacklevel=2)


def build(directory, catalog):
    members = set()
    path_dirs = set()
    for entry in catalog.values():
        if entry.get("type") in {"journey", "path"}:
            path_dirs.add(Path(entry["path"]))
            members.update(entry.get("milestones", []))
            for track in entry.get("tracks", []):
                members.update(track["guides"])
    for guide, entry in catalog.items():
        if entry.get("type") == "guide" and any(parent in path_dirs for parent in Path(entry["path"]).parents):
            members.add(guide)
    result, owners = [], {}
    for source in sorted(directory.iterdir()):
        if source.suffix != ".json":
            continue
        try:
            items = json.loads(source.read_text())
            if not isinstance(items, list):
                raise ValueError("expected an array of spotlight objects")
            for item in items:
                validate(item, catalog, members, owners, source.name)
                result.append(item)
        except ValueError as err:
            raise ValueError(f"{source}: {err}") from err
    return {"schemaVersion": 1, "spotlights": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("directory", "repository", "output"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    result = build(args.directory, json.loads(args.repository.read_text()))
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")

#!/usr/bin/env python3
"""
Regenerate `shared/snippets/index.json` from the snippet bodies.

The snippet body is the source of truth — the index is derived from it,
so authors only edit one file per snippet and the index never drifts.
Run after adding, renaming, or editing the metadata of any snippet:

    python3 scripts/build-snippets-index.py

The script also validates that every body has the required fields
(`id`, `title`, `description`) and that `id` matches the filename.
"""
from __future__ import annotations

import json
import os
import sys
from collections import OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPPETS_DIR = os.path.join(REPO, "shared", "snippets")
INDEX_FILE = os.path.join(SNIPPETS_DIR, "index.json")

# Fields surfaced in the catalog. `blocks` is deliberately omitted —
# consumers fetch the body when they need the actual content.
METADATA_FIELDS = ("id", "title", "description", "category", "tags", "schemaVersion")

REQUIRED = ("id", "title", "description")


def main() -> int:
    if not os.path.isdir(SNIPPETS_DIR):
        print(f"Snippets directory not found: {SNIPPETS_DIR}", file=sys.stderr)
        return 1

    index: "OrderedDict[str, OrderedDict[str, object]]" = OrderedDict()
    errors: list[str] = []

    filenames = sorted(
        name
        for name in os.listdir(SNIPPETS_DIR)
        if name.endswith(".json") and name != "index.json"
    )

    for filename in filenames:
        path = os.path.join(SNIPPETS_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                body = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{filename}: invalid JSON ({e})")
            continue

        expected_id = filename[:-len(".json")]
        if body.get("id") != expected_id:
            errors.append(f"{filename}: id {body.get('id')!r} does not match filename")
            continue

        missing = [field for field in REQUIRED if not body.get(field)]
        if missing:
            errors.append(f"{filename}: missing required field(s) {missing}")
            continue

        entry: "OrderedDict[str, object]" = OrderedDict()
        for field in METADATA_FIELDS:
            if field in body:
                entry[field] = body[field]
        index[body["id"]] = entry

    if errors:
        print("Snippet index build failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(index)} snippet(s) to {os.path.relpath(INDEX_FILE, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

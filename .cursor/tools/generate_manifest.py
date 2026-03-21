#!/usr/bin/env python3
"""
Generate a Pathfinder package manifest.json from structured metadata input.

Reads metadata JSON from stdin (or --input file), reads content.json to extract
and validate the guide ID, then writes a clean manifest.json.

Fields omitted per manifest-reference.md:
  - repository  (schema default "interactive-tutorials" applies)
  - language    (schema default "en" applies)

Usage:
  python generate_manifest.py < assets/package-metadata.json > manifest.json
  python generate_manifest.py --input assets/package-metadata.json --content content.json --output manifest.json

Input schema (all fields in package-metadata.json):
  contentJsonPath   str        -- path to content.json (relative to guide dir or absolute)
  type              str        -- "guide" | "path"
  description       str        -- short description
  category          str        -- content category (default "general")
  author            object     -- { "team": "...", "name": "..." (optional) }
  startingLocation  str        -- URL path (e.g. "/connections/datasources/edit")
  targeting         object     -- { "match": { ... } }
  testEnvironment   object     -- { "tier": "cloud|local|managed", "instance": "..." (optional) }
  depends           array      -- package IDs (default [])
  recommends        array      -- package IDs (default [])
  suggests          array      -- package IDs (default [])
  provides          array      -- capability tokens (default [])
  milestones        array      -- for type:"path" only

Exit codes:
  0  success
  1  validation error (ID mismatch, missing required fields, bad JSON)
"""

import json
import sys
import argparse
import os


REQUIRED_FIELDS = ["type", "description", "author"]
OMIT_FIELDS = {"repository", "language"}  # schema defaults apply


def load_json(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def build_manifest(meta: dict, content_id: str) -> dict:
    """Build the manifest dict from metadata, inserting the validated ID."""
    manifest = {}

    # ID — always from content.json (source of truth)
    manifest["id"] = content_id

    # Required fields
    manifest["type"] = meta.get("type", "guide")
    manifest["description"] = meta["description"]

    # Author — required
    author = meta.get("author", {})
    if not isinstance(author, dict):
        author = {"team": str(author)}
    manifest["author"] = author

    # Optional fields — only include if present in metadata
    if "category" in meta and meta["category"]:
        manifest["category"] = meta["category"]

    if "startingLocation" in meta and meta["startingLocation"]:
        manifest["startingLocation"] = meta["startingLocation"]

    if "targeting" in meta and meta["targeting"]:
        manifest["targeting"] = meta["targeting"]

    if "testEnvironment" in meta and meta["testEnvironment"]:
        test_env = meta["testEnvironment"]
        # Validate tier
        valid_tiers = {"local", "cloud", "managed"}
        tier = test_env.get("tier", "")
        if tier not in valid_tiers:
            print(
                f"WARNING: testEnvironment.tier '{tier}' is not valid; "
                f"expected one of {valid_tiers}. 'play' is not a tier — "
                f"use tier:'cloud' + instance:'play.grafana.org'.",
                file=sys.stderr,
            )
        manifest["testEnvironment"] = test_env

    # Omit empty dependency arrays
    for field in ("depends", "recommends", "suggests", "provides"):
        if field in meta and meta[field]:
            manifest[field] = meta[field]

    # milestones — only for type: "path"
    if manifest["type"] == "path":
        if "milestones" in meta and meta["milestones"]:
            manifest["milestones"] = meta["milestones"]
        else:
            print(
                "WARNING: type is 'path' but no milestones provided.",
                file=sys.stderr,
            )

    # Explicitly drop omitted fields
    for field in OMIT_FIELDS:
        manifest.pop(field, None)

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Generate manifest.json from package metadata"
    )
    parser.add_argument(
        "--input", "-i",
        help="Path to package-metadata.json (default: stdin)",
        default=None,
    )
    parser.add_argument(
        "--content", "-c",
        help="Path to content.json for ID extraction (default: derived from contentJsonPath in metadata)",
        default=None,
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path for manifest.json (default: stdout)",
        default=None,
    )
    args = parser.parse_args()

    # Load metadata
    if args.input:
        meta = load_json(args.input)
    else:
        raw = sys.stdin.read()
        try:
            meta = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid JSON on stdin: {exc}", file=sys.stderr)
            sys.exit(1)

    # Validate required fields
    missing = [f for f in REQUIRED_FIELDS if f not in meta]
    if missing:
        print(f"ERROR: missing required fields: {missing}", file=sys.stderr)
        sys.exit(1)

    # Determine content.json path
    content_path = args.content
    if not content_path:
        content_path = meta.get("contentJsonPath")
    if not content_path:
        print(
            "ERROR: content.json path not specified. "
            "Provide --content or include 'contentJsonPath' in metadata.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load content.json and extract ID
    content = load_json(content_path)
    content_id = content.get("id")
    if not content_id:
        print(f"ERROR: content.json at {content_path} has no 'id' field.", file=sys.stderr)
        sys.exit(1)

    # Check for ID mismatch if metadata provides an id
    meta_id = meta.get("id")
    if meta_id and meta_id != content_id:
        print(
            f"ERROR: ID mismatch — metadata has '{meta_id}' "
            f"but content.json has '{content_id}'. "
            f"The manifest ID must match content.json.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build manifest
    manifest = build_manifest(meta, content_id)

    # Output
    output_str = json.dumps(manifest, indent=2) + "\n"
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_str)
        print(f"Written: {args.output}", file=sys.stderr)
        print(f"  id: {manifest['id']}", file=sys.stderr)
        print(f"  type: {manifest['type']}", file=sys.stderr)
        print(f"  Fields: {list(manifest.keys())}", file=sys.stderr)
    else:
        print(output_str, end="")


if __name__ == "__main__":
    main()

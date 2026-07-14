#!/usr/bin/env python3
"""Validate Pathfinder learning-path packaging conventions used by Learning Hub.

These checks catch review findings that Pathfinder CLI validate does not cover:

1. Framing packages must not appear in path manifest ``milestones``.
2. The first hands-on milestone must not ``depends`` on a framing package
   (use ``"depends": []``).
3. Path-level and step-level ``website.yaml`` files require a non-empty
   ``description`` (Learning Hub meta / listings).

Framing packages may still exist on disk for the website companion path; they
must simply be omitted from Pathfinder path ``milestones``.

Usage:
  python3 .github/scripts/validate_learning_path_packages.py
  python3 .github/scripts/validate_learning_path_packages.py --path run-first-k6-test-lj
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable


# Directory / short-name patterns for website-only framing milestones.
# Keep in sync with .cursor/skills/review-learning-path/reference-checks.md
#
# Do NOT treat every "understand-*" milestone as framing. Product teach steps
# like understand-alerts / understand-dashboards stay in path milestones.
# Only known concept-intro short names (and shared value/advantages prefixes)
# are framing.
FRAMING_EXACT = frozenset(
    {
        "advantages",
        "business-value",
        "build-mental-model",
        "how-it-works",
        "understand-baselines",
        "understand-value",
        "welcome",
    }
)

FRAMING_PREFIXES = (
    "advantages-",
    "business-value-",
    "build-mental-model-",
    "how-it-works-",
    "value-",
    "value-of-",
    "welcome-",
)


class Finding:
    def __init__(self, path: Path, message: str) -> None:
        self.path = path
        self.message = message

    def format(self) -> str:
        return f"{self.path}: {self.message}"


def path_slug(path_id: str) -> str:
    return path_id[:-3] if path_id.endswith("-lj") else path_id


def milestone_short_name(path_id: str, milestone_id: str) -> str:
    prefix = f"{path_slug(path_id)}-"
    if milestone_id.startswith(prefix):
        return milestone_id[len(prefix) :]
    return milestone_id


def is_framing_short_name(short_name: str) -> bool:
    if short_name in FRAMING_EXACT:
        return True
    return any(short_name.startswith(prefix) for prefix in FRAMING_PREFIXES)


def is_framing_milestone_id(path_id: str, milestone_id: str) -> bool:
    return is_framing_short_name(milestone_short_name(path_id, milestone_id))


def iter_path_packages(root: Path) -> Iterable[Path]:
    for manifest in sorted(root.glob("*-lj/manifest.json")):
        yield manifest.parent


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def top_level_description(text: str) -> str | None:
    """Return the top-level YAML ``description`` value, or None if missing.

    Avoids a PyYAML dependency. Supports single-line and simple folded
    continuations used in Learning Hub website.yaml files.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        value = line[len("description:") :].strip()
        if value in {"|", ">", "|-", ">-", ""}:
            parts: list[str] = []
            if value not in {"|", ">", "|-", ">-", ""}:
                parts.append(value)
            for cont in lines[i + 1 :]:
                if cont.startswith((" ", "\t")):
                    parts.append(cont.strip())
                elif cont.strip() == "":
                    continue
                else:
                    break
            joined = " ".join(parts).strip()
            return joined or None
        return value.strip().strip("\"'")
    return None


def find_guide_dir(path_dir: Path, guide_id: str) -> Path | None:
    for child in path_dir.iterdir():
        if not child.is_dir():
            continue
        manifest = child / "manifest.json"
        if not manifest.is_file():
            continue
        try:
            data = load_json(manifest)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if data.get("id") == guide_id:
            return child
    return None


def validate_path_package(path_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    path_manifest = path_dir / "manifest.json"
    try:
        path_data = load_json(path_manifest)
    except (OSError, ValueError, json.JSONDecodeError) as err:
        return [Finding(path_manifest, f"unable to read path manifest ({err})")]

    if path_data.get("type") != "path":
        return findings

    path_id = path_data.get("id")
    if not isinstance(path_id, str) or not path_id:
        findings.append(Finding(path_manifest, 'path manifest missing string "id"'))
        return findings

    milestones = path_data.get("milestones")
    if not isinstance(milestones, list) or not milestones:
        findings.append(
            Finding(path_manifest, 'path manifest missing non-empty "milestones" array')
        )
        return findings

    for milestone_id in milestones:
        if not isinstance(milestone_id, str):
            findings.append(
                Finding(path_manifest, f"milestone entry must be a string: {milestone_id!r}")
            )
            continue
        if is_framing_milestone_id(path_id, milestone_id):
            short = milestone_short_name(path_id, milestone_id)
            findings.append(
                Finding(
                    path_manifest,
                    f'framing milestone "{milestone_id}" (short name "{short}") must not '
                    f"appear in path milestones — keep the package directory for the website "
                    f"but omit it from Pathfinder milestones",
                )
            )

    first_id = milestones[0]
    if isinstance(first_id, str):
        first_dir = find_guide_dir(path_dir, first_id)
        if first_dir is None:
            findings.append(
                Finding(
                    path_manifest,
                    f'first milestone "{first_id}" has no matching guide directory/manifest',
                )
            )
        else:
            first_manifest = first_dir / "manifest.json"
            try:
                first_data = load_json(first_manifest)
            except (OSError, ValueError, json.JSONDecodeError) as err:
                findings.append(
                    Finding(first_manifest, f"unable to read first hands-on manifest ({err})")
                )
            else:
                depends = first_data.get("depends") or []
                if not isinstance(depends, list):
                    findings.append(
                        Finding(first_manifest, '"depends" must be an array')
                    )
                else:
                    for dep in depends:
                        if isinstance(dep, str) and is_framing_milestone_id(path_id, dep):
                            findings.append(
                                Finding(
                                    first_manifest,
                                    f'first hands-on milestone depends on framing package '
                                    f'"{dep}" — use "depends": []',
                                )
                            )

    website_files: list[Path] = []
    path_website = path_dir / "website.yaml"
    if path_website.is_file():
        website_files.append(path_website)
    for child in sorted(path_dir.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name == "assets":
            continue
        step_website = child / "website.yaml"
        if step_website.is_file():
            website_files.append(step_website)

    for website in website_files:
        try:
            text = website.read_text(encoding="utf-8")
        except OSError as err:
            findings.append(Finding(website, f"unable to read website.yaml ({err})"))
            continue
        description = top_level_description(text)
        if not description:
            findings.append(
                Finding(
                    website,
                    'missing required non-empty top-level "description" '
                    "(Learning Hub meta / listings)",
                )
            )

    return findings


def validate_repo(root: Path, only: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    packages = list(iter_path_packages(root))
    if only:
        packages = [p for p in packages if p.name == only]
        if not packages:
            return [Finding(root / only, "learning path directory not found")]
    for path_dir in packages:
        findings.extend(validate_path_package(path_dir))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate learning-path framing, depends, and website.yaml description fields."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--path",
        dest="only",
        help="Validate a single *-lj package directory name",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    findings = validate_repo(root, only=args.only)
    if not findings:
        scope = args.only or "all *-lj packages"
        print(f"✅ Learning path packaging checks passed ({scope})")
        return 0

    print("❌ Learning path packaging check failures:")
    print("")
    for finding in findings:
        rel = finding.path
        try:
            rel = finding.path.relative_to(root)
        except ValueError:
            pass
        print(f"  - {rel}: {finding.message}")
        print(f"::error file={rel}::{finding.message}")
    print("")
    print(f"{len(findings)} issue(s) found.")
    print(
        "See docs/website-yaml-reference.md and "
        ".cursor/skills/review-learning-path/reference-checks.md (Framing milestones)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

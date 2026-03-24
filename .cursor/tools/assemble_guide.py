#!/usr/bin/env python3
"""
Guide assembly with structural validation for autogen skills.

Assembles a Pathfinder content.json from a guide shell and per-section JSON files,
then validates the assembled guide for structural issues.

Usage:
  # Assemble mode (reads shell + sections, writes content.json)
  python assemble_guide.py --shell guide-shell.json --sections s1.json s2.json ... > content.json
  python assemble_guide.py --shell guide-shell.json --sections s1.json s2.json ... --output {guide_dir}/content.json

  # Validate-only mode (validates an existing content.json)
  python assemble_guide.py --validate-only {guide_dir}/content.json

Exit codes:
  0  success (or success with warnings)
  1  validation errors (blocking issues found)
  2  JSON parse error

Validation checks (exit 1 on failure):
  - JSON parse validity for all inputs
  - Section IDs are unique
  - No multistep singletons (multistep with 1 step = error)
  - No exists-reftarget in requirements
  - Tooltip length <= 250 chars
  - Section bookend check (first block is markdown, last block is markdown)
  - Step count per section (warn if <3 or >10 interactive steps)
  - No noop-only sections (all interactive steps are noop)
"""

import json
import sys
import argparse
from pathlib import Path


def parse_json_file(path: str) -> dict | list:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def parse_json_string(s: str, label: str = "input") -> dict | list:
    try:
        return json.loads(s)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {label}: {exc}", file=sys.stderr)
        sys.exit(2)


def is_interactive(block: dict) -> bool:
    return block.get("type") in ("interactive", "multistep", "guided")


def is_targeting(block: dict) -> bool:
    """True if the block targets a DOM element (has a reftarget or guided steps with reftarget)."""
    if block.get("type") == "interactive":
        return bool(block.get("reftarget")) and block.get("action") != "noop"
    if block.get("type") == "guided":
        return any(step.get("reftarget") for step in block.get("steps", []))
    if block.get("type") == "multistep":
        return any(
            step.get("reftarget") or step.get("action") != "noop"
            for step in block.get("steps", [])
        )
    return False


def is_noop(block: dict) -> bool:
    """True if block is interactive but non-targeting (noop action, no reftarget)."""
    if block.get("type") == "interactive" and block.get("action") == "noop":
        return True
    return False


def validate_guide(guide: dict) -> tuple[list, list]:
    """
    Validate a complete guide dict.

    Returns:
      errors   list[str]  -- blocking issues (exit 1)
      warnings list[str]  -- non-blocking issues (logged but continue)
    """
    errors = []
    warnings = []

    blocks = guide.get("blocks", [])
    seen_section_ids: set = set()

    for i, block in enumerate(blocks):
        block_type = block.get("type")

        # ── Section-level checks ─────────────────────────────────────────────
        if block_type == "section":
            section_id = block.get("id", "")
            section_title = block.get("title", f"(section {i})")

            # Unique section IDs
            if section_id in seen_section_ids:
                errors.append(f"Section '{section_id}': duplicate section ID")
            else:
                seen_section_ids.add(section_id)

            if not section_id:
                errors.append(f"Section at index {i} ('{section_title}'): missing 'id'")

            # Requirements check: no exists-reftarget
            requirements = block.get("requirements", [])
            for req in requirements:
                if isinstance(req, str) and req.startswith("exists-reftarget"):
                    errors.append(
                        f"Section '{section_id}': 'exists-reftarget' in requirements is auto-applied — remove it"
                    )
                elif isinstance(req, dict) and req.get("type") == "exists-reftarget":
                    errors.append(
                        f"Section '{section_id}': 'exists-reftarget' in requirements is auto-applied — remove it"
                    )

            section_blocks = block.get("blocks", [])
            interactive_steps = [b for b in section_blocks if is_interactive(b)]
            targeting_steps = [b for b in interactive_steps if is_targeting(b)]
            noop_steps = [b for b in interactive_steps if is_noop(b)]

            # Section bookends
            non_empty_blocks = [b for b in section_blocks if b.get("type") != "section"]
            if non_empty_blocks:
                if non_empty_blocks[0].get("type") != "markdown":
                    warnings.append(
                        f"Section '{section_id}': first block should be markdown intro (bookend missing)"
                    )
                if non_empty_blocks[-1].get("type") != "markdown":
                    warnings.append(
                        f"Section '{section_id}': last block should be markdown summary (bookend missing)"
                    )

            # Step count
            n_interactive = len(interactive_steps)
            if n_interactive == 0:
                warnings.append(f"Section '{section_id}': no interactive steps (too thin)")
            elif n_interactive < 3:
                warnings.append(f"Section '{section_id}': only {n_interactive} interactive step(s) (aim for 3–8)")
            elif n_interactive > 10:
                warnings.append(
                    f"Section '{section_id}': {n_interactive} interactive steps (consider splitting; aim for ≤10)"
                )

            # Noop-only check
            if interactive_steps and len(noop_steps) == len(interactive_steps):
                errors.append(
                    f"Section '{section_id}': all interactive steps are noop (noop-only section) — "
                    f"merge into adjacent section"
                )

            # Validate blocks within section
            for j, sub_block in enumerate(section_blocks):
                sub_errs, sub_warns = validate_block(sub_block, f"Section '{section_id}', block {j}")
                errors.extend(sub_errs)
                warnings.extend(sub_warns)

        else:
            # Top-level non-section block
            sub_errs, sub_warns = validate_block(block, f"Top-level block {i}")
            errors.extend(sub_errs)
            warnings.extend(sub_warns)

    return errors, warnings


def validate_block(block: dict, location: str) -> tuple[list, list]:
    """Validate an individual block."""
    errors = []
    warnings = []
    block_type = block.get("type")

    # Tooltip length
    tooltip = block.get("tooltip", "")
    if tooltip and len(tooltip) > 250:
        errors.append(
            f"{location}: tooltip exceeds 250 chars ({len(tooltip)} chars): '{tooltip[:60]}...'"
        )

    # Multistep singletons
    if block_type == "multistep":
        steps = block.get("steps", [])
        if len(steps) == 1:
            errors.append(
                f"{location}: multistep with a single step — convert to a plain 'interactive' block"
            )
        if len(steps) == 0:
            errors.append(f"{location}: multistep with no steps")

    # Guided blocks: validate steps
    if block_type == "guided":
        steps = block.get("steps", [])
        if not steps:
            errors.append(f"{location}: guided block with no steps")
        for k, step in enumerate(steps):
            step_tooltip = step.get("tooltip", "")
            if step_tooltip and len(step_tooltip) > 250:
                errors.append(
                    f"{location}, guided step {k}: tooltip exceeds 250 chars"
                )

    # Interactive blocks: check exists-reftarget
    if block_type == "interactive":
        reftarget = block.get("reftarget", "")
        if reftarget and "exists-reftarget" in str(block.get("requirements", [])):
            errors.append(
                f"{location}: 'exists-reftarget' in requirements is auto-applied — remove it"
            )

    return errors, warnings


def assemble(shell: dict, sections: list) -> dict:
    """Assemble a guide from a shell and list of section dicts."""
    guide = dict(shell)
    blocks = list(guide.get("blocks", []))
    for section in sections:
        blocks.append(section)
    guide["blocks"] = blocks
    return guide


def main():
    parser = argparse.ArgumentParser(
        description="Assemble and validate Pathfinder content.json"
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--validate-only", metavar="CONTENT_JSON",
        help="Validate an existing content.json without assembling",
    )
    mode_group.add_argument(
        "--shell",
        help="Path to guide shell JSON (root structure with intro markdown)",
    )

    parser.add_argument(
        "--sections", nargs="*",
        help="Section JSON files to append (in order)",
        default=[],
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path for assembled content.json (default: stdout)",
        default=None,
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors (exit 1 if any warnings)",
    )

    args = parser.parse_args()

    if args.validate_only:
        guide = parse_json_file(args.validate_only)
    else:
        shell = parse_json_file(args.shell)
        section_dicts = [parse_json_file(s) for s in (args.sections or [])]
        guide = assemble(shell, section_dicts)

    errors, warnings = validate_guide(guide)

    # Report
    if warnings:
        print("\nWarnings:", file=sys.stderr)
        for w in warnings:
            print(f"  ⚠  {w}", file=sys.stderr)

    if errors:
        print("\nErrors (blocking):", file=sys.stderr)
        for e in errors:
            print(f"  ✗  {e}", file=sys.stderr)
        print(f"\nValidation failed: {len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        sys.exit(1)

    if args.strict and warnings:
        print(f"\nStrict mode: {len(warnings)} warning(s) treated as errors.", file=sys.stderr)
        sys.exit(1)

    if not args.validate_only:
        output_str = json.dumps(guide, indent=2) + "\n"
        if args.output:
            with open(args.output, "w") as f:
                f.write(output_str)
            print(f"Written: {args.output}", file=sys.stderr)
        else:
            print(output_str, end="")

    section_count = sum(1 for b in guide.get("blocks", []) if b.get("type") == "section")
    print(
        f"Validation passed: {section_count} section(s), {len(warnings)} warning(s).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()

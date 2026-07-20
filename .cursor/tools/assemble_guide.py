#!/usr/bin/env python3
"""
Guide assembly with structural validation for autogen skills.

Assembles a Pathfinder content.json from a guide shell and per-section JSON files,
then validates the assembled guide for structural issues.

Usage:
  # Assemble mode (reads shell + section packages, writes content.json)
  python assemble_guide.py --shell guide-shell.json --sections s1.json s2.json ... > content.json
  python assemble_guide.py --shell guide-shell.json --sections s1.json s2.json ... \\
      --closing closing.json --output {guide_dir}/content.json

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
  - Tooltip length <= 250 chars
  - Section bookends (intro markdown immediately before each section, summary
    immediately after) — missing or misordered bookends are errors
  - Warn if in-section "You'll…" intro looks like a fake step
  - Step count per section (warn if <3 or >10 interactive steps)
  - No noop-only sections (all interactive steps are noop)

Section package format (each --sections file):
  {
    "intro": {"type": "markdown", "content": "..."},
    "section": {"type": "section", "id": "...", ...},
    "summary": {"type": "markdown", "content": "..."}
  }
  Or a JSON array of those three blocks in order.

Shell should contain opening blocks only (guide intro). Pass guide-level
closing via --closing so it lands after every section — never as a trailing
shell block before --sections (that yields intro → closing → sections).
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Optional


def parse_json_file(path: str) -> Any:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def parse_json_string(s: str, label: str = "input") -> Any:
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


def is_markdown_block(block) -> bool:
    return isinstance(block, dict) and block.get("type") == "markdown"


def is_section_block(block) -> bool:
    return isinstance(block, dict) and block.get("type") == "section"


def unpack_section_package(raw, label: str) -> tuple[dict, dict, dict]:
    """
    Normalize a section input into (intro, section, summary) markdown/section blocks.

    Accepts:
      - {"intro": md, "section": section, "summary": md}
      - [md, section, md]
    Rejects bare section objects (those produce intro → sections without bookends).
    """
    if isinstance(raw, list):
        if len(raw) != 3:
            raise ValueError(
                f"{label}: section package array must have exactly 3 blocks "
                f"(intro markdown, section, summary markdown); got {len(raw)}"
            )
        intro, section, summary = raw
    elif isinstance(raw, dict) and "section" in raw:
        intro = raw.get("intro")
        section = raw.get("section")
        summary = raw.get("summary")
    elif is_section_block(raw):
        raise ValueError(
            f"{label}: bare section object is not allowed — wrap as a package with "
            f"intro and summary markdown (rule 14 bookends)"
        )
    else:
        raise ValueError(
            f"{label}: expected section package "
            f'{{"intro", "section", "summary"}} or [intro, section, summary]'
        )

    if not is_markdown_block(intro):
        raise ValueError(f"{label}: intro must be a markdown block")
    if not is_section_block(section):
        raise ValueError(f"{label}: section must be a section block")
    if not is_markdown_block(summary):
        raise ValueError(f"{label}: summary must be a markdown block")

    return intro, section, summary


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

            section_blocks = block.get("blocks", [])
            interactive_steps = [b for b in section_blocks if is_interactive(b)]
            targeting_steps = [b for b in interactive_steps if is_targeting(b)]
            noop_steps = [b for b in interactive_steps if is_noop(b)]
            non_empty_blocks = [b for b in section_blocks if b.get("type") != "section"]

            # In-section "You'll…" intros often number as step 1 in Pathfinder
            if non_empty_blocks and non_empty_blocks[0].get("type") == "markdown":
                intro = (non_empty_blocks[0].get("content") or "").lstrip()
                if intro.startswith(("You'll ", "You will ", "In this section")):
                    warnings.append(
                        f"Section '{section_id}': first in-section markdown looks like an "
                        f"action-preview intro (may number as step 1) — move outside the section"
                    )

            # Outside bookends: markdown immediately before / after this section in parent blocks
            prev_block = blocks[i - 1] if i > 0 else None
            next_block = blocks[i + 1] if i + 1 < len(blocks) else None
            if not prev_block or prev_block.get("type") != "markdown":
                errors.append(
                    f"Section '{section_id}': missing intro markdown immediately before the section "
                    f"(rule 14 bookend)"
                )
            if not next_block or next_block.get("type") != "markdown":
                errors.append(
                    f"Section '{section_id}': missing summary markdown immediately after the section "
                    f"(rule 14 bookend)"
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

    return errors, warnings


def assemble(shell: dict, sections: list, closing: Optional[dict] = None) -> dict:
    """
    Assemble a guide from a shell, section packages, and optional closing markdown.

    Shell blocks are opening content only. Each section package contributes
    intro → section → summary. Closing (if any) is appended last.

    Do not put the guide-level closing summary in the shell before sections —
    that produces intro → closing → sections and breaks bookend ordering.
    """
    guide = dict(shell)
    blocks = list(guide.get("blocks", []))

    for i, raw in enumerate(sections):
        label = f"section[{i}]"
        if isinstance(raw, dict) and raw.get("id"):
            label = f"section '{raw.get('id')}'"
        elif isinstance(raw, dict) and isinstance(raw.get("section"), dict):
            label = f"section '{raw['section'].get('id', i)}'"
        intro, section, summary = unpack_section_package(raw, label)
        blocks.extend([intro, section, summary])

    if closing is not None:
        if not is_markdown_block(closing):
            raise ValueError("closing must be a markdown block")
        blocks.append(closing)

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
        help="Path to guide shell JSON (root structure with opening intro markdown only)",
    )

    parser.add_argument(
        "--sections", nargs="*",
        help="Section package JSON files (intro+section+summary) in order",
        default=[],
    )
    parser.add_argument(
        "--closing",
        help="Optional guide-level closing markdown JSON (appended after all sections)",
        default=None,
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
        closing = parse_json_file(args.closing) if args.closing else None
        try:
            guide = assemble(shell, section_dicts, closing=closing)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

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

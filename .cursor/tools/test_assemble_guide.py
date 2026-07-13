#!/usr/bin/env python3
"""Regression tests for assemble_guide.py bookend ordering and validation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_guide import assemble, unpack_section_package, validate_guide  # noqa: E402

TOOLS = Path(__file__).resolve().parent
ASSEMBLE = TOOLS / "assemble_guide.py"


def _md(content: str) -> dict:
    return {"type": "markdown", "content": content}


def _section(section_id: str, title: Optional[str] = None) -> dict:
    return {
        "type": "section",
        "id": section_id,
        "title": title or section_id.replace("-", " ").title(),
        "blocks": [
            {
                "type": "interactive",
                "action": "button",
                "reftarget": "Next",
                "content": "Click **Next**.",
                "tooltip": "Continue.",
            },
            {
                "type": "interactive",
                "action": "button",
                "reftarget": "Save",
                "content": "Click **Save**.",
                "tooltip": "Persist.",
            },
            {
                "type": "interactive",
                "action": "button",
                "reftarget": "Done",
                "content": "Click **Done**.",
                "tooltip": "Finish.",
            },
        ],
    }


def _pkg(section_id: str) -> dict:
    return {
        "intro": _md(f"In this part you configure {section_id}."),
        "section": _section(section_id),
        "summary": _md(f"You configured {section_id}."),
    }


class TestUnpackAndAssemble(unittest.TestCase):
    def test_assemble_interleaves_bookends_then_closing(self):
        shell = {"title": "Demo", "blocks": [_md("Welcome to the guide.")]}
        closing = _md("You finished the guide.")
        guide = assemble(shell, [_pkg("alpha"), _pkg("beta")], closing=closing)

        types = [b.get("type") for b in guide["blocks"]]
        ids = [b.get("id") for b in guide["blocks"] if b.get("type") == "section"]
        self.assertEqual(
            types,
            [
                "markdown",  # shell opening
                "markdown",
                "section",
                "markdown",
                "markdown",
                "section",
                "markdown",
                "markdown",  # closing
            ],
        )
        self.assertEqual(ids, ["alpha", "beta"])
        self.assertEqual(guide["blocks"][0]["content"], "Welcome to the guide.")
        self.assertEqual(guide["blocks"][-1]["content"], "You finished the guide.")

        errors, _warnings = validate_guide(guide)
        self.assertEqual(errors, [])

    def test_bare_section_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            unpack_section_package(_section("bare"), "section 'bare'")
        self.assertIn("bare section object is not allowed", str(ctx.exception))

    def test_array_package_accepted(self):
        intro, section, summary = unpack_section_package(
            [_md("intro"), _section("arrayed"), _md("summary")],
            "section 'arrayed'",
        )
        self.assertEqual(intro["content"], "intro")
        self.assertEqual(section["id"], "arrayed")
        self.assertEqual(summary["content"], "summary")

    def test_closing_in_shell_then_bare_append_is_the_bug_pattern(self):
        """Reproduce moxious's failure mode: closing in shell + append sections.

        Old assemble() did this and only warned. New assemble refuses bare sections;
        validate_guide treats missing bookends as errors (not warnings).
        """
        buggy = {
            "title": "Bug",
            "blocks": [
                _md("Welcome."),
                _md("Closing summary too early."),
                _section("one"),
                _section("two"),
            ],
        }
        errors, warnings = validate_guide(buggy)
        bookend_errors = [e for e in errors if "bookend" in e]
        # three bookend failures: one missing summary, two missing intro, two's missing summary
        # section one: prev=markdown OK, next=section → missing summary
        # section two: prev=section → missing intro, next=none → missing summary
        self.assertEqual(len(bookend_errors), 3, bookend_errors)
        self.assertFalse(any("bookend" in w for w in warnings))


class TestValidateBookendsAreErrors(unittest.TestCase):
    def test_consecutive_sections_fail(self):
        guide = {
            "title": "X",
            "blocks": [_section("a"), _section("b")],
        }
        errors, _ = validate_guide(guide)
        self.assertGreaterEqual(len([e for e in errors if "bookend" in e]), 3)

    def test_correct_bookends_pass(self):
        guide = assemble({"title": "X", "blocks": []}, [_pkg("a"), _pkg("b")])
        errors, _ = validate_guide(guide)
        self.assertEqual(errors, [])


class TestCliRegression(unittest.TestCase):
    def test_cli_assemble_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shell = {"title": "CLI", "blocks": [_md("Opening.")]}
            closing = _md("All done.")
            (tmp_path / "shell.json").write_text(json.dumps(shell))
            (tmp_path / "s1.json").write_text(json.dumps(_pkg("one")))
            (tmp_path / "s2.json").write_text(json.dumps(_pkg("two")))
            (tmp_path / "closing.json").write_text(json.dumps(closing))
            out = tmp_path / "content.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(ASSEMBLE),
                    "--shell",
                    str(tmp_path / "shell.json"),
                    "--sections",
                    str(tmp_path / "s1.json"),
                    str(tmp_path / "s2.json"),
                    "--closing",
                    str(tmp_path / "closing.json"),
                    "--output",
                    str(out),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            guide = json.loads(out.read_text())
            self.assertEqual(
                [b.get("id") for b in guide["blocks"] if b.get("type") == "section"],
                ["one", "two"],
            )
            self.assertEqual(guide["blocks"][-1]["content"], "All done.")

    def test_cli_validate_only_fails_on_missing_bookends(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bad = {
                "title": "Bad",
                "blocks": [
                    _md("Welcome."),
                    _md("Early closing."),
                    _section("one"),
                    _section("two"),
                ],
            }
            path = tmp_path / "content.json"
            path.write_text(json.dumps(bad))
            result = subprocess.run(
                [sys.executable, str(ASSEMBLE), "--validate-only", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("bookend", result.stderr)


if __name__ == "__main__":
    unittest.main()

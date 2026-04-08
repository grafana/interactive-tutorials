#!/usr/bin/env python3
"""
Regex-based React/TSX component extraction for autogen-guide skill.

Reads one or more TSX/TS source files and outputs a structured JSON report
of all interactive UI components, their props, selectors, and section groupings.

This covers ~80% of Grafana plugin source patterns without requiring a full AST.

Usage:
  python extract_components.py src/ConfigEditor.tsx src/Auth.tsx
  python extract_components.py {source_dir}/**/*.tsx

Output JSON schema:
  entryPoint    str     -- path to the first/primary file analyzed
  files         array   -- per-file extraction results
  selectorSummary object -- { green, yellow, red } counts across all files
  scopeEstimate object  -- { totalComponents, totalFieldSets }
"""

import json
import sys
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from grade_selector import grade_element


# Components that produce interactive guide targets
INTERACTIVE_COMPONENTS = {
    "Field", "InlineField",
    "Input", "SecretInput", "TextArea",
    "Select", "MultiSelect",
    "Switch", "Checkbox",
    "Button",
    "RadioButtonGroup",
    "Alert",
    "ColorPicker",
    "Slider",
    "TagsInput",
    "AsyncSelect",
    "AsyncMultiSelect",
}

FIELDSET_COMPONENTS = {"FieldSet", "InlineFieldRow"}

# Component type → guide action mapping
COMPONENT_GUIDE_TYPE = {
    "Input": "input",
    "SecretInput": "secret",
    "TextArea": "textarea",
    "Select": "select",
    "MultiSelect": "select",
    "AsyncSelect": "select",
    "AsyncMultiSelect": "select",
    "Switch": "switch",
    "Checkbox": "checkbox",
    "Button": "button",
    "RadioButtonGroup": "radio",
    "Alert": "alert",
    "ColorPicker": "colorpicker",
    "Slider": "slider",
    "TagsInput": "input",
    "Field": "wrapper",
    "InlineField": "wrapper",
}


def extract_prop_value(jsx_attrs: str, prop_name: str) -> str | None:
    """
    Extract the value of a JSX prop from a string of JSX attributes.

    Handles: prop="value", prop={'value'}, prop={expr}, prop (boolean shorthand)
    Returns the string value or None if not found.
    """
    # String literal: prop="value" or prop='value'
    m = re.search(
        r'\b' + re.escape(prop_name) + r'\s*=\s*["\']([^"\']*)["\']',
        jsx_attrs
    )
    if m:
        return m.group(1)

    # JSX expression: prop={"value"} or prop={'value'}
    m = re.search(
        r'\b' + re.escape(prop_name) + r"""\s*=\s*\{["']([^"']*)["']\}""",
        jsx_attrs
    )
    if m:
        return m.group(1)

    # Template literal: prop={`value`}
    m = re.search(
        r'\b' + re.escape(prop_name) + r'\s*=\s*\{`([^`]*)`\}',
        jsx_attrs
    )
    if m:
        return m.group(1)

    # Boolean shorthand: prop (no value)
    m = re.search(
        r'(?<![a-zA-Z0-9_-])\b' + re.escape(prop_name) + r'\b(?!\s*=)',
        jsx_attrs
    )
    if m:
        return "true"

    return None


def extract_component_props(tag_content: str) -> dict:
    """Extract all relevant props from a JSX opening tag's attribute string."""
    props = {}
    for prop in ["data-testid", "id", "aria-label", "name", "placeholder",
                 "label", "description", "tooltip", "required", "disabled",
                 "isCollapsible", "onClick", "onChange", "value", "type"]:
        val = extract_prop_value(tag_content, prop)
        if val is not None:
            props[prop] = val
    return props


def detect_conditional(before_text: str) -> dict | None:
    """
    Detect if a component is inside a conditional rendering context
    by examining the lines before it in the file.
    """
    lines = before_text.split("\n")
    # Look at the last 10 lines for conditional patterns
    recent = "\n".join(lines[-10:]) if len(lines) > 10 else before_text

    # Logical AND: {condition && (
    m = re.search(r'\{([^}]+)\s*&&\s*[\(\n]', recent)
    if m:
        return {"type": "logical-and", "condition": m.group(1).strip()}

    # Ternary: condition ? ... : ...
    m = re.search(r'([^{]+)\s*\?\s*[\(\n]', recent)
    if m:
        cond = m.group(1).strip()
        if len(cond) < 80 and not cond.startswith(("//", "*")):
            return {"type": "ternary", "condition": cond}

    # Switch/case
    if re.search(r'\bcase\b', recent):
        m = re.search(r'case\s+["\']?([^"\':\s]+)["\']?', recent)
        if m:
            return {"type": "switch-case", "condition": f"case {m.group(1)}"}

    return None


def find_parent_fieldset(before_text: str, fieldsets: list) -> str | None:
    """Find the most recently opened FieldSet that hasn't been closed yet."""
    # Track FieldSet labels seen before this position
    fs_pattern = re.compile(
        r'<(?:FieldSet|InlineFieldRow)\s[^>]*\blabel\s*=\s*["\']([^"\']+)["\']',
        re.DOTALL
    )
    parent = None
    for m in fs_pattern.finditer(before_text):
        # Check if this FieldSet appears to still be open (not closed)
        text_after_fs = before_text[m.end():]
        closes = text_after_fs.count("</FieldSet>") + text_after_fs.count("</InlineFieldRow>")
        opens = len(re.findall(r'<(?:FieldSet|InlineFieldRow)[\s>]', text_after_fs))
        if closes <= opens:
            parent = m.group(1)
    return parent


def extract_file(file_path: str) -> dict:
    """Extract components, FieldSets, and imports from a single TSX/TS file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        return {"path": file_path, "error": str(e), "components": [], "fieldSets": [], "imports": {}}

    lines = content.split("\n")
    components = []
    fieldsets = []

    # ── Extract imports ──────────────────────────────────────────────────────
    imports = {"local": [], "grafana": [], "external": []}
    import_pattern = re.compile(r"^import\s+.*?from\s+['\"]([^'\"]+)['\"]", re.MULTILINE)
    for m in import_pattern.finditer(content):
        source = m.group(1)
        if source.startswith("."):
            imports["local"].append(source)
        elif source.startswith("@grafana"):
            imports["grafana"].append(source)
        else:
            imports["external"].append(source)

    # ── Extract FieldSets ────────────────────────────────────────────────────
    fieldset_names = "|".join(re.escape(name) for name in FIELDSET_COMPONENTS)
    fs_pattern = re.compile(
        r'<(?:' + fieldset_names + r')\s([^>]*?)(?:/>|>)',
        re.DOTALL
    )
    for m in fs_pattern.finditer(content):
        line_num = content[:m.start()].count("\n") + 1
        attrs = m.group(1)
        label = extract_prop_value(attrs, "label") or ""
        is_collapsible = extract_prop_value(attrs, "isCollapsible") == "true"
        fieldsets.append({
            "label": label,
            "line": line_num,
            "isCollapsible": is_collapsible,
            "componentCount": 0,  # filled in below
        })

    # ── Extract interactive components ───────────────────────────────────────
    # Build a pattern that matches opening tags for interactive components
    component_names = "|".join(re.escape(c) for c in INTERACTIVE_COMPONENTS)
    tag_pattern = re.compile(
        r'<(' + component_names + r')\b([^>]*?)(?:/>|>)',
        re.DOTALL,
    )

    for m in tag_pattern.finditer(content):
        component_name = m.group(1)
        tag_attrs = m.group(2)
        line_num = content[:m.start()].count("\n") + 1

        props = extract_component_props(tag_attrs)
        component_type = COMPONENT_GUIDE_TYPE.get(component_name, "unknown")

        if component_type == "wrapper":
            # Field/InlineField: emit as wrapper context, not a step
            continue

        # Look up enclosing Field wrapper for label/description
        # Find the nearest <Field label="..."> before this position
        before = content[:m.start()]
        field_label_m = re.search(
            r'<(?:Field|InlineField)\s[^>]*\blabel\s*=\s*["\']([^"\']+)["\'](?:[^>]*>)?(?:(?!</(?:Field|InlineField)>).)*$',
            before, re.DOTALL
        )
        if field_label_m and not props.get("label"):
            props["label"] = field_label_m.group(1)

        field_desc_m = re.search(
            r'<(?:Field|InlineField)\s[^>]*\bdescription\s*=\s*["\']([^"\']+)["\'](?:[^>]*>)?(?:(?!</(?:Field|InlineField)>).)*$',
            before, re.DOTALL
        )
        if field_desc_m and not props.get("description"):
            props["description"] = field_desc_m.group(1)

        field_tooltip_m = re.search(
            r'<(?:Field|InlineField)\s[^>]*\btooltip\s*=\s*["\']([^"\']+)["\'](?:[^>]*>)?(?:(?!</(?:Field|InlineField)>).)*$',
            before, re.DOTALL
        )
        if field_tooltip_m and not props.get("tooltip"):
            props["tooltip"] = field_tooltip_m.group(1)

        # Extract button children text when no label prop is available
        button_text = None
        if component_name == "Button":
            button_text = props.get("label")
            if not button_text and content[m.end() - 1] == ">":
                after = content[m.end():]
                close_m = re.search(r'^(.*?)</Button>', after, re.DOTALL)
                if close_m:
                    inner = re.sub(r'<[^>]+>', '', close_m.group(1)).strip()
                    if inner and len(inner) < 60:
                        button_text = inner

        # Grade the selector
        grading = grade_element({
            "data-testid": props.get("data-testid"),
            "id": props.get("id"),
            "aria-label": props.get("aria-label"),
            "name": props.get("name"),
            "button_text": button_text,
            "componentType": component_name,
        })

        # Detect conditional context
        conditional = detect_conditional(before)

        # Find parent FieldSet
        parent_fs = find_parent_fieldset(before, fieldsets)

        components.append({
            "name": component_name,
            "line": line_num,
            "props": props,
            "selector": grading["selector"],
            "selectorGrade": grading["grade"],
            "gradeReason": grading["grade_reason"],
            "componentType": component_name,
            "guideActionType": component_type,
            "parentFieldSet": parent_fs,
            "conditional": conditional,
        })

    # Assign component counts to FieldSets
    for fs in fieldsets:
        fs["componentCount"] = sum(
            1 for c in components
            if c.get("parentFieldSet") == fs["label"]
        )

    return {
        "path": file_path,
        "components": components,
        "fieldSets": fieldsets,
        "imports": imports,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract React/TSX interactive components from source files"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="TSX/TS source file paths to analyze",
    )
    parser.add_argument(
        "--entry", "-e",
        help="Explicit entry point file (default: first file argument)",
        default=None,
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="Compact JSON output",
    )
    args = parser.parse_args()

    entry_point = args.entry or args.files[0]

    file_results = []
    total_components = 0
    total_fieldsets = 0
    selector_summary = {"green": 0, "yellow": 0, "red": 0}

    for file_path in args.files:
        result = extract_file(file_path)
        file_results.append(result)
        total_components += len(result.get("components", []))
        total_fieldsets += len(result.get("fieldSets", []))
        for comp in result.get("components", []):
            grade = comp.get("selectorGrade", "red")
            selector_summary[grade] = selector_summary.get(grade, 0) + 1

    output = {
        "entryPoint": entry_point,
        "files": file_results,
        "selectorSummary": selector_summary,
        "scopeEstimate": {
            "totalComponents": total_components,
            "totalFieldSets": total_fieldsets,
        },
    }

    if args.compact:
        print(json.dumps(output, separators=(",", ":")))
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Shared selector grading utility for autogen skills.

Grades UI element selectors as Green/Yellow/Red and derives the best selector
and recommended guide action.

Usage (standalone):
  echo '{"data-testid": "config-url"}' | python grade_selector.py
  python grade_selector.py --element '{"panelTitle": "CPU Usage", "duplicateTitle": false, "fold": "above"}'

Usage (as module):
  from grade_selector import grade_element
"""

import json
import sys
import argparse
import re


def grade_element(element: dict) -> dict:
    """
    Grade a UI element's best selector and derive recommended guide action.

    Input fields (all optional, use None/null for missing):
      For source-code elements:
        data_testid   str | None   -- data-testid attribute value
        id            str | None   -- id attribute value
        aria_label    str | None   -- aria-label attribute value
        name          str | None   -- name attribute (e.g. "jsonData.url")
        button_text   str | None   -- visible button/link text
        component_type str | None  -- e.g. "Input", "Button", "Select", "Switch", "SecretInput"

      For dashboard panel elements:
        panel_title        str | None   -- panel title field
        duplicate_title    bool        -- true if another panel shares this title
        fold               str         -- "above" | "below" (gridPos.y < 8 = above)
        variable_in_title  bool        -- true if title contains $variable

    Returns:
      grade            str   -- "green" | "yellow" | "red"
      selector         str   -- best CSS selector string
      recommended_action str -- "formfill" | "button" | "highlight" | "noop"
      do_it_allowed    bool  -- whether doIt: true is appropriate
      requires_lazy_render bool -- whether guided+lazyRender is required
      grade_reason     str   -- human-readable explanation
    """
    # Normalize field names (support both camelCase and snake_case keys)
    def get(key, *aliases):
        for k in (key, *aliases):
            if k in element and element[k] is not None:
                return element[k]
        return None

    data_testid = get("data-testid", "data_testid", "dataTestid")
    id_attr = get("id")
    aria_label = get("aria-label", "aria_label", "ariaLabel")
    name = get("name")
    button_text = get("buttonText", "button_text", "buttontext")
    component_type = get("componentType", "component_type", "componenttype") or ""
    panel_title = get("panelTitle", "panel_title", "paneltitle")
    duplicate_title = get("duplicateTitle", "duplicate_title", "duplicatetitle") or False
    variable_in_title = get("variableInTitle", "variable_in_title", "variableintitle") or False
    fold = (get("fold") or "above").lower()

    is_secret = component_type.lower() in ("secretinput", "secret", "password")
    requires_lazy = fold == "below"

    # ── Dashboard panel grading ──────────────────────────────────────────────
    if panel_title is not None:
        if not panel_title or not panel_title.strip():
            # Empty/missing title
            grade = "red"
            selector = "section[data-testid='data-testid Panel header ']:nth-match(1)"
            reason = "No panel title — uses fragile nth-match selector"
            action = "highlight"
            do_it = False
        elif variable_in_title or "$" in panel_title:
            # Variable-interpolated title
            grade = "red"
            safe_title = panel_title
            selector = f"section[data-testid='data-testid Panel header {safe_title}']"
            reason = "Variable-interpolated title — selector depends on current variable value"
            action = "highlight"
            do_it = False
        elif duplicate_title:
            # Duplicate title — Yellow
            grade = "yellow"
            selector = f"section[data-testid='data-testid Panel header {panel_title}']:nth-match(1)"
            reason = "Duplicate panel title — nth-match or row-scoped selector required"
            action = "highlight"
            do_it = False
        else:
            # Unique title — Green
            grade = "green"
            selector = f"section[data-testid='data-testid Panel header {panel_title}']"
            reason = "Unique panel title — stable data-testid selector"
            action = "highlight"
            do_it = False  # Dashboard panels are view-only by default

        return {
            "grade": grade,
            "selector": selector,
            "recommended_action": action,
            "do_it_allowed": do_it,
            "requires_lazy_render": requires_lazy,
            "grade_reason": reason,
        }

    # ── Source-code element grading ──────────────────────────────────────────

    # Green: data-testid or id
    if data_testid:
        selector = f"[data-testid='{data_testid}']"
        if is_secret:
            action = "highlight"
            do_it = False
            reason = f"Green (data-testid) but secret — doIt: false required"
        elif component_type.lower() in ("button",):
            action = "button"
            do_it = True
            reason = "Green — data-testid on button"
        elif component_type.lower() in ("input", "textarea"):
            action = "formfill"
            do_it = True
            reason = "Green — data-testid on input; formfill supported"
        elif component_type.lower() in ("select", "switch", "radiobuttongroup", "checkbox", "slider"):
            action = "highlight"
            do_it = False
            reason = "Green — data-testid but non-text input; highlight with doIt:false"
        else:
            action = "highlight"
            do_it = True
            reason = "Green — data-testid"
        return {
            "grade": "green",
            "selector": selector,
            "recommended_action": action,
            "do_it_allowed": do_it,
            "requires_lazy_render": False,
            "grade_reason": reason,
        }

    if id_attr:
        selector = f"#{id_attr}"
        if is_secret:
            action = "highlight"
            do_it = False
            reason = "Green (id) but secret — doIt: false required"
        elif component_type.lower() == "button":
            action = "button"
            do_it = True
            reason = "Green — id on button"
        else:
            action = "formfill" if component_type.lower() in ("input", "textarea") else "highlight"
            do_it = not is_secret
            reason = "Green — id attribute"
        return {
            "grade": "green",
            "selector": selector,
            "recommended_action": action,
            "do_it_allowed": do_it,
            "requires_lazy_render": False,
            "grade_reason": reason,
        }

    # Yellow: aria-label, name, or button text
    if component_type.lower() == "button" and button_text:
        selector = button_text  # Guide system matches button text natively
        return {
            "grade": "yellow",
            "selector": selector,
            "recommended_action": "button",
            "do_it_allowed": True,
            "requires_lazy_render": False,
            "grade_reason": "Yellow — button text matching; no data-testid",
        }

    if aria_label:
        selector = f"[aria-label='{aria_label}']"
        if is_secret:
            action, do_it = "highlight", False
            reason = "Yellow (aria-label) but secret — doIt: false required"
        else:
            action = "formfill" if component_type.lower() in ("input", "textarea") else "highlight"
            do_it = not is_secret
            reason = "Yellow — aria-label"
        return {
            "grade": "yellow",
            "selector": selector,
            "recommended_action": action,
            "do_it_allowed": do_it,
            "requires_lazy_render": False,
            "grade_reason": reason,
        }

    if name:
        selector = f"[name='{name}']"
        if is_secret:
            action, do_it = "highlight", False
            reason = "Yellow (name attr) but secret — doIt: false required"
        else:
            action = "formfill" if component_type.lower() in ("input", "textarea") else "highlight"
            do_it = not is_secret
            reason = "Yellow — name attribute"
        return {
            "grade": "yellow",
            "selector": selector,
            "recommended_action": action,
            "do_it_allowed": do_it,
            "requires_lazy_render": False,
            "grade_reason": reason,
        }

    if button_text:
        # Non-button component with visible text fallback
        selector = f":contains('{button_text}')"
        return {
            "grade": "yellow",
            "selector": selector,
            "recommended_action": "highlight",
            "do_it_allowed": False,
            "requires_lazy_render": False,
            "grade_reason": "Yellow — visible text only; fragile if text is not unique",
        }

    # Red: no stable attribute
    selector = "/* no stable selector — use structural fallback */"
    return {
        "grade": "red",
        "selector": selector,
        "recommended_action": "noop" if not component_type else "highlight",
        "do_it_allowed": False,
        "requires_lazy_render": False,
        "grade_reason": "Red — no data-testid, id, aria-label, name, or stable text",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Grade a UI element selector as Green/Yellow/Red"
    )
    parser.add_argument(
        "--element", "-e",
        help="JSON string describing the element (default: read from stdin)",
        default=None,
    )
    args = parser.parse_args()

    if args.element:
        raw = args.element
    else:
        raw = sys.stdin.read()

    try:
        element = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON input: {exc}", file=sys.stderr)
        sys.exit(1)

    result = grade_element(element)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

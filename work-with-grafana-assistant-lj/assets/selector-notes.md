# Selector notes - work-with-grafana-assistant-lj

Same Assistant chat patterns as `get-started-grafana-assistant-lj`.

| Element | Selector | Notes |
| --- | --- | --- |
| Open Assistant toolbar | `div[data-testid='data-testid Nav toolbar'] button[data-testid='extension-toolbar-button-open']` | skippable when open |
| Prompt input | `[data-testid='grafana-assistant-chat'] [data-testid='prompt-input-body'] [role='textbox'][contenteditable='true']` | TipTap; use `highlight` + `doIt: false` |
| Send | `[data-testid='grafana-assistant-chat'] button[aria-label='Send message']` | |

Avoid lone `` `@` `` in prose (Pathfinder layout break). Use "at-mention" / "at symbol (@)".

# Selector notes - get-started-grafana-assistant-lj

Live DOM checks on `learn.grafana.net` (2026-08-04).

| Element | Selector | Notes |
| --- | --- | --- |
| Plugins search | `div[data-testid='input-wrapper'] input[placeholder='Search Grafana plugins']` | exists |
| Assistant plugin card | `a[href^='/plugins/grafana-assistant-app']` | exists after search |
| Enable checkbox | `input[type='checkbox']` (skippable) | missing when Assistant already enabled |
| Save | button text `Save` (skippable) | missing when already enabled |
| Open Assistant toolbar | `div[data-testid='data-testid Nav toolbar'] button[data-testid='extension-toolbar-button-open']` | exists |
| Chat panel | `[data-testid='grafana-assistant-chat']` | scope chat controls here (homepage has a second prompt) |
| Prompt input | `[data-testid='grafana-assistant-chat'] [data-testid='prompt-input-body'] [role='textbox'][contenteditable='true']` | TipTap contenteditable. Pathfinder `formfill` cannot fill it (sets `textContent` without editor events). Guides use `highlight` + `doIt: false` and ask the learner to paste. |
| Send | `[data-testid='grafana-assistant-chat'] button[aria-label='Send message']` | exists |
| Mode pill | `[data-testid='grafana-assistant-chat'] [data-testid='pde-lab-mode-selector-pill']` | label shows current mode |
| Learn menu item | `[role='menuitem']:contains('Learn')` | no dedicated testid yet |
| Assistant menu item | `[role='menuitem']:text('Assistant')` | switch back from Learn |

AI reply review / lesson pick stay `noop` (non-deterministic). Mention picker has no durable listbox testid; steps use `highlight` + `doIt: false` on the prompt.

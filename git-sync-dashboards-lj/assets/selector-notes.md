# Selector notes — git-sync-dashboards-lj

## Status

Discovered on a personal Grafana Cloud stack (2026-07-10) with Git Sync connected to a test repository.

## Confirmed selectors (new dashboard save drawer)

New dashboards from `/dashboard/new` open the **standard** Save dashboard drawer first (Title / Description / Folder). Git Sync fields appear after you select a provisioned folder.

| UI element | Selector | Notes |
| --- | --- | --- |
| Save (toolbar) | `button[data-testid='data-testid Save dashboard button']` | Label shows **Save** |
| Title (standard drawer) | `input[aria-label='Save dashboard title field']` | Not `#dashboard-title` on first save |
| Description (standard drawer) | `textarea[aria-label='Save dashboard description field']` | Not `#dashboard-description` on first save |
| Folder | Folder picker in drawer | Select provisioned folder (shows **Provisioned** label) |
| Title (provisioned form) | `#dashboard-title` | After folder is provisioned / existing synced dashboards |
| Description (provisioned form) | `#dashboard-description` | After folder is provisioned / existing synced dashboards |
| Branch | `#provisioned-ref` | Combobox; `main` = direct commit; new name = PR path |
| Repository folder | `#folder-path` | Optional subdirectory |
| Filename | `#dashboard-filename` | e.g. `http-monitoring.json` |
| Comment | `#provisioned-resource-form-comment` | Also `textarea[name='comment']` |
| Changes tab | `button[data-testid='data-testid Tab Changes']` | Review before setting Branch. Switching Changes → Details can reset Branch to `main`. |
| Details tab | `button[data-testid='data-testid Tab Details']` | Save lives here; stay on Details after setting Branch |
| Save (drawer) | `button[type='submit']` | Prefer over button text `Save` (ambiguous with toolbar). Click immediately after Branch is set — no tab switch. |
| Open PR | button text `Open pull request in GitHub` | Appears on Git Sync **preview** page after save to a non-default branch (`/dashboard/provisioning/.../preview/...`). Not a drawer alert. If still on normal dashboard edit with no banner, the save used the configured branch (e.g. `main`). |

## Create dashboard (new editor)

| UI element | Selector |
| --- | --- |
| Dashboards nav | `a[data-testid='data-testid Nav menu item'][href='/dashboards']` |
| New dashboard | navigate `/dashboard/new` or `a[role='menuitem'][href='/dashboard/new']` |
| Add panel | `[data-testid='data-testid sidebar add new panel']` |
| Edit visualization | `[data-testid='data-testid edit pane configure panel button']` |

## Pathfinder dock / undock bookends

- `create-new-dashboard` ends with `popout` → `sidebar` so the next milestone starts docked.
- Save milestones (`save-dashboard-git`, `save-with-commit`, `save-with-pr`) start with dock → then undock to `floating` for the save drawer, and dock again at the end.
- Popout steps are behind `renderer:pathfinder` conditionals (hidden in plain markdown viewers).

## UI drift vs original learning path markdown

Original LP described **Workflow** radios (**Push to main** / **Push to a new branch**) and a single **Path** field.

Live UI (and current docs) use:

- **Target folder**
- **Branch**
- **Repository folder**
- **Filename**
- **Comment**

Guides were updated to match the live UI. Enter `main` for direct commits; enter a new branch name for the PR workflow.

## Provisioned folder

- Browse row pattern: `data-testid browse dashboards row <folder-title>`
- Folder URL pattern: `/dashboards/f/repository-<id>/`

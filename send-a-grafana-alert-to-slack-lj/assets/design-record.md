# Design record: Send a Grafana alert to Slack

Built 2026-10-28 from the approved outline of the Grafana Learn journey "Send Grafana alerts to Slack" (docs-ai `journeys/alerting-slack-notifications/outline/outline.md`, section "Learning Paths / Needed"). The journey's slides 10, 16, 23, and 32 embed milestones 1 to 4.

## Plan that was built

| Milestone | Package | Interactive | Ends when |
| --- | --- | --- | --- |
| 1. Get your Slack credential | `get-your-slack-credential/` | No (happens on api.slack.com and in Slack) | A bot token and channel ID, or a Slack incoming webhook URL, are copied |
| 2. Create and test the contact point | `create-and-test-the-contact-point/` | Yes | The test message is in the channel and the contact point is saved |
| 3. Make a real alert arrive | `make-a-real-alert-arrive/` | Yes | A firing notification from the learner's rule is in the channel |
| 4. Shape the message | `shape-the-message/` | Yes | A notification with the pasted title and body is in the channel, every value filled |
| Conclusion | `end-journey/` | No | Cleanup of the practice rule |

UI labels follow the journey's jargon inventory (`outline/reference/jargon-inventory.md`, "UI elements"): **+ New contact point**, **Name**, **Integration**, **Recipient**, **Token**, **Webhook URL**, **Optional Slack settings**, **Test** then **Send test notification**, **Save contact point**, **Configure notifications** with the **Advanced options** switch and the **Contact point** picker, **Save**, **Notification policies** tab, **+ Add route** on the **Default policy**, **Matching labels**, **Add route**, **Title** and **Text Body**, **Edit Title** / **Edit Text Body**, **Enter custom title** / **Enter custom text body**, **Custom template value**, **Templates** tab, **+ New notification template**, **Template group name**, **Template group**, **Payload**, **Edit payload**, **Use existing alert instances**, **Select alert instances**, **Add alert data to payload**, **Preview**.

## Decisions the outline left to the path

**Which rule fires on demand (milestone 3).** The path reuses the prerequisite path's rule, **QuickPizza server errors** from `alerting-first-rule-lj`: `sum(increase(quickpizza_server_http_requests_total{status=~"5.."}[5m]))`, condition **Is above** `0`, evaluation every 1m, pending period 1m, keep firing for 0s, on `grafanacloud-play-prom`. Whether it fires with its real condition depends on whether QuickPizza is returning 5xx at that moment, so the path gives the learner two switches:

- To make the rule fire: change the **status** label filter value from `5..` to `2..`. Successful responses flow constantly, so the count is above 0 and the rule fires after the pending period. Done once, in milestone 3.
- To resolve and re-fire (milestone 4 needs a state change so a notification with the new template is sent; a firing alert that stays firing only re-notifies at **Repeat interval**, 4 hours): set the **Is above** value to `1000000000` (resolves) and back to `0` (fires). Both are the same input (`data-testid alert-rule threshold-input`), so they can be automated with `formfill`.
- Cleanup, on the conclusion page: restore `5..` and `0`.

The alternative, a small rule against a TestData data source, was not chosen because the journey's reader arrives from Introduction to Grafana Alerting with this rule already saved.

**Route taught interactively.** Selecting the contact point on the rule is the automated path. The one-child-policy route is a markdown checklist in the same milestone, because a learner picks one of the two and automating both would conflict.

**Where the preview happens (milestone 4).** The title and body are pasted as custom messages on the contact point (the drawer's **Enter custom title** / **Enter custom text body**), following slide 26 and 32. The preview against a real alert instance uses the **Templates** tab editor, because that is where **Use existing alert instances** lives; the learner can close the form without saving.

**Prerequisites stated on the path cover page.** Own Slack workspace or a Workspace Owner who approves the install; a Grafana-managed rule that can be made to fire; the Grafana Alertmanager.

## Source docs pages the path was built from

- /docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/configure-slack/
- /docs/grafana/latest/alerting/configure-notifications/manage-contact-points/
- /docs/grafana/latest/alerting/fundamentals/notifications/
- /docs/grafana/latest/alerting/fundamentals/notifications/contact-points/
- /docs/grafana/latest/alerting/alerting-rules/create-grafana-managed-rule/
- /docs/grafana/latest/alerting/configure-notifications/create-notification-policy/
- /docs/grafana/latest/alerting/fundamentals/notifications/notification-policies/
- /docs/grafana/latest/alerting/configure-notifications/template-notifications/
- /docs/grafana/latest/alerting/configure-notifications/template-notifications/manage-notification-templates/
- /docs/grafana/latest/alerting/configure-notifications/template-notifications/examples/
- /docs/grafana/latest/alerting/alerting-rules/templates/reference/
- /docs/grafana/latest/alerting/configure-notifications/template-notifications/images-in-notifications/

Slack pages (not tracked by the freshness check): https://docs.slack.dev/app-management/quickstart-app-settings/ , https://api.slack.com/scopes/chat:write.public , https://api.slack.com/authentication/token-types , https://api.slack.com/messaging/webhooks#create_a_webhook , https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace

Re-check the path when any page above changes: `python3 skills/learning/create-learning-journey/scripts/check-path-freshness.py <this file>` from the docs-ai repo; reset the baseline with `--record` after re-checking.

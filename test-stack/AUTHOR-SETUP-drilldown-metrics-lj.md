# Author setup: test drilldown-metrics-lj on the shared stack

Audience: a docs writer who wants to run `drilldown-metrics-lj` end to end on `https://docsteam.grafana.net/`.

Status: written from the pilot logs, not yet followed by a writer. Anywhere a writer gets stuck is a finding, so note it. Steps marked **[needs a person with access]** cannot be done by a writer alone today.

You need about 15 minutes after the one-time setup. Run the reseed (step 3) right before every test, because the data goes stale.

## One-time setup

### 1. Get the access you need

- Edit access to `docsteam.grafana.net` (to save and delete a test dashboard).
- Python 3 and a checkout of this repository.
- A token that can write metrics to the stack's Prometheus. **[needs a person with access]** Someone with Grafana Cloud portal rights creates an access policy for this stack with the `metrics:write` scope only, and a token with a short expiry (the pilot used 7 days). Ask for the token privately; do not paste it in chat or commit it.

### 2. Save the credentials outside the repository

The scripts read `~/.config/grafana-docsteam-metrics.env`. This command prompts for the token without echoing it or saving it in shell history:

```bash
mkdir -p ~/.config && umask 077
read -rs "METRICS_TOKEN?Paste token: " && echo
printf 'METRICS_USER=3694997\nMETRICS_TOKEN=%s\n' "$METRICS_TOKEN" > ~/.config/grafana-docsteam-metrics.env
unset METRICS_TOKEN
```

`3694997` is the stack's Prometheus instance id. It is not a secret.

## Each test run

### 3. Reseed the metrics

Both scripts do a dry run by default. Check the output looks sensible, then add `--send`.

```bash
python3 test-stack/scripts/seed-metrics.py --send
python3 test-stack/scripts/seed-remote-write.py --send
```

Expected: `seed-metrics.py` prints `sent chunk 1 -> 204`. `seed-remote-write.py` prints `sent -> 200`. Any other number means the write failed; see "Where you may get stuck".

### 4. Check the data arrived

1. In `docsteam.grafana.net`, open **Explore** and pick the data source `grafanacloud-docsteam-prom` (its uid is `grafanacloud-prom`).
2. Run `up{job="node"}`. Expect 6 series.
3. Run `asserts:resource:threshold`. Expect 4 series.

If either returns nothing, go back to step 3.

### 5. Start from a clean progress state

Pathfinder saves progress per user. If you have run the path before, its milestones show as complete.

1. Open `https://docsteam.grafana.net/a/grafana-metricsdrilldown-app/drilldown`.
2. Open the Pathfinder panel and find "Explore data using Metrics Drilldown".
3. Use **Redo** on each completed milestone, or **Reset section**, until the path starts at milestone 1.

### 6. Run the path

Follow the guide as a learner would. The pilot notes list what to expect at each milestone:

| Milestone | Expect |
|---|---|
| 1. Search and filter metrics | Step 1 may say the nav menu must be docked. Use **Fix this**. |
| 2. Investigate the data | Step 2 highlights the Select button for `asserts:resource:threshold`. Click Select yourself, or steps 5 and 6 will say the target element is not visible. |
| 3. Open in Explore | Explore opens in a new tab. Switch to it. |
| 4. Add to dashboard | Ends at the Save dialog for a new dashboard. |
| 5. End journey | Closing text. |

Write down every place the guide and the stack disagree. The known issues are in [drilldown-metrics-lj-notes.md](drilldown-metrics-lj-notes.md#issues-to-address-drilldown-metrics-lj-passes-end-to-end-but-these-should-be-looked-at).

### 7. Clean up (every run)

The shared stack is used by others, so leave it as you found it.

1. If you saved the dashboard in milestone 4, open **Dashboards**, search for `New dashboard`, and delete it. Delete only what you created.
2. Reset your Pathfinder progress (step 5) if you want the next run to start fresh.
3. Nothing else needs deleting. Seeded metrics cannot be removed and age out on their own.

## Where you may get stuck

These are the places I expect a writer to need help. They are guesses until a writer tries.

- **No token.** Step 1 depends on someone with Cloud portal access. There is no self-service route today.
- **Token expiry.** The pilot token lasts 7 days. After that, step 3 fails with an authentication error (HTTP 401 or 403) and someone must issue a new one.
- **Stale data.** Samples are only queryable for a short window after writing. If Metrics Drilldown shows no metrics, reseed.
- **Python on your machine.** The commands assume macOS or Linux with `python3`. Windows is untested.
- **Duplicate saved dashboards.** A previous tester's `New dashboard` may still be on the stack. Delete only your own.
- **Explore in a new tab.** Milestone 3 opens a new tab. If your browser blocks pop-ups, allow them for the stack.

## When you are done

- Tell the stack owner so the token can be revoked when the pilot ends.
- Report what was confusing in this document, not only in the guide.

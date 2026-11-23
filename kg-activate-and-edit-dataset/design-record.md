# Design record: Activate the knowledge graph and edit a dataset

Package id: `kg-activate-and-edit-dataset`

Built 2026-10-28 from the approved outline for the Grafana Learn journey "Connect your full stack with the knowledge graph". The outline specifies one interactive guide, embedded on slide 11 with `{{< interactive-guide package_id="kg-activate-and-edit-dataset" >}}`. It is not a multi-milestone learning path.

## Plan that was built

The guide follows procedure 1 steps 1 to 5 (activate) and procedure 5 steps 1 to 9 (edit the Kubernetes Monitoring dataset), plus the journey's check that environment and region values show in the Entity catalog.

Sections, in order:

1. Open **Observability** > **Entity catalog** and click **Get started**.
2. Choose **Kubernetes** or **Applications** (or both), confirm with **Activate** when a dialog opens, and click **Build knowledge graph**.
3. Return to the Entity catalog and check that entities are listed.
4. Open **Observability** > **Configuration** > **Connect knowledge graph** and click **Edit** next to Kubernetes Monitoring.
5. Complete **Environment label**, **Environments**, **Cloud region label**, and **Cloud regions**, then click **Save Kubernetes settings**. **+ Add filter** is optional.
6. Return to the Entity catalog and check the environment and region on a row.

Activation steps require Admin and are skippable when **Get started** is absent because the catalog already lists entities. Kubernetes dataset steps are skippable when the Kubernetes Monitoring row has no **Edit**. There is no Application Observability dataset branch.

## Source docs pages

- /docs/grafana-cloud/platform/knowledge-graph/get-started/
- /docs/grafana-cloud/platform/knowledge-graph/get-started/manage-datasets/
- /docs/grafana-cloud/platform/knowledge-graph/get-started/manage-datasets/kubernetes/

UI labels in the guide follow `journeys/get-started-knowledge-graph/outline/reference/jargon-inventory.md` (UI elements).

## Notes for the next check

The activation page in the product (asserts app, `HomeLanding`) shows **Kubernetes**, **Applications**, and sometimes **Hosts**. It does not show a **Multiple datasets** control. Choosing more than one product is how a learner covers several datasets. The **Build knowledge graph** control on the get-started page opens **Configuration**. The **Build knowledge graph** control on **Configuration** (`kg-actions-build-btn`) runs the build, and its label becomes **Knowledge graph built** or **Building knowledge graph** while that work is underway. The docs say several datasets build on their own; that step is skippable for that case.

**Cloud region label**, **Cloud regions**, and **+ Add filter** sit inside **Advanced settings** on the Kubernetes form. The visible filter control text is "Add filter".

The **Edit** link for Kubernetes Monitoring points at `/a/grafana-asserts-app/configuration/connect-env/kubernetes`.

Selectors come from the asserts app source and from selectors already used by `knowledge-graph-guide`. On 2026-10-29 the author ran the guide in the Block Editor on learn.grafana.net and reported pass.

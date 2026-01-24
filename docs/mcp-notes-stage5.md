# Stage 5 Notes (Widget Assumptions)

The Stage 5 widget list was not explicitly defined in `docs/mcp-scope.md`, so the
implementation assumes the smallest possible set of widgets that map directly to the
existing incident/runbook tool surface:

- Incident list widget (invoked via `incident_list_widget`)
- Incident detail widget (invoked via `incident_detail_widget`)
- Runbook list widget (invoked via `runbook_list_widget`)
- Runbook detail widget (invoked via `runbook_detail_widget`)

Each widget maps to its corresponding backend read-only operation and follows the
tool/resource metadata contract required for ChatGPT App rendering.

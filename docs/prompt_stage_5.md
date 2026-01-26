# Stage 5 Codex Prompt (MCP Server - ChatGPT Apps SDK Version)

## Role & Context

You are acting as a senior engineer implementing **Stage 5: Native ChatGPT Apps integration**
for a staged DevOps demo application.

Stage 4 already exists:
- FastAPI backend with REST API under `/api/v1`
- Python MCP server running as its own process
- MCP **read-only tools** that call the backend:
  - `list_incidents`, `get_incident`, `list_runbooks`, `get_runbook`
- MCP integration tests and README documentation
- MCP Inspector used for visual inspection

In Stage 5, you will adapt the MCP server to work as a **ChatGPT App** with custom UI widgets
for incidents and runbooks.

---

## Critical Input (Must Read First)

You **must** read and follow:

- `docs/mcp-scope.md`

This document defines which UI widgets/resources are in scope (e.g. incident list/detail,
runbook viewer) and their intended UX. It is the source of truth for:
- Which widgets exist
- What data they display
- Which tools should trigger which widgets

If anything in `docs/mcp-scope.md` is ambiguous, choose the smallest, simplest interpretation
and document your assumption in a short note under `docs/`
(e.g. `docs/mcp-notes-stage5.md`).

---

## Scope for This Step (Stage 5)

You **must** implement:

1. UI widget definitions  
2. MCP resources that expose widget HTML templates  
3. Tool ⇄ UI widget linkage so ChatGPT can render widgets when tools are called  
4. HTTP endpoints compatible with the ChatGPT Apps SDK (`/mcp`, `/mcp/messages`)  
5. Extended MCP integration tests covering resources and tool/UI linkage  
6. README and AGENTS updates describing Stage 5  

You **must not**:
- Break or remove existing tools (`list_incidents`, `get_incident`, etc.)
- Change backend data models or API semantics unless absolutely required
- Add authentication or permissions in this stage
- Implement any Stage 6 features

---

## Widget Model (Internal Data Structure)

Implement a small internal widget model inspired by the “Pizza App” example.

Define a `Widget` structure with at least:
- `id`: unique string (used as `tool.name`)
- `title`: human-readable title
- `template_uri`: URI for the HTML template resource (e.g. `ui://widget/incident-detail.html`)
- `invoking`: short text shown while the tool is running (e.g. “Loading incident details…”)
- `invoked`: short text shown when the tool completes (e.g. “Incident details loaded.”)
- `html`: HTML markup for the widget, including root element and JS/CSS references
- `response_text`: short chat message such as “Showing incident INC-123.”

Create:
- an in-memory list of widgets
- `widgets_by_id` (id → widget)
- `widgets_by_uri` (template_uri → widget)

---

## Widget Metadata (for ChatGPT Apps)

MCP allows arbitrary metadata via the `_meta` field. ChatGPT Apps uses this metadata to
understand which tool results can produce which widget UI.

For each widget, implement a helper:

```json
{
  "openai/outputTemplate": "<widget.template_uri>",
  "openai/toolInvocation/invoking": "<widget.invoking>",
  "openai/toolInvocation/invoked": "<widget.invoked>",
  "openai/widgetAccessible": true,
  "openai/resultCanProduceWidget": true
}
```

This `_meta` structure must be used consistently in:
- Tool registrations
- Resource registrations

Additional metadata may be added if required, but these keys must remain unchanged.

---

## MCP Resources for UI Templates

For each widget, register an MCP **resource** that exposes its HTML:

- `uri`: widget `template_uri`
- `name`: widget title
- `description`: e.g. “HTML markup for the Incident Detail widget.”
- `mimeType`: `text/html+skybridge`
- `_meta`: widget metadata

**Resource behavior:**
- `listResources` must list all widget resources
- `readResource(uri)` must return:
  - `content`: a single `{ type: "text/html", text: widget.html }`
  - `_meta`: widget metadata

These resources are how ChatGPT fetches HTML, JavaScript, and CSS for widgets.

---

## Tools ⇄ UI Widget Link

You must expose tools that:
- Map directly to widgets
- Return both text output and widget metadata so ChatGPT knows to render the widget

### Tool Registration

For each widget marked as invokable in `docs/mcp-scope.md`, define a tool with:
- `name`: widget id
- `description`: widget title (or a more natural description)
- `title`: widget title
- `inputSchema`: arguments required by the widget (e.g. `incidentId`, filters, `runbookId`)
- `_meta`: widget metadata

Keep existing read-only tools unchanged. Add widget-centric tools if clearer
(e.g. `show_incident_detail_widget`).

---

### Tool Handlers

When a widget tool is invoked:
- Look up the widget via `widgets_by_id`
- Parse and validate input arguments
- Fetch required data from the backend via the existing HTTP client
- Return an MCP `CallTool` result containing:
  - `content`: a short text message
  - `structuredContent`: JSON payload consumed by the widget’s JavaScript
  - `_meta`: widget metadata

The structure of `structuredContent` must match what the widget expects.

---

## Stable Contract

The following mappings must remain stable:
- `tool.name == widget.id`
- `resource.uri == widget.template_uri`
- `widget_meta(widget)` is used in both tool and resource metadata

---

## MCP Server Endpoints for ChatGPT Apps

The MCP server must expose HTTP endpoints compatible with ChatGPT Apps:
- `GET /mcp` — SSE stream endpoint
- `POST /mcp/messages` — message ingestion endpoint

Reuse the existing Stage 4 MCP server framework and extend it where necessary rather than rewriting it.

---

## Testing Requirements (MCP + UI Resources)

Extend MCP integration tests to cover UI resources.

**Minimum tests:**

1. **resources_expose_widget_templates**
   - Verify widget resources exist with the correct `mimeType`
   - Read one resource and validate the returned HTML

2. **tools_link_to_widgets**
   - Invoke each widget tool with valid arguments
   - Assert presence of text output, `structuredContent`, and correct `_meta`

3. **widget_meta_consistency**
   - Verify tool and resource metadata match for each widget

4. **error_handling**
   - Invalid IDs or arguments must produce clean MCP errors

**Test harness:**
- Spin up the backend on a random port using a temporary state file
- Start the MCP server pointing to that backend
- Run tests using `pytest` and the existing MCP test utilities

---

## README & AGENTS Updates

Update `README.md`:
- Add a **Stage 5: ChatGPT App Integration** section explaining:
  - Widget-based UI rendered inside ChatGPT
  - Tools triggering widgets and resources providing HTML templates
  - Local workflow:
    1. Start backend
    2. Start MCP server
    3. Optionally use MCP Inspector
    4. Use ChatGPT Developer Mode and point the app to `https://YOUR_PUBLIC_URL/mcp`
  - Clarify that UI rendering happens inside ChatGPT

Do **not** remove or weaken:
- Frontend (Angular + Playwright)
- Backend (FastAPI + OpenAPI + tests)
- Stage 4 MCP documentation

Update `AGENTS.md`:
- Widgets must be defined centrally
- Tool, resource, and widget metadata must stay consistent
- Contract changes require corresponding code, test, and documentation updates

---

## Deliverables

1. Widget model and registry in the MCP server
2. Widget resources exposing HTML templates with `text/html+skybridge`
3. Widget tools that validate input, call the backend, and return text, `structuredContent`, and metadata
4. HTTP endpoints `/mcp` and `/mcp/messages`
5. Integration tests validating resources, tool–widget linkage, and metadata consistency
6. Updated `README.md` and `AGENTS.md`, preserving Stage 2–4 content

---

## Output Format

1. Brief summary of:
   - Widgets added
   - Tool-to-widget mappings
   - Any MCP endpoint changes

2. Updated directory tree for:
   - `mcp/`
   - `docs/` (if changed)
   - Root-level documentation files

3. Exact commands for:
   - Starting the backend
   - Starting the MCP server
   - Running MCP tests

4. Any assumptions made due to ambiguity in `docs/mcp-scope.md`


from __future__ import annotations

from dataclasses import dataclass

from mcp.server.fastmcp.resources import TextResource
from pydantic import Field


@dataclass(frozen=True)
class Widget:
    id: str
    title: str
    template_uri: str
    invoking: str
    invoked: str
    html: str
    response_text: str
    root_id: str


class WidgetResource(TextResource):
    meta: dict[str, object] | None = Field(default=None)


def widget_meta(widget: Widget) -> dict[str, object]:
    return {
        "openai/outputTemplate": widget.template_uri,
        "openai/toolInvocation/invoking": widget.invoking,
        "openai/toolInvocation/invoked": widget.invoked,
        "openai/widgetAccessible": True,
        "openai/resultCanProduceWidget": True,
    }


def _build_list_html(root_id: str, title: str, item_label: str) -> str:
    return f"""
<div id="{root_id}" class="widget-root">
  <h3>{title}</h3>
  <div class="widget-body" data-role="content"></div>
</div>
<style>
  .widget-root {{ font-family: Arial, sans-serif; border: 1px solid #e0e0e0; padding: 12px; border-radius: 8px; }}
  .widget-root h3 {{ margin: 0 0 8px 0; }}
  .widget-list {{ margin: 0; padding-left: 16px; }}
  .widget-list li {{ margin: 4px 0; }}
</style>
<script>
  (function () {{
    console.debug("Global data:", window.openai);
    const data = window.openai.toolOutput;
    console.debug("Widget data:", data);
    const items = data.items || [];
    const root = document.getElementById("{root_id}");
    if (!root) return;
    const target = root.querySelector('[data-role="content"]');
    if (!target) return;
    if (!items.length) {{
      target.textContent = "No {item_label} found.";
      return;
    }}
    const list = document.createElement('ul');
    list.className = 'widget-list';
    items.forEach((item) => {{
      const li = document.createElement('li');
      li.textContent = item.title || item.id || "{item_label}";
      list.appendChild(li);
    }});
    target.appendChild(list);
  }})();
</script>
""".strip()


def _build_detail_html(root_id: str, title: str, empty_label: str) -> str:
    return f"""
<div id="{root_id}" class="widget-root">
  <h3>{title}</h3>
  <pre class="widget-body" data-role="content"></pre>
</div>
<style>
  .widget-root {{ font-family: Arial, sans-serif; border: 1px solid #e0e0e0; padding: 12px; border-radius: 8px; }}
  .widget-root h3 {{ margin: 0 0 8px 0; }}
  .widget-body {{ background: #f7f7f7; padding: 8px; border-radius: 6px; white-space: pre-wrap; }}
</style>
<script>

  (function () {{
    const data = window.openai.toolOutput;
    console.debug("Widget data:", data);
    const item = data.item;
    const root = document.getElementById("{root_id}");
    if (!root) return;
    const target = root.querySelector('[data-role="content"]');
    if (!target) return;
    if (!item) {{
      target.textContent = "{empty_label}";
      return;
    }}
    target.textContent = JSON.stringify(item, null, 2);
  }})();
</script>
""".strip()

WIDGETS: list[Widget] = [
    Widget(
        id="incident_list_widget",
        title="Incident List",
        template_uri="ui://widget/incident-list.html",
        invoking="Loading incidents…",
        invoked="Incident list loaded.",
        html=_build_list_html("incident-list-widget", "Incidents", "incidents"),
        response_text="Showing incident list.",
        root_id="incident-list-widget",
    ),
    Widget(
        id="incident_detail_widget",
        title="Incident Detail",
        template_uri="ui://widget/incident-detail.html",
        invoking="Loading incident details…",
        invoked="Incident details loaded.",
        html=_build_detail_html("incident-detail-widget", "Incident Detail", "Incident not available."),
        response_text="Showing incident {incident_id}.",
        root_id="incident-detail-widget",
    ),
    Widget(
        id="runbook_list_widget",
        title="Runbook List",
        template_uri="ui://widget/runbook-list.html",
        invoking="Loading runbooks…",
        invoked="Runbook list loaded.",
        html=_build_list_html("runbook-list-widget", "Runbooks", "runbooks"),
        response_text="Showing runbook list.",
        root_id="runbook-list-widget",
    ),
    Widget(
        id="runbook_detail_widget",
        title="Runbook Detail",
        template_uri="ui://widget/runbook-detail.html",
        invoking="Loading runbook details…",
        invoked="Runbook details loaded.",
        html=_build_detail_html("runbook-detail-widget", "Runbook Detail", "Runbook not available."),
        response_text="Showing runbook {runbook_id}.",
        root_id="runbook-detail-widget",
    ),
]

widgets_by_id = {widget.id: widget for widget in WIDGETS}
widgets_by_uri = {widget.template_uri: widget for widget in WIDGETS}

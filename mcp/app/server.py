from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Iterable

from mcp import types
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ResourceError
from mcp.types import Resource as MCPResource
from mcp.types import ResourceTemplate as MCPResourceTemplate
from starlette.routing import Route


@dataclass
class ReadResourceContentsWithMeta:
    content: str | bytes
    mime_type: str | None = None
    meta: dict[str, object] | None = None


class ChatGPTFastMCP(FastMCP):
    _messages_route_added: bool = False

    async def list_resources(self) -> list[MCPResource]:
        resources = self._resource_manager.list_resources()
        return [
            MCPResource(
                uri=resource.uri,
                name=resource.name or "",
                title=resource.title,
                description=resource.description,
                mimeType=resource.mime_type,
                icons=resource.icons,
                annotations=resource.annotations,
                _meta=getattr(resource, "meta", None),
            )
            for resource in resources
        ]

    async def list_resource_templates(self) -> list[MCPResourceTemplate]:
        templates = self._resource_manager.list_templates()
        return [
            MCPResourceTemplate(
                uriTemplate=template.uri_template,
                name=template.name,
                title=template.title,
                description=template.description,
                mimeType=template.mime_type,
                icons=template.icons,
                annotations=template.annotations,
                _meta=getattr(template, "meta", None),
            )
            for template in templates
        ]

    async def read_resource(self, uri: str) -> Iterable[ReadResourceContentsWithMeta]:
        context = self.get_context()
        resource = await self._resource_manager.get_resource(uri, context=context)
        if not resource:
            raise ResourceError(f"Unknown resource: {uri}")

        try:
            content = await resource.read()
            return [
                ReadResourceContentsWithMeta(
                    content=content,
                    mime_type=resource.mime_type,
                    meta=getattr(resource, "meta", None),
                )
            ]
        except Exception as exc:  # pragma: no cover
            raise ResourceError(str(exc)) from exc

    def _setup_handlers(self) -> None:
        super()._setup_handlers()

        async def handler(req: types.ReadResourceRequest):
            result = await self.read_resource(str(req.params.uri))
            contents_list: list[
                types.TextResourceContents | types.BlobResourceContents
            ] = []
            for item in result:
                if isinstance(item.content, bytes):
                    contents_list.append(
                        types.BlobResourceContents(
                            uri=req.params.uri,
                            blob=base64.b64encode(item.content).decode(),
                            mimeType=item.mime_type or "application/octet-stream",
                            _meta=item.meta,
                        )
                    )
                else:
                    contents_list.append(
                        types.TextResourceContents(
                            uri=req.params.uri,
                            text=item.content,
                            mimeType=item.mime_type or "text/plain",
                            _meta=item.meta,
                        )
                    )
            return types.ServerResult(types.ReadResourceResult(contents=contents_list))

        self._mcp_server.request_handlers[types.ReadResourceRequest] = handler

    def streamable_http_app(self):
        app = super().streamable_http_app()
        if self._messages_route_added:
            return app
        endpoint = None
        for route in app.routes:
            if isinstance(route, Route) and route.path == self.settings.streamable_http_path:
                endpoint = route.endpoint
                break
        if endpoint is not None:
            app.router.routes.append(Route("/mcp/messages", endpoint=endpoint))
            self._messages_route_added = True
        return app

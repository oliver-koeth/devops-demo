from app.client import BackendClient
from app.core import get_mcp_host, get_mcp_port
from app.resources import register_resources
from app.server import ChatGPTFastMCP
from app.tools import register_tools


def create_server() -> ChatGPTFastMCP:
    mcp = ChatGPTFastMCP("incidents-runbooks-mcp")
    mcp.settings.host = get_mcp_host()
    mcp.settings.port = get_mcp_port()
    client = BackendClient()
    register_tools(mcp, client)
    register_resources(mcp, client)
    return mcp


def main() -> None:
    server = create_server()
    server.run(
        transport="streamable-http",
    )


if __name__ == "__main__":
    main()

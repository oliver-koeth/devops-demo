from mcp.server.fastmcp import FastMCP

from app.client import BackendClient
from app.tools import register_tools


def create_server() -> FastMCP:
    mcp = FastMCP("DevOps Runbook MCP")
    client = BackendClient()
    register_tools(mcp, client)
    return mcp


def main() -> None:
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()

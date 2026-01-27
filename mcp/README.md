# MCP Server

## Overview
The MCP server is a separate Python process that exposes read-only tools and resources by calling the backend API over HTTP. It enables MCP Inspector testing and ChatGPT App integration without embedding backend logic.

## Prerequisites
- Python 3.11+
- Backend API running at `http://localhost:8000`
- Node.js and npm (for MCP Inspector)

## Install Dependencies
```bash
cd mcp
python -m pip install -e .
```

## Run (Local)
```bash
cd mcp
export BACKEND_BASE_URL=http://localhost:8000
export MCP_HOST=127.0.0.1
export MCP_PORT=8090

python -m app.main
```
The MCP HTTP endpoint will be available at `http://127.0.0.1:8090/mcp`.

## Test
```bash
cd mcp
python -m pip install -e '.[dev]'
pytest
```

## Interactive Testing (MCP Inspector)
1. Start the backend and the MCP server (see above).
2. Run the Inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```
3. In the Inspector UI, select **Streamable HTTP** transport and connect to:
   - `http://localhost:8090/mcp`
   - If using ngrok: `https://<generated>.ngrok-free.dev/mcp`
4. Copy the session proxy token shown in the Inspector UI logs when prompted.

Notes:
- The Inspector validates tool/resource discovery and payload shapes.
- Resource lists can be reloaded from the **Resources** tab.

## Exposing the MCP Server with ngrok
1. Install ngrok (example on macOS):
   ```bash
   brew install ngrok
   ```
2. Configure auth (either environment variable or config):
   ```bash
   export NGROK_AUTHTOKEN=<your_token>
   # or
   ngrok config add-authtoken <your_token>
   ```
3. Start a tunnel (with host header rewrite):
   ```bash
   ngrok http 8090 --host-header=rewrite
   ```
4. Use the generated HTTPS URL as your public MCP endpoint (append `/mcp`).

## ChatGPT App Integration (Developer Mode)
1. In ChatGPT, open **Settings** and enable **Developer Mode**.
2. Create a new app in Developer Mode.
3. Configure the app:
   - **MCP Server URL**: `https://YOUR_PUBLIC_URL/mcp` (ngrok URL or any public HTTPS URL)
   - **Auth**: None
4. Use the **Refresh** button in the app configuration to re-fetch tools/resources after server changes.

Tip: If you change tool schemas or resources, restart the MCP server and use the refresh button to update ChatGPT's cached config.

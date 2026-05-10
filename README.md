# Home Assistant MCP Server

This is a Model Context Protocol (MCP) server for Home Assistant. It exposes your Home Assistant entities and services to AI models via the MCP protocol.

## Features
- List all entities and states
- Get specific entity state and attributes
- Call Home Assistant services
- Get error logs
- Get entity history

## Setup

1. Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```
2. Set your `HASS_URL` and `HASS_TOKEN` (Long-Lived Access Token) in the `.env` file.

## Running with Docker

First, build the Docker image:
```bash
docker build -t homeassistant-mcp .
# or
docker-compose build
```

Since this MCP server uses StreamableHTTP for communication over HTTP, it can run continuously in the background and you can point your AI or MCP client to its network URL.

### Running the Server

Start the server continuously in the background:
```bash
docker-compose up -d
```
This will expose the MCP Server on port `8000`.

### Connecting your AI / MCP Client

Point your AI tool or MCP Client to the StreamableHTTP endpoint. For example:
- **StreamableHTTP URL:** `http://<IP_OF_HOMEMINIPC>:8000/mcp`

If you are using OpenClaw or another tool that supports `streamable-http`, simply provide the URL above.

## Running Locally (without Docker)

If you prefer to run it directly:
```bash
pip install -r requirements.txt
python server.py
```
And point your MCP client configuration to `python` and the absolute path of `server.py`.

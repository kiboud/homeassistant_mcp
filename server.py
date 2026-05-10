import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

HASS_URL = os.getenv("HASS_URL", "").rstrip("/")
HASS_TOKEN = os.getenv("HASS_TOKEN", "")

# Initialize FastMCP
mcp = FastMCP("homeassistant", host="0.0.0.0", port=8000)

def get_headers():
    return {
        "Authorization": f"Bearer {HASS_TOKEN}",
        "Content-Type": "application/json",
    }

@mcp.tool()
async def get_all_entities() -> str:
    """Get a list of all entities in Home Assistant, along with their current states."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HASS_URL}/api/states", headers=get_headers())
        response.raise_for_status()
        states = response.json()
        
        result = []
        for state in states:
            entity_id = state.get("entity_id")
            s = state.get("state")
            friendly_name = state.get("attributes", {}).get("friendly_name", "")
            result.append(f"{entity_id} ({friendly_name}): {s}")
            
        return "\n".join(result)

@mcp.tool()
async def get_entity_state(entity_id: str) -> str:
    """Get the current state and attributes of a specific entity in Home Assistant."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HASS_URL}/api/states/{entity_id}", headers=get_headers())
        if response.status_code == 404:
            return f"Entity {entity_id} not found."
        response.raise_for_status()
        return str(response.json())

@mcp.tool()
async def call_service(domain: str, service: str, entity_id: str = None, service_data: dict = None) -> str:
    """
    Call a service in Home Assistant.
    domain: e.g., 'light', 'switch'
    service: e.g., 'turn_on', 'turn_off'
    entity_id: (optional) e.g., 'light.lampu_kamar_depan'
    service_data: (optional) a dictionary of additional parameters
    """
    payload = service_data or {}
    if entity_id:
        payload["entity_id"] = entity_id
        
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HASS_URL}/api/services/{domain}/{service}", 
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return f"Service {domain}.{service} called successfully. Response: {response.json()}"

@mcp.tool()
async def get_error_log() -> str:
    """Get the error log from Home Assistant."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HASS_URL}/api/error_log", headers=get_headers())
        response.raise_for_status()
        return response.text

@mcp.tool()
async def get_entity_history(entity_id: str) -> str:
    """Get the recent history of a specific entity in Home Assistant."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HASS_URL}/api/history/period?filter_entity_id={entity_id}", headers=get_headers())
        response.raise_for_status()
        return str(response.json())

if __name__ == "__main__":
    mcp.run(transport='streamable-http')

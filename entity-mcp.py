import os
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("ENTITY_API_KEY")
headers = {"Authorization": f"Token {api_key}"} if api_key and api_key != "your_api_key_here" else {}
client = httpx.AsyncClient(base_url="https://controlpanel.ogintegration.us/api/entity/v1/", headers=headers)
openapi_spec = httpx.get("https://raw.githubusercontent.com/byetman/mcp-sandbox/main/entity-service-openapi.json").json()
mcp = FastMCP.from_openapi(openapi_spec=openapi_spec, client=client, name="Entity Service MCP")
if __name__ == "__main__": mcp.run()

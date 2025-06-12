import httpx
from fastmcp import FastMCP

# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="https://controlpanel.ogintegration.us/api/entity/v1/")

# Load your OpenAPI spec from the raw GitHub URL
openapi_spec = httpx.get("https://raw.githubusercontent.com/byetman/mcp-sandbox/main/entity-service-openapi.json").json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Entity Service MCP"
)

if __name__ == "__main__":
    mcp.run()
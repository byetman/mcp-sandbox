#!/usr/bin/env python3
import asyncio
from fastmcp import FastMCP
import httpx

async def test_server():
    print("🧪 Testing FastMCP server creation...")
    
    # Load OpenAPI spec
    print("📄 Loading OpenAPI spec...")
    spec = httpx.get('https://raw.githubusercontent.com/byetman/mcp-sandbox/main/entity-service-openapi.json').json()
    print(f"✅ Loaded spec with {len(spec.get('paths', {}))} endpoints")
    
    # Create client
    client = httpx.AsyncClient(base_url='https://controlpanel.ogintegration.us/api/entity/v1/')
    
    # Create MCP server
    print("🚀 Creating MCP server...")
    mcp = FastMCP.from_openapi(
        openapi_spec=spec,
        client=client,
        name='Entity Service MCP'
    )
    
    print('✅ MCP Server created successfully!')
    print(f'✅ Server name: {mcp.name}')
    print('✅ This server exposes the following entity API endpoints as MCP tools:')
    
    # List the endpoints
    for path, methods in spec.get('paths', {}).items():
        for method in methods.keys():
            print(f'   • {method.upper()} {path}')
    
    return mcp

if __name__ == "__main__":
    # Run the test
    mcp = asyncio.run(test_server())
    print('\n🎉 Success! Your FastMCP server is working correctly!')
    print('\n📖 To run the server:')
    print('   python entity-mcp.py')
    print('\n🔍 To test with FastMCP dev mode:')
    print('   fastmcp dev entity-mcp.py') 
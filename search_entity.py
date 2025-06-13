#!/usr/bin/env python3
import asyncio
import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def search_entity(entity_name):
    # Get API key from environment variables
    api_key = os.getenv("ENTITY_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ Error: API key not found or not set. Please set ENTITY_API_KEY in .env file.")
        return
    
    # Set up authentication headers
    headers = {"Authorization": f"Token {api_key}"}
    
    # Create HTTP client
    async with httpx.AsyncClient(
        base_url="https://controlpanel.ogintegration.us/api/entity/v1/", 
        headers=headers
    ) as client:
        print(f"🔍 Searching for entity: '{entity_name}'...")
        
        # First, try GraphQL search which offers more flexibility
        try:
            graphql_query = """
            query SearchEntities($search: String!) {
                entities(search: $search) {
                    id
                    name
                    displayName
                    entityType
                    friendlyId
                }
            }
            """
            
            response = await client.post(
                "graphql", 
                json={
                    "query": graphql_query,
                    "variables": {"search": entity_name}
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "entities" in data["data"]:
                    entities = data["data"]["entities"]
                    return entities
            
            # If GraphQL approach failed, fall back to other methods
            print("   GraphQL search failed or returned no results, trying alternative methods...")
        
        except Exception as e:
            print(f"   GraphQL search error: {e}")
        
        # Try to get all entities and filter client-side
        try:
            response = await client.get("")
            if response.status_code == 200:
                entities = response.json().get("entities", [])
                
                # Filter entities that match the search term
                matches = []
                for entity in entities:
                    if (entity_name.lower() in entity.get("name", "").lower() or
                        entity_name.lower() in entity.get("displayName", "").lower()):
                        matches.append(entity)
                
                return matches
        
        except Exception as e:
            print(f"❌ Error while searching entities: {e}")
            return None

def print_entity_details(entities):
    if not entities:
        print("❌ No entities found matching the search criteria.")
        return
    
    print(f"\n✅ Found {len(entities)} matching entities:\n")
    
    for i, entity in enumerate(entities, 1):
        print(f"Entity #{i}:")
        print(f"   ID: {entity.get('id')}")
        print(f"   Name: {entity.get('name')}")
        print(f"   Display Name: {entity.get('displayName')}")
        print(f"   Entity Type: {entity.get('entityType')}")
        print(f"   Friendly ID: {entity.get('friendlyId')}")
        print()

async def main():
    entity_name = "Cloud City"
    entities = await search_entity(entity_name)
    print_entity_details(entities)

if __name__ == "__main__":
    asyncio.run(main()) 
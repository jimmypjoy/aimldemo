from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("example-tools")

# Define a tool
@mcp.tool()
def get_weather(city: str) -> str:
    """Return the weather for a given city"""
    
    weather_data = {
        "New York": "Rainy 15C",
        "San Francisco": "Sunny 20C",
        "London": "Cloudy 12C"
    }

    return weather_data.get(city, "Weather data not available")


# Start MCP server
if __name__ == "__main__":
    mcp.run(transport="sse")
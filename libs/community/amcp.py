from fastmcp.server import FastMCP

mcp = FastMCP("Demo MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def echo(text: str) -> str:
    """Echo input text."""
    return text


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("nitrostack-sample")


@mcp.tool()
def echo(message: str) -> str:
    """Return the provided message."""
    return f"NitroStack MCP echo: {message}"


@mcp.resource("nitrostack://status")
def status() -> str:
    return "NitroStack MCP sample server is ready."


if __name__ == "__main__":
    mcp.run()

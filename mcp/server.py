from mcp.server.fastmcp import FastMCP

from modules import register_all_modules

mcp = FastMCP("nitrostack-demo")


@mcp.tool()
def ping(message: str = "hello") -> str:
    """Return a simple response so the client can verify MCP communication."""
    return f"pong: {message}"


register_all_modules(mcp)


if __name__ == "__main__":
    mcp.run()

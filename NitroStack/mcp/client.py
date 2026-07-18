import asyncio
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_path = Path(__file__).with_name("server.py")
    params = StdioServerParameters(command=sys.executable, args=[str(server_path)])

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("ping", {"message": "nitrostack"})
            text = result.content[0].text if result.content else ""
            print(text)
            if "pong: nitrostack" not in text:
                raise SystemExit("MCP ping returned an unexpected response")


if __name__ == "__main__":
    asyncio.run(main())

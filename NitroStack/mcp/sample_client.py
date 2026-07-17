import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["sample_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("echo", {"message": "hello from client"})
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())

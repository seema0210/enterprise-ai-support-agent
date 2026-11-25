
import asyncio
import sys

from mcp import Client, StdioServerParameters


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp_server.server"]
    )

    async with Client(server_params) as client:

        tools = await client.list_tools()

        print("Available tools:")
        for tool in tools.tools:
            print(tool.name)

        result = await client.call_tool(
            "get_ticket_status",
            {"ticket_id": "T102"}
        )

        print("Tool result:", result)


if __name__ == "__main__":
    asyncio.run(main())

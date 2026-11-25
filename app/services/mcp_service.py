
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient


class MCPService:

    def __init__(self):
        self.client = MultiServerMCPClient({
            "support": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["-m", "app.mcp_server.server"]
            }
        })

    async def get_tools(self):
        return await self.client.get_tools()


mcp_service = MCPService()

# MultiServerMCPClient : connects to our MCP server and converts its tools into LangChain-compatible tool objects.
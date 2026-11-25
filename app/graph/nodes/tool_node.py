import logging

from app.graph.state import AgentState
from app.tools.calculator_tool import calculate_percentage
from app.tools.addition_tool import add_numbers

from app.services.mcp_service import mcp_service

logger = logging.getLogger(__name__)


async def tool_node(state: AgentState) -> dict:

    logger.info("Tool execution started")

    mcp_tools = await mcp_service.get_tools()

    available_tools = {
        calculate_percentage.name: calculate_percentage,
        add_numbers.name: add_numbers,
        **{tool.name: tool for tool in mcp_tools}
    }

    tool_calls = state.get("tool_calls", [])

    if not tool_calls:
        return {"context": ""}

    results = []

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = available_tools.get(tool_name)

        if selected_tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        result = await selected_tool.ainvoke(tool_args)

        results.append( f"Tool: {tool_name}\nResult: {result}" )

    return {"context": "\n\n".join(results)}

import logging

from langchain_core.messages import HumanMessage, SystemMessage

from app.graph.state import AgentState
from app.services.llm_service import llm_service
from app.tools.calculator_tool import calculate_percentage
from app.tools.addition_tool import add_numbers

from app.services.mcp_service import mcp_service
from app.tools.addition_tool import add_numbers


logger = logging.getLogger(__name__)


async def tool_llm_node(state: AgentState) -> dict:

    logger.info("Tool LLM node started")

    # 1. Get tools from MCP server
    mcp_tools = await mcp_service.get_tools()

    # 2. Combine local tools and MCP tools
    available_tools = [ calculate_percentage, add_numbers, *mcp_tools ]

     # 3. Bind all tools to Qwen
    llm_with_tools = llm_service.llm.bind_tools( available_tools )
    # Qwen receives the calculator tool definition and decides whether to request it.
    # bind_tools() gives Qwen information about both tools. Based on the user's question, Qwen decides which one to request.

    question = state.get("rewritten_question")

    response = await llm_with_tools.ainvoke([
        SystemMessage( content="Use the available tool when calculation is needed." ),
        HumanMessage(content=question)
    ])

    logger.info("Selected tool calls: %s", response.tool_calls)

    return {"tool_calls": response.tool_calls}

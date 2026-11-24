
import logging

from app.graph.state import AgentState
from app.services.llm_service import llm_service
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT


logger = logging.getLogger(__name__)


async def supervisor_node(state: AgentState) -> dict:

    question = state["rewritten_question"]

    decision = await llm_service.generate_response(
        question=question,
        system_prompt=SUPERVISOR_PROMPT
    )

    route = decision.strip().lower()

    if route not in ("rag", "llm", "search", "history", "tools"):
        raise ValueError(
            f"Invalid supervisor route: {route!r}"
        )

    logger.info("Supervisor selected route: %s", route)

    return {
        "route": route
    }

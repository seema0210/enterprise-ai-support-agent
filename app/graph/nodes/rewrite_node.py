
import logging

from app.graph.state import AgentState
from app.services.rewrite_service import rewrite_service


logger = logging.getLogger(__name__)


async def rewrite_node(state: AgentState) -> dict:

    logger.info("Rewrite node started")

    rewritten_question = await rewrite_service.rewrite_question( question=state["question"] )

    logger.info("Question rewriting completed")

    return {
        "rewritten_question": rewritten_question
    }

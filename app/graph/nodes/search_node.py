import logging

from app.graph.state import AgentState
from app.services.search_service import search_service
from app.prompts.search_prompt import SEARCH_SYSTEM_PROMPT


logger = logging.getLogger(__name__)


async def search_node(state: AgentState) -> dict:

    question = state["rewritten_question"]
    
    logger.info("Search node started")
    context = await search_service.search( question=question )

    return {"context": context}
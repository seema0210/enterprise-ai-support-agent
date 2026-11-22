
import logging

from app.graph.state import AgentState
from app.db.database import SessionLocal
from app.db.chat_repository import ChatRepository

logger = logging.getLogger(__name__)


async def save_node(state: AgentState) -> dict:

    logger.info("Save node started")

    with SessionLocal() as db:
        repository = ChatRepository(db)

        repository.save_message(
            session_id=state["session_id"],
            role="user",
            message=state["question"]
        )

        repository.save_message(
            session_id=state["session_id"],
            role="assistant",
            message=state["answer"]
        )

    logger.info("Conversation saved successfully")

    return {}

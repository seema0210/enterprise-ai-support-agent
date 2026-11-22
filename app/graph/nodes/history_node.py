
import asyncio
import logging

from app.graph.state import AgentState
from app.db.database import SessionLocal
from app.db.chat_repository import ChatRepository


logger = logging.getLogger(__name__)


def load_history(session_id: str) -> list[dict[str, str]]:

    with SessionLocal() as db:
        repository = ChatRepository(db)

        messages = repository.get_recent_messages( session_id=session_id, limit=10 )

        return [
            {
                "role": item.role,
                "message": item.message
            }
            for item in messages
        ]


async def history_node(state: AgentState) -> dict:

    logger.info("History node started")

    history = await asyncio.to_thread( load_history, state["session_id"] )

    logger.info("Loaded %d history messages", len(history))

    return {"history": history}

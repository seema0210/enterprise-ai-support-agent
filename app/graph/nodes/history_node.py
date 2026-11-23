
import asyncio
import logging

from app.graph.state import AgentState
from app.db.database import SessionLocal
from app.db.chat_repository import ChatRepository


logger = logging.getLogger(__name__)


def load_history(session_id: str) -> dict:

    with SessionLocal() as db:
        repository = ChatRepository(db)

        saved_summary = repository.get_summary(session_id)

        summary = saved_summary.summary if saved_summary else ""

        last_message_id = ( saved_summary.last_message_id if saved_summary else 0 )

        messages = repository.get_messages_after(
            session_id=session_id,
            last_message_id=last_message_id
        )

        history = [
            {
                "role": item.role,
                "message": item.message
            }
            for item in messages
        ]

        return {
            "summary": summary,
            "history": history
        }


async def history_node(state: AgentState) -> dict:

    logger.info("History node started")

    result = await asyncio.to_thread(
        load_history,
        state["session_id"]
    )

    logger.info(
        "Loaded %d recent messages",
        len(result["history"])
    )

    return result

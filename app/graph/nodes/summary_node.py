
import logging

from app.graph.state import AgentState
from app.db.database import SessionLocal
from app.db.chat_repository import ChatRepository
from app.services.summary_service import summary_service

logger = logging.getLogger(__name__)

SUMMARY_THRESHOLD = 10
RECENT_MESSAGES = 6


async def summary_node(state: AgentState) -> dict:

    session_id = state["session_id"]

    logger.info("Summary node started")

    with SessionLocal() as db:
        repository = ChatRepository(db)

        existing_summary = repository.get_summary(session_id)

        last_message_id = ( existing_summary.last_message_id if existing_summary else 0 )

        previous_summary = ( existing_summary.summary if existing_summary else "" )

        messages = repository.get_messages_after(
            session_id=session_id,
            last_message_id=last_message_id
        )

        if len(messages) < SUMMARY_THRESHOLD:
            logger.info("Summary threshold not reached")
            return {}

        older_messages = messages[:-RECENT_MESSAGES]

        if not older_messages:
            return {}

        history = [
            {
                "role": item.role,
                "message": item.message
            }
            for item in older_messages
        ]

        updated_summary = await summary_service.summarize( previous_summary=previous_summary, messages=history )

        if not updated_summary:
            raise ValueError("Generated summary cannot be empty")

        repository.save_summary(
            session_id=session_id,
            summary_text=updated_summary,
            last_message_id=older_messages[-1].id
        )

    logger.info("Conversation summary updated")

    return {}


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChatMessage


class ChatRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_message( self, session_id: str, role: str, message: str ) -> ChatMessage:

        chat_message = ChatMessage(
            session_id=session_id,
            role=role,
            message=message
        )

        self.db.add(chat_message)
        self.db.commit()
        self.db.refresh(chat_message)

        return chat_message

    def get_recent_messages( self, session_id: str, limit: int = 10 ) -> list[ChatMessage]:

        if limit < 1:
            raise ValueError("Limit must be at least 1")

        statement = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.id.desc())
            .limit(limit)
        )

        messages = self.db.scalars(statement).all()

        return list(reversed(messages))

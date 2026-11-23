
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChatMessage, ChatSummary


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

    
    def get_summary(self, session_id: str) -> ChatSummary | None:

        statement = select(ChatSummary).where( ChatSummary.session_id == session_id )

        return self.db.scalar(statement)


    def get_messages_after( self, session_id: str, last_message_id: int ) -> list[ChatMessage]:

        statement = (
            select(ChatMessage)
            .where(
                ChatMessage.session_id == session_id,
                ChatMessage.id > last_message_id
            )
            .order_by(ChatMessage.id.asc())
        )

        return list(self.db.scalars(statement).all())


    def save_summary( self, session_id: str, summary_text: str, last_message_id: int ) -> ChatSummary:

        chat_summary = self.get_summary(session_id)

        if chat_summary is None:
            chat_summary = ChatSummary(
                session_id=session_id,
                summary=summary_text,
                last_message_id=last_message_id
            )
            self.db.add(chat_summary)

        else:
            chat_summary.summary = summary_text
            chat_summary.last_message_id = last_message_id

        self.db.commit()
        self.db.refresh(chat_summary)

        return chat_summary




    
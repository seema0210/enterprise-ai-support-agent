from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length= 1,
        description="Unique conversation session ID"
    )
    question: str = Field(
        min_length= 1,
        description="User's question"
    )

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    status: str


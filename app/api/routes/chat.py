from fastapi import APIRouter
from app.api.schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter(
    prefix= "/api/v1",
    tags=["Chat"]
)

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        session_id=request.session_id,
        answer="Chat endpoint connected. LLM not integrated yet.",
        status="placeholder"
    )

# -> ChatResponse: this function is expected to return a ChatResponse object
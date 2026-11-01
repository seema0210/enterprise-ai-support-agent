from fastapi import APIRouter
from app.api.schemas.chat_schema import ChatRequest, ChatResponse
from app.graph.workflow import graph

router = APIRouter(
    prefix= "/api/v1",
    tags=["Chat"]
)

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:

    initial_state = {
        "session_id": request.session_id,
        "question": request.question,
        "answer": "",
        "status": "pending"
    }

    result = await graph.ainvoke(initial_state) # calling the graph
    return ChatResponse(
        session_id=result["session_id"],
        answer=result["answer"],
        status=result["status"]
    )

# -> ChatResponse: this function is expected to return a ChatResponse object
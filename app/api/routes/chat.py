
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.api.schemas.chat_schema import ChatRequest, ChatResponse
from app.graph.workflow import graph

router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"]
)

# -> ChatResponse: that function is expected to return a ChatResponse object

# Normal Chat API
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:

    initial_state = {
        "session_id": request.session_id,
        "question": request.question,
        "answer": "",
        "status": "pending"
    }

    result = await graph.ainvoke(initial_state)

    return ChatResponse(
        session_id=result["session_id"],
        answer=result["answer"],
        status=result["status"]
    )


# SSE Streaming Chat API
@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):

    initial_state = {
        "session_id": request.session_id,
        "question": request.question,
        "answer": "",
        "status": "pending"
    }

    async def generate():

        try:
            async for chunk, metadata in graph.astream(
                initial_state,
                stream_mode="messages"
            ):

                # Only stream messages from the LLM node
                if metadata.get("langgraph_node") != "llm":
                    continue

                # Send text chunks to the client
                if isinstance(chunk.content, str) and chunk.content:

                    yield chunk.content


        except Exception:
            yield (
                "event: error\n"
                'data: {"message": "LLM streaming failed"}\n\n'
            )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )



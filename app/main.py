from fastapi import FastAPI, Request
from app.api.routes.chat import router as chat_router

from fastapi.responses import JSONResponse
from app.core.exceptions import LLMServiceError
from app.core.logging import setup_logging

app = FastAPI(
    title = "Enterprise AI Support Agent",
    description = "Production-oriented  Agentic AI Application",
    version = "1.0.0"
)

setup_logging()
app.include_router(chat_router)

@app.get('/test') # Whenever a client sends an HTTP GET request to /test, execute the following function.
async def test_api(): # bcoz async : other task will work during this time
    return {
        "status": "testing",
        "service": "enterprise-ai-agent-support"
    }

@app.exception_handler(LLMServiceError)
async def llm_service_exception_handler(
    request: Request,
    exc: LLMServiceError
):
    return JSONResponse(
        status_code=503,
        content={
            "status": "error",
            "message": str(exc)
        }
    )

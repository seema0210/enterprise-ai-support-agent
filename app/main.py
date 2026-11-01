from fastapi import FastAPI
from app.api.routes.chat import router as chat_router

app = FastAPI(
    title = "Enterprise AI Support Agent",
    description = "Production-oriented  Agentic AI Application",
    version = "1.0.0"
)

app.include_router(chat_router)

@app.get('/test') # Whenever a client sends an HTTP GET request to /test, execute the following function.
async def test_api(): # boz asunc other task will work during this time
    return {
        "status": "testing",
        "service": "enterprise-ai-agent-support"
    }

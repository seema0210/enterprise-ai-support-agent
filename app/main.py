from fastapi import FastAPI

app = FastAPI(
    title = "Enterprise AI Support Agent",
    description = "Production-oriented  Agentic AI Application",
    version = "1.0.0"
)

@app.get('/test') # Whenever a client sends an HTTP GET request to /test, execute the following function.
async def test_api():
    return {
        "status": "testing",
        "service": "enterprise-ai-agent-support"
    }

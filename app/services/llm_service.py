
# Uses configuration
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.core.exceptions import LLMServiceError
from app.prompts.llm_prompt import SYSTEM_PROMPT

import httpx
from ollama import ResponseError


class LLMService:

    def __init__(self):
        self.llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.ollama_temperature
        )

    async def generate_response(self, question: str) -> str:

        messages = [ SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=question) ]

        try:

            response = await self.llm.ainvoke(messages)
            return str(response.content)
        
        except httpx.TimeoutException as exc:
            raise LLMServiceError(
                "The LLM request timed out."
            ) from exc
        except ResponseError as exc:
            raise LLMServiceError(
                "Ollama could not process the model request."
            ) from exc



llm_service = LLMService()

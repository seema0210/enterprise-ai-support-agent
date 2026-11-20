
# Uses configuration
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.core.exceptions import LLMServiceError
from app.prompts.llm_prompt import SYSTEM_PROMPT
import logging

import httpx
from ollama import ResponseError

logger = logging.getLogger(__name__)

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
            logger.info("Calling Ollama LLM")
            response = await self.llm.ainvoke(messages)
            logger.info("Ollama response generated successfully")
            return str(response.content)
        
        except httpx.TimeoutException as exc:
            logger.error("Ollama request timed out")
            raise LLMServiceError( "The LLM request timed out." ) from exc
        except ResponseError as exc:
            logger.error("Ollama returned an error: %s", exc.status_code)
            raise LLMServiceError( "Ollama could not process the model request." ) from exc



llm_service = LLMService()

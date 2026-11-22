
import logging

import httpx

from ollama import ResponseError
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.core.exceptions import LLMServiceError
from app.prompts.llm_prompt import SYSTEM_PROMPT


logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        self.llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.ollama_temperature
        )

    async def generate_response(
        self,
        question: str,
        context: str | None = None,
        history: str | None = None,
        system_prompt: str = SYSTEM_PROMPT
    ) -> str:

        user_content = question

        if context is not None:
            user_content = ( f"Retrieved context:\n{context}\n\n" f"User question:\n{question}" )
        
        if history is not None:
            user_content = ( f"Retrieved context:\n{history}\n\n" f"User question:\n{question}" )

        messages = [ SystemMessage(content=system_prompt), HumanMessage(content=user_content) ]

        try:
            logger.info("Calling Ollama LLM")
            response = await self.llm.ainvoke(messages)
            logger.info("Ollama response generated successfully")
            return str(response.content)

        except httpx.TimeoutException as exc:
            logger.error("Ollama request timed out")
            raise LLMServiceError( "The LLM request timed out." ) from exc

        except (httpx.ConnectError, ConnectionError) as exc:
            logger.error("Cannot connect to Ollama")
            raise LLMServiceError( "Cannot connect to the Ollama server." ) from exc

        except ResponseError as exc:
            logger.error( "Ollama returned an error: %s", exc.status_code )
            raise LLMServiceError( "Ollama could not process the model request." ) from exc


llm_service = LLMService()

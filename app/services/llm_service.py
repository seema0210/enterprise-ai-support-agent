
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage
from app.prompts.llm_prompt import SYSTEM_PROMPT


class LLMService:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:7b",
            temperature=0
        )

    async def generate_response(self,question: str) -> str:

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=question)
        ]

        response = await self.llm.ainvoke(messages) # This sends the messages to Ollama and waits for the complete model response

        return str(response.content)


llm_service = LLMService()

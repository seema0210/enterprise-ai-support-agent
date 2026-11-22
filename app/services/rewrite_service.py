
from app.services.llm_service import llm_service
from app.prompts.rewrite_prompt import REWRITE_PROMPT


class RewriteService:

    async def rewrite_question(self, question: str) -> str:

        if not question.strip():
            raise ValueError("Question cannot be empty")

        rewritten_question = await llm_service.generate_response(
            question=question,
            system_prompt=REWRITE_PROMPT
        )

        rewritten_question = rewritten_question.strip()

        if not rewritten_question:
            raise ValueError("Rewritten question cannot be empty")

        return rewritten_question


rewrite_service = RewriteService()

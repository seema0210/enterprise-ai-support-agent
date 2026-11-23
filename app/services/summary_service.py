
from app.services.llm_service import llm_service
from app.prompts.summary_prompt import SUMMARY_PROMPT


class SummaryService:

    async def summarize( self, previous_summary: str, messages: list[dict[str, str]] ) -> str:

        if not messages:
            return previous_summary

        history_text = "\n".join(
            f"{item['role']}: {item['message']}"
            for item in messages
        )

        question = (
            f"Previous summary:\n{previous_summary}\n\n"
            f"New conversation messages:\n{history_text}"
        )

        updated_summary = await llm_service.generate_response(
            question=question,
            system_prompt=SUMMARY_PROMPT
        )

        return updated_summary.strip()


summary_service = SummaryService()

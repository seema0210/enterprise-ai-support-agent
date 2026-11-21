
from app.graph.state import AgentState
from app.services.llm_service import llm_service

from app.prompts.llm_prompt import SYSTEM_PROMPT
from app.prompts.rag_prompt import RAG_SYSTEM_PROMPT


ROUTE_PROMPTS = {
    "llm": SYSTEM_PROMPT,
    "rag": RAG_SYSTEM_PROMPT
}


async def llm_node(state: AgentState) -> dict:

    route = state["route"]
    context = state.get("context")

    # Select prompt dynamically based on Supervisor route
    system_prompt = ROUTE_PROMPTS.get(route)

    if system_prompt is None:
        raise ValueError(f"Unsupported LLM route: {route}")

    # RAG requires retrieved context
    if route == "rag" and not context:
        return {
            "answer": "I could not find the answer in the provided documents.",
            "status": "success"
        }

    answer = await llm_service.generate_response(
        question=state["question"],
        context=context,
        system_prompt=system_prompt
    )

    return {
        "answer": answer,
        "status": "success"
    }

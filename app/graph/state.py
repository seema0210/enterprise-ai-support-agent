from typing import TypedDict, NotRequired


class AgentState(TypedDict):
    session_id: str
    question: str
    answer: str
    status: str
    route: NotRequired[str]
    context: NotRequired[str]
    rewritten_question: NotRequired[str]
    history: NotRequired[list[dict[str, str]]]
    summary: NotRequired[str]
    tool_calls: NotRequired[list[dict]]
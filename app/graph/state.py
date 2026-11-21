from typing import TypedDict, NotRequired


class AgentState(TypedDict):
    session_id: str
    question: str
    answer: str
    status: str
    route: NotRequired[str]
    context: NotRequired[str]
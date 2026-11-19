from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.services.llm_service import llm_service

async def llm_node(state: AgentState) -> dict:
    question = state['question']
    answer = await llm_service.generate_response(question=question)
    return {
        "answer": answer,
        "status": "Success"
    }

def build_graph():
    workflow = StateGraph(AgentState) # data flowing through its nodes should follow the AgentState structure.
    workflow.add_node("llm", llm_node)
    workflow.add_edge(START, "llm")
    workflow.add_edge("llm", END)

    return workflow.compile() # converts our graph definition into an executable graph that can be invoked.

graph = build_graph()

# We can call methods such as invoke(), ainvoke(), and astream() on the compiled graph.
# LangGraph nodes can return partial state updates. LangGraph applies the node's updates to the state.
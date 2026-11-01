from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState

def response_node(state: AgentState) -> dict:
    question = state["question"]

    return {
        "answer": f"Graph received your question: {question}",
        "status": "success"
    }

def build_graph():
    workflow = StateGraph(AgentState) # creates a graph builder
    workflow.add_node("response_node", response_node)
    workflow.add_edge(START, "response_node")
    workflow.add_edge("response_node", END)

    return workflow.compile() # converts our graph definition into an executable graph that can be invoked.

graph = build_graph()

# We can then call methods such as invoke(), ainvoke(), and astream() on the compiled graph.
# LangGraph nodes can return partial state updates. LangGraph applies the node's updates to the state.
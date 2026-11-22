from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState

from app.graph.nodes.rewrite_node import rewrite_node
from app.graph.nodes.supervisor_node import supervisor_node
from app.graph.nodes.rag_node import rag_node
from app.graph.nodes.search_node import search_node
from app.graph.nodes.llm_node import llm_node


def build_graph():
    workflow = StateGraph(AgentState) # data flowing through its nodes should follow the AgentState structure.

    # Register nodes
    workflow.add_node("rewrite", rewrite_node)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("search", search_node)
    workflow.add_node("llm", llm_node)

    # Start with question rewriting
    workflow.add_edge(START, "rewrite")

    # Supervisor decides which flow to execute
    workflow.add_edge("rewrite", "supervisor")

    # Route based on supervisor decision
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: state["route"],
        {
            "rag": "rag",
            "llm": "llm",
            "search": "search"
        }
    )

    # End after RAG execution
    workflow.add_edge("rag", "llm")
    workflow.add_edge("search", "llm")

    workflow.add_edge("llm", END)

    return workflow.compile() # converts our graph definition into an executable graph that can be invoked.

graph = build_graph()

# We can call methods such as invoke(), ainvoke(), and astream() on the compiled graph.
# LangGraph nodes can return partial state updates. LangGraph applies the node's updates to the state.
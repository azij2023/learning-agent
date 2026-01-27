# src/graph.py
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.define_checkpoint import define_checkpoint
from src.nodes.gather_context import gather_context
from src.nodes.validate_context import validate_context

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("define_checkpoint", define_checkpoint)
    graph.add_node("gather_context", gather_context)
    graph.add_node("validate_context", validate_context)

    graph.set_entry_point("define_checkpoint")
    graph.add_edge("define_checkpoint", "gather_context")
    graph.add_edge("gather_context", "validate_context")
    graph.add_edge("validate_context", END)

    return graph.compile()

# src/nodes/context_processor.py
from src.state import AgentState

def context_processor(state: AgentState) -> AgentState:
    # Instead of embeddings, just store raw context
    state.messages.append("ContextProcessor: passed raw context (no embeddings)")
    return state

# src/nodes/validate_context.py
from src.state import AgentState

def validate_context(state: AgentState) -> AgentState:
    cp = state.checkpoints[state.checkpoint_index]
    text = (state.context_raw or "").lower()
    # ✅ FIXED: use cp.objectives
    hits = sum(1 for obj in cp.objectives if obj.lower() in text)
    score = hits / len(cp.objectives)
    state.relevance_score = score
    state.messages.append(f"ValidateContext: relevance={score:.2f}")
    return state

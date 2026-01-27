# src/nodes/logic.py
from src.state import AgentState

def conditional_logic(state: AgentState) -> AgentState:
    """
    Decide whether to proceed or halt based on verification score.
    """
    score = getattr(state, "verification_score", None)

    if score is None:
        state.messages.append("Logic: no score available, proceeding by default")
        return state

    if score >= 70:
        state.messages.append("Logic: score sufficient, proceeding to next checkpoint")
        state.checkpoint_index += 1
    else:
        state.messages.append("Logic: score too low (<70%), halting at Feynman node placeholder")
        state.feynman_required = True

    return state

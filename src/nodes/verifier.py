# src/nodes/verifier.py
from src.state import AgentState

def verifier(state: AgentState) -> AgentState:
    """
    Evaluate learner answers against generated MCQs.
    If no learner answers are provided, skip scoring but keep pipeline stable.
    """
    if not hasattr(state, "learner_answers") or not state.learner_answers:
        state.messages.append("Verifier: no learner answers provided, skipping verification")
        state.verification_score = None
        return state

    correct = 0
    total = len(state.questions)

    for i, q in enumerate(state.questions):
        learner_ans = state.learner_answers[i] if i < len(state.learner_answers) else None
        if learner_ans and learner_ans.upper() == q["answer"]:
            correct += 1

    score = (correct / total) * 100
    state.verification_score = score
    state.messages.append(f"Verifier: learner score = {score:.1f}%")
    return state

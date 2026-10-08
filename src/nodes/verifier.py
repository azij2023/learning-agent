# src/nodes/verifier.py
from src.state import AgentState
import re


def _option_index(answer, options):
    if not isinstance(answer, str):
        return None

    normalized_answer = answer.strip().casefold()
    for index, option in enumerate(options):
        if isinstance(option, str) and option.strip().casefold() == normalized_answer:
            return index

    match = re.match(r"^\s*([A-D])(?:\s*[).:-]|\s*$)", answer, re.IGNORECASE)
    if match:
        index = ord(match.group(1).upper()) - ord("A")
        return index if index < len(options) else None
    return None

def verifier(state: AgentState) -> AgentState:
    """
    Evaluate learner answers against generated MCQs.
    If no learner answers are provided, skip scoring but keep pipeline stable.
    """
    if not state.learner_answers:
        state.messages.append("Verifier: no learner answers provided, skipping verification")
        state.verification_score = None
        return state

    questions = state.questions or []
    total = len(questions)
    if not total:
        state.messages.append("Verifier: no questions available, skipping verification")
        state.verification_score = None
        return state

    correct = 0
    state.answer_feedback = []
    for i, question in enumerate(questions):
        options = question.get("options", [])
        learner_answer = (
            state.learner_answers[i]
            if i < len(state.learner_answers)
            else None
        )
        learner_index = _option_index(learner_answer, options)
        correct_index = _option_index(question.get("answer"), options)
        is_correct = (
            learner_index is not None
            and correct_index is not None
            and learner_index == correct_index
        )
        if is_correct:
            correct += 1
        state.answer_feedback.append(
            {
                "question": question.get("question", ""),
                "selectedAnswer": (
                    options[learner_index] if learner_index is not None else None
                ),
                "correctAnswer": (
                    options[correct_index] if correct_index is not None else None
                ),
                "correct": is_correct,
                "explanation": question.get("explanation", ""),
            }
        )

    score = (correct / total) * 100
    state.verification_score = score
    state.messages.append(
        f"Verifier: learner score = {score:.1f}% ({correct}/{total})"
    )
    return state

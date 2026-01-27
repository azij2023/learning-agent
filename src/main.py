# src/main.py
from dotenv import load_dotenv
load_dotenv()

from src.state import AgentState
from src.nodes.gather_context import gather_context
from src.nodes.relevance_scorer import relevance_scorer
from src.nodes.topic_explainer import topic_explainer
from src.nodes.question_generator import question_generator
from src.nodes.verifier import verifier
from src.nodes.logic import conditional_logic
from src.nodes.feynman import feynman_node

def run_checkpoint(topic: str, context: str = ""):
    state = AgentState()
    state.checkpoints = [{"topic": topic}]
    state.context_raw = context

    # Step 1: Context + relevance
    state = gather_context(state)
    state = relevance_scorer(state)
    print("\n".join(state.messages))  # show immediately

    # Step 2: Topic explanation + first quiz
    state = topic_explainer(state)
    state = question_generator(state)

    print("\nExplanation:\n", state.explanation)

    learner_answers = []
    print("\nAnswer the following questions:")
    for i, q in enumerate(state.questions, start=1):
        print(f"\nQ{i}: {q['question']}")
        for opt in q["options"]:
            print(opt)
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        learner_answers.append(ans)

    state.learner_answers = learner_answers

    # Step 3: Verify answers
    state = verifier(state)
    state = conditional_logic(state)

    if state.verification_score is not None:
        print(f"\nYour score: {state.verification_score:.1f}%")

    # Step 4: If score <70%, Feynman explanation THEN repeat quiz
    if getattr(state, "feynman_required", False):
        # Feynman explanation first
        state = feynman_node(state)
        print("\n".join(state.messages))  # show explanation immediately

        # THEN repeat quiz
        print("\nLet's reinforce your understanding with a fresh set of questions!\n")
        state = question_generator(state)

        learner_answers = []
        for i, q in enumerate(state.questions, start=1):
            print(f"\nRetry Q{i}: {q['question']}")
            for opt in q["options"]:
                print(opt)
            ans = input("Your answer (A/B/C/D): ").strip().upper()
            learner_answers.append(ans)

        state.learner_answers = learner_answers
        state = verifier(state)
        state = conditional_logic(state)

        if state.verification_score is not None:
            print(f"\nYour retry score: {state.verification_score:.1f}%")

    # Step 5: Final pipeline messages
    print("\n".join(state.messages))
    return state


if __name__ == "__main__":
    while True:
        topic = input("\nEnter a topic (or 'quit' to exit): ")
        if topic.lower() == "quit":
            break
        context = input("Optional context (press Enter to skip): ")
        run_checkpoint(topic, context)

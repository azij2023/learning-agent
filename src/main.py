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


def run_checkpoint(topic: str, context: str = "", learner_answers=None, retry_answers=None):
    """
    Run the full learning agent pipeline.
    Returns the final AgentState with explanations, questions, scores, and messages.
    """
    state = AgentState()
    state.checkpoints = [{"topic": topic}]
    state.context_raw = context

    # Step 1: Context + relevance
    state = gather_context(state)
    state = relevance_scorer(state)

    # Step 2: Topic explanation + first quiz
    state = topic_explainer(state)
    state = question_generator(state)

    # Collect learner answers (CLI or Streamlit will provide them)
    if learner_answers:
        state.learner_answers = learner_answers
        state = verifier(state)
        state = conditional_logic(state)

    # Step 3: If score <70%, Feynman explanation THEN repeat quiz
    if getattr(state, "feynman_required", False):
        state = feynman_node(state)
        state = question_generator(state)

        if retry_answers:
            state.learner_answers = retry_answers
            state = verifier(state)
            state = conditional_logic(state)

    return state


if __name__ == "__main__":
    while True:
        topic = input("\nEnter a topic (or 'quit' to exit): ")
        if topic.lower() == "quit":
            break
        context = input("Optional context (press Enter to skip): ")

        # Run pipeline
        state = run_checkpoint(topic, context)

        # Show explanation
        print("\nExplanation:\n", state.explanation)

        # Ask questions
        learner_answers = []
        print("\nAnswer the following questions:")
        for i, q in enumerate(state.questions, start=1):
            print(f"\nQ{i}: {q['question']}")
            for opt in q["options"]:
                print(opt)
            ans = input("Your answer (A/B/C/D): ").strip().upper()
            learner_answers.append(ans)

        # Re-run with answers
        state = run_checkpoint(topic, context, learner_answers=learner_answers)

        if state.verification_score is not None:
            print(f"\nYour score: {state.verification_score:.1f}%")

        # Retry if needed
        if getattr(state, "feynman_required", False):
            print("\n".join(state.messages))
            print("\nLet's reinforce your understanding with a fresh set of questions!\n")

            retry_answers = []
            for i, q in enumerate(state.questions, start=1):
                print(f"\nRetry Q{i}: {q['question']}")
                for opt in q["options"]:
                    print(opt)
                ans = input("Your answer (A/B/C/D): ").strip().upper()
                retry_answers.append(ans)

            state = run_checkpoint(topic, context, retry_answers=retry_answers)

            if state.verification_score is not None:
                print(f"\nYour retry score: {state.verification_score:.1f}%")

        print("\n".join(state.messages))

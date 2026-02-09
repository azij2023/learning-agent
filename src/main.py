# main.py
from dotenv import load_dotenv
load_dotenv()

from src.state import AgentState
from src.nodes.runnables import agent_pipeline

def run_checkpoint(topic: str, context: str = "", learner_answers=None, retry_answers=None):
    """
    Run the full learning agent pipeline using the RunnableSequence.
    Returns the final AgentState with explanations, questions, scores, and messages.
    """
    state = AgentState()
    state.checkpoints = [{"topic": topic}]
    state.context_raw = context

    # Run the pipeline once
    state = agent_pipeline.invoke(state)

    # Collect learner answers if provided
    if learner_answers:
        state.learner_answers = learner_answers
        state = agent_pipeline.invoke(state)

    # Retry logic if needed
    if getattr(state, "feynman_required", False):
        if retry_answers:
            state.learner_answers = retry_answers
            state = agent_pipeline.invoke(state)

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
        print("\nExplanation:\n", getattr(state, "explanation", None))

        # Ask questions
        learner_answers = []
        print("\nAnswer the following questions:")
        for i, q in enumerate(getattr(state, "questions", []), start=1):
            print(f"\nQ{i}: {q['question']}")
            for opt in q["options"]:
                print(opt)
            ans = input("Your answer (A/B/C/D): ").strip().upper()
            learner_answers.append(ans)

        # Re-run with answers
        state = run_checkpoint(topic, context, learner_answers=learner_answers)

        if getattr(state, "verification_score", None) is not None:
            print(f"\nYour score: {state.verification_score:.1f}%")

        # Retry if needed
        if getattr(state, "feynman_required", False):
            print("\n".join(state.messages))
            print("\nLet's reinforce your understanding with a fresh set of questions!\n")

            retry_answers = []
            for i, q in enumerate(getattr(state, "questions", []), start=1):
                print(f"\nRetry Q{i}: {q['question']}")
                for opt in q["options"]:
                    print(opt)
                ans = input("Your answer (A/B/C/D): ").strip().upper()
                retry_answers.append(ans)

            state = run_checkpoint(topic, context, retry_answers=retry_answers)

            if getattr(state, "verification_score", None) is not None:
                print(f"\nYour retry score: {state.verification_score:.1f}%")

        print("\n".join(state.messages))

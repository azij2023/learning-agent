import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent 🚀")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

# Run agent once and store state
if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)

# If we have a pipeline state, show everything
if "state" in st.session_state:
    state = st.session_state.state

    # ✅ Show relevance score
    if hasattr(state, "relevance_score"):
        st.write("### Relevance Score")
        st.progress(state.relevance_score / 10)  # assuming score is 0–10
        st.write(f"Context relevance score = {state.relevance_score}")

    # ✅ Show pipeline messages
    if state.messages:
        st.write("### Pipeline Messages")
        for msg in state.messages:
            st.write(msg)

    # ✅ Show explanation
    if hasattr(state, "explanation"):
        st.write("### Explanation")
        st.write(state.explanation)

    # ✅ Show quiz
    if state.questions:
        st.write("### Quiz")
        learner_answers = []
        for i, q in enumerate(state.questions, start=1):
            selected = st.radio(
                f"Q{i}: {q['question']}",
                q["options"],
                key=f"q{i}"
            )
            if selected:
                learner_answers.append(selected.split()[0])  # capture A/B/C/D

        if st.button("Submit Answers"):
            st.session_state.state = run_checkpoint(
                topic, context, learner_answers=learner_answers
            )
            st.write(f"Your score: {st.session_state.state.verification_score:.1f}%")

            if getattr(st.session_state.state, "feynman_required", False):
                st.write("### Feynman Explanation")
                st.write("\n".join(st.session_state.state.messages))

import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)

if "state" in st.session_state:
    state = st.session_state.state

    # Show relevance score
    if hasattr(state, "relevance_score"):
        st.write("### Relevance Score")
        st.write(f"Context relevance score = {state.relevance_score}")

    # Show pipeline messages
    if state.messages:
        st.write("### Pipeline Messages")
        for msg in state.messages:
            st.write(msg)

    # Show explanation
    if hasattr(state, "explanation"):
        st.write("### Explanation")
        st.write(state.explanation)

    # First quiz
    if state.questions and not getattr(state, "feynman_required", False):
        st.write("### Quiz")
        learner_answers = []
        for i, q in enumerate(state.questions, start=1):
            selected = st.radio(f"Q{i}: {q['question']}", q["options"], key=f"q{i}")
            if selected:
                learner_answers.append(selected.split()[0])
        if st.button("Submit Answers"):
            st.session_state.state = run_checkpoint(
                topic, context, learner_answers=learner_answers
            )
            st.write(f"Your score: {st.session_state.state.verification_score:.1f}%")

    # Feynman explanation + retry quiz
    if getattr(state, "feynman_required", False):
        st.write("### Feynman Explanation")
        st.write("\n".join(state.messages))

        if state.questions:
            st.write("### Retry Quiz")
            retry_answers = []
            for i, q in enumerate(state.questions, start=1):
                selected = st.radio(f"Retry Q{i}: {q['question']}", q["options"], key=f"retry{i}")
                if selected:
                    retry_answers.append(selected.split()[0])
            if st.button("Submit Retry Answers"):
                st.session_state.state = run_checkpoint(
                    topic, context, retry_answers=retry_answers
                )
                st.write(f"Your retry score: {st.session_state.state.verification_score:.1f}%")

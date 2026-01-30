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

    # ✅ Show relevance score only
    if hasattr(state, "relevance_score"):
        st.write("### Relevance Score")
        st.progress(state.relevance_score / 10)  # assuming score is 0–10
        st.write(f"Context relevance score = {state.relevance_score}")

    # ✅ First quiz
    if state.questions and not getattr(state, "feynman_required", False):
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
            score = st.session_state.state.verification_score
            st.write(f"Your score: {score:.1f}%")

            # 🎉 Congratulate if score >=70
            if score >= 70.0:
                st.success("🎉 Congratulations! Great job on the quiz!")

    # ✅ Feynman explanation + retry quiz if required
    if getattr(state, "feynman_required", False):
        st.write("### Feynman Explanation")
        st.write("\n".join(state.messages))

        if state.questions:
            st.write("### Retry Quiz")
            retry_answers = []
            for i, q in enumerate(state.questions, start=1):
                selected = st.radio(
                    f"Retry Q{i}: {q['question']}",
                    q["options"],
                    key=f"retry{i}"
                )
                if selected:
                    retry_answers.append(selected.split()[0])
            if st.button("Submit Retry Answers"):
                st.session_state.state = run_checkpoint(
                    topic, context, retry_answers=retry_answers
                )
                retry_score = st.session_state.state.verification_score
                st.write(f"Your retry score: {retry_score:.1f}%")

                if retry_score >= 70.0:
                    st.success("🎉 Congratulations! You nailed it after retry!")

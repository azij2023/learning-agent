import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

# Run agent once and store state
if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)

if "state" in st.session_state:
    state = st.session_state.state

    # 1️⃣ Show relevance score only
    if hasattr(state, "relevance_score") and state.relevance_score is not None:
        st.write("### Relevance Score")
        st.write(f"Context relevance score = {state.relevance_score}")
    else:
        for msg in getattr(state, "messages", []):
            if "RelevanceScorer" in msg and "score" in msg.lower():
                st.write("### Relevance Score")
                st.write(msg)
                break

    # 2️⃣ Explanation + first quiz
    if hasattr(state, "explanation") and state.questions and not getattr(state, "feynman_required", False):
        st.write("### Explanation")
        st.write(state.explanation)

        st.write("### Quiz")
        learner_answers = []
        for i, q in enumerate(state.questions, start=1):
            selected = st.radio(
                f"Q{i}: {q['question']}",
                q["options"],
                key=f"q{i}"
            )
            if selected:
                learner_answers.append(selected.split()[0])

        if st.button("Submit Answers"):
            st.session_state.state = run_checkpoint(
                topic, context, learner_answers=learner_answers
            )

    # 3️⃣ Feynman explanation + retry quiz (separate block)
    state = st.session_state.state
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
                retry_state = st.session_state.state
                retry_score = retry_state.verification_score
                st.write(f"Your retry score: {retry_score:.1f}%")

                if retry_score >= 70.0:
                    st.success("🎉 Congratulations! You nailed it after retry!")

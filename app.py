import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

# Initialize flags to enforce sequence
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "feynman_done" not in st.session_state:
    st.session_state.feynman_done = False
if "retry_done" not in st.session_state:
    st.session_state.retry_done = False

# Run agent once and reset flags
if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)
    st.session_state.quiz_done = False
    st.session_state.feynman_done = False
    st.session_state.retry_done = False

if "state" in st.session_state:
    state = st.session_state.state

    # 1️⃣ Show relevance score only
    if hasattr(state, "relevance_score") and state.relevance_score is not None:
        st.write("### Relevance Score")
        st.write(f"Context relevance score = {state.relevance_score}")

    # 2️⃣ Explanation + first quiz
    if not st.session_state.quiz_done and hasattr(state, "explanation") and state.questions:
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
            st.session_state.quiz_done = True

    # ✅ Show quiz score if available
    if st.session_state.quiz_done and hasattr(state, "verification_score") and state.verification_score is not None:
        score = state.verification_score
        st.write(f"Your score: {score:.1f}%")
        if score >= 70.0:
            st.success("🎉 Congratulations! Great job on the quiz!")
        else:
            st.session_state.feynman_done = True

    # 3️⃣ Feynman explanation + retry quiz
    # 3️⃣ Feynman explanation + retry quiz
if st.session_state.feynman_done:
    st.write("### Feynman Explanation")

    # Filter messages: only show relevance score + Feynman explanation
    for msg in getattr(state, "messages", []):
        if "context relevance score" in msg.lower():
            st.write(msg)
        elif "feynman explanation" in msg.lower():
            st.write(msg)

    if not st.session_state.retry_done and state.questions:
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
            st.session_state.retry_done = True


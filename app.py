import streamlit as st
import re
from src.main import run_checkpoint

st.title("Learning Agent")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

# Initialize flags and storage
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "feynman_done" not in st.session_state:
    st.session_state.feynman_done = False
if "retry_done" not in st.session_state:
    st.session_state.retry_done = False
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "questions" not in st.session_state:
    st.session_state.questions = None
if "relevance_score" not in st.session_state:
    st.session_state.relevance_score = None

# Run agent once and reset flags
if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)
    st.session_state.quiz_done = False
    st.session_state.feynman_done = False
    st.session_state.retry_done = False
    st.session_state.explanation = getattr(st.session_state.state, "explanation", None)
    st.session_state.questions = getattr(st.session_state.state, "questions", None)
    st.session_state.relevance_score = getattr(st.session_state.state, "relevance_score", None)

if "state" in st.session_state:
    state = st.session_state.state

    # 1️⃣ Show relevance score
    score_val = None
    if hasattr(state, "relevance_score") and state.relevance_score is not None:
        score_val = state.relevance_score
    else:
        for msg in getattr(state, "messages", []):
            match = re.search(r"relevance score\s*=\s*([0-9\.]+)", msg, re.IGNORECASE)
            if match:
                score_val = float(match.group(1))
                break

    if score_val is not None:
        st.session_state.relevance_score = score_val
        st.subheader("📊 Relevance Score")
        st.metric("Context Match", f"{score_val*100:.1f}%")

    # 2️⃣ Explanation + first quiz
    if not st.session_state.quiz_done and st.session_state.explanation and st.session_state.questions:
        st.subheader("📝 Explanation")
        st.write(st.session_state.explanation)

        st.subheader("❓ Quiz")
        learner_answers = []
        for i, q in enumerate(st.session_state.questions, start=1):
            selected = st.radio(
                f"Q{i}: {q['question']}",
                q["options"],
                key=f"q{i}"
            )
            if selected:
                learner_answers.append(selected)  # ✅ capture full option text

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
            st.session_state.feynman_done = False
        else:
            st.session_state.feynman_done = True

    # 3️⃣ Feynman explanation + retry quiz
    if st.session_state.feynman_done:
        st.subheader("🧠 Feynman Explanation")
        for msg in getattr(state, "messages", []):
            if "feynman explanation" in msg.lower():
                st.write(msg)

        if not st.session_state.retry_done and st.session_state.questions:
            st.subheader("🔄 Retry Quiz")
            retry_answers = []
            for i, q in enumerate(st.session_state.questions, start=1):
                selected = st.radio(
                    f"Retry Q{i}: {q['question']}",
                    q["options"],
                    key=f"retry{i}"
                )
                if selected:
                    retry_answers.append(selected)  # ✅ full option text again

            if st.button("Submit Retry Answers"):
                st.session_state.state = run_checkpoint(
                    topic, context, retry_answers=retry_answers
                )
                st.session_state.retry_done = True

    # ✅ Show retry score if available
    if st.session_state.retry_done and hasattr(state, "verification_score") and state.verification_score is not None:
        retry_score = state.verification_score
        st.write(f"Your retry score: {retry_score:.1f}%")

        if retry_score >= 70.0:
            st.success("🎉 You nailed it after retry!")
            st.session_state.feynman_done = False
        else:
            st.warning("Score still too low (<70%). Another Feynman explanation will be triggered.")
            st.session_state.feynman_done = True
            st.session_state.retry_done = False

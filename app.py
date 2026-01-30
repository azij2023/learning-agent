import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent 🚀")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

# Run agent when button clicked
if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)

# If we have questions, show them
if "state" in st.session_state and st.session_state.state.questions:
    st.write("### Explanation")
    st.write(st.session_state.state.explanation)

    st.write("### Quiz")
    learner_answers = []
    for i, q in enumerate(st.session_state.state.questions, start=1):
        # Show radio buttons for each question
        selected = st.radio(
            f"Q{i}: {q['question']}",
            q["options"],
            key=f"q{i}"
        )
        # Store only the letter (A/B/C/D)
        learner_answers.append(selected.split()[0])

    # Submit button to evaluate answers
    if st.button("Submit Answers"):
        st.session_state.state = run_checkpoint(
            topic, context, learner_answers=learner_answers
        )
        st.write(f"Your score: {st.session_state.state.verification_score:.1f}%")

        # If Feynman explanation is required
        if getattr(st.session_state.state, "feynman_required", False):
            st.write("### Feynman Explanation")
            st.write("\n".join(st.session_state.state.messages))

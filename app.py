import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent 🚀")

topic = st.text_input("Enter a topic:")
context = st.text_area("Optional context:")

# Run agent and store state
if st.button("Run Agent"):
    st.session_state.state = run_checkpoint(topic, context)

# Display pipeline output if state exists
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

    # Show quiz
import streamlit as st
from src.main import run_checkpoint

st.title("Learning Agent 🚀")

# Input fields
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
        st.progress(state.relevance_score / 10)  # assuming
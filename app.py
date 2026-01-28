import streamlit as st

st.title("Learning Agent")

st.write("Welcome to your Streamlit app! 🚀")

# Example: read secrets securely
groq_key = st.secrets.get("GROQ_API_KEY", "Not set")
langchain_key = st.secrets.get("LANGCHAIN_API_KEY", "Not set")

st.write("Groq Key (hidden in Streamlit Cloud):", groq_key[:4] + "****")
st.write("LangChain Key (hidden in Streamlit Cloud):", langchain_key[:4] + "****")

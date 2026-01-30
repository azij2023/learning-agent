import streamlit as st
from groq import Groq

# Load Groq key from secrets
groq_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=groq_key)

st.title("Learning Agent 🚀")
user_input = st.text_input("Ask me anything:")

if user_input:
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",  # Groq model
        messages=[{"role": "user", "content": user_input}],
    )
    st.write("Answer:", response.choices[0].message.content)

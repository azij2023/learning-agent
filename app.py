import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Learning Agent")
user_input = st.text_input("Ask me anything:")

if user_input.strip():
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",   # ✅ valid Groq model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
    )
    st.write("Answer:", response.choices[0].message.content)

# src/nodes/topic_explainer.py
from src.state import AgentState
from groq import Groq
import os

def topic_explainer(state: AgentState) -> AgentState:
    checkpoint = state.checkpoints[state.checkpoint_index]
    topic = checkpoint["topic"]
    context = state.context_raw[:800] if state.context_raw else ""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""Explain the topic "{topic}" clearly for a beginner.
Use this context if helpful:
{context}
Keep it under 300 words, structured, and easy to understand."""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  
    messages=[
        {"role": "system", "content": "You are a helpful tutor."},
        {"role": "user", "content": prompt}
    ]
    )


    state.explanation = response.choices[0].message.content
    state.messages.append(f"TopicExplainer: explained {topic} with Groq")
    return state

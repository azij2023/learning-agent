# src/nodes/feynman.py
from src.state import AgentState
from groq import Groq
import os

def feynman_node(state: AgentState) -> AgentState:
    topic = state.checkpoints[state.checkpoint_index]["topic"]

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
    Explain the topic "{topic}" in very simple language,
    as if teaching a beginner or a child.
    Use analogies and avoid jargon.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful teacher using the Feynman technique."},
            {"role": "user", "content": prompt}
        ]
    )

    explanation = response.choices[0].message.content.strip()

    # Save explanation in state and messages (no direct print)
    state.feynman_explanation = explanation
    state.messages.append(f"Feynman Explanation:\n{explanation}")

    return state

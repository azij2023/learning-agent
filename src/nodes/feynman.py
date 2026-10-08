# src/nodes/feynman.py
from src.state import AgentState
from groq import Groq
import os

def feynman_node(state: AgentState) -> AgentState:
    topic = state.checkpoints[state.checkpoint_index]["topic"]

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""Re-teach "{topic}" to a beginner using the Feynman technique.

Explain the main idea in plain language, define any necessary jargon, and use a familiar analogy
plus one concrete example. Break it into a few short sections with descriptive headings and bullets.
Do not use Markdown tables. Do not merely repeat the previous explanation."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a helpful teacher using the Feynman technique."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    explanation = (response.choices[0].message.content or "").strip()

    # Save explanation in state and messages (no direct print)
    state.feynman_explanation = explanation
    state.messages.append(f"Feynman Explanation:\n{explanation}")

    return state

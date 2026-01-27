# src/nodes/gather_context.py
from src.state import AgentState
from groq import Groq
import os

def gather_context(state: AgentState) -> AgentState:
    """
    Collect raw context for the current checkpoint.
    Priority:
      1. Use user-provided notes if available.
      2. Otherwise, auto-fetch context using Groq (or later, web search).
    """

    topic = state.checkpoints[state.checkpoint_index]["topic"]
    context = state.context_raw.strip()

    # Case 1: User provided notes
    if context:
        state.messages.append("ContextGatherer: using user-provided notes")
        return state

    # Case 2: No notes → auto-generate context
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""Provide a concise background summary (200 words max) about the topic "{topic}".
Focus on definitions, key concepts, and examples that would help a learner understand it.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast model for context fetching
        messages=[
            {"role": "system", "content": "You are a helpful context gatherer."},
            {"role": "user", "content": prompt}
        ]
    )

    state.context_raw = response.choices[0].message.content.strip()
    state.messages.append("ContextGatherer: auto-fetched context with Groq")
    return state

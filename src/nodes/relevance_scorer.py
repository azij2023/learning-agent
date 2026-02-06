# src/nodes/relevance_scorer.py
from src.state import AgentState
from groq import Groq
import os

def relevance_scorer(state: AgentState) -> AgentState:
    topic = state.checkpoints[state.checkpoint_index]["topic"]
    context = state.context_raw

    if not context:
        state.messages.append("RelevanceScorer: no context provided, skipping scoring")
        state.relevance_score = None
        return state

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""Evaluate how relevant the following context is to the topic "{topic}".
Return only a numeric score between 1 and 5, where:
1 = completely irrelevant
3 = partially relevant
5 = highly relevant and directly supports the topic.

Context:
{context}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict relevance scorer."},
            {"role": "user", "content": prompt}
        ]
    )

    score_text = response.choices[0].message.content.strip()

    try:
        score_val = float(score_text)
    except ValueError:
        score_val = None

    state.relevance_score = score_val
    state.messages.append(f"RelevanceScorer: context relevance score = {score_text}")
    return state

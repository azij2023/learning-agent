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
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Rate context relevance from 1 to 5. Return only a numeric score.",
            },
            {
                "role": "user",
                "content": f'Topic: "{topic}"\n\nContext:\n{context}',
            },
        ],
    )
    result = response.choices[0].message.content.strip()

    try:
        score = float(result)
        if not 1 <= score <= 5:
            raise ValueError("Relevance score must be between 1 and 5")
        state.relevance_score = score / 5
    except ValueError:
        state.relevance_score = None

    state.messages.append(f"RelevanceScorer: context relevance score = {result}")
    return state

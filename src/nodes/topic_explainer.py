# src/nodes/topic_explainer.py
from src.state import AgentState
from groq import Groq
import os

def topic_explainer(state: AgentState) -> AgentState:
    checkpoint = state.checkpoints[state.checkpoint_index]
    topic = checkpoint["topic"]
    context = state.context_raw[:800] if state.context_raw else ""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""Teach "{topic}" to a beginner in a clear, accurate, self-contained lesson.

Use the supplied context as supporting information, but correct obvious errors and do not invent facts:
{context or "(No additional context supplied.)"}

Use readable Markdown with a short title, descriptive headings, short paragraphs, and bullet lists.
Explain key terms in plain language and include a concrete example or analogy.
Do not use Markdown tables. Do not include literal Markdown syntax as quoted text.
Keep the lesson focused and under 350 words."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a patient, accurate tutor. Return a polished Markdown lesson, not instructions about how to write one.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    state.explanation = (response.choices[0].message.content or "").strip()
    state.messages.append(f"TopicExplainer: explained {topic} with Groq")
    return state

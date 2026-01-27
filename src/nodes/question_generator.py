# src/nodes/question_generator.py
from src.state import AgentState
from groq import Groq
import os
import json

def question_generator(state: AgentState) -> AgentState:
    checkpoint = state.checkpoints[state.checkpoint_index]
    topic = checkpoint["topic"]

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
Generate 5 multiple-choice questions (MCQs) on the topic "{topic}".
Return ONLY valid JSON. Do not include any text outside the JSON.
Format:
[
  {{
    "question": "...",
    "options": ["A ...", "B ...", "C ...", "D ..."],
    "answer": "A",
    "explanation": "..."
  }},
  ...
]
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ updated
        messages=[
            {"role": "system", "content": "You are a precise question generator."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_content = response.choices[0].message.content.strip()

    try:
        # Parse JSON string into Python list of dicts
        state.questions = json.loads(raw_content)
        state.messages.append(f"QuestionGenerator: parsed MCQs for {topic}")
    except Exception as e:
        # Fallback: keep empty list if parsing fails
        state.questions = []
        state.messages.append(f"QuestionGenerator: failed to parse MCQs → {e}")

    return state

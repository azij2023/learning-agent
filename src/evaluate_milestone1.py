# src/evaluate_milestone1.py
import os
from dotenv import load_dotenv
from src.state import AgentState
from src.nodes.relevance_scorer import relevance_scorer

load_dotenv()

# Define 5–10 sample checkpoints
checkpoints = [
    {"topic": "Machine Learning", "objectives": ["Understand supervised vs unsupervised learning"]},
    {"topic": "Neural Networks", "objectives": ["Explain feedforward vs recurrent networks"]},
    {"topic": "Decision Trees", "objectives": ["Know how splitting criteria work"]},
    {"topic": "Reinforcement Learning", "objectives": ["Understand reward signals and policies"]},
    {"topic": "Support Vector Machines", "objectives": ["Explain margin maximization"]},
]

def run_evaluation():
    scores = []
    for cp in checkpoints:
        state = AgentState()
        state.checkpoints = [cp]
        state.context_raw = f"Context notes about {cp['topic']} for testing relevance scoring."

        # Run relevance scorer
        state = relevance_scorer(state)

        # Extract score text from last message
        last_msg = state.messages[-1]
        print(f"{cp['topic']} → {last_msg}")

        try:
            score = int("".join([c for c in last_msg if c.isdigit()]))
            scores.append(score)
        except ValueError:
            print("⚠️ Could not parse score, skipping.")

    if scores:
        avg_score = sum(scores) / len(scores)
        print("\nAverage relevance score:", avg_score)
        if avg_score >= 4:
            print("✅ Success: Milestone 1 achieved (≥4/5 average relevance).")
        else:
            print("❌ Needs improvement: Average relevance below 4/5.")

if __name__ == "__main__":
    run_evaluation()

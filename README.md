# 🚀 Autonomous Learning Agent with Checkpoint Verification & Feynman Pedagogy

An AI-powered learning agent built with **LangGraph** and **LangChain**, designed to guide learners through structured checkpoints, verify understanding, and apply the **Feynman Technique** when comprehension falls below threshold.

---

## 📊 Architecture Overview

```mermaid
flowchart TD
    A[Define Checkpoint] --> B[Gather Context]
    B --> C[Validate Context]
    C --> D[Process Context]
    D --> E[Generate Questions]
    E --> F[Assess Learner]
    F --> G{Score >= 70%?}
    G -->|Yes| H[Mark Complete & Progress]
    G -->|No| I[Feynman Teaching]
    I --> E
    H --> J[Next Checkpoint or End]
🎯 Project Objectives
Structured guidance through checkpoints

Flexible context (notes + web search)

Rigorous assessment with ≥70% threshold

Adaptive simplification using Feynman pedagogy

Mastery-based progression

Interactive learner interface

🛠️ Tech Stack
Python

LangGraph (stateful learning workflow)

LangChain (LLM integration, embeddings, search)

LLM APIs (Gemini, OpenAI, Claude)

Vector Stores (FAISS, ChromaDB)

Streamlit (UI deployment)

📌 Milestones
Milestone	Focus	Deliverables	Status
1	Checkpoint Structure & Context Gathering	Environment setup, checkpoint schema, context validation	✅ Completed
2	Context Processing & Initial Verification	Chunking, embeddings, question generation, scoring logic	✅ Completed
3	Feynman Teaching Implementation	Adaptive explanations, loop-back mechanism	✅ Completed
4	Integration & End-to-End Testing	Full workflow, multi-checkpoint progression, UI	✅ Completed
📈 Results
Reliable context gathering (avg relevance ≥4/5)

Accurate question generation (>80% relevance)

Scoring logic validated (>90% accuracy)

Feynman explanations rated “simpler” in >80% of cases

End-to-end learning path completion in >80% of test runs

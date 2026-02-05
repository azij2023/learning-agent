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




Feynman explanations rated “simpler” in >80% of cases

End-to-end learning path completion in >80% of test runs

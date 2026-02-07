from src.state import AgentState
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from src.nodes.groq_llm import GroqLLM

def relevance_scorer(state: AgentState) -> AgentState:
    topic = state.checkpoints[state.checkpoint_index]["topic"]
    context = state.context_raw

    if not context:
        state.messages.append("RelevanceScorer: no context provided, skipping scoring")
        state.relevance_score = None
        return state

    llm = GroqLLM()
    prompt = PromptTemplate.from_template(
        """Evaluate how relevant the following context is to the topic "{topic}".
Return only a numeric score between 1 and 5.

Context:
{context}"""
    )

    # ✅ Build a Runnable sequence instead of LLMChain
    chain = RunnableSequence(prompt | llm)

    # ✅ Run the chain
    result = chain.invoke({"topic": topic, "context": context}).strip()

    try:
        state.relevance_score = float(result)
    except ValueError:
        state.relevance_score = None

    state.messages.append(f"RelevanceScorer: context relevance score = {result}")
    return state

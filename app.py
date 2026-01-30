import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict

# Define state
class AgentState(TypedDict):
    question: str
    answer: str

# Node function
def ask_llm(state: AgentState) -> AgentState:
    llm = ChatOpenAI(api_key=st.secrets["LANGCHAIN_API_KEY"], model="gpt-4o-mini")
    response = llm.invoke(state["question"])
    return {"question": state["question"], "answer": response.content}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("llm", ask_llm)
graph.set_entry_point("llm")
graph.set_finish_point("llm")
app = graph.compile()

# Streamlit UI
st.title("Learning Agent 🚀")
user_input = st.text_input("Ask me anything:")
if user_input:
    result = app.invoke({"question": user_input})
    st.write("Answer:", result["answer"])

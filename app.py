"""
LangGraph Chatbot Workflow
==========================
Defines a simple conversational workflow using LangGraph + Google Gemini.
Used by chatbot_st.py as the backend for the Streamlit chatbot UI.
"""

import os
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.checkpoint.memory import MemorySaver

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_output_tokens=4096,
)

# ---------------------------------------------------------------------------
# Graph node
# ---------------------------------------------------------------------------
def chatbot_node(state: MessagesState):
    """Invoke the LLM with the current message history."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile with a memory checkpointer so we can persist threads
memory = MemorySaver()
workflow = graph_builder.compile(checkpointer=memory)

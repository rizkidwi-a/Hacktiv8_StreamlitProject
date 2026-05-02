from langgraph.graph.message import BaseMessage
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from app import workflow
from dotenv import load_dotenv
import streamlit as st
import uuid
import os

load_dotenv()

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat():
    new_id = generate_thread_id()
    st.session_state["thread_id"] = new_id
    add_thread(new_id)
    st.session_state["messages_history"] = []

def load_conversation(thread_id):
    try:
        state = workflow.get_state({"configurable": {"thread_id": thread_id}})
        return state.values.get("messages", [])
    except Exception as e:
        st.error(f"Failed to load conversation: {str(e)}")
        return []

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(x.get("text", "") for x in content)
    if isinstance(content, dict):
        return content.get("text", "")
    return str(content)

if "messages_history" not in st.session_state:
    st.session_state["messages_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread(st.session_state["thread_id"])

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Chat History", divider="blue")

for tid in st.session_state["chat_threads"][ : : -1]:
    if st.sidebar.button(tid):
        st.session_state["thread_id"] = tid
        msgs = load_conversation(tid)
        temp = []
        for msg in msgs:
            if isinstance(msg, HumanMessage):
                role = "user"
                content = msg.content
            else:
                role = "assistant"
                content = extract_text(msg.content)
            temp.append({"role": role, "content": content})
        st.session_state["messages_history"] = temp

for m in st.session_state["messages_history"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

user_input = st.chat_input("Ask a question")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state["messages_history"].append({"role": "user", "content": user_input})
    
    CONFIG = {
        "configurable": {
            "thread_id": st.session_state["thread_id"],
        }
    }
    
    def stream_response():
        for msg, meta in workflow.stream(
            {"messages": [("user", user_input)]},
            config=CONFIG,
            stream_mode="messages",
        ):
            if isinstance(msg, AIMessage) and msg.content:
                yield extract_text(msg.content)
            
    with st.chat_message("assistant"): 
        final_text = st.write_stream(stream_response())
        
    st.session_state["messages_history"].append(
        {"role": "assistant", "content": final_text} )
         
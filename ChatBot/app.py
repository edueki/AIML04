# app.py
import streamlit as st
from rag import RAGPipeline
#from langchain_rag import RAGPipeline

st.set_page_config(page_title="Valaxy Chatbot", page_icon="💬", layout="centered")
st.title("💬 Valaxy Chatbot")

# init RAG once
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline(
        data_path="data.csv",
        collection_name="faqs",
        persist_path="./chat_vectorDB",
    )

# simple chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Your personal assistant is here! Ask me anything."}
    ]

# render history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# chat input
user_q = st.chat_input("Type your question…")
if user_q:
    # show user
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    # get answer (simple + minimal)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                answer = st.session_state.rag.answer(user_q)
            except Exception as e:
                answer = f"Sorry—something went wrong: {e}"
        st.markdown(answer)

    # store assistant reply
    st.session_state.messages.append({"role": "assistant", "content": answer})

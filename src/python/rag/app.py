import os
import tempfile
import streamlit as st
from streamlit_chat import message

from grongier.pex import Director

_service = Director.create_python_business_service("ChatService")
_service.clear()

st.set_page_config(page_title="ChatIRIS")


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def read_and_save_file():
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False,suffix=f".{file.name.split('.')[-1]}") as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)

def rag_enabled():
    if len(st.session_state["file_uploader"]) <= 0:
        # pop an alert
        st.error("Please ingest a document first")
        # uncheck the checkbox
        st.session_state["rag_enabled"] = False


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = _service

    st.header("ChatIRIS")

    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf", "md", "txt"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    # add a toggle button to enable/disable RAG
    st.subheader("Enable RAG")
    st.checkbox("Enable RAG", key="rag_enabled", on_change=rag_enabled)

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()
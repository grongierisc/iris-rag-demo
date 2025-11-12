import os
import tempfile
import time
import streamlit as st
from streamlit_chat import message

from iop import Director

_service = Director.create_python_business_service("ChatService")

st.set_page_config(page_title="ChatIRIS")


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.spinner(f"Thinking about {user_text}"):
            rag_enabled = False
            if len(st.session_state["file_uploader"]) > 0:
                rag_enabled = True
            time.sleep(1) # help the spinner to show up
            agent_text = _service.ask(user_text, rag_enabled)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def read_and_save_file():

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False,suffix=f".{file.name.split('.')[-1]}") as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.spinner(f"Ingesting {file.name}"):
            _service.ingest(file_path)
        os.remove(file_path)

    if len(st.session_state["file_uploader"]) > 0:
        st.session_state["messages"].append(
            ("File(s) successfully ingested", False)
        )

    if len(st.session_state["file_uploader"]) == 0:
        _service.clear()
        st.session_state["messages"].append(
            ("Clearing all data", False)
        )

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        _service.clear()

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

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()
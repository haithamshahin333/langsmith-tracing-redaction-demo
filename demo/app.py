"""Streamlit chat UI for the compliance demo."""

import uuid

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agent import create_support_agent, stream_agent  # noqa: E402
from redaction import presidio_available  # noqa: E402

st.set_page_config(page_title="Acme Galactic Financial Services", layout="centered")
st.title("Acme Galactic Financial Services")
st.caption("Customer Support Portal")

# --- Sidebar: observability controls -----------------------------------------

with st.sidebar:
    st.header("Observability")
    redaction_enabled = st.toggle("PII Redaction", value=True)

    if redaction_enabled:
        st.success("Traces are redacted before leaving this process.")
        layers = ["Regex (email, SSN, phone, credit card, account ID)"]
        if presidio_available():
            layers.append("Presidio NLP (names, addresses)")
        else:
            layers.append("Presidio NLP — *not installed, regex only*")
        st.caption("Active redaction layers:")
        for layer in layers:
            st.caption(f"  \u2022 {layer}")
    else:
        st.warning("Traces contain raw PII — for demo comparison only.")

    st.divider()
    st.caption(
        "Toggle redaction off, send a message, then toggle it back on and "
        "send the same message. Compare the two traces in LangSmith — "
        "filter by the `redaction_mode` metadata tag."
    )

# --- Agent (cached) ----------------------------------------------------------


@st.cache_resource
def get_agent():
    return create_support_agent()


agent = get_agent()

# --- Chat history -------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---------------------------------------------------------------

if prompt := st.chat_input("Ask about your account..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(
            stream_agent(
                agent,
                prompt,
                st.session_state.messages[:-1],  # history excludes current input
                redaction_enabled,
                st.session_state.thread_id,
            )
        )

    st.session_state.messages.append({"role": "assistant", "content": response})

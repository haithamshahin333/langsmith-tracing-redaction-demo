"""Customer support agent for Acme Galactic Financial Services."""

import json
import os

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_core.tracers.langchain import LangChainTracer

from mock_data import find_customer
from redaction import get_langsmith_client

SYSTEM_PROMPT = """You are a customer support agent for Acme Galactic Financial Services.

You help customers check their account balances, review recent transactions,
and answer questions about their accounts.

When a customer provides identifying information (name, email, or account ID),
use the lookup_customer_account tool to retrieve their account details before
responding.

Be friendly, professional, and concise."""


@tool
def lookup_customer_account(identifier: str) -> str:
    """Look up a customer account by name, email, or account ID.

    Use this when a customer asks about their account, balance,
    or transaction history. Pass the customer's name, email address,
    or account ID as the identifier.
    """
    customer = find_customer(identifier)
    if customer:
        return json.dumps(customer, indent=2)
    return "No account found for the given identifier."


def create_llm():
    """Create the LLM, auto-detecting OpenAI vs Azure OpenAI from env vars."""
    if os.getenv("AZURE_OPENAI_API_KEY"):
        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-08-01-preview"),
        )

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"))


def create_support_agent():
    """Build the agent graph (cached at app startup)."""
    llm = create_llm()
    return create_agent(llm, [lookup_customer_account], system_prompt=SYSTEM_PROMPT)


def _build_config(redaction_enabled: bool, thread_id: str) -> dict:
    """Build the LangGraph config with tracer and metadata."""
    client = get_langsmith_client(redaction_enabled)
    project = os.getenv("LANGSMITH_PROJECT", "compliance-demo")
    tracer = LangChainTracer(client=client, project_name=project)
    return {
        "callbacks": [tracer],
        "metadata": {
            "redaction_mode": "on" if redaction_enabled else "off",
            "thread_id": thread_id,
        },
    }


def _build_messages(user_input: str, history: list[dict]) -> list:
    """Convert Streamlit chat history to LangChain messages."""
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_input))
    return messages


def stream_agent(
    agent,
    user_input: str,
    history: list[dict],
    redaction_enabled: bool,
    thread_id: str,
):
    """Stream the agent response token-by-token."""
    config = _build_config(redaction_enabled, thread_id)
    messages = _build_messages(user_input, history)

    for chunk, metadata in agent.stream(
        {"messages": messages},
        config=config,
        stream_mode="messages",
    ):
        if chunk.content and metadata.get("langgraph_node") == "model":
            yield chunk.content

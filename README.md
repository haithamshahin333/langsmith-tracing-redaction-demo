# Compliant AI Observability Demo

A Streamlit chatbot demonstrating LangSmith tracing with client-side PII redaction, mapped to the NIST AI Risk Management Framework. See the [blog post](docs/blog-post.md) for the full writeup.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- A [LangSmith](https://smith.langchain.com/) account (free tier works)
- An OpenAI API key **or** Azure OpenAI deployment

## Setup

```bash
# Install dependencies
uv sync

# Copy and configure environment variables
cp demo/.env.example demo/.env
# Edit demo/.env: add LANGSMITH_API_KEY and OPENAI_API_KEY (or Azure OpenAI vars)

# (Optional) Install spaCy model for Presidio NLP name/address detection
uv pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl"
```

Without the spaCy model, redaction falls back to regex-only (emails, SSNs, phones, credit cards, account IDs). Presidio adds detection of person names and street addresses.

## Run

```bash
uv run streamlit run demo/app.py
```

Open http://localhost:8501 in your browser.

## Example Queries

- "I'm Leia Organa, can you show me my recent transactions?"
- "My email is han.solo@millenniumfalcon.net, what's my balance?"
- "I'm Din Djarin, I need to dispute the Beskar charge on my account."
- "Can you look up account ACT-40088 for Padme Amidala?"

Toggle **PII Redaction** on/off in the sidebar, then compare traces in LangSmith by filtering on the `redaction_mode` metadata tag.

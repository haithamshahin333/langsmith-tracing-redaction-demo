"""PII redaction for LangSmith traces.

Two layers:
  1. Regex patterns — catches structured PII (emails, SSNs, phones, credit cards)
  2. Presidio NLP  — catches unstructured PII (names, addresses)

Presidio is optional. If not installed or the spacy model is missing,
only regex redaction is used.
"""

import re

from langsmith import Client
from langsmith.anonymizer import create_anonymizer

# --- Regex patterns -----------------------------------------------------------

_PATTERNS = [
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "<EMAIL>"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "<SSN>"),
    (re.compile(r"\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"), "<PHONE>"),
    (re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"), "<CREDIT_CARD>"),
    (re.compile(r"\bACT-\d{4,6}\b"), "<ACCOUNT_ID>"),
]


def _regex_redact(text: str) -> str:
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text


# --- Presidio NLP (lazy-initialized) -----------------------------------------

_PRESIDIO_ENTITIES = [
    "PERSON",
    "PHONE_NUMBER",
    "EMAIL_ADDRESS",
    "US_SSN",
    "CREDIT_CARD",
    "LOCATION",
]

_presidio_state = {"checked": False, "available": False, "analyzer": None, "anonymizer": None}


def _init_presidio():
    """Try to initialize Presidio. Only runs once."""
    if _presidio_state["checked"]:
        return _presidio_state["available"]
    _presidio_state["checked"] = True
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_anonymizer import AnonymizerEngine

        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        # Verify the spacy model works
        analyzer.analyze(text="John Smith lives in Seattle", language="en")
        _presidio_state["analyzer"] = analyzer
        _presidio_state["anonymizer"] = anonymizer
        _presidio_state["available"] = True
    except Exception:
        _presidio_state["available"] = False
    return _presidio_state["available"]


def presidio_available() -> bool:
    return _init_presidio()


def _presidio_redact(text: str) -> str:
    if not _init_presidio():
        return text
    results = _presidio_state["analyzer"].analyze(
        text=text, entities=_PRESIDIO_ENTITIES, language="en"
    )
    if results:
        return _presidio_state["anonymizer"].anonymize(
            text=text, analyzer_results=results
        ).text
    return text


# --- Combined redaction -------------------------------------------------------


def redact(text: str) -> str:
    """Apply all redaction layers to a string."""
    text = _regex_redact(text)
    text = _presidio_redact(text)
    return text


# --- LangSmith client factory -------------------------------------------------


def get_langsmith_client(redaction_enabled: bool) -> Client:
    """Return a LangSmith Client with or without PII redaction."""
    if redaction_enabled:
        anonymizer = create_anonymizer(redact)
        return Client(anonymizer=anonymizer)
    return Client()

from pathlib import Path

# Project Paths

DOCS_DIR = Path("docs")

FAISS_INDEX = Path("store.faiss")

CHUNKS_FILE = Path("store_chunks.pkl")

# Supported Files


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt"
}

# Streamlit

APP_TITLE = " 🚀 FlexRAG"

APP_DESCRIPTION = (
    "Local & Cloud AI-powered document retrieval with multi-document RAG,  "
    "source attribution and pluggable LLM providers."
)

PAGE_ICON = "🧠"

PAGE_LAYOUT = "wide"

import os

ALLOW_OLLAMA = os.getenv("ALLOW_OLLAMA", "true").lower() == "true"
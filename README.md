

# 🚀 FlexRAG

> **Local & Cloud AI-powered Retrieval-Augmented Generation (RAG) platform for intelligent multi-document question answering.**

FlexRAG is an end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF and TXT documents, build a semantic knowledge base using FAISS, and ask natural language questions with source-grounded answers.

The application supports both:

- 🖥️ Local inference using Ollama
- ☁️ Cloud inference using Groq API

Developed by **Mohd Rayyan**

---

## ✨ Features

- 📄 Upload multiple PDF and TXT documents
- 🧠 Semantic search using Sentence Transformers
- ⚡ FAISS vector database
- 🤖 Retrieval-Augmented Generation (RAG)
- 🖥️ Local LLM support (Ollama)
- ☁️ Cloud LLM support (Groq)
- 🔄 Switch between Local and Cloud inference
- 💬 Conversation history
- 📚 Source attribution with page numbers
- 🗂️ Built-in document manager
- 🗑️ Delete indexed documents directly from the UI
- ⚙️ Automatic knowledge base rebuilding after document updates
- 🎨 Clean Streamlit interface

---

# 🏗 Architecture

```
                 Documents
                     │
           PDF / TXT Loader
                     │
             Text Chunking
                     │
      Sentence Transformer Embeddings
                     │
              FAISS Vector Store
                     │
           Semantic Similarity Search
                     │
         Retrieved Context Chunks
                     │
        ┌────────────┴────────────┐
        │                         │
   Ollama (Local)          Groq API (Cloud)
        │                         │
        └────────────┬────────────┘
                     │
              Final Response
```

---

# 📂 Project Structure

```
FlexRAG/
│
├── docs/                   # Uploaded documents
├── utils/
│   ├── constants.py
│   ├── file_manager.py
│   ├── llm_factory.py
│   └── ui_components.py
│
├── app.py                  # Streamlit application
├── build_index.py          # Builds FAISS index
├── embed_store.py          # Embedding & vector storage
├── retriever.py            # Semantic retrieval
├── rag_chain.py            # RAG pipeline
├── load_file.py            # PDF/TXT loading
├── agent.py                # Future AI Agent module
├── main.py                 # Future CLI entry point
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/reyan-000/FlexRAG.git

cd FlexRAG
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running FlexRAG

```bash
python -m streamlit run app.py
```

---

# 🖥 Local Mode

Requirements

- Ollama installed
- Supported model downloaded

Example

```bash
ollama pull phi3:mini
```

No API key required.

Works completely offline after setup.

---

# ☁ Cloud Mode

Requirements

- Groq API Key
- Internet connection

Paste your API key into the sidebar and choose the desired model.

No Ollama installation required.

---

# 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Sentence Transformers
- Ollama
- Groq API
- PyMuPDF

---

# 🚀 Future Roadmap

- Hybrid Search (BM25 + Vector Search)
- Cross-Encoder Re-ranking
- OCR Support
- DOCX and Markdown support
- Image-aware RAG
- Streaming Responses
- REST API
- Desktop Application
- AI Agent Integration
- Authentication
- Docker Support

---

# 👨‍💻 About

Developed by **Mohd Rayyan**

AI • Machine Learning • Automation • Retrieval-Augmented Generation

GitHub:
https://github.com/reyan-000


---

# 📜 License

This project is licensed under the MIT License.

---

⭐ If you found FlexRAG useful, consider starring the repository.python -m streamlit run app.py
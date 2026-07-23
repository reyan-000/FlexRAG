
from langchain_core.prompts import PromptTemplate

from utils.llm_factory import get_llm

from retriever import retrieve

from embed_store import VectorStore




from pathlib import Path

def load_vector_store():
    """
    Load the latest FAISS index from disk.
    """

    if not Path("store.faiss").exists():
        raise FileNotFoundError(
            "Knowledge base not found.\n"
            "Run: python build_index.py"
        )

    vs = VectorStore()
    vs.load()

    return vs

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant. Answer ONLY using the context below.
If the context does not contain the answer, say "I don't know."

Context:
{context}

Question: {question}

Answer:
"""
)


# Encapsulating this logic keeps our codebase modular and testable
def rag_answer(
    question,
    provider="ollama",
    model="phi3:mini",
    api_key=None
    ):
    vs= load_vector_store()
    hits = retrieve(question, vs, k=4)

    if not hits:
        return {
            "answer": "I couldn't find relevant information in the indexed documents.",
            "sources": []
        }

    context = "\n---\n".join(h["text"] for h in hits)
    prompt = RAG_PROMPT.format(context=context, question=question)
    llm = get_llm(
    provider=provider,
    model=model,
    api_key=api_key
    )
    answer = llm.invoke(prompt)
    if hasattr(answer, "content"):
        answer = answer.content
    sources = []

    for h in hits:

        source = {
            "title": h["source"],
            "page": h["page"],
            "preview": h["text"][:350] + "..."
            if len(h["text"]) > 350
            else h["text"]
        }

        sources.append(source)
        
    return {"answer": answer.strip(), "sources": sources}

if __name__ == "__main__":
    result = rag_answer("What is retrieval-augmented generation?")
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])
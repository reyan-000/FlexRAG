
from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_chain import rag_answer
from agent import ask_agent  

app = FastAPI(title="RAG Knowledge Assistant")

class ChatRequest(BaseModel):
    question: str
    mode: str = "rag"  # "rag" or "agent"

class ChatResponse(BaseModel):
    answer: str
    sources: list = []


# This decorator exposes the function directly as a REST API endpoint
@app.post("/chat", response_model=ChatResponse)

# async functions run concurrently, freeing up the thread while waiting for I/O tasks
async def chat(req: ChatRequest):
    if req.mode == "agent":
        answer = ask_agent(req.question)
        return {"answer": answer, "sources": []}
    result = rag_answer(req.question)
    return result

@app.get("/health")

async def health():
    return {"status": "ok"}

# minimal JS snippet to call this endpoint from a browser:
# fetch("/chat", { method: "POST",
#   headers: { "Content-Type": "application/json" },
#   body: JSON.stringify({ question: input.value, mode: "rag" }) })
#   .then(r => r.json()).then(d => renderAnswer(d.answer, d.sources));

# Run with: uvicorn main:app --reload --port 8000
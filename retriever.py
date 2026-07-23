
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


# Encapsulating this logic keeps our codebase modular and testable
def retrieve(query, vector_store, k=5):
    """Return top-k chunk texts with their L2 distances."""
    q_vec = model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = vector_store.index.search(q_vec, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        
        metadata = vector_store.chunks[idx]

        results.append(
            {
                "text": metadata["text"],
                "source": metadata["source"],
                "page": metadata["page"],
                "distance": float(dist)
            }
        )
        
    return results

if __name__ == "__main__":
    
    from embed_store import VectorStore
    vs = VectorStore()
    vs.load("store.faiss")
    hits = retrieve("How does FAISS search work?", vs, k=3)
    for i, h in enumerate(hits):
        print(f"[{i+1}] distance={h['distance']:.4f}")

        print(f"Source   : {h['source']}")
        print(f"Page     : {h['page']}")
        print(f"Distance : {h['distance']:.4f}")
        print(f"Text     : {h['text'][:160]}")
        print("-" * 60)
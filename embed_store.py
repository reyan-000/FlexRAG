import faiss
import pickle
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


class VectorStore:
    """
    Handles vector embedding, storage, saving and loading.
    """

    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add_chunks(self, chunks):
        """
        Embed metadata chunks and store them.
        """

        if not chunks:
            print("No chunks provided.")
            return

        # Extract only the text for embeddings
        texts = [chunk["text"] for chunk in chunks]

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        ).astype("float32")

        self.index.add(embeddings)

        # Save complete metadata
        self.chunks.extend(chunks)

        print(f"Indexed {len(chunks)} chunks.")
        print(f"Total vectors: {self.index.ntotal}")
    

    def save(
        self,
        faiss_path="store.faiss",
        chunks_path="store_chunks.pkl"
    ):
        """Save FAISS index and chunk list."""

        faiss.write_index(self.index, faiss_path)

        with open(chunks_path, "wb") as f:
            pickle.dump(self.chunks, f)

    def load(
        self,
        faiss_path="store.faiss",
        chunks_path="store_chunks.pkl"
    ):
        """Load FAISS index and chunk list."""

        self.index = faiss.read_index(faiss_path)

        with open(chunks_path, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"Loaded {self.index.ntotal} vectors.")
        print(f"Loaded {len(self.chunks)} chunks.")


if __name__ == "__main__":

    print(
        "\nVectorStore module loaded successfully."
        "\nUse build_index.py to create an index."
    )
from pathlib import Path
from load_file import (
    load_text,
    load_pdf_pages,
    chunk_text
)
from embed_store import VectorStore

from utils.constants import DOCS_DIR, SUPPORTED_EXTENSIONS


def build_index():
    """
    Build a FAISS vector index from all supported documents
    inside the docs/ folder.
    """

    if not DOCS_DIR.exists():
        raise FileNotFoundError(
            f"'{DOCS_DIR}' folder not found. Please create it and add documents."
        )

    files = sorted(
        [
            file
            for file in DOCS_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    )

    if not files:
        raise ValueError(
            "No supported (.pdf/.txt) files found inside the docs folder."
        )

    print("=" * 60)
    print("Building Knowledge Base")
    print("=" * 60)

    all_chunks = []

    processed_files = 0
    skipped_files = 0

    for file in files:

        print(f"\nReading: {file.name}")
        
        try:

            metadata_chunks = []

            if file.suffix.lower() == ".pdf":

                pages = load_pdf_pages(file)

                if not pages:
                    print(f"⚠ '{file.name}' contains no extractable text.")
                    skipped_files += 1
                    continue

                for page in pages:

                    chunks = chunk_text(page["text"])

                    for chunk in chunks:

                        metadata_chunks.append(
                            {
                                "text": chunk,
                                "source": file.name,
                                "page": page["page"]
                            }
                        )

            else:

                text = load_text(file)

                if not text.strip():
                    print(f"⚠ '{file.name}' contains no text.")
                    skipped_files += 1
                    continue

                chunks = chunk_text(text)

                for chunk in chunks:

                    metadata_chunks.append(
                        {
                            "text": chunk,
                            "source": file.name,
                            "page": None
                        }
                    )

        except Exception as e:

            print(f"❌ Skipping '{file.name}'")
            print(f"   Reason: {e}")
            skipped_files += 1
            continue

        if not metadata_chunks:
            print(f"⚠ No chunks generated for '{file.name}'.")
            skipped_files += 1
            continue

        print(f"✓ Chunks created: {len(metadata_chunks)}")

        all_chunks.extend(metadata_chunks)

        processed_files += 1

    if not all_chunks:
        raise RuntimeError(
            "No valid chunks were generated. Index was not created."
        )

    print("\nEmbedding chunks...")

    vector_store = VectorStore()
    vector_store.add_chunks(all_chunks)
    vector_store.save()

    print("\n" + "=" * 60)
    print("Knowledge Base Built Successfully")
    print("=" * 60)

    print(f"Processed files : {processed_files}")
    print(f"Skipped files   : {skipped_files}")
    print(f"Total chunks    : {len(all_chunks)}")
    print("Saved files     : store.faiss")
    print("                  store_chunks.pkl")
    print("=" * 60)


if __name__ == "__main__":
    build_index()
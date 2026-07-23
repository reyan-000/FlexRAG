




import os

from pathlib import Path





#Encapsulating this logic keeps our codebase modular and testable

def load_text(file_path):

    """Return raw text from a .txt or .pdf file."""

    path = Path(file_path)

    if path.suffix == ".pdf":

        try:

            

            import fitz  # PyMuPDF

            with fitz.open(path) as doc:
                return "\n".join(page.get_text() for page in doc)

        except ImportError:

            raise ImportError("Install PyMuPDF: pip install pymupdf")

    return path.read_text(encoding="utf-8")


def load_pdf_pages(file_path):
    """
    Return a list of pages.

    Each item contains:
        page_number
        text
    """

    import fitz

    pages = []

    with fitz.open(file_path) as doc:

        for page_num, page in enumerate(doc, start=1):

            text = page.get_text().strip()

            if text:

                pages.append(
                    {
                        "page": page_num,
                        "text": text
                    }
                )

    return pages


#Encapsulating 

def chunk_text(text, chunk_size=500, overlap=100):

    """Split text into overlapping windows."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = min(start + chunk_size, len(words))

        chunks.append(" ".join(words[start:end]))

        if end == len(words):

            break

        start += chunk_size - overlap

    return chunks



if __name__ == "__main__":

    text = load_text("docs/sample.txt")

    chunks = chunk_text(text)

    print(f"Total chunks: {len(chunks)}")

    print("First chunk preview:", chunks[0][:120])

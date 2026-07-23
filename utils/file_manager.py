from pathlib import Path
import shutil

from build_index import build_index
from utils.constants import DOCS_DIR, SUPPORTED_EXTENSIONS


def get_documents():
    """Return all indexed documents."""
    DOCS_DIR.mkdir(exist_ok=True)
    return sorted(
        [
            file
            for file in DOCS_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    )


def save_uploaded_files(uploaded_files):
    """
    Save uploaded files.

    Returns
    -------
    uploaded_count
    existing_count
    """

    DOCS_DIR.mkdir(exist_ok=True)

    uploaded_count = 0
    existing_count = 0

    for uploaded_file in uploaded_files:

        destination = DOCS_DIR / uploaded_file.name

        if destination.exists():

            existing_count += 1

            continue

        with open(destination, "wb") as f:

            f.write(uploaded_file.getbuffer())

        uploaded_count += 1

    if uploaded_count >0:

        build_index()

    return uploaded_count, existing_count


def delete_document(file_path):
    """
    Delete one document and rebuild index.
    """

    file_path.unlink(missing_ok=True)

    remaining = [
    f
    for f in DOCS_DIR.iterdir()
    if f.is_file()
]    

    if remaining:

        build_index()

    else:

        Path("store.faiss").unlink(missing_ok=True)

        Path("store_chunks.pkl").unlink(missing_ok=True)
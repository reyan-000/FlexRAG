import streamlit as st


def show_answer(answer: str):
    """
    Display the AI answer inside a nice bordered container.
    """

    st.subheader("🤖 Answer")

    with st.container(border=True):
        st.write(answer)


def show_sources(sources):
    """
    Display retrieved sources.
    """

    st.subheader("📚 Sources")

    if not sources:
        st.info("No sources available.")
        return

    for source in sources:

        with st.expander(source):
            st.write(source)


def show_empty_documents():
    """
    Sidebar placeholder when no files exist.
    """

    st.sidebar.info(
        "No documents uploaded.\n\nUpload a PDF or TXT file to get started."
    )


def show_document_count(count):
    """
    Display number of indexed documents.
    """

    st.sidebar.caption(f"Indexed Documents: {count}")
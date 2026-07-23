from utils.constants import *
from utils.file_manager import *
from utils.ui_components import *

from rag_chain import rag_answer

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT
)


# Session State


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "provider" not in st.session_state:
    st.session_state.provider = "Ollama"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "phi3:mini"

documents = get_documents()

st.sidebar.title("📂 Document Manager")

st.sidebar.markdown("---")

    
if documents:

    st.sidebar.subheader("Indexed Documents")

    show_document_count(len(documents))

    for document in documents:

        size = document.stat().st_size / 1024

        col1, col2 = st.sidebar.columns([5, 1])

        with col1:

            st.markdown(
                f"**📄 {document.name}**"
            )

            st.caption(
                f"{size:.1f} KB"
            )
        with col2:

            if st.button("🗑", key=document.name):

                delete_document(document)

                st.rerun()

else:

    show_empty_documents()

left, right = st.columns([4, 1])

with left:

    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)

with right:

    st.markdown(
        """
**Developed by Mohd Rayyan**

[🐙 GitHub](https://github.com/reyan-000)

[💼 LinkedIn](https://www.linkedin.com/in/mohd-rayyan-934354316)

⭐ **[Found FlexRAG useful? Star the repository.](https://github.com/reyan-000/FlexRAG)**
        """
    )

st.divider()


st.sidebar.subheader("➕ Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:

    with st.spinner("Updating Knowledge Base..."):

        uploaded_count, existing_count = save_uploaded_files(uploaded_files)

    if uploaded_count:

        st.toast(
            f"✅ {uploaded_count} new document(s) indexed."
        )

        st.rerun()

    elif existing_count:

        st.info(
            "All selected documents are already indexed."
        )

st.divider()

st.sidebar.markdown("---")

st.sidebar.subheader("⚙ AI Provider")

from utils.constants import ALLOW_OLLAMA

providers = ["Groq"]

if ALLOW_OLLAMA:
    providers.insert(0, "Ollama")

provider = st.sidebar.radio(
    "Choose Provider",
    providers,
    key="provider"
)

if provider == "Ollama":

    model = st.sidebar.selectbox(
        "Model",
        [
            "phi3:mini",
            "llama3",
            "mistral"
        ],
        key="selected_model"
    )

    api_key = None

else:

    api_key = st.sidebar.text_input(
        "Groq API Key",
        type="password",
        key="groq_api_key"
    )

    model = st.sidebar.selectbox(
        "Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it"
        ],
        key="groq_model"
    )

if st.sidebar.button("🗑 Clear Chat"):

    st.session_state.chat_history.clear()

    st.rerun()

question = st.text_input(
    "Ask anything about your uploaded documents"
)

if st.button("Ask 🚀"):

    if not question.strip():
        st.warning("Please enter a question.")
    
    if provider == "Groq" and not api_key.strip():

        st.warning("Please enter your Groq API key.")

        st.stop()

    else:

        with st.spinner("Thinking..."):

            result = rag_answer(
                question=question,
                provider=provider.lower(),
                model=model,
                api_key=api_key
            )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"]
            }
        )

        
if st.session_state.chat_history:

    st.divider()

    st.header("💬 Conversation")

    for chat in reversed(st.session_state.chat_history):

        with st.chat_message("user"):

            st.markdown(chat["question"])

        with st.chat_message("assistant"):
            with st.container(border=True):

                st.markdown(chat["answer"])

            st.markdown("**📚 Retrieved Evidence**")

            if chat["sources"]:

                for source in chat["sources"]:

                    title = source["title"]

                    if source["page"] is not None:
                        title += f" (Page {source['page']})"

                    with st.expander(f"📄 {title}"):

                        st.write(source["preview"])
            else:

                st.info("No sources available.")
            
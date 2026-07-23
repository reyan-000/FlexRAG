from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq


def get_llm(
    provider="ollama",
    model=None,
    api_key=None
):
    """
    Returns the selected LLM instance.
    """

    provider = provider.lower()

    if provider == "ollama":

        return OllamaLLM(
            model=model or "phi3:mini"
        )

    elif provider == "groq":

        if not api_key:

            raise ValueError(
                "Groq API key is required."
            )

        return ChatGroq(
            api_key=api_key,
            model=model or "llama-3.3-70b-versatile"
        )

    raise ValueError(
        f"Unsupported provider: {provider}"
    )
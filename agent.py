import numexpr

from ddgs import DDGS
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="phi3:mini")


def safe_eval(expr):
    """Safely evaluate a mathematical expression."""
    try:
        return str(numexpr.evaluate(expr.strip()).item())
    except Exception:
        return None


def web_search(query):
    """Search the web using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No search results found."

        output = []

        for r in results:
            output.append(
                f"Title: {r['title']}\n"
                f"Body: {r['body']}\n"
                f"URL: {r['href']}\n"
            )

        return "\n".join(output)

    except Exception as e:
        return f"Search Error: {e}"


def ask_agent(question):
    """
    Simple AI Agent:
    - Uses calculator for math
    - Uses DuckDuckGo for current events
    - Otherwise uses Phi-3
    """

    lower = question.lower()

    # Calculator
    math_keywords = [
        "+", "-", "*", "/", "^",
        "sqrt", "calculate",
        "multiply", "divide",
        "add", "subtract"
    ]

    if any(k in lower for k in math_keywords):
        result = safe_eval(question)

        if result is not None:
            return f"Calculator Result: {result}"

    # Web Search
    search_keywords = [
        "latest",
        "today",
        "news",
        "who",
        "when",
        "current",
        "search"
    ]

    if any(k in lower for k in search_keywords):

        context = web_search(question)

        prompt = f"""
Answer the user's question using the search results.

Search Results:
{context}

Question:
{question}

Answer:
"""

        return llm.invoke(prompt)

    # Normal LLM

    return llm.invoke(question)


if __name__ == "__main__":

    while True:

        q = input("\nAsk Agent (type exit to quit): ")

        if q.lower() == "exit":
            break

        print("\n")
        print(ask_agent(q))
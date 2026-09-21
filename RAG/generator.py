import requests
from rag.config import OLLAMA_URL, OLLAMA_MODEL


def generate_answer(question, contexts):
    context_text = "\n\n".join(
        f"[Source: {item['source']}]\n{item['text']}"
        for item in contexts
    )

    prompt = f"""
You are a workforce analytics assistant.

Answer the user's question using only the retrieved project context below.
Do not invent facts. If the context does not contain enough information,
say that the available project files do not provide enough information.

User question:
{question}

Retrieved project context:
{context_text}
""".strip()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        answer = data.get("response", "").strip()
        if answer:
            return answer, "ollama"
    except Exception:
        pass

    # Safe fallback when no local LLM is running.
    if contexts:
        return (
            "I found the following relevant information in your project files:\n\n"
            + "\n\n".join(
                f"• {item['text'][:500]} "
                f"(source: {item['source']})"
                for item in contexts[:3]
            ),
            "retrieval-only"
        )

    return "No relevant information was found in the project files.", "retrieval-only"

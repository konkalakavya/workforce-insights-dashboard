from rag.vector_store import search, build_index as _build_index
from rag.generator import generate_answer


def build_index():
    return _build_index()


def ask_rag(question):
    contexts = search(question, top_k=5)
    answer, generation_mode = generate_answer(question, contexts)

    return {
        "question": question,
        "answer": answer,
        "generation_mode": generation_mode,
        "sources": [
            {
                "source": item["source"],
                "score": item["score"]
            }
            for item in contexts
        ]
    }

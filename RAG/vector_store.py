import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from rag.config import INDEX_FILE, METADATA_FILE, TOP_K
from rag.document_loader import load_all_documents


_MODEL = None


def model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def build_index():
    documents = load_all_documents()

    if not documents:
        raise RuntimeError("No supported files were found in data/ or ML/.")

    texts = [d["text"] for d in documents]
    embeddings = model().encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_FILE))
    METADATA_FILE.write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return {
        "status": "index_created",
        "documents": len(documents),
        "index": str(INDEX_FILE)
    }


def search(question, top_k=TOP_K):
    if not INDEX_FILE.exists() or not METADATA_FILE.exists():
        build_index()

    index = faiss.read_index(str(INDEX_FILE))
    documents = json.loads(METADATA_FILE.read_text(encoding="utf-8"))

    query_vector = model().encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    k = min(top_k, len(documents))
    scores, ids = index.search(query_vector, k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0:
            continue
        item = dict(documents[idx])
        item["score"] = round(float(score), 4)
        results.append(item)

    return results

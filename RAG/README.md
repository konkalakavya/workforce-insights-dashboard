# Workforce RAG

This RAG module reads the existing project files from:

```text
data/
ML/
```

It automatically discovers:

- CSV files
- XLSX/XLS files
- DOCX files
- TXT/MD files

This means files such as:

```text
ML/ML part.docx
ML/Feature_Classification.xlsx
ML/ML_Ready_Dataset.csv
ML/X_train.csv
ML/X_test.csv
ML/y_train.csv
ML/y_test.csv
data/workforce data.csv
data/workforce processed data.csv
```

can be indexed without copying them into the backend.

## Build the vector index

From the project root:

```bash
cd backend
pip install -r requirements.txt
cd ..
python -m rag.build_index
```

Or call:

```text
POST http://127.0.0.1:5000/api/rag/rebuild
```

## Ask a question

```text
POST /api/rag/ask
```

JSON:

```json
{
  "question": "What features are used in the workforce ML project?"
}
```

The retrieval layer uses Sentence Transformers + FAISS.

For actual generated answers, install and run Ollama locally with a compatible
model. If Ollama is unavailable, the API safely falls back to retrieval-only
answers instead of inventing information.

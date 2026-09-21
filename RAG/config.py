from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
ML_DIR = PROJECT_ROOT / "ML"

STORE_DIR = BASE_DIR / "vector_store"
INDEX_FILE = STORE_DIR / "index.faiss"
METADATA_FILE = STORE_DIR / "metadata.json"

TOP_K = 5

# Optional local generation through Ollama.
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

STORE_DIR.mkdir(parents=True, exist_ok=True)

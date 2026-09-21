from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
ML_DIR = PROJECT_ROOT / "ml"
MODEL_DIR = ML_DIR / "saved_models"

# Existing dataset. Change this filename if your uploaded dataset has a different name.
DATA_FILE = DATA_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

from pathlib import Path
import pandas as pd


def clean_columns(df):
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def load_dataset(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. "
            "Place your existing dataset in the project's data folder."
        )

    suffix = path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError("Supported dataset formats are CSV, XLSX and XLS.")

    df = clean_columns(df)
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def records(df):
    if df is None:
        return []

    clean = df.where(pd.notnull(df), None)
    return clean.to_dict(orient="records")

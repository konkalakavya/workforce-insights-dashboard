from pathlib import Path
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.model_selection import train_test_split

from config import MODEL_DIR
from utils.preprocessing import prepare_features


MODEL_FILE = MODEL_DIR / "attrition_model.joblib"


def train_attrition_model(df):
    X, y, transformer = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42
    )

    X_train_t = transformer.fit_transform(X_train)
    X_test_t = transformer.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train_t, y_train)

    predictions = model.predict(X_test_t)
    probabilities = model.predict_proba(X_test_t)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "precision": round(
            precision_score(y_test, predictions, zero_division=0), 4
        ),
        "recall": round(
            recall_score(y_test, predictions, zero_division=0), 4
        ),
        "f1": round(
            f1_score(y_test, predictions, zero_division=0), 4
        )
    }

    if len(set(y_test)) == 2:
        metrics["auc"] = round(roc_auc_score(y_test, probabilities), 4)

    bundle = {
        "model": model,
        "transformer": transformer,
        "metrics": metrics,
        "feature_columns": X.columns.tolist()
    }

    joblib.dump(bundle, MODEL_FILE)
    return bundle


def load_or_train(df):
    if MODEL_FILE.exists():
        try:
            return joblib.load(MODEL_FILE)
        except Exception:
            pass

    return train_attrition_model(df)


def _risk(probability):
    if probability >= 0.70:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"


def predict_attrition(payload, df):
    if df is None or df.empty:
        raise ValueError("Dataset is not loaded.")

    bundle = load_or_train(df)

    feature_columns = bundle["feature_columns"]

    row = {}
    for column in feature_columns:
        row[column] = payload.get(column, None)

    input_df = pd.DataFrame([row])
    transformed = bundle["transformer"].transform(input_df)

    probability = float(bundle["model"].predict_proba(transformed)[0][1])
    predicted = int(bundle["model"].predict(transformed)[0])

    return {
        "predicted_attrition": bool(predicted),
        "probability": round(probability, 4),
        "percentage": round(probability * 100, 2),
        "risk_category": _risk(probability),
        "model": "Random Forest",
        "metrics": bundle["metrics"]
    }

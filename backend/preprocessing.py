import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


TARGET = "Attrition"


def prepare_features(df):
    data = df.copy()

    if TARGET not in data.columns:
        raise ValueError("The dataset must contain an 'Attrition' column.")

    y = data[TARGET].map({
        "Yes": 1,
        "No": 0,
        "yes": 1,
        "no": 0,
        True: 1,
        False: 0
    })

    if y.isna().any():
        y = pd.to_numeric(y, errors="coerce")

    if y.isna().any():
        raise ValueError("Attrition contains unsupported target values.")

    drop_cols = [
        TARGET,
        "EmployeeNumber",
        "Employee_ID",
        "EmployeeId"
    ]

    X = data.drop(columns=[c for c in drop_cols if c in data.columns])

    numeric_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_cols = [
        c for c in X.columns if c not in numeric_cols
    ]

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    transformer = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_cols),
        ("categorical", categorical_pipeline, categorical_cols)
    ])

    return X, y.astype(int), transformer

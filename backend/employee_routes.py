from flask import Blueprint, current_app, jsonify, request
from utils.data_loader import records

employee_bp = Blueprint("employees", __name__)


@employee_bp.get("/")
def employees():
    df = current_app.config.get("DATA")

    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500

    result = df.copy()

    search = request.args.get("search", "").strip().lower()
    department = request.args.get("department", "").strip().lower()
    job_role = request.args.get("job_role", "").strip().lower()

    if search:
        mask = result.astype(str).apply(
            lambda column: column.str.lower().str.contains(search, na=False)
        ).any(axis=1)
        result = result[mask]

    if department and "Department" in result.columns:
        result = result[
            result["Department"].astype(str).str.lower().eq(department)
        ]

    if job_role and "JobRole" in result.columns:
        result = result[
            result["JobRole"].astype(str).str.lower().eq(job_role)
        ]

    try:
        limit = min(max(int(request.args.get("limit", 100)), 1), 1000)
    except ValueError:
        limit = 100

    return jsonify({
        "count": int(len(result)),
        "employees": records(result.head(limit))
    })


@employee_bp.get("/top-performers")
def top_performers():
    df = current_app.config.get("DATA")

    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500

    if "PerformanceRating" not in df.columns:
        return jsonify({"employees": []})

    result = df.sort_values("PerformanceRating", ascending=False).head(10)
    return jsonify({"employees": records(result)})


@employee_bp.get("/high-risk")
def high_risk():
    df = current_app.config.get("DATA")

    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500

    # Historical attrition records, not future ML predictions.
    if "Attrition" not in df.columns:
        return jsonify({"employees": []})

    result = df[
        df["Attrition"].astype(str).str.lower().eq("yes")
    ].head(20)

    return jsonify({
        "count": int(len(result)),
        "employees": records(result)
    })

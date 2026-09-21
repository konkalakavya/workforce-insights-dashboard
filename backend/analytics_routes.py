from flask import Blueprint, current_app, jsonify

from services.analytics_service import (
    summary,
    performance_stats,
    salary_stats,
    attrition_stats,
    department_stats,
    workforce_health
)

analytics_bp = Blueprint("analytics", __name__)


def get_data():
    df = current_app.config.get("DATA")
    if df is None:
        return None
    return df


@analytics_bp.get("/overview")
def overview():
    df = get_data()
    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
    return jsonify(summary(df))


@analytics_bp.get("/performance")
def performance():
    df = get_data()
    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
    return jsonify(performance_stats(df))


@analytics_bp.get("/salary")
def salary():
    df = get_data()
    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
    return jsonify(salary_stats(df))


@analytics_bp.get("/attrition")
def attrition():
    df = get_data()
    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
    return jsonify(attrition_stats(df))


@analytics_bp.get("/departments")
def departments():
    df = get_data()
    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
    return jsonify(department_stats(df))


@analytics_bp.get("/health")
def health():
    df = get_data()
    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500
    return jsonify(workforce_health(df))

from flask import Blueprint, current_app, jsonify
from services.analytics_service import summary, department_stats

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
def dashboard():
    df = current_app.config.get("DATA")

    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500

    return jsonify({
        "summary": summary(df),
        "departments": department_stats(df)
    })

from flask import Blueprint, current_app, jsonify, request

from services.chat_service import answer

chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/")
def chat():
    df = current_app.config.get("DATA")

    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500

    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "")

    return jsonify(answer(question, df))

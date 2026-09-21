from flask import Blueprint, current_app, jsonify, request

from services.prediction_service import attrition, promotion

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.post("/attrition")
def attrition_prediction():
    df = current_app.config.get("DATA")

    if df is None:
        return jsonify({"error": "Dataset is not loaded."}), 500

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "Request body must be a JSON object containing employee features."
        }), 400

    try:
        return jsonify(attrition(payload, df))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@prediction_bp.post("/promotion")
def promotion_prediction():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    try:
        return jsonify(promotion(payload, current_app.config.get("DATA")))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

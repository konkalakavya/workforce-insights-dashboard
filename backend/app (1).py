from flask import Flask, jsonify
from flask_cors import CORS

from config import DATA_FILE
from utils.data_loader import load_dataset
from routes.dashboard_routes import dashboard_bp
from routes.employee_routes import employee_bp
from routes.analytics_routes import analytics_bp
from routes.prediction_routes import prediction_bp
from routes.chat_routes import chat_bp

app = Flask(__name__)
CORS(app)

# Load the existing dataset once when the API starts.
try:
    DATA = load_dataset(DATA_FILE)
    DATA_ERROR = None
except Exception as exc:
    DATA = None
    DATA_ERROR = str(exc)

app.config["DATA"] = DATA

app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
app.register_blueprint(employee_bp, url_prefix="/api/employees")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(prediction_bp, url_prefix="/api/predict")
app.register_blueprint(chat_bp, url_prefix="/api/chat")


@app.get("/")
def home():
    return jsonify({
        "project": "AI-Powered Workforce Analytics Backend",
        "status": "running",
        "dataset_loaded": DATA is not None
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "dataset_loaded": DATA is not None,
        "dataset_error": DATA_ERROR
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

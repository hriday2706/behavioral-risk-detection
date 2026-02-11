from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# -------------------------------------------------
# FIX PYTHON PATH (ADD PROJECT ROOT)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# -------------------------------------------------
# NOW SAFE IMPORTS
# -------------------------------------------------
from backend.event_logger import log_event, get_events
from backend.feature_extractor import extract_features
from ml_model.risk_engine import assess_risk

# -------------------------------------------------
# FLASK APP
# -------------------------------------------------
app = Flask(__name__)
CORS(app)

USER_PROFILE = {
    "usual_login_hour": 10,
    "known_devices": ["Chrome"]
}

@app.route("/")
def home():
    return "Behavior Risk Backend Running"

# ---------- LOG EVENT ----------
@app.route("/log-event", methods=["POST"])
def log_user_event():
    data = request.json

    log_event(
        data["session_id"],
        data["user_id"],
        data["event_type"],
        data.get("metadata", {})
    )
    return jsonify({"status": "event logged"})

# ---------- VIEW EVENTS ----------
@app.route("/events/<session_id>")
def view_events(session_id):
    return jsonify(get_events(session_id))

# ---------- RISK ASSESSMENT ----------
@app.route("/risk/<session_id>")
def assess_session_risk(session_id):
    events = get_events(session_id)

    if not events:
        return jsonify({"error": "No events found for this session"})

    features = extract_features(events, USER_PROFILE)
    risk = assess_risk(features)

    return jsonify({
        "features": features,
        "risk": risk
    })

if __name__ == "__main__":
    app.run(debug=True)

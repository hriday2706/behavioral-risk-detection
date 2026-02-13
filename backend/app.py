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
# SAFE IMPORTS
# -------------------------------------------------
from backend.event_logger import log_event, get_events
from backend.behavioral_risk_engine import BehavioralRiskEngine

# -------------------------------------------------
# FLASK APP
# -------------------------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------------------------
# SESSION ENGINE STORE
# -------------------------------------------------
SESSION_ENGINES = {}

@app.route("/")
def home():
    return "Behavioral Risk Engine Running"

# -------------------------------------------------
# LOG EVENT + AUTO RISK UPDATE
# -------------------------------------------------
@app.route("/log-event", methods=["POST"])
def log_user_event():
    data = request.json

    session_id = data["session_id"]
    user_id = data["user_id"]
    event_type = data["event_type"]
    metadata = data.get("metadata", {})
    timestamp = data.get("timestamp")

    if not timestamp:
        return jsonify({"error": "Timestamp required"}), 400

    # Store raw event
    log_event(session_id, user_id, event_type, metadata)

    # Force fresh engine on login attempt
    if event_type == "LOGIN_ATTEMPT":
        SESSION_ENGINES[session_id] = BehavioralRiskEngine()

    # Otherwise create if not exists
    elif session_id not in SESSION_ENGINES:
        SESSION_ENGINES[session_id] = BehavioralRiskEngine()


    engine = SESSION_ENGINES[session_id]

    # Build event object for engine
    event_obj = {
        "event_type": event_type,
        "timestamp": timestamp,
        "metadata": metadata
    }

    # Process event through risk engine
    engine.process_event(event_obj)

    # Return live risk
    return jsonify(engine.get_risk_report())

# -------------------------------------------------
# VIEW EVENTS
# -------------------------------------------------
@app.route("/events/<session_id>")
def view_events(session_id):
    return jsonify(get_events(session_id))

# -------------------------------------------------
# OPTIONAL: VIEW CURRENT RISK WITHOUT NEW EVENT
# -------------------------------------------------
@app.route("/risk/<session_id>")
def view_risk(session_id):
    if session_id not in SESSION_ENGINES:
        return jsonify({"error": "Session not found"})

    engine = SESSION_ENGINES[session_id]
    return jsonify(engine.get_risk_report())

# -------------------------------------------------
# RUN APP
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

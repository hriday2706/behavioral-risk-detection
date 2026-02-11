# ml_model/risk_engine.py

import os
import joblib

from ml_model.feature_schema import FEATURE_NAMES, RISK_LABELS
from ml_model.explain_model import explain_prediction



# -------------------------------------------------
# LOAD MODEL USING ABSOLUTE PATH (CRITICAL FIX)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_model", "risk_decision_tree.pkl")

model = joblib.load(MODEL_PATH)


# -------------------------------------------------
# RISK SCORE MAPPING
# -------------------------------------------------
RISK_SCORES = {
    "LOW": 20,
    "MEDIUM": 55,
    "HIGH": 85
}


# -------------------------------------------------
# HUMAN-READABLE REASON MAPPING
# -------------------------------------------------
REASON_MAP = {
    "avg_time_between_login_attempts": "Very fast repeated login attempts detected",
    "rapid_attempt_flag": "Automated-style login attempts detected",
    "time_to_sensitive_action": "Sensitive actions performed immediately after login",
    "sensitive_action_count": "Multiple sensitive actions performed in one session",
    "new_device_flag": "Login from an unfamiliar device or browser",
    "impossible_travel_flag": "Suspicious location change detected (simulated)",
    "time_deviation_score": "Login time deviates from usual behavior",
    "action_burst_flag": "Multiple actions performed unusually fast",
    "session_duration": "Unusually short session with sensitive activity"
}


def generate_user_friendly_reasons(raw_reasons):
    """
    Converts decision-tree rules into user-friendly explanations
    """
    final_reasons = []

    for rule in raw_reasons:
        for feature in FEATURE_NAMES:
            if feature in rule:
                final_reasons.append(REASON_MAP[feature])
                break

    return list(set(final_reasons))  # remove duplicates


def assess_risk(feature_vector):
    """
    feature_vector: list of 9 values in FEATURE_NAMES order
    """
    risk_label, raw_reasons = explain_prediction(model, feature_vector)

    return {
        "risk_class": risk_label,
        "risk_score": RISK_SCORES[risk_label],
        "reasons": generate_user_friendly_reasons(raw_reasons)
    }


# -------------------------------------------------
# LOCAL TEST (OPTIONAL)
# -------------------------------------------------
if __name__ == "__main__":
    fraud_example = [
        0.6,   # avg_time_between_login_attempts
        1,     # rapid_attempt_flag
        4,     # time_to_sensitive_action
        3,     # sensitive_action_count
        1,     # new_device_flag
        1,     # impossible_travel_flag
        0.8,   # time_deviation_score
        1,     # action_burst_flag
        50     # session_duration
    ]

    result = assess_risk(fraud_example)
    print("\n🚨 FINAL RISK ASSESSMENT")
    for k, v in result.items():
        print(f"{k}: {v}")

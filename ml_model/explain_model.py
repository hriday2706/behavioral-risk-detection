# explain_model.py

import joblib
import numpy as np
from sklearn.tree import _tree

from ml_model.feature_schema import FEATURE_NAMES, RISK_LABELS



def explain_prediction(model, input_features):
    """
    input_features: list or numpy array in FEATURE_NAMES order
    """
    tree = model.tree_
    feature = tree.feature
    threshold = tree.threshold

    node = 0
    explanations = []

    while feature[node] != _tree.TREE_UNDEFINED:
        feature_name = FEATURE_NAMES[feature[node]]
        value = input_features[feature[node]]
        thresh = threshold[node]

        if value <= thresh:
            explanations.append(
                f"{feature_name} ≤ {round(thresh, 2)} (observed {round(value, 2)})"
            )
            node = tree.children_left[node]
        else:
            explanations.append(
                f"{feature_name} > {round(thresh, 2)} (observed {round(value, 2)})"
            )
            node = tree.children_right[node]

    risk_class = np.argmax(tree.value[node])
    risk_label = RISK_LABELS[risk_class]

    return risk_label, explanations

if __name__ == "__main__":
    model = joblib.load("saved_model/risk_decision_tree.pkl")

    # Example: FRAUD-like behavior
    fraud_sample = [
        0.8,   # avg_time_between_login_attempts
        1,     # rapid_attempt_flag
        5,     # time_to_sensitive_action
        4,     # sensitive_action_count
        1,     # new_device_flag
        1,     # impossible_travel_flag
        0.9,   # time_deviation_score
        1,     # action_burst_flag
        45     # session_duration
    ]

    label, reasons = explain_prediction(model, fraud_sample)

    print("\n🧠 RISK PREDICTION:", label)
    print("🔍 REASONS:")
    for r in reasons:
        print(" -", r)

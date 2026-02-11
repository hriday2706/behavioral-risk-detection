# feature_schema.py

FEATURE_NAMES = [
    "avg_time_between_login_attempts",
    "rapid_attempt_flag",
    "time_to_sensitive_action",
    "sensitive_action_count",
    "new_device_flag",
    "impossible_travel_flag",
    "time_deviation_score",
    "action_burst_flag",
    "session_duration"
]

RISK_LABELS = {
    0: "LOW",
    1: "MEDIUM",
    2: "HIGH"
}

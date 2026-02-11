# backend/feature_extractor.py

import datetime
import numpy as np

SENSITIVE_ACTIONS = {"DOWNLOAD_STATEMENT", "CHANGE_PASSWORD"}


def mean(values):
    return sum(values) / len(values) if values else 0


def extract_features(events, user_profile):
    # Sort events by timestamp
    events = sorted(events, key=lambda e: e["timestamp"])
    timestamps = [e["timestamp"] for e in events]

    # -----------------------------
    # 1️⃣ avg_time_between_login_attempts
    # -----------------------------
    login_attempts = [
        e["timestamp"] for e in events if e["event_type"] == "LOGIN_ATTEMPT"
    ]

    if len(login_attempts) > 1:
        gaps = [
            login_attempts[i + 1] - login_attempts[i]
            for i in range(len(login_attempts) - 1)
        ]
        avg_time_between_login_attempts = mean(gaps)
    else:
        avg_time_between_login_attempts = 999  # safe default

    # -----------------------------
    # 2️⃣ rapid_attempt_flag
    # -----------------------------
    rapid_attempt_flag = 1 if avg_time_between_login_attempts < 3 else 0

    # -----------------------------
    # 3️⃣ time_to_sensitive_action
    # -----------------------------
    login_success_time = next(
        (e["timestamp"] for e in events if e["event_type"] == "LOGIN_SUCCESS"),
        None
    )

    sensitive_times = [
        e["timestamp"] for e in events if e["event_type"] in SENSITIVE_ACTIONS
    ]

    if login_success_time is not None and sensitive_times:
        time_to_sensitive_action = sensitive_times[0] - login_success_time
    else:
        time_to_sensitive_action = 999

    # -----------------------------
    # 4️⃣ sensitive_action_count
    # -----------------------------
    sensitive_action_count = len(sensitive_times)

    # -----------------------------
    # 5️⃣ new_device_flag
    # -----------------------------
    user_agents = [
        e.get("metadata", {}).get("user_agent")
        for e in events
        if e.get("metadata")
    ]

    first_device = user_agents[0] if user_agents else None

    new_device_flag = (
        1 if first_device and first_device not in user_profile["known_devices"] else 0
    )

    # -----------------------------
    # 6️⃣ impossible_travel_flag (SIMULATED)
    # -----------------------------
    locations = [
        e.get("metadata", {}).get("location")
        for e in events
        if e.get("metadata")
    ]

    impossible_travel_flag = 1 if len(set(locations)) > 1 else 0

    # -----------------------------
    # 7️⃣ time_deviation_score
    # -----------------------------
    if login_success_time is not None:
        login_hour = datetime.datetime.fromtimestamp(login_success_time).hour
        deviation = abs(login_hour - user_profile["usual_login_hour"]) / 12
        time_deviation_score = min(deviation, 1)
    else:
        time_deviation_score = 0

    # -----------------------------
    # 8️⃣ action_burst_flag (CORRECTED)
    # -----------------------------
    action_burst_flag = 0

    if len(timestamps) >= 3:
        diffs = np.diff(timestamps)
        rapid_gaps = sum(1 for gap in diffs if gap < 2)

        if rapid_gaps >= 2:
            action_burst_flag = 1

    # -----------------------------
    # 9️⃣ session_duration (SAFE)
    # -----------------------------
    if len(timestamps) > 1:
        session_duration = timestamps[-1] - timestamps[0]
    else:
        session_duration = 0

    return [
        avg_time_between_login_attempts,
        rapid_attempt_flag,
        time_to_sensitive_action,
        sensitive_action_count,
        new_device_flag,
        impossible_travel_flag,
        time_deviation_score,
        action_burst_flag,
        session_duration
    ]

# generate_data.py

import numpy as np
import pandas as pd

np.random.seed(42)  # deterministic demo behavior

N_NORMAL = 600
N_FRAUD = 600


def generate_normal_users(n):
    data = []

    for _ in range(n):
        avg_time_between_login_attempts = np.random.uniform(8, 30)
        rapid_attempt_flag = 0

        time_to_sensitive_action = np.random.uniform(60, 300)
        sensitive_action_count = np.random.choice([0, 1], p=[0.7, 0.3])

        new_device_flag = np.random.choice([0, 1], p=[0.85, 0.15])
        impossible_travel_flag = 0

        time_deviation_score = np.random.uniform(0.0, 0.3)
        action_burst_flag = 0

        session_duration = np.random.uniform(120, 600)

        data.append([
            avg_time_between_login_attempts,
            rapid_attempt_flag,
            time_to_sensitive_action,
            sensitive_action_count,
            new_device_flag,
            impossible_travel_flag,
            time_deviation_score,
            action_burst_flag,
            session_duration,
            0  # LOW risk
        ])

    return data


def generate_fraud_users(n):
    data = []

    for _ in range(n):
        avg_time_between_login_attempts = np.random.uniform(0.3, 2)
        rapid_attempt_flag = 1

        time_to_sensitive_action = np.random.uniform(0, 15)
        sensitive_action_count = np.random.randint(2, 6)

        new_device_flag = 1
        impossible_travel_flag = np.random.choice([0, 1], p=[0.3, 0.7])

        time_deviation_score = np.random.uniform(0.6, 1.0)
        action_burst_flag = 1

        session_duration = np.random.uniform(20, 90)

        data.append([
            avg_time_between_login_attempts,
            rapid_attempt_flag,
            time_to_sensitive_action,
            sensitive_action_count,
            new_device_flag,
            impossible_travel_flag,
            time_deviation_score,
            action_burst_flag,
            session_duration,
            2  # HIGH risk
        ])

    return data


if __name__ == "__main__":
    columns = [
        "avg_time_between_login_attempts",
        "rapid_attempt_flag",
        "time_to_sensitive_action",
        "sensitive_action_count",
        "new_device_flag",
        "impossible_travel_flag",
        "time_deviation_score",
        "action_burst_flag",
        "session_duration",
        "risk_label"
    ]

    normal_data = generate_normal_users(N_NORMAL)
    fraud_data = generate_fraud_users(N_FRAUD)

    df = pd.DataFrame(normal_data + fraud_data, columns=columns)

    df.to_csv("behavior_risk_dataset.csv", index=False)
    print("✅ Synthetic dataset generated:", df.shape)

import numpy as np
import pandas as pd

np.random.seed(42)

N_LOW = 10000
N_MEDIUM = 10000
N_HIGH = 10000


def generate_low(n):
    data = []
    for _ in range(n):
        data.append([
            np.random.uniform(8, 30),
            0,
            np.random.uniform(60, 300),
            np.random.choice([0, 1], p=[0.85, 0.15]),
            np.random.choice([0, 1], p=[0.9, 0.1]),
            0,
            np.random.uniform(0.0, 0.3),
            0,
            np.random.uniform(200, 800),
            0
        ])
    return data


def generate_medium(n):
    data = []
    for _ in range(n):
        data.append([
            np.random.uniform(1, 6),
            np.random.choice([0, 1], p=[0.3, 0.7]),
            np.random.uniform(10, 80),
            np.random.randint(1, 3),
            np.random.choice([0, 1], p=[0.4, 0.6]),
            np.random.choice([0, 1], p=[0.7, 0.3]),
            np.random.uniform(0.3, 0.6),
            np.random.choice([0, 1], p=[0.5, 0.5]),
            np.random.uniform(60, 250),
            1
        ])
    return data


def generate_high(n):
    data = []
    for _ in range(n):
        data.append([
            np.random.uniform(0.2, 2),
            1,
            np.random.uniform(0, 15),
            np.random.randint(2, 6),
            1,
            np.random.choice([0, 1], p=[0.2, 0.8]),
            np.random.uniform(0.6, 1.0),
            1,
            np.random.uniform(10, 100),
            2
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

    df = pd.DataFrame(
        generate_low(N_LOW) +
        generate_medium(N_MEDIUM) +
        generate_high(N_HIGH),
        columns=columns
    )

    df.to_csv("behavior_risk_dataset.csv", index=False)
    print("Dataset generated:", df.shape)

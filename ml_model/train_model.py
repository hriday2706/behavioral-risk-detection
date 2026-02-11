import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("behavior_risk_dataset.csv")

X = df.drop("risk_label", axis=1)
y = df["risk_label"]

# Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train Decision Tree
model = DecisionTreeClassifier(
    max_depth=6,               # deeper than before
    min_samples_split=50,      # prevents tiny splits
    class_weight="balanced",   # ensures equal importance
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# Save model
joblib.dump(model, "saved_model/risk_decision_tree.pkl")

print("\nModel saved successfully.")

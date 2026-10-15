"""Train and evaluate a Random Forest on the safe demonstration dataset."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "dataset.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "ransomware_model.pkl"
METRICS_PATH = MODEL_DIR / "evaluation_metrics.json"

FEATURES = [
    "file_size_kb",
    "entropy",
    "file_extension_changed",
    "rapid_file_modifications",
    "high_write_activity",
    "suspicious_api_calls",
]

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError("Dataset not found. Run: python generate_dataset.py")

    df = pd.read_csv(DATA_PATH)
    required = FEATURES + ["label"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")

    X = df[FEATURES].fillna(0)
    y = df["label"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150, random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = float(accuracy_score(y_test, predictions))
    report = classification_report(
        y_test, predictions, target_names=["Benign-like", "Ransomware-like"],
        output_dict=True, zero_division=0
    )
    matrix = confusion_matrix(y_test, predictions).tolist()

    MODEL_DIR.mkdir(exist_ok=True)
    bundle = {"model": model, "features": FEATURES, "label_names": {0: "Benign-like", 1: "Ransomware-like"}}
    joblib.dump(bundle, MODEL_PATH)
    metrics = {"accuracy": accuracy, "classification_report": report, "confusion_matrix": matrix}
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("Training complete.")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Accuracy on held-out synthetic test split: {accuracy:.3f}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, target_names=["Benign-like", "Ransomware-like"], zero_division=0))
    print("Note: this score only measures performance on synthetic demonstration data.")

if __name__ == "__main__":
    main()

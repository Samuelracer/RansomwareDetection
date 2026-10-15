"""Streamlit dashboard for a safe ransomware-detection ML demonstration."""
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "ransomware_model.pkl"
METRICS_PATH = ROOT / "models" / "evaluation_metrics.json"

st.set_page_config(page_title="Ransomware Detection", page_icon="🛡️", layout="centered")
st.title("🛡️ Ransomware Detection Using Machine Learning")
st.caption("BCA Final-Year Cybersecurity Project — educational demonstration")

st.warning(
    "This project uses synthetic, made-up feature data. Results are not proof of "
    "real-world ransomware detection. Do not upload or execute suspicious files."
)

if not MODEL_PATH.exists():
    st.error("Trained model not found. In the project terminal, run these commands first:")
    st.code("python generate_dataset.py\npython train_model.py", language="powershell")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
features = bundle["features"]

st.subheader("Analyze a feature record")
st.write("Enter example numeric features. These values are a classroom simulation, not a file scan.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        file_size_kb = st.number_input("File size (KB)", min_value=0.0, value=120.0, step=10.0)
        entropy = st.slider("Entropy (0–8)", min_value=0.0, max_value=8.0, value=5.0, step=0.1)
        file_extension_changed = st.selectbox("File extension changed?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    with col2:
        rapid_file_modifications = st.number_input("Rapid file modifications", min_value=0, max_value=500, value=2, step=1)
        high_write_activity = st.selectbox("High write activity?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        suspicious_api_calls = st.number_input("Suspicious API-call count (simulated)", min_value=0, max_value=500, value=1, step=1)
    submitted = st.form_submit_button("Predict")

if submitted:
    row = pd.DataFrame([{
        "file_size_kb": file_size_kb,
        "entropy": entropy,
        "file_extension_changed": file_extension_changed,
        "rapid_file_modifications": rapid_file_modifications,
        "high_write_activity": high_write_activity,
        "suspicious_api_calls": suspicious_api_calls,
    }], columns=features)
    prediction = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    if prediction == 1:
        st.error("Prediction: RANSOMWARE-LIKE PATTERN")
        st.write("Treat this only as a simulated warning. Investigate with approved security tools.")
    else:
        st.success("Prediction: BENIGN-LIKE PATTERN")
        st.write("This prediction does not guarantee that a file is safe.")
    st.metric("Model confidence for predicted class", f"{probabilities[prediction] * 100:.1f}%")
    st.caption("Confidence is the model's probability estimate on synthetic training data, not a verified risk score.")

st.divider()
st.subheader("Model evaluation")
if METRICS_PATH.exists():
    import json
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    st.metric("Held-out synthetic test accuracy", f"{metrics['accuracy'] * 100:.1f}%")
    st.caption("This is measured on a synthetic test split and should not be reported as real-world accuracy.")
    st.write("Confusion matrix (rows = actual class; columns = predicted class; order: benign-like, ransomware-like):")
    st.dataframe(pd.DataFrame(
        metrics["confusion_matrix"],
        index=["Actual benign-like", "Actual ransomware-like"],
        columns=["Predicted benign-like", "Predicted ransomware-like"]
    ))
else:
    st.info("Evaluation metrics will appear after you run train_model.py.")

st.caption("Feature definitions are illustrative. This application does not inspect, modify, encrypt, or execute files.")

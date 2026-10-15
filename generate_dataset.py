"""Generate a SAFE synthetic dataset for demonstrating ransomware classification.
This creates made-up numeric features only; it does not inspect or execute files.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT = DATA_DIR / "dataset.csv"

def main():
    rng = np.random.default_rng(42)
    n_each = 500

    # Synthetic benign-like feature distributions
    benign = pd.DataFrame({
        "file_size_kb": rng.lognormal(mean=4.2, sigma=1.0, size=n_each),
        "entropy": np.clip(rng.normal(5.0, 0.8, n_each), 0, 8),
        "file_extension_changed": rng.binomial(1, 0.03, n_each),
        "rapid_file_modifications": rng.poisson(2, n_each),
        "high_write_activity": rng.binomial(1, 0.05, n_each),
        "suspicious_api_calls": rng.poisson(1, n_each),
        "label": 0,
    })

    # Synthetic ransomware-like feature distributions for demonstration only
    ransomware = pd.DataFrame({
        "file_size_kb": rng.lognormal(mean=4.0, sigma=1.1, size=n_each),
        "entropy": np.clip(rng.normal(7.0, 0.55, n_each), 0, 8),
        "file_extension_changed": rng.binomial(1, 0.72, n_each),
        "rapid_file_modifications": rng.poisson(24, n_each),
        "high_write_activity": rng.binomial(1, 0.78, n_each),
        "suspicious_api_calls": rng.poisson(15, n_each),
        "label": 1,
    })

    df = pd.concat([benign, ransomware], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(OUTPUT, index=False)
    print(f"Created {OUTPUT}")
    print(f"Rows: {len(df)}")
    print("Label 0 = benign-like synthetic sample; label 1 = ransomware-like synthetic sample.")
    print("This dataset is for a classroom demo and is not real-world detection evidence.")

if __name__ == "__main__":
    main()

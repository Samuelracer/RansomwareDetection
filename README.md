# Ransomware Detection Using Machine Learning

A beginner-friendly BCA final-year cybersecurity project using Python, scikit-learn, and Streamlit.

## What it does

- Creates a labeled **synthetic** dataset for a classroom demonstration.
- Trains a Random Forest classifier.
- Evaluates the model on a held-out synthetic test split.
- Shows predictions and evaluation metrics in a Streamlit dashboard.

## Important limitation

The included dataset is generated from artificial distributions. It is only useful for demonstrating the ML workflow and user interface. It does **not** establish real-world ransomware detection performance. For research-grade evaluation, replace it with a properly labeled, legally obtained dataset and test on an independent dataset. This project does not include or run ransomware.

## Folder structure

```text
RansomwareDetection/
├── app.py
├── train_model.py
├── generate_dataset.py
├── requirements.txt
├── README.md
├── data/
│   └── dataset.csv
└── models/
    ├── ransomware_model.pkl
    └── evaluation_metrics.json
```

## Requirements

- Windows 10/11
- Python 3.10 or newer recommended
- Visual Studio Code (optional but recommended)
- Internet connection for the initial package installation

## Run in Windows PowerShell (VS Code terminal)

Open the `RansomwareDetection` folder in VS Code. Select **Terminal → New Terminal** and run each command separately:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python generate_dataset.py
python train_model.py
python -m streamlit run app.py
```

The last command normally opens the dashboard in your browser at `http://localhost:8501`.

### If PowerShell says scripts are disabled

You can avoid changing the PowerShell execution policy by using Command Prompt:

1. In VS Code terminal, use the dropdown beside the `+` and select **Command Prompt**.
2. Run each command separately:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python generate_dataset.py
python train_model.py
python -m streamlit run app.py
```

If `python` is not recognized, install Python from https://www.python.org/downloads/ and select **Add Python to PATH** during installation. Restart VS Code afterward.

## What you should see

- `generate_dataset.py` creates `data/dataset.csv`.
- `train_model.py` prints classification metrics and creates model files in `models/`.
- Streamlit opens the dashboard, where you can enter simulated numeric features and get a prediction.

## Feature descriptions

| Feature | Meaning in this demo |
|---|---|
| `file_size_kb` | Simulated file size in kilobytes |
| `entropy` | Simulated entropy score from 0 to 8 |
| `file_extension_changed` | Whether a simulated extension-change event occurred (0/1) |
| `rapid_file_modifications` | Simulated count of rapid modification events |
| `high_write_activity` | Whether high write activity was simulated (0/1) |
| `suspicious_api_calls` | Simulated count of suspicious API-call indicators |
| `label` | 0 = benign-like synthetic sample; 1 = ransomware-like synthetic sample |

These are teaching features, not a validated detection signature. The UI's "confidence" is a model estimate, not a verified security score.

## Troubleshooting

- **Model not found:** run `python generate_dataset.py` and then `python train_model.py`.
- **ModuleNotFoundError:** activate `.venv` and run `python -m pip install -r requirements.txt`.
- **Port 8501 already in use:** run `python -m streamlit run app.py --server.port 8502`.
- **Terminal doesn't recognize `python`:** try `py` in place of `python`, for example `py -m venv .venv`.

## Academic project sections you can write

1. Abstract and introduction
2. Problem statement and objectives
3. Existing system and proposed system
4. System architecture and data flow
5. Dataset and feature description
6. Random Forest algorithm
7. Implementation and screenshots
8. Testing and evaluation
9. Limitations and future enhancements
10. Conclusion

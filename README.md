# 🛡️ Project: The Sentinel
**Real-Time Fraud Detection with Automated Feedback Loops**

## 🎯 Goal
A production-ready ML system that detects credit card fraud, tracks experiments, and self-heals when data drift is detected.

## 🏗️ The Stack
* **Data:** DVC (Versioning), Pandas (Validation)
* **ML:** Scikit-Learn (Random Forest), MLflow (Experiment Tracking & Registry)
* **Serving:** FastAPI (REST API)
* **Monitoring:** EvidentlyAI (Drift Detection)

## 🚀 How to Run
1. `pip install -r requirements.txt`
2. `python src/setup_gx.py` (Validate Data)
3. `python src/train.py` (Train Model)
4. `uvicorn src.serve:app` (Start API)
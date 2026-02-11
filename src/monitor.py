import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import os
import sys

def check_for_drift():
    print("🕵️ Analyzing for Data Drift...")
    
    # 1. Load Reference Data (The data the model was trained on)
    reference_data = pd.read_csv("data/raw/transactions.csv")
    
    # 2. Load "Current" Data (In a real app, this would be from your API logs)
    # For now, let's create a dummy 'production' dataset to simulate drift
    current_data = pd.DataFrame({
        "id": [101, 102, 103],
        "amount": [5.0, 4.5, 6.2], # Patterns have changed! Much smaller amounts.
        "is_fraud": [1, 1, 1]      # But these are actually fraud now!
    })

    # 3. Generate Drift Report
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference_data, current_data=current_data)
    
    # 4. Check results
    report_dict = drift_report.as_dict()
    drift_detected = report_dict["metrics"][0]["result"]["dataset_drift"]

    if drift_detected:
        print("🚨 DRIFT DETECTED! The model's world has changed.")
        # In a full pipeline, we would trigger 'src/train.py' here
        return True
    else:
        print("✅ No drift detected. Model is still performing well.")
        return False

if __name__ == "__main__":
    drift_status = check_for_drift()
    if drift_status:
        sys.exit(100) # Special exit code for "Retrain Needed"
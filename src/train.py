import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import subprocess
import sys
import os

def main():
    # --- STEP 1: AUTOMATED DATA VALIDATION ---
    print("🧐 Phase 1: Validating Data...")
    # We call our gatekeeper script (which we named setup_gx.py)
    result = subprocess.run(["python", "src/setup_gx.py"])
    if result.returncode != 0:
        print("🛑 Pipeline Aborted: Data quality is too poor for training.")
        sys.exit(1)

    # --- STEP 2: MLFLOW SETUP ---
    mlflow.set_experiment("Fraud_Detection_Sentinel")
    
    with mlflow.start_run():
        print("🧪 Starting Model Training...")
        
        # Load Data
        df = pd.read_csv("data/raw/transactions.csv")
        
        # Simple Preprocessing
        X = df[["amount"]] 
        y = df["is_fraud"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define Hyperparameters
        params = {"n_estimators": 50, "max_depth": 5, "random_state": 42}
        
        # Train Model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        # Evaluate
        predictions = model.predict(X_test)
        f1 = f1_score(y_test, predictions, zero_division=0)

        # --- STEP 3: LOGGING ---
        mlflow.log_params(params)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "fraud_model")
        
        print(f"🎯 Training Complete! F1 Score: {f1}")
        print("🚀 Open MLflow UI (port 5000) to see the results.")

if __name__ == "__main__":
    main()
import mlflow
from mlflow.tracking import MlflowClient
import os

# Ensure we are talking to the Docker MLflow server
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))

def promote_latest_model():
    client = MlflowClient()
    experiment_name = "Fraud_Detection_Sentinel"
    
    # 1. Safely get the experiment
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"❌ Experiment '{experiment_name}' not found. Did you run train.py inside Docker?")
        return

    # 2. Search for the best run
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id], 
        order_by=["metrics.f1_score DESC"], 
        max_results=1
    )
    
    if not runs:
        print("❌ No runs found in MLflow!")
        return

    run_id = runs[0].info.run_id
    f1 = runs[0].data.metrics.get('f1_score', 0)
    print(f"✅ Found best run: {run_id} (F1: {f1})")

    # 3. Register and Alias
    model_name = "SentinelFraudModel"
    model_uri = f"runs:/{run_id}/fraud_model"
    
    print(f"📦 Registering model as '{model_name}'...")
    mv = mlflow.register_model(model_uri, model_name)

    # 4. SET BOTH ALIASES
    # Champion = Production traffic
    client.set_registered_model_alias(model_name, "champion", mv.version)
    
    # Candidate = Shadow traffic (For testing your new logic!)
    client.set_registered_model_alias(model_name, "candidate", mv.version)
    
    print(f"🚀 Model v{mv.version} promoted to @champion and @candidate!")

if __name__ == "__main__":
    promote_latest_model()
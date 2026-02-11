import mlflow
from mlflow.tracking import MlflowClient

def promote_latest_model():
    client = MlflowClient()
    experiment_name = "Fraud_Detection_Sentinel"
    
    # 1. Get the latest run from our experiment
    experiment = client.get_experiment_by_name(experiment_name)
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.f1_score DESC"], max_results=1)
    
    if not runs:
        print("❌ No runs found in MLflow!")
        return

    latest_run_id = runs[0].info.run_id
    print(f"✅ Found best run: {latest_run_id} (F1 Score: {runs[0].data.metrics['f1_score']})")

    # 2. Register the model (Give it a permanent name)
    model_name = "SentinelFraudModel"
    model_uri = f"runs:/{latest_run_id}/fraud_model"
    
    print(f"📦 Registering model as '{model_name}'...")
    result = mlflow.register_model(model_uri, model_name)

    # 3. Promote to 'Staging'
    # In MLOps, we move models through stages: None -> Staging -> Production
    client.set_registered_model_alias(model_name, "champion", result.version)
    print(f"🚀 Model version {result.version} promoted to 'Champion' alias!")

if __name__ == "__main__":
    promote_latest_model()
import mlflow.pyfunc
from fastapi import FastAPI
from pydantic import BaseModel
from src.features import engineer_features
import pandas as pd

app = FastAPI(title="The Sentinel: Fraud Detection API")

model_name = "SentinelFraudModel"

# Load BOTH at startup to keep the /predict endpoint lightning fast
models = {"champion": None, "candidate": None}

def load_models():
    for alias in models.keys():
        try:
            uri = f"models:/{model_name}@{alias}"
            models[alias] = mlflow.pyfunc.load_model(uri)
            print(f"✅ {alias.capitalize()} model loaded")
        except Exception as e:
            print(f"ℹ️ {alias.capitalize()} model not available in registry: {e}")

load_models()

class Transaction(BaseModel):
    id: int
    amount: float

@app.post("/predict")
def predict(data: Transaction):
    if models["champion"] is None:
        return {"error": "Champion model not available. System in maintenance."}

    # 1. Single Source of Truth for Features
    features = engineer_features(pd.DataFrame([data.model_dump()]))
    
    # 2. Production Prediction
    champ_pred = int(models["champion"].predict(features)[0])
    
    # 3. Shadow Prediction (Pre-loaded, so it's instant!)
    if models["candidate"] is not None:
        try:
            cand_pred = int(models["candidate"].predict(features)[0])
            if champ_pred != cand_pred:
                print(f"🚨 MISMATCH: ID {data.id} | Champ: {champ_pred} | Cand: {cand_pred}")
        except Exception as e:
            print(f"⚠️ Shadow prediction failed: {e}")

    return {
        "transaction_id": data.id,
        "is_fraud": champ_pred,
        "metadata": {"model_alias": "champion"}
    }
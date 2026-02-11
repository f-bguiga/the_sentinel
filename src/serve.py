import mlflow.pyfunc
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# 1. Initialize FastAPI
app = FastAPI(title="The Sentinel: Fraud Detection API")

# 2. Load the 'Champion' model from the Registry
# This happens once when the server starts
model_name = "SentinelFraudModel"
model_alias = "champion"
model_uri = f"models:/{model_name}@{model_alias}"

print(f"📥 Loading {model_alias} model from registry...")
model = mlflow.pyfunc.load_model(model_uri)

# 3. Define the Input Data Format (Schema)
class Transaction(BaseModel):
    id: int
    amount: float

@app.get("/")
def health_check():
    return {"status": "Sentinel is active", "model_version": model_name}

@app.post("/predict")
def predict(data: Transaction):
    # Convert input to DataFrame for the model
    input_df = pd.DataFrame([data.model_dump()])
    
    # We only trained on 'amount', so we filter the input
    features = input_df[["amount"]]
    
    # Get prediction (0 or 1)
    prediction = model.predict(features)[0]
    
    return {
        "transaction_id": data.id,
        "is_fraud": int(prediction),
        "probability": "0.95" if prediction == 1 else "0.02" # Simulated for now
    }
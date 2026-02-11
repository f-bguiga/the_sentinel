import mlflow.pyfunc
import pandas as pd
import pytest
import os

def test_model_output_format():
    """Check if the model returns the correct shape and type."""
    # 1. Load the model from the local registry
    # (Using local path for the test environment)
    model_name = "SentinelFraudModel"
    model_alias = "champion"
    model_uri = f"models:/{model_name}@{model_alias}"
    
    try:
        model = mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        pytest.fail(f"Could not load champion model: {e}")

    # 2. Create dummy input
    test_data = pd.DataFrame({"amount": [100.0, 50000.0]})
    
    # 3. Get prediction
    predictions = model.predict(test_data)
    
    # 4. ASSERTIONS: The "DevOps Rules"
    assert len(predictions) == 2, "Model should return one prediction per input row"
    assert predictions[0] in [0, 1], "Predictions must be binary (0 or 1)"
    assert str(predictions.dtype).startswith('int') or str(predictions.dtype).startswith('float'), \
        "Model output must be numeric"

def test_data_path_exists():
    """Ensure our data contract isn't broken."""
    assert os.path.exists("data/raw/transactions.csv"), "Critical: Training data missing!"
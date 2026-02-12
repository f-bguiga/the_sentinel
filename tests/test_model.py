import mlflow.pyfunc
import pandas as pd
import pytest
import os
from src.features import engineer_features  # 👈 Import your feature logic

def test_model_output_format():
    """Check if the model returns the correct shape and type."""
    model_name = "SentinelFraudModel"
    model_alias = "champion"
    model_uri = f"models:/{model_name}@{model_alias}"
    
    try:
        model = mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        pytest.fail(f"Could not load champion model: {e}")

    # 1. Create RAW dummy input
    raw_data = pd.DataFrame({"amount": [100.0, 50000.0]})
    
    # 2. TRANSFORM the data using your feature engine
    # This automatically adds 'is_high_value', satisfying Scikit-Learn
    test_data = engineer_features(raw_data)
    
    # 3. Get prediction
    predictions = model.predict(test_data)
    
    # 4. ASSERTIONS
    assert len(predictions) == 2, "Model should return one prediction per input row"
    assert predictions[0] in [0, 1], "Predictions must be binary (0 or 1)"
    assert str(predictions.dtype).lower().startswith(('int', 'float')), \
        "Model output must be numeric"

def test_data_path_exists():
    """Ensure our data contract isn't broken."""
    assert os.path.exists("data/raw/transactions.csv"), "Critical: Training data missing!"
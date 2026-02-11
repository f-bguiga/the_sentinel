import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    The Single Source of Truth for feature engineering.
    Both training and serving MUST use this function.
    """
    # 1. Ensure we only have the columns the model expects
    # Even if the API receives extra data, we filter it here
    required_cols = ["amount"]
    
    # 2. Example transformation: Let's add a 'is_high_value' flag
    # This is a 'derived feature'
    df["is_high_value"] = (df["amount"] > 1000).astype(int)
    
    # 3. Return only the features the model was trained on
    # (Update this list as you add more features!)
    features = df[["amount", "is_high_value"]]
    
    return features
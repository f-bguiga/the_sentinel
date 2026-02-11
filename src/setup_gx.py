import pandas as pd
import sys
import os

def run_data_validation():
    print("🛠️ Starting Data Validation...")
    csv_path = "data/raw/transactions.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found!")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    errors = []

    # Rule 1: Check if required columns exist
    required_columns = ["id", "amount", "is_fraud"]
    missing_cols = []
    for col in required_columns:
        if col not in df.columns:
            missing_cols.append(col)
            errors.append(f"Missing column: {col}")

    # ONLY run these checks if the columns actually exist (to avoid KeyError)
    if "amount" not in missing_cols:
        if not (df['amount'] >= 0).all():
            errors.append("Negative values found in 'amount' column")
            
    if "is_fraud" not in missing_cols:
        if not df['is_fraud'].isin([0, 1]).all():
            errors.append("Invalid values in 'is_fraud' column (must be 0 or 1)")

    # Rule 2: Check for null values
    if df.isnull().values.any():
        errors.append("Dataset contains null values")

    # Final Report
    if errors:
        print("❌ [DEVOPS CHECK] Data Quality Failed!")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("🚀 [DEVOPS CHECK] Data Quality Passed!")
        print(f"✅ Verified {len(df)} transactions.")
        sys.exit(0)

if __name__ == "__main__":
    run_data_validation()
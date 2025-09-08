"""
Script: evaluate_model.py
Purpose: Evaluate trained GradientBoostingRegressor model, save predictions and metrics.
"""
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import os

def main():
    # Load model and test data
    in_dir = "data/processed_data"
    X_test = pd.read_csv(f"{in_dir}/X_test_scaled.csv")
    y_test = pd.read_csv(f"{in_dir}/y_test.csv")
    model = joblib.load("models/model.pkl")
    # Make predictions
    predictions = model.predict(X_test)
    # Save predictions
    pd.DataFrame(predictions, columns=["predicted_silica_concentrate"]).to_csv("data/predictions.csv", index=False)
    # Calculate metrics
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    metrics = {"MSE": mse, "R2": r2}
    # Save metrics
    out_dir = "metrics"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/scores.json", "w") as f:
        json.dump(metrics, f, indent=4)
    print("Predictions and metrics saved.")

if __name__ == "__main__":
    main()

"""
Script: train_model.py
Purpose: Train regression model using best parameters and save the trained model.
"""
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import os

def main():
    # Load data and best parameters
    in_dir = "data/processed_data"
    X_train = pd.read_csv(f"{in_dir}/X_train_scaled.csv")
    y_train = pd.read_csv(f"{in_dir}/y_train.csv")
    params = joblib.load("models/best_params.pkl")
    # Train GradientBoostingRegressor model
    model = GradientBoostingRegressor(random_state=42, **params)
    model.fit(X_train, y_train.values.ravel())
    # Save trained model
    out_dir = "models"
    joblib.dump(model, f"{out_dir}/model.pkl")
    print("Trained model saved to models/model.pkl")

if __name__ == "__main__":
    main()

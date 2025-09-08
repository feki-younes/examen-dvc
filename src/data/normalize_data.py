"""
Script: normalize_data.py
Purpose: Normalize training and testing data for silica concentration modeling.
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def main():
    # Load train/test data
    in_dir = "data/processed_data"
    X_train = pd.read_csv(f"{in_dir}/X_train.csv")
    X_test = pd.read_csv(f"{in_dir}/X_test.csv")
    # If datetime column exists, drop it
    if X_train.columns[0].lower().startswith("date"):
        X_train = X_train.drop(X_train.columns[0], axis=1)
        X_test = X_test.drop(X_test.columns[0], axis=1)
    # Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    # Save normalized data
    pd.DataFrame(X_train_scaled, columns=X_train.columns).to_csv(f"{in_dir}/X_train_scaled.csv", index=False)
    pd.DataFrame(X_test_scaled, columns=X_test.columns).to_csv(f"{in_dir}/X_test_scaled.csv", index=False)
    print("Data normalized and saved to data/processed_data/")

if __name__ == "__main__":
    main()

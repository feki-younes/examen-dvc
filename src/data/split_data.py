"""
Script: split_data.py
Purpose: Split raw data into training and testing sets for silica concentration modeling.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def main():
    # Load raw data
    raw_path = "data/raw_data/raw.csv"
    df = pd.read_csv(raw_path)
    # Target variable is the last column
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Ensure output directory exists
    out_dir = "data/processed_data"
    os.makedirs(out_dir, exist_ok=True)
    # Save splits
    X_train.to_csv(f"{out_dir}/X_train.csv", index=False)
    X_test.to_csv(f"{out_dir}/X_test.csv", index=False)
    y_train.to_csv(f"{out_dir}/y_train.csv", index=False)
    y_test.to_csv(f"{out_dir}/y_test.csv", index=False)
    print("Data split and saved to data/processed_data/")

if __name__ == "__main__":
    main()

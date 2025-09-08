"""
Script: grid_search.py
Purpose: Perform GridSearchCV to find best regression model parameters.
"""
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import os

def main():
    # Load normalized data
    in_dir = "data/processed_data"
    X_train = pd.read_csv(f"{in_dir}/X_train_scaled.csv")
    y_train = pd.read_csv(f"{in_dir}/y_train.csv")
    # Define GradientBoostingRegressor model and parameter grid
    model = GradientBoostingRegressor(random_state=42)
    param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0]
    }
    grid = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    grid.fit(X_train, y_train.values.ravel())
    # Save best parameters
    out_dir = "models"
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(grid.best_params_, f"{out_dir}/best_params.pkl")
    print("Best parameters saved to models/best_params.pkl")

if __name__ == "__main__":
    main()

#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

# 1. Create and activate virtual environment, install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt

# Ensure all commands run inside the virtual environment
export VIRTUAL_ENV="$(pwd)/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"



# 2. Track raw data (DVC already initialized)
dvc add data/raw_data/raw.csv
git add data/raw_data/raw.csv.dvc .gitignore
git commit -m "Track raw data with DVC"

# 3. Add DVC pipeline stages (use --force to overwrite if they exist)
dvc stage add --force -n split_data \
	-d src/data/split_data.py -d data/raw_data/raw.csv \
	-o data/processed_data/X_train.csv -o data/processed_data/X_test.csv -o data/processed_data/y_train.csv -o data/processed_data/y_test.csv \
	python src/data/split_data.py

dvc stage add --force -n normalize_data \
	-d src/data/normalize_data.py -d data/processed_data/X_train.csv -d data/processed_data/X_test.csv \
	-o data/processed_data/X_train_scaled.csv -o data/processed_data/X_test_scaled.csv \
	python src/data/normalize_data.py

dvc stage add --force -n grid_search \
	-d src/models/grid_search.py -d data/processed_data/X_train_scaled.csv -d data/processed_data/y_train.csv \
	-o models/best_params.pkl \
	python src/models/grid_search.py

dvc stage add --force -n train_model \
	-d src/models/train_model.py -d data/processed_data/X_train_scaled.csv -d data/processed_data/y_train.csv -d models/best_params.pkl \
	-o models/model.pkl \
	python src/models/train_model.py

dvc stage add --force -n evaluate_model \
	-d src/models/evaluate_model.py -d data/processed_data/X_test_scaled.csv -d data/processed_data/y_test.csv -d models/model.pkl \
	-o data/predictions.csv -o metrics/scores.json \
	python src/models/evaluate_model.py

# 4. Commit pipeline files
git add dvc.yaml dvc.lock .gitignore
git commit -m "Add DVC pipeline stages for full workflow"

# 5. Run the pipeline
dvc repro
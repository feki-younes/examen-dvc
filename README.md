# Examen DVC et Dagshub
Dans ce dépôt vous trouverez l'architecture proposé pour mettre en place la solution de l'examen. 

**Nom :** Younes FEKI  
**Email :** younes.feki.93@gmail.com  
**DagsHub Repo :** [https://dagshub.com/feki-younes/examen-dvc.git](https://dagshub.com/feki-younes/examen-dvc.git)
```bash       
├── examen_dvc          
│   ├── data       
│   │   ├── processed_data      
│   │   └── raw_data       
│   ├── metrics       
│   ├── models      
│   │   ├── data      
│   │   └── models        
│   ├── src       
│   └── README.md.py       
```
N'hésitez pas à rajouter les dossiers ou les fichiers qui vous semblent pertinents.
---
## Setup & Execution Instructions


1. **Run the workflow manually (bash script):**
		```bash
		bash src/pipeline.sh
		```

2. **Run the workflow using DVC for full reproducibility:**
		```bash
		# Create and activate a virtual environment
		python3 -m venv .venv
		source .venv/bin/activate
		pip install -r src/requirements.txt

		# Initialize DVC (if not already done)
		dvc init

		# Track your raw data with DVC
		dvc add data/raw_data/raw.csv
		git add data/raw_data/raw.csv.dvc .gitignore
		git commit -m "Track raw data with DVC"

		# Add DVC pipeline stages
		dvc stage add -n split_data \
			-d src/data/split_data.py -d data/raw_data/raw.csv \
			-o data/processed_data/X_train.csv -o data/processed_data/X_test.csv -o data/processed_data/y_train.csv -o data/processed_data/y_test.csv \
			python src/data/split_data.py

		dvc stage add -n normalize_data \
			-d src/data/normalize_data.py -d data/processed_data/X_train.csv -d data/processed_data/X_test.csv \
			-o data/processed_data/X_train_scaled.csv -o data/processed_data/X_test_scaled.csv \
			python src/data/normalize_data.py

		dvc stage add -n grid_search \
			-d src/models/grid_search.py -d data/processed_data/X_train_scaled.csv -d data/processed_data/y_train.csv \
			-o models/best_params.pkl \
			python src/models/grid_search.py

		dvc stage add -n train_model \
			-d src/models/train_model.py -d data/processed_data/X_train_scaled.csv -d data/processed_data/y_train.csv -d models/best_params.pkl \
			-o models/model.pkl \
			python src/models/train_model.py

		dvc stage add -n evaluate_model \
			-d src/models/evaluate_model.py -d data/processed_data/X_test_scaled.csv -d data/processed_data/y_test.csv -d models/model.pkl \
			-o data/predictions.csv -o metrics/scores.json \
			python src/models/evaluate_model.py

		# Commit pipeline files
		git add dvc.yaml dvc.lock .gitignore
		git commit -m "Add DVC pipeline stages for full workflow"

		# Run the pipeline
		dvc repro
		```

---
## Script Descriptions

### src/data/split_data.py
Splits the raw dataset into training and testing sets. Outputs: `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` in `data/processed_data/`.

### src/data/normalize_data.py
Normalizes the training and testing features using standard scaling. Outputs: `X_train_scaled.csv`, `X_test_scaled.csv` in `data/processed_data/`.

### src/models/grid_search.py
Performs grid search to find the best hyperparameters for the regression model. Outputs: `best_params.pkl` in `models/`.

### src/models/train_model.py
Trains the regression model using the best parameters and saves the trained model as `model.pkl` in `models/`.

### src/models/evaluate_model.py
Evaluates the trained model on the test set, saves predictions as `predictions.csv` in `data/`, and evaluation metrics as `scores.json` in `metrics/`.

---

Vous devez dans un premier temps *Fork* le repo et puis le cloner pour travailler dessus. Le rendu de cet examen sera le lien vers votre dépôt sur DagsHub. Faites attention à bien mettre https://dagshub.com/licence.pedago en tant que colaborateur avec des droits de lecture seulement pour que ce soit corrigé.

Vous pouvez télécharger les données à travers le lien suivant : https://datascientest-mlops.s3.eu-west-1.amazonaws.com/mlops_dvc_fr/raw.csv.

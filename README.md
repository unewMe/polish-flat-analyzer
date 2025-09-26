# Polish Flat Analyzer

A small Python project for analyzing Polish flat/room listings and producing plots and simple models.

# Goal

The main goal of this project was to build a model to predict apartment prices based on given parameters (for example: area, location, number of rooms, floor, furnishing/standard, distance to city center, etc.).

# Model details

- Preprocessing:

  - Categorical features (City, Furnished, Market, Building type, Floor, Rooms) are encoded using scikit-learn's OneHotEncoder.
  - The `Floor` field is cleaned (string values like `floor_2` are parsed to integers) and numerical features such as `Area`, `Floor`, and `Rooms` are used in the models.
  - The `Preprocessor` class provides methods to encode/decode data and to cast single inputs into the trained encoding scheme so the model can be used for prediction.

- Models implemented:

  - Random Forest regressor (RandomForestRegressor) — the main model. Hyperparameters are tuned with `GridSearchCV` (search over n_estimators, max_depth, min_samples_split, min_samples_leaf).
  - Linear Regression — a simple baseline model.

- Evaluation:

  - Models are evaluated using Mean Absolute Error (MAE) on a hold-out test set (15% per-city split is used to preserve city distributions).
  - City-wise MAE is also computed and plotted to inspect per-city performance and residuals.

- Outputs and report:
  - Plots (actual vs predicted, residual distributions, MAE by city) can be saved from the model classes.
  - The final experimental results, figures and discussion have been collected in `report/main.pdf`.

# Contents

- `src/` — core modules: data reading, processing, filtering, simple ML models.
- `plots/` — plotting helpers for visual analysis.
- `room-analyzer/` — small utilities and scrapers for fetching/analyzing room listings.
- `notebook.ipynb` — exploratory notebook.

# Quickstart

1. Create a virtual environment (recommended):

```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```
   pip install -r requirements.txt
```

3. (Optional) If you plan to use the spaCy-based bot or any language models, install a spaCy model. For Polish, for example:

```
   python -m spacy download pl_core_news_sm
```

# Running

- Open `notebook.ipynb` in Jupyter Lab / Notebook to explore data and visualizations.
- Run a script directly, for example:

```
  python src/read_data.py
```

Or run the small room analyzer script:

```
python "room-analyzer/main.py"
```

# Notes

- If you add new packages, update `requirements.txt`.

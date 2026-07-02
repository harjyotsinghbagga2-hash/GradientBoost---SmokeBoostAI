"""
Static, verified data pulled directly from GradientBoost__1_.ipynb and the
serialized model. Nothing here is invented — every number traces back to a
notebook cell output or a model attribute.
"""

# ── Model identity ───────────────────────────────────────────────────────
MODEL_NAME = "GradientBoostingClassifier"
MODEL_PARAMS = {
    "n_estimators": 100,
    "learning_rate": 0.05,
    "max_depth": 5,
    "criterion": "friedman_mse",
    "subsample": 1.0,
    "loss": "log_loss",
}

# ── Dataset ───────────────────────────────────────────────────────────────
DATASET_NAME = "Medical Insurance Payout"
DATASET_SOURCE = "Kaggle · harshsingh2209/medical-insurance-payout"
N_ROWS = 1338
N_ROWS_DEDUP = 1337
N_FEATURES_RAW = 6
TARGET_BALANCE = {"non_smoker": 79.51, "smoker": 20.49}

FEATURE_STATS = {
    "age":      {"min": 18,     "max": 64,    "mean": 39.21,  "std": 14.05, "median": 39},
    "bmi":      {"min": 15.96,  "max": 53.13, "mean": 30.66,  "std": 6.10,  "median": 30.4},
    "children": {"min": 0,      "max": 5,     "mean": 1.09,   "std": 1.21,  "median": 1},
    "charges":  {"min": 1121.87, "max": 63770.43, "mean": 13270.42, "std": 12110.01, "median": 9382.03},
}

REGIONS = ["northeast", "northwest", "southeast", "southwest"]
SEXES = ["female", "male"]

# ── Trained model performance (test split, 20%, n=268) ──────────────────
TEST_ACCURACY = 0.9739
TRAIN_ACCURACY = 0.9972  # base (untuned) estimator, shown for overfit context

CLASSIFICATION_REPORT = {
    "non_smoker": {"precision": 0.99, "recall": 0.98, "f1": 0.98, "support": 208},
    "smoker":     {"precision": 0.92, "recall": 0.95, "f1": 0.93, "support": 60},
    "macro_avg":  {"precision": 0.95, "recall": 0.96, "f1": 0.96},
    "weighted_avg": {"precision": 0.97, "recall": 0.97, "f1": 0.97},
}

# Feature importances exactly as reported by the fitted estimator
FEATURE_IMPORTANCE = {
    "charges": 0.7754,
    "bmi": 0.1588,
    "age": 0.0592,
    "children": 0.0031,
    "sex_male": 0.0011,
    "sex_female": 0.0010,
    "region_southwest": 0.0006,
    "region_southeast": 0.0006,
    "region_northwest": 0.0002,
    "region_northeast": 0.0001,
}

# The exact column order the estimator expects at inference time
MODEL_FEATURE_ORDER = [
    "age", "bmi", "children", "charges",
    "sex_female", "sex_male",
    "region_northeast", "region_northwest", "region_southeast", "region_southwest",
]

# Hyperparameter search space explored via RandomizedSearchCV (cv=5, n_iter=10)
SEARCH_SPACE = {
    "n_estimators": [100, 150, 200, 250],
    "learning_rate": [0.1, 0.2, 0.05, 0.4],
    "max_depth": [3, 4, 5, 6],
    "min_samples_split": [2, 3, 4, 5],
}

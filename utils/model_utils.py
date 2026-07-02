"""
Model loading + inference helpers.

Uses pathlib for path resolution (not a hardcoded OS-specific path) so the
app behaves identically on Windows, macOS, Linux, and Streamlit Cloud.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils.data import MODEL_FEATURE_ORDER

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "GradientBoost.pkl"


@st.cache_resource(show_spinner=False)
def load_model():
    """Load the trained GradientBoostingClassifier once per session."""
    return joblib.load(MODEL_PATH)


def build_feature_row(age: int, bmi: float, children: int, charges: float,
                       sex: str, region: str) -> pd.DataFrame:
    """
    Reconstruct the exact one-hot-encoded row the model was trained on.
    Column order matters for a small number of sklearn versions, so we
    always reindex against MODEL_FEATURE_ORDER before returning.
    """
    row = {
        "age": age,
        "bmi": bmi,
        "children": children,
        "charges": charges,
        "sex_female": 1 if sex == "female" else 0,
        "sex_male": 1 if sex == "male" else 0,
        "region_northeast": 1 if region == "northeast" else 0,
        "region_northwest": 1 if region == "northwest" else 0,
        "region_southeast": 1 if region == "southeast" else 0,
        "region_southwest": 1 if region == "southwest" else 0,
    }
    df = pd.DataFrame([row])
    return df.reindex(columns=MODEL_FEATURE_ORDER)


def predict(model, features: pd.DataFrame):
    """Return (predicted_label:int, probability_smoker:float, probability_non_smoker:float)."""
    proba = model.predict_proba(features)[0]
    pred = int(model.predict(features)[0])
    prob_non_smoker, prob_smoker = float(proba[0]), float(proba[1])
    return pred, prob_smoker, prob_non_smoker

import streamlit as st
from utils.components import icon, eyebrow
from utils.data import MODEL_NAME, DATASET_NAME, DATASET_SOURCE, MODEL_FEATURE_ORDER


def render():
    st.markdown(f"""
    <div class="reveal d1" style="margin-bottom:20px;">
      {eyebrow("PROJECT NOTES")}
      <h2 style="margin:14px 0 6px;">About this build</h2>
      <div style="color:var(--text-mid); font-size:.95rem; max-width:700px;">
        A portfolio piece demonstrating an end-to-end path from a raw Kaggle CSV to a
        production-styled inference app — preprocessing choices, tuning, and honest
        limitations included.
      </div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("layers", "1 · Ingest & clean", "Loaded via kagglehub, checked for nulls (none) and duplicates (1 row, dropped)."),
        ("cube", "2 · Encode", "Categorical sex/region one-hot encoded with pd.get_dummies; smoker target mapped yes/no → 1/0."),
        ("target", "3 · Split", "80/20 train/test split, random_state=42, stratification implicit in class proportions."),
        ("chart", "4 · Tune", f"RandomizedSearchCV (cv=5, n_iter=10) over n_estimators/learning_rate/max_depth/min_samples_split."),
        ("shield", "5 · Evaluate", "Accuracy, per-class precision/recall/F1, and confusion matrix on the untouched test split."),
        ("flame", "6 · Serve", f"Best estimator persisted with joblib and loaded here via @st.cache_resource for zero-reload inference."),
    ]
    cols = st.columns(3, gap="medium")
    for i, (ic, title, body) in enumerate(steps):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="glass glass-pad glass-hover" style="margin-bottom:18px; height:200px;">
              <div class="icon-orb" style="width:52px; height:52px; margin-bottom:12px; background:rgba(59,130,246,.1); color:var(--cyan);">{icon(ic)}</div>
              <div style="font-family:var(--font-display); font-weight:600; color:var(--text-hi); margin-bottom:6px;">{title}</div>
              <div style="font-size:.83rem; line-height:1.55;">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.1, 1], gap="large")
    with c1:
        st.markdown('<div class="glass glass-pad" style="height:100%;">', unsafe_allow_html=True)
        st.markdown("**Model card**")
        rows = [
            ("Algorithm", MODEL_NAME),
            ("Task", "Binary classification (smoker vs. non-smoker)"),
            ("Training data", f"{DATASET_NAME} — {DATASET_SOURCE}"),
            ("Input features", f"{len(MODEL_FEATURE_ORDER)} (post-encoding)"),
            ("Serialization", "joblib (.pkl)"),
            ("Known limitation", "77.5% of importance sits on one feature (charges) — the model is largely a charges-threshold detector, not a holistic behavioral profile."),
        ]
        for k, v in rows:
            st.markdown(f'<div style="padding:9px 0; border-bottom:1px solid var(--glass-border);"><div style="font-size:.7rem; text-transform:uppercase; letter-spacing:.05em; color:var(--text-low);">{k}</div><div style="color:var(--text-hi); font-size:.88rem; margin-top:2px;">{v}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass glass-pad" style="height:100%;">', unsafe_allow_html=True)
        st.markdown("**Stack**")
        stack = ["Streamlit", "scikit-learn", "Plotly", "pandas / NumPy", "joblib", "Custom CSS (no UI framework)"]
        for s in stack:
            st.markdown(f'<span class="badge badge-blue" style="margin:4px 6px 4px 0;">{s}</span>', unsafe_allow_html=True)
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown("**Links**")
        st.caption("Drop your own URLs into `sections/about.py` — placeholders below.")
        lc1, lc2, lc3 = st.columns(3)
        lc1.link_button("GitHub", "https://github.com", width="stretch")
        lc2.link_button("LinkedIn", "https://linkedin.com", width="stretch")
        lc3.link_button("Live demo", "https://streamlit.io", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

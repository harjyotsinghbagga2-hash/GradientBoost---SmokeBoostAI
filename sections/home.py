import streamlit as st
from utils.components import icon, eyebrow
from utils.data import (
    TEST_ACCURACY, CLASSIFICATION_REPORT, N_ROWS, MODEL_NAME,
)


def render():
    st.markdown(f"""
    <div class="hero-wrap reveal d1">
      {eyebrow("GRADIENT BOOSTING &middot; BINARY CLASSIFIER")}
      <div class="hero-title">
        Predict smoker status<br/>
        from a <span class="grad-text">medical insurance profile.</span>
      </div>
      <div class="hero-sub">
        SmokeBoost AI reads six everyday insurance-application fields — age, BMI, dependents,
        billed charges, sex, and region — and infers smoker status with a tuned
        {MODEL_NAME}, trained on 1,338 real policyholder records. Built for underwriters,
        actuarial teams, and anyone auditing risk models for leakage and fairness.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1], gap="medium")
    with c1:
        if st.button("Run a prediction  →", type="primary", width="stretch", key="hero_cta"):
            st.session_state.page = "Predict"
            st.rerun()
    with c2:
        if st.button("Inspect model internals", type="secondary", width="stretch", key="hero_cta2"):
            st.session_state.page = "Insights"
            st.rerun()

    st.markdown('<div style="height:34px"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row reveal d2">
      <div class="glass glass-pad stat-chip">
        <div class="val">{TEST_ACCURACY*100:.1f}%</div>
        <div class="lab">Held-out accuracy</div>
      </div>
      <div class="glass glass-pad stat-chip">
        <div class="val">{CLASSIFICATION_REPORT['smoker']['recall']*100:.0f}%</div>
        <div class="lab">Smoker recall</div>
      </div>
      <div class="glass glass-pad stat-chip">
        <div class="val">{N_ROWS:,}</div>
        <div class="lab">Training records</div>
      </div>
      <div class="glass glass-pad stat-chip">
        <div class="val">10</div>
        <div class="lab">Encoded features</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

    cards = [
        ("target", "Charges dominate the signal", "Billed medical charges alone carry 77.5% of the model's decision weight — smokers are billed dramatically more, and the model learned that pattern directly."),
        ("layers", "Tuned via RandomizedSearchCV", "A 5-fold cross-validated random search swept 10 candidate configurations across n_estimators, learning_rate, max_depth, and min_samples_split."),
        ("shield", "Class imbalance, handled honestly", "The source population is 79.5% non-smokers. Metrics below are reported per-class so the minority (smoker) performance isn't hidden behind overall accuracy."),
    ]
    cols = st.columns(3, gap="medium")
    for col, (ic, title, body) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="glass glass-pad glass-hover reveal d3" style="height:100%;">
              <div class="icon-orb" style="background:linear-gradient(140deg, rgba(59,130,246,.16), rgba(168,85,247,.12)); color:var(--cyan);">{icon(ic)}</div>
              <div style="font-family:var(--font-display); font-weight:600; font-size:1.02rem; color:var(--text-hi); text-align:center; margin-bottom:8px;">{title}</div>
              <div style="font-size:.87rem; line-height:1.6; text-align:center;">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

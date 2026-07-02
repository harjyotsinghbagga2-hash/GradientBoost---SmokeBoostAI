import streamlit as st

from utils.components import icon, eyebrow, gauge, confetti_burst
from utils.data import FEATURE_STATS, REGIONS, SEXES
from utils.model_utils import load_model, build_feature_row, predict


def render():
    st.markdown(f"""
    <div class="reveal d1" style="margin-bottom:26px;">
      {eyebrow("LIVE INFERENCE")}
      <h2 style="margin:14px 0 6px;">Applicant profile</h2>
      <div style="color:var(--text-mid); font-size:.95rem;">Fill in the six fields exactly as they'd appear on an insurance intake form.</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([0.92, 1.08], gap="large")

    with left:
        st.markdown('<div class="glass glass-pad reveal d2">', unsafe_allow_html=True)

        age = st.slider("Age", min_value=18, max_value=64,
                         value=int(FEATURE_STATS["age"]["median"]), help="Applicant age in years (dataset range: 18–64).")

        bmi = st.slider("Body Mass Index (BMI)", min_value=15.0, max_value=54.0,
                         value=float(FEATURE_STATS["bmi"]["median"]), step=0.1,
                         help="kg/m². Dataset range: 15.96–53.13.")

        children = st.slider("Dependents covered", min_value=0, max_value=5,
                              value=int(FEATURE_STATS["children"]["median"]),
                              help="Number of children/dependents on the policy.")

        charges = st.number_input("Billed annual charges ($)", min_value=1000.0, max_value=65000.0,
                                   value=float(FEATURE_STATS["charges"]["median"]), step=100.0,
                                   help="Total medical charges billed — the single strongest predictor (77.5% importance).")

        c1, c2 = st.columns(2)
        with c1:
            sex = st.selectbox("Sex", SEXES, index=0)
        with c2:
            region = st.selectbox("Region", REGIONS, index=2)

        st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
        run = st.button("Run prediction", type="primary", width="stretch", key="predict_cta")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("What exactly gets sent to the model?"):
            st.caption("Categorical fields are one-hot encoded to match training-time preprocessing, then reindexed to the model's exact column order before inference.")
            st.code(
                f'{{"age": {age}, "bmi": {bmi}, "children": {children}, "charges": {charges},\n'
                f' "sex_female": {1 if sex=="female" else 0}, "sex_male": {1 if sex=="male" else 0},\n'
                f' "region_northeast": {1 if region=="northeast" else 0}, "region_northwest": {1 if region=="northwest" else 0},\n'
                f' "region_southeast": {1 if region=="southeast" else 0}, "region_southwest": {1 if region=="southwest" else 0}}}',
                language="python",
            )

    if run:
        model = load_model()
        row = build_feature_row(age, bmi, children, charges, sex, region)
        pred, prob_smoker, prob_non_smoker = predict(model, row)
        st.session_state.last_result = {
            "pred": pred, "prob_smoker": prob_smoker, "prob_non_smoker": prob_non_smoker,
        }

    with right:
        result = st.session_state.get("last_result")
        if not result:
            st.markdown("""
            <div class="glass glass-pad reveal d2" style="height:100%; display:flex; flex-direction:column;
                 align-items:center; justify-content:center; text-align:center; min-height:420px;">
              <div class="icon-orb" style="background:rgba(255,255,255,.05); color:var(--text-low); width:64px; height:64px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" style="width:28px;height:28px;">
                  <path d="M12 2c1 3-2 4-2 7a4 4 0 0 0 8 0c0-1.5-1-2.5-1-2.5 1 4-1 6-3 6a3 3 0 0 1-3-3c0-2 2-3 1-7.5Z"/>
                </svg>
              </div>
              <div style="color:var(--text-mid); font-size:.92rem; max-width:280px;">
                Set the applicant profile and run a prediction — the risk verdict and Combustion Index
                will render here.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            is_smoker = result["pred"] == 1
            prob_pct = result["prob_smoker"] * 100 if is_smoker else result["prob_non_smoker"] * 100
            color = "var(--ember)" if is_smoker else "var(--safe)"
            color_hex = "#FF5A3C" if is_smoker else "#2BE7A6"
            panel_class = "result-ember" if is_smoker else "result-safe"
            badge_class = "badge-ember" if is_smoker else "badge-safe"
            label = "Smoker detected" if is_smoker else "Non-smoker profile"
            sub = "Elevated risk indicators align with the smoker cohort in training data." if is_smoker \
                else "Profile aligns with the non-smoker cohort in training data."
            ic = icon("flame") if is_smoker else icon("shield")

            st.markdown(f"""
            <div class="glass glass-pad {panel_class} reveal" style="text-align:center;">
              <div class="icon-orb" style="background:{'rgba(255,90,60,.12)' if is_smoker else 'rgba(43,231,166,.12)'}; color:{color};">{ic}</div>
              <div class="badge {badge_class}" style="margin-bottom:10px;">{label.upper()}</div>
              <div style="font-family:var(--font-display); font-size:1.3rem; font-weight:600; color:var(--text-hi); margin-bottom:4px;">{label}</div>
              <div style="font-size:.85rem; max-width:320px; margin:0 auto 6px;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

            fig = gauge(round(prob_pct, 1), "COMBUSTION INDEX — MODEL CONFIDENCE", color_hex)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

            bc1, bc2 = st.columns(2)
            with bc1:
                st.markdown(f"""
                <div class="glass glass-pad" style="text-align:center;">
                  <div class="mono" style="font-size:1.35rem; font-weight:600; color:var(--ember);">{result['prob_smoker']*100:.1f}%</div>
                  <div style="font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; color:var(--text-low);">P(smoker)</div>
                </div>
                """, unsafe_allow_html=True)
            with bc2:
                st.markdown(f"""
                <div class="glass glass-pad" style="text-align:center;">
                  <div class="mono" style="font-size:1.35rem; font-weight:600; color:var(--safe);">{result['prob_non_smoker']*100:.1f}%</div>
                  <div style="font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; color:var(--text-low);">P(non-smoker)</div>
                </div>
                """, unsafe_allow_html=True)

            if not is_smoker and prob_pct > 60:
                confetti_burst()

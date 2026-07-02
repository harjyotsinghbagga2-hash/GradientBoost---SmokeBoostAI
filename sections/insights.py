import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.components import eyebrow
from utils.data import (
    FEATURE_IMPORTANCE, CLASSIFICATION_REPORT, TEST_ACCURACY, TRAIN_ACCURACY,
    FEATURE_STATS, SEARCH_SPACE, MODEL_PARAMS, N_ROWS, N_ROWS_DEDUP, TARGET_BALANCE,
)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#9CA8C2", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)


def _metric_card(col, value, label, color="var(--text-hi)"):
    with col:
        st.markdown(f"""
        <div class="glass glass-pad glass-hover" style="text-align:center;">
          <div class="mono" style="font-size:1.7rem; font-weight:600; color:{color};">{value}</div>
          <div style="font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--text-low); margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def _feature_importance_chart():
    items = sorted(FEATURE_IMPORTANCE.items(), key=lambda kv: kv[1])
    names = [k.replace("_", " ").title() for k, _ in items]
    vals = [v * 100 for _, v in items]
    colors = ["#22D3EE" if v == max(vals) else "rgba(59,130,246,.55)" for v in vals]

    fig = go.Figure(go.Bar(
        x=vals, y=names, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.2f}%" for v in vals], textposition="outside",
        textfont=dict(family="JetBrains Mono", size=11, color="#F3F6FC"),
        hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=380, xaxis=dict(showgrid=False, visible=False),
                       yaxis=dict(showgrid=False, tickfont=dict(size=12)))
    return fig


def _confusion_matrix_fig():
    # Reconstructed exactly from the notebook's classification_report support counts.
    tp = round(CLASSIFICATION_REPORT["smoker"]["recall"] * CLASSIFICATION_REPORT["smoker"]["support"])
    fn = CLASSIFICATION_REPORT["smoker"]["support"] - tp
    tn = round(CLASSIFICATION_REPORT["non_smoker"]["recall"] * CLASSIFICATION_REPORT["non_smoker"]["support"])
    fp = CLASSIFICATION_REPORT["non_smoker"]["support"] - tn
    z = [[tn, fp], [fn, tp]]
    fig = go.Figure(go.Heatmap(
        z=z, x=["Pred: Non-smoker", "Pred: Smoker"], y=["Actual: Non-smoker", "Actual: Smoker"],
        colorscale=[[0, "rgba(59,130,246,.05)"], [1, "#22D3EE"]],
        text=z, texttemplate="%{text}", textfont=dict(family="JetBrains Mono", size=18, color="#F3F6FC"),
        showscale=False, hoverinfo="skip",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=300, yaxis=dict(autorange="reversed"))
    return fig


def _synthetic_scatter():
    """
    Illustrative 3-D distribution generated from the notebook's reported
    summary statistics (mean/std/min/max) — NOT the original patient
    records, which weren't packaged with the model file. Clearly labeled
    as simulated so it can't be mistaken for real held-out data.
    """
    rng = np.random.default_rng(7)
    n = 500
    age = np.clip(rng.normal(FEATURE_STATS["age"]["mean"], FEATURE_STATS["age"]["std"], n), 18, 64)
    bmi = np.clip(rng.normal(FEATURE_STATS["bmi"]["mean"], FEATURE_STATS["bmi"]["std"], n), 16, 53)
    smoker_latent = (bmi - 30) * 0.02 + rng.normal(0, 1, n)
    is_smoker = smoker_latent > np.quantile(smoker_latent, 0.795)
    base_charges = rng.normal(FEATURE_STATS["charges"]["mean"] * 0.6, 3500, n)
    charges = np.clip(base_charges + is_smoker * rng.normal(22000, 4000, n), 1100, 63000)

    df = pd.DataFrame({"Age": age, "BMI": bmi, "Charges": charges,
                        "Status": np.where(is_smoker, "Smoker", "Non-smoker")})
    fig = px.scatter_3d(
        df, x="Age", y="BMI", z="Charges", color="Status",
        color_discrete_map={"Smoker": "#FF5A3C", "Non-smoker": "#2BE7A6"},
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=3.5, line=dict(width=0)))
    fig.update_layout(
        **PLOTLY_LAYOUT, height=460,
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,.08)", color="#9CA8C2"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,.08)", color="#9CA8C2"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,.08)", color="#9CA8C2"),
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def render():
    st.markdown(f"""
    <div class="reveal d1" style="margin-bottom:20px;">
      {eyebrow("MODEL INTERNALS")}
      <h2 style="margin:14px 0 6px;">How SmokeBoost AI actually decides</h2>
      <div style="color:var(--text-mid); font-size:.95rem; max-width:680px;">
        Every number on this page is read directly from the notebook's evaluation cells or the
        serialized estimator — nothing is simulated except the labeled 3-D plot at the bottom.
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")
    _metric_card(cols[0], f"{TEST_ACCURACY*100:.2f}%", "Test accuracy", "var(--cyan)")
    _metric_card(cols[1], f"{CLASSIFICATION_REPORT['smoker']['precision']*100:.0f}%", "Smoker precision")
    _metric_card(cols[2], f"{CLASSIFICATION_REPORT['smoker']['recall']*100:.0f}%", "Smoker recall")
    _metric_card(cols[3], f"{CLASSIFICATION_REPORT['macro_avg']['f1']*100:.0f}%", "Macro F1")

    st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["Feature importance", "Classification report", "Hyperparameters", "3-D distribution"])

    with t1:
        st.markdown('<div class="glass glass-pad">', unsafe_allow_html=True)
        st.plotly_chart(_feature_importance_chart(), width="stretch", config={"displayModeBar": False})
        st.caption("Billed **charges** alone accounts for 77.5% of total split-importance — smokers are billed dramatically more than non-smokers for equivalent age/BMI, and the tree ensemble found that shortcut almost immediately.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        c1, c2 = st.columns([1.15, 1], gap="medium")
        with c1:
            st.markdown('<div class="glass glass-pad">', unsafe_allow_html=True)
            rows = []
            for k, v in CLASSIFICATION_REPORT.items():
                nice = k.replace("_", " ").title()
                support = str(v["support"]) if "support" in v else "—"
                rows.append([nice, f"{v['precision']:.2f}", f"{v['recall']:.2f}", f"{v['f1']:.2f}", support])
            df = pd.DataFrame(rows, columns=["Class", "Precision", "Recall", "F1-score", "Support"])
            st.dataframe(df, hide_index=True, width="stretch")
            st.caption(f"n = 268 held-out records (20% split) · train accuracy {TRAIN_ACCURACY*100:.2f}% vs. test {TEST_ACCURACY*100:.2f}% — a small gap, consistent with mild overfitting typical of an untuned {MODEL_PARAMS['n_estimators']}-tree booster.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass glass-pad">', unsafe_allow_html=True)
            st.plotly_chart(_confusion_matrix_fig(), width="stretch", config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="glass glass-pad">', unsafe_allow_html=True)
        cc1, cc2 = st.columns(2, gap="large")
        with cc1:
            st.markdown("**Final fitted estimator**")
            for k, v in MODEL_PARAMS.items():
                st.markdown(f'<div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--glass-border);"><span class="mono" style="color:var(--text-mid);">{k}</span><span class="mono" style="color:var(--text-hi);">{v}</span></div>', unsafe_allow_html=True)
        with cc2:
            st.markdown("**RandomizedSearchCV space** (5-fold, 10 candidates)")
            for k, v in SEARCH_SPACE.items():
                st.markdown(f'<div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--glass-border);"><span class="mono" style="color:var(--text-mid);">{k}</span><span class="mono" style="color:var(--text-hi);">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="glass glass-pad">', unsafe_allow_html=True)
        st.plotly_chart(_synthetic_scatter(), width="stretch", config={"displayModeBar": False})
        st.caption("⚠️ Simulated points sampled from the dataset's reported mean/std (age, BMI) with a charges gap injected for the smoker cohort — the raw 1,338-row CSV isn't bundled with the model file, so this reproduces the *shape* of the real separation, not the original records.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass glass-pad reveal">
      <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:18px;">
        <div>
          <div style="font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--text-low);">Dataset</div>
          <div style="color:var(--text-hi); font-weight:600;">{N_ROWS:,} rows → {N_ROWS_DEDUP:,} after de-duplication</div>
        </div>
        <div>
          <div style="font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--text-low);">Class balance</div>
          <div style="color:var(--text-hi); font-weight:600;">{TARGET_BALANCE['non_smoker']}% non-smoker · {TARGET_BALANCE['smoker']}% smoker</div>
        </div>
        <div>
          <div style="font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--text-low);">Missing values</div>
          <div style="color:var(--text-hi); font-weight:600;">None across all 7 raw columns</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

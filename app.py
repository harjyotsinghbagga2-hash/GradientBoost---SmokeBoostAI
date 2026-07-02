import streamlit as st

from utils.theme import inject_theme
from utils.particles import inject_background
from utils.data import TEST_ACCURACY, MODEL_PARAMS, N_ROWS
from sections import home, predict, insights, about

st.set_page_config(
    page_title="SmokeBoost AI · Smoker Status Classifier",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
inject_background()

if "page" not in st.session_state:
    st.session_state.page = "Home"

PAGES = {
    "Home": (":material/home:", home),
    "Predict": (":material/bolt:", predict),
    "Insights": (":material/insights:", insights),
    "About": (":material/info:", about),
}

with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-mark"></div>
      <div>
        <div class="brand-name">SmokeBoost AI</div>
        <div class="brand-tag">RISK INFERENCE ENGINE</div>
      </div>
    </div>
    <div style="height:22px"></div>
    """, unsafe_allow_html=True)

    for name, (mat_icon, _) in PAGES.items():
        active = st.session_state.page == name
        if st.button(name, icon=mat_icon, key=f"nav_{name}",
                     type="primary" if active else "secondary",
                     width="stretch"):
            st.session_state.page = name
            st.rerun()

    st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
    st.markdown("""<div style="font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; color:var(--text-low); margin-bottom:10px;">Model snapshot</div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass mini-metric">
      <div class="mv">{TEST_ACCURACY*100:.2f}%</div>
      <div class="ml">Test accuracy</div>
    </div>
    <div class="glass mini-metric">
      <div class="mv">{MODEL_PARAMS['n_estimators']} trees</div>
      <div class="ml">Depth {MODEL_PARAMS['max_depth']} · lr {MODEL_PARAMS['learning_rate']}</div>
    </div>
    <div class="glass mini-metric">
      <div class="mv">{N_ROWS:,}</div>
      <div class="ml">Training records</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    st.caption("Gradient Boosting · scikit-learn · Streamlit")

_, page_module = PAGES[st.session_state.page]
page_module.render()

st.markdown("""
<div class="footer-strip">
  <div>SmokeBoost AI — portfolio build, not a medical or underwriting decision tool.</div>
  <div class="mono">v1.0 · GradientBoostingClassifier</div>
</div>
""", unsafe_allow_html=True)

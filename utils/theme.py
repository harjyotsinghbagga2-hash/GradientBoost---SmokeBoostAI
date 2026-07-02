"""
SmokeBoost AI — visual design system.

Palette rationale (documented, not arbitrary):
  --void        #050505   true-black canvas
  --navy        #0B1220   secondary glass substrate
  --blue        #3B82F6   primary structural accent (charts, links, focus)
  --cyan        #22D3EE   secondary accent (highlights, active nav)
  --violet      #A855F7   tertiary accent (hero glow, decorative only)
  --ember       #FF5A3C   RISK accent — reserved exclusively for "Smoker
                           Detected" states. Warm/red reads as elevated
                           health risk, which is the correct semantic here
                           (unlike a generic dashboard, "positive" is not
                           "good news" in this domain).
  --safe        #2BE7A6   SAFE accent — reserved exclusively for
                           "Non-Smoker" states.
Ember and Safe are used nowhere else in the UI, so when they appear the
user's eye reads them instantly as the verdict — that restraint is the
whole point of having them.

Typography:
  Space Grotesk — display / headings (angular, technical, on-brand for an
                  instrument-panel feel)
  Inter         — UI text / body copy
  JetBrains Mono — numeric readouts, feature values, code-like data
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --void:#050505;
  --navy:#0B1220;
  --navy-soft:#101a2c;
  --blue:#3B82F6;
  --cyan:#22D3EE;
  --violet:#A855F7;
  --ember:#FF5A3C;
  --safe:#2BE7A6;
  --glass:rgba(255,255,255,0.045);
  --glass-strong:rgba(255,255,255,0.075);
  --glass-border:rgba(255,255,255,0.09);
  --text-hi:#F3F6FC;
  --text-mid:#9CA8C2;
  --text-low:#5C6884;
  --font-display:'Space Grotesk',sans-serif;
  --font-body:'Inter',sans-serif;
  --font-mono:'JetBrains Mono',monospace;
}

/* ── base reset ─────────────────────────────────────────────── */
html, body, [class*="css"]{ font-family: var(--font-body); }
#MainMenu, header[data-testid="stHeader"], footer{ visibility:hidden; height:0; }
.stApp{
  background: var(--void);
  color: var(--text-hi);
}
.block-container{
  padding-top: 1.5rem !important;
  padding-bottom: 4rem !important;
  max-width: 1180px;
}
::selection{ background: var(--blue); color:#fff; }

/* thin neon scrollbar */
::-webkit-scrollbar{ width:8px; height:8px; }
::-webkit-scrollbar-track{ background:var(--void); }
::-webkit-scrollbar-thumb{ background:linear-gradient(var(--blue),var(--violet)); border-radius:8px; }

/* ── fixed aurora + particle canvas layer (see particles.py) ──── */
#aurora-layer{
  position:fixed; inset:0; z-index:-2; overflow:hidden; pointer-events:none;
  background: var(--void);
}
.aurora-blob{
  position:absolute; border-radius:50%; filter: blur(90px); opacity:.38;
  will-change: transform;
}
.blob-a{ width:560px; height:560px; top:-180px; left:-120px;
  background: radial-gradient(circle at 30% 30%, var(--blue), transparent 70%);
  animation: drift-a 26s ease-in-out infinite; }
.blob-b{ width:620px; height:620px; bottom:-220px; right:-160px;
  background: radial-gradient(circle at 60% 40%, var(--violet), transparent 70%);
  animation: drift-b 32s ease-in-out infinite; }
.blob-c{ width:480px; height:480px; top:38%; left:46%;
  background: radial-gradient(circle at 50% 50%, var(--cyan), transparent 72%);
  animation: drift-c 22s ease-in-out infinite; opacity:.22; }
@keyframes drift-a{ 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(80px,60px) scale(1.12)} }
@keyframes drift-b{ 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(-70px,-50px) scale(1.08)} }
@keyframes drift-c{ 0%,100%{transform:translate(-30px,0) scale(.9)} 50%{transform:translate(40px,-40px) scale(1.05)} }

#particles-canvas{ position:fixed; inset:0; z-index:-1; pointer-events:none; }

.grain{ position:fixed; inset:0; z-index:-1; pointer-events:none; opacity:.025;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* ── typography ─────────────────────────────────────────────── */
h1,h2,h3,h4{ font-family: var(--font-display); letter-spacing:-0.02em; color:var(--text-hi); }
p, span, div, label{ color: var(--text-mid); }
.mono{ font-family: var(--font-mono); }

.eyebrow{
  display:inline-flex; align-items:center; gap:8px; font-family:var(--font-mono);
  font-size:.72rem; letter-spacing:.18em; text-transform:uppercase; color:var(--cyan);
  padding:5px 12px; border:1px solid rgba(34,211,238,.28); border-radius:100px;
  background:rgba(34,211,238,.06);
}
.eyebrow .dot{ width:6px; height:6px; border-radius:50%; background:var(--cyan);
  box-shadow:0 0 8px var(--cyan); animation:pulse-dot 2s ease-in-out infinite; }
@keyframes pulse-dot{ 0%,100%{opacity:1} 50%{opacity:.3} }

.grad-text{
  background: linear-gradient(100deg, #fff 10%, var(--cyan) 45%, var(--violet) 80%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  background-size:200% auto; animation: sheen 6s linear infinite;
}
@keyframes sheen{ to{ background-position:200% center; } }

/* ── glass panel primitive ─────────────────────────────────── */
.glass{
  background: linear-gradient(160deg, var(--glass-strong), var(--glass));
  border:1px solid var(--glass-border);
  border-radius:20px;
  backdrop-filter: blur(18px) saturate(140%);
  -webkit-backdrop-filter: blur(18px) saturate(140%);
  box-shadow: 0 8px 32px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.04);
  position:relative;
}
.glass::before{
  content:''; position:absolute; inset:0; border-radius:20px; padding:1px;
  background: linear-gradient(120deg, rgba(59,130,246,.35), rgba(255,255,255,0) 30%, rgba(168,85,247,.28));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  opacity:.7; pointer-events:none;
}
.glass-pad{ padding: 28px 30px; }
.glass-hover{ transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease, border-color .35s ease; }
.glass-hover:hover{
  transform: translateY(-6px);
  border-color: rgba(34,211,238,.35);
  box-shadow: 0 20px 45px rgba(0,0,0,.45), 0 0 0 1px rgba(34,211,238,.12), inset 0 1px 0 rgba(255,255,255,.06);
}

/* ── hero ───────────────────────────────────────────────────── */
.hero-wrap{ padding: 46px 4px 10px; }
.hero-title{ font-size: clamp(2.4rem, 5.2vw, 4.1rem); line-height:1.04; font-weight:700; margin:18px 0 14px; }
.hero-sub{ font-size:1.06rem; color:var(--text-mid); max-width:640px; line-height:1.65; margin-bottom:28px; }

/* stat chips row */
.stat-row{ display:flex; gap:16px; flex-wrap:wrap; margin-top:8px; }
.stat-chip{ flex:1; min-width:150px; padding:18px 20px; }
.stat-chip .val{ font-family:var(--font-mono); font-size:1.7rem; font-weight:600; color:var(--text-hi); }
.stat-chip .lab{ font-size:.76rem; letter-spacing:.06em; text-transform:uppercase; color:var(--text-low); margin-top:4px; }

/* ── badges ─────────────────────────────────────────────────── */
.badge{ display:inline-flex; align-items:center; gap:6px; font-family:var(--font-mono);
  font-size:.72rem; padding:4px 11px; border-radius:100px; letter-spacing:.05em; }
.badge-blue{ color:var(--blue); background:rgba(59,130,246,.1); border:1px solid rgba(59,130,246,.3); }
.badge-safe{ color:var(--safe); background:rgba(43,231,166,.1); border:1px solid rgba(43,231,166,.32); }
.badge-ember{ color:var(--ember); background:rgba(255,90,60,.1); border:1px solid rgba(255,90,60,.32); }

/* ── nav (sidebar) ─────────────────────────────────────────── */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, rgba(11,18,32,.92), rgba(5,5,5,.96));
  border-right:1px solid var(--glass-border);
}
section[data-testid="stSidebar"] .block-container{ padding-top:1.6rem; }
.brand{ display:flex; align-items:center; gap:10px; margin-bottom:6px; }
.brand-mark{ width:34px; height:34px; border-radius:10px;
  background: conic-gradient(from 180deg, var(--blue), var(--violet), var(--cyan), var(--blue));
  box-shadow:0 0 18px rgba(59,130,246,.5); }
.brand-name{ font-family:var(--font-display); font-weight:700; font-size:1.05rem; color:var(--text-hi); }
.brand-tag{ font-family:var(--font-mono); font-size:.68rem; color:var(--text-low); letter-spacing:.08em; margin-top:-4px; }

.nav-item{
  display:flex; align-items:center; gap:10px; padding:11px 14px; margin:4px 0;
  border-radius:12px; font-family:var(--font-body); font-weight:500; font-size:.92rem;
  color:var(--text-mid); border:1px solid transparent; cursor:pointer; transition:.25s ease;
}
.nav-item:hover{ background:var(--glass); border-color:var(--glass-border); color:var(--text-hi); }
.nav-item.active{
  background: linear-gradient(90deg, rgba(59,130,246,.16), rgba(168,85,247,.10));
  border-color: rgba(34,211,238,.3); color:#fff;
  box-shadow: inset 0 0 0 1px rgba(34,211,238,.12), 0 0 16px rgba(59,130,246,.15);
}

/* sidebar mini metric cards */
.mini-metric{ padding:12px 14px; margin-bottom:9px; }
.mini-metric .mv{ font-family:var(--font-mono); font-weight:600; font-size:1.1rem; color:var(--text-hi); }
.mini-metric .ml{ font-size:.7rem; color:var(--text-low); text-transform:uppercase; letter-spacing:.05em; }

/* ── streamlit buttons -> premium CTA ─────────────────────────*/
div.stButton > button{
  font-family:var(--font-body); font-weight:600; letter-spacing:.01em;
  border-radius:14px; padding:.65rem 1.3rem;
  transition: transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .25s ease, filter .25s ease;
  position:relative; overflow:hidden;
}
div.stButton > button:active{ transform:translateY(1px) scale(.985); }

/* primary = active nav item / main CTA (predict button, active page) */
div.stButton > button[kind="primary"]{
  color:#fff; background:linear-gradient(100deg, var(--blue), var(--violet) 130%);
  border:1px solid rgba(255,255,255,.14);
  box-shadow:0 8px 24px rgba(59,130,246,.28), inset 0 1px 0 rgba(255,255,255,.18);
}
div.stButton > button[kind="primary"]:hover{
  filter:brightness(1.1); box-shadow:0 10px 30px rgba(59,130,246,.42), 0 0 24px rgba(168,85,247,.28);
  transform:translateY(-2px);
}
div.stButton > button[kind="primary"] p{ color:#fff !important; font-weight:600 !important; }

/* secondary = inactive nav item, quiet glass pill */
div.stButton > button[kind="secondary"]{
  background:var(--glass); border:1px solid var(--glass-border); color:var(--text-mid);
  box-shadow:none;
}
div.stButton > button[kind="secondary"]:hover{
  background:var(--glass-strong); border-color:rgba(34,211,238,.28); color:var(--text-hi);
  transform:translateX(2px);
}
div.stButton > button[kind="secondary"] p{ color:inherit !important; text-align:left; }

/* sidebar nav buttons: left align + full width already via use_container_width */
section[data-testid="stSidebar"] div.stButton > button{ justify-content:flex-start; }

/* ── inputs ─────────────────────────────────────────────────── */
[data-testid="stNumberInput"] input, [data-baseweb="select"] > div, [data-baseweb="input"] > div{
  background:var(--glass) !important; border:1px solid var(--glass-border) !important;
  border-radius:12px !important; color:var(--text-hi) !important; font-family:var(--font-mono) !important;
  transition:.25s ease;
}
[data-testid="stNumberInput"] input:focus, [data-baseweb="select"]:focus-within > div{
  border-color:var(--cyan) !important; box-shadow:0 0 0 3px rgba(34,211,238,.14) !important;
}
[data-testid="stSlider"] [role="slider"]{
  background:linear-gradient(135deg, var(--cyan), var(--blue)) !important;
  box-shadow:0 0 12px rgba(34,211,238,.6) !important; border: 3px solid #050505 !important;
}
[data-testid="stSlider"] > div > div > div{ background:linear-gradient(90deg, var(--blue), var(--cyan)) !important; }
[data-testid="stSlider"] > div > div{ background:rgba(255,255,255,.08) !important; }
label{ font-family:var(--font-body) !important; font-size:.82rem !important; font-weight:500 !important; color:var(--text-mid) !important; }
[data-testid="stRadio"] label{ color: var(--text-hi) !important; }

/* tabs */
.stTabs [data-baseweb="tab-list"]{ gap:6px; background:transparent; border-bottom:1px solid var(--glass-border); }
.stTabs [data-baseweb="tab"]{
  height:42px; border-radius:10px 10px 0 0; color:var(--text-mid); font-family:var(--font-body); font-weight:500;
  background:transparent;
}
.stTabs [aria-selected="true"]{ color:var(--cyan) !important; border-bottom:2px solid var(--cyan) !important; }

/* dataframe */
[data-testid="stDataFrame"]{ border-radius:14px; overflow:hidden; border:1px solid var(--glass-border); }

/* dividers */
hr{ border-color: var(--glass-border) !important; }

/* footer credit strip */
.footer-strip{ margin-top:60px; padding-top:22px; border-top:1px solid var(--glass-border);
  display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px; font-size:.78rem; color:var(--text-low); }

/* animations for on-load reveal */
@keyframes rise{ from{opacity:0; transform:translateY(16px)} to{opacity:1; transform:translateY(0)} }
.reveal{ animation: rise .7s cubic-bezier(.2,.8,.2,1) both; }
.d1{animation-delay:.05s} .d2{animation-delay:.12s} .d3{animation-delay:.19s} .d4{animation-delay:.26s}

/* result banner pulse */
.result-safe{ box-shadow:0 0 0 1px rgba(43,231,166,.3), 0 0 46px rgba(43,231,166,.18); }
.result-ember{ box-shadow:0 0 0 1px rgba(255,90,60,.32), 0 0 46px rgba(255,90,60,.2); animation: ember-pulse 2.4s ease-in-out infinite; }
@keyframes ember-pulse{ 0%,100%{ box-shadow:0 0 0 1px rgba(255,90,60,.32), 0 0 30px rgba(255,90,60,.16); } 50%{ box-shadow:0 0 0 1px rgba(255,90,60,.45), 0 0 56px rgba(255,90,60,.3); } }

.icon-orb{ width:76px; height:76px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 14px; }
.icon-orb svg{ width:34px; height:34px; }

@media (max-width: 640px){
  .hero-title{ font-size:2.1rem; }
  .stat-row{ flex-direction:column; }
}
</style>
"""


def inject_theme():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)

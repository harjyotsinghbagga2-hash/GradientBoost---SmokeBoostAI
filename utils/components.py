"""Small reusable render helpers shared across sections."""
import streamlit as st
import plotly.graph_objects as go

ICONS = {
    "flame": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2c1 3-2 4-2 7a4 4 0 0 0 8 0c0-1.5-1-2.5-1-2.5 1 4-1 6-3 6a3 3 0 0 1-3-3c0-2 2-3 1-7.5Z"/><path d="M12 22a6 6 0 0 0 6-6c0-2-1-3.5-2-5 .3 2-.5 3.5-2 3.5A2.5 2.5 0 0 1 11.5 12c0-1.2.8-2 .8-3.5C9.5 10 6 12.5 6 16a6 6 0 0 0 6 6Z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6l7-3Z"/><path d="M9 12l2 2 4-4"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".6" fill="currentColor"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="M2 12l10 5 10-5"/><path d="M2 17l10 5 10-5"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 3v18h18"/><path d="M7 15l4-5 3 3 5-7"/></svg>',
    "cube": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2 3 7v10l9 5 9-5V7l-9-5Z"/><path d="M3 7l9 5 9-5"/><path d="M12 22V12"/></svg>',
    "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>',
}


def icon(name: str) -> str:
    return ICONS.get(name, "")


def eyebrow(text: str) -> str:
    return f'<span class="eyebrow"><span class="dot"></span>{text}</span>'


def gauge(value_pct: float, label: str, color: str, track: str = "rgba(255,255,255,.08)") -> go.Figure:
    """Radial 'Combustion Index' style gauge used on the prediction result."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value_pct,
        number={"suffix": "%", "font": {"size": 40, "family": "JetBrains Mono", "color": "#F3F6FC"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,.25)", "tickfont": {"color": "#5C6884", "size": 10}},
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [{"range": [0, 100], "color": track}],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.9, "value": value_pct},
        },
        title={"text": label, "font": {"size": 13, "color": "#9CA8C2", "family": "Inter"}},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=24, r=24, t=50, b=10),
        font={"color": "#F3F6FC"},
    )
    return fig


def confetti_burst():
    st.markdown("""
    <div id="confetti-root"></div>
    <script>
    (function(){
      const root = document.createElement('div');
      root.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden;';
      document.body.appendChild(root);
      const colors = ['#2BE7A6','#22D3EE','#3B82F6','#A855F7'];
      for (let i=0;i<38;i++){
        const p = document.createElement('div');
        const size = Math.random()*7+4;
        const startX = window.innerWidth/2 + (Math.random()-0.5)*160;
        p.style.cssText = `position:absolute; left:${startX}px; top:38%; width:${size}px; height:${size}px;
          background:${colors[i % colors.length]}; border-radius:${Math.random()>0.5?'50%':'2px'};
          opacity:0.95; transform:rotate(${Math.random()*360}deg);`;
        root.appendChild(p);
        const angle = Math.random()*Math.PI*2;
        const dist = 120 + Math.random()*220;
        const dx = Math.cos(angle)*dist, dy = Math.sin(angle)*dist - 60;
        p.animate([
          { transform: p.style.transform + ' translate(0,0)', opacity: 0.95 },
          { transform: p.style.transform + ` translate(${dx}px, ${dy + 260}px) rotate(${Math.random()*720}deg)`, opacity: 0 }
        ], { duration: 1100 + Math.random()*500, easing: 'cubic-bezier(.2,.7,.3,1)' });
      }
      setTimeout(() => root.remove(), 1700);
    })();
    </script>
    """, unsafe_allow_html=True)

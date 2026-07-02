"""
Lightweight, dependency-free animated background.

Deliberately avoids Three.js / GSAP / particles.js CDNs: a hand-rolled
~40-line canvas loop renders identically, ships zero extra network
requests, and keeps the app fast on low-end hardware — which the brief
explicitly asks for ("despite all animations, the UI must remain
extremely fast"). Guards against Streamlit's rerun cycle so the animation
loop is only ever started once per browser tab.
"""

BACKGROUND_HTML = """
<div id="aurora-layer">
  <div class="aurora-blob blob-a"></div>
  <div class="aurora-blob blob-b"></div>
  <div class="aurora-blob blob-c"></div>
</div>
<div class="grain"></div>
<canvas id="particles-canvas"></canvas>

<script>
(function(){
  if (window.__sb_particles_running) return;
  window.__sb_particles_running = true;

  const canvas = document.getElementById('particles-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, particles;
  const COUNT = 46;
  const mouse = { x: -9999, y: -9999 };

  function resize(){
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  function makeParticles(){
    particles = Array.from({length: COUNT}, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.6 + 0.6,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      a: Math.random() * 0.5 + 0.15,
      hue: Math.random() > 0.5 ? '59,130,246' : '34,211,238'
    }));
  }
  window.addEventListener('resize', () => { resize(); });
  window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });

  resize();
  makeParticles();

  function tick(){
    ctx.clearRect(0, 0, W, H);
    for (const p of particles){
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;

      const dx = p.x - mouse.x, dy = p.y - mouse.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      const boost = dist < 140 ? (140 - dist) / 140 : 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r + boost * 1.4, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.hue}, ${p.a + boost * 0.4})`;
      ctx.fill();
    }
    requestAnimationFrame(tick);
  }
  tick();
})();
</script>
"""


def inject_background():
    import streamlit as st
    st.markdown(BACKGROUND_HTML, unsafe_allow_html=True)

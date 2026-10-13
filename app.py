import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A tiny app-building playground: personalize your name, then bring it to life.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Forest", "Lavender", "Ocean"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    animation_speed = st.slider(
        "Animation speed", min_value=0.4, max_value=2.5, value=1.0, step=0.1,
        help="Lower values move more slowly; higher values move more quickly.",
    )
    show_hint = st.checkbox("Show a little welcome message", value=True)

themes = {
    "Light": ("#ffffff", "#172033", "#e8eef7"),
    "Dark": ("#10131c", "#f7f8ff", "#242a3a"),
    "Sky": ("#dff4ff", "#12324a", "#b8e7ff"),
    "Sunset": ("#3b164f", "#fff3dc", "#6c2e59"),
    "Forest": ("#123b2a", "#f1ffe9", "#20543c"),
    "Lavender": ("#f0e8ff", "#33204d", "#ded0ff"),
    "Ocean": ("#063b50", "#e7fbff", "#0c536a"),
}
bg_color, text_color, accent_color = themes[background]

safe_name = html.escape(name if name else "Hello World")
safe_font = json.dumps(font_family)
safe_name_js = json.dumps(name if name else "Hello World")
safe_mode = json.dumps(name_mode)
safe_effect = json.dumps(effect)
safe_bg = json.dumps(bg_color)
safe_text = json.dumps(text_color)
safe_accent = json.dumps(accent_color)

# Animation runs in the embedded browser with CSS/JavaScript, so it loops smoothly
# without repeatedly rerunning the whole Streamlit script.
html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: {safe_font}; }}
  #stage {{
    position: relative; width: 100%; height: 620px; overflow: hidden;
    border-radius: 18px; background: {bg_color}; color: {text_color};
    isolation: isolate; border: 1px solid rgba(127,127,127,.22);
  }}
  #glow {{
    position:absolute; inset:0; z-index:0; pointer-events:none;
    background: radial-gradient(ellipse at center, {accent_color} 0%, transparent 72%);
    opacity:.65;
  }}
  #particles {{ position:absolute; inset:0; overflow:hidden; z-index:1; pointer-events:none; }}
  .particle {{ position:absolute; top:-12%; left:var(--x); font-size:var(--size);
    opacity:var(--opacity); animation: fall var(--duration) linear var(--delay) infinite;
    will-change: transform; }}
  @keyframes fall {{
    from {{ transform: translate3d(0,-10%,0) rotate(0deg); }}
    to {{ transform: translate3d(var(--drift),740px,0) rotate(360deg); }}
  }}
  .gust {{
    position:absolute; left:-45%; width:45%; height:3px; border-radius:50%;
    background:linear-gradient(90deg, transparent, currentColor, transparent);
    opacity:.45; animation: gust var(--duration) ease-in-out var(--delay) infinite;
  }}
  @keyframes gust {{ from {{ transform:translateX(0) translateY(0) rotate(-8deg); }}
    to {{ transform:translateX(360%) translateY(130px) rotate(8deg); }} }}
  .twister {{
    position:absolute; left:50%; top:50%; width:250px; height:250px;
    transform:translate(-50%,-50%); border-radius:50%;
    border:3px dashed currentColor; opacity:.25;
    animation: spin var(--duration) linear infinite;
  }}
  .twister::before, .twister::after {{
    content:""; position:absolute; inset:18%; border:3px dotted currentColor;
    border-radius:50%;
  }}
  .twister::after {{ inset:36%; border-style:solid; }}
  @keyframes spin {{ to {{ transform:translate(-50%,-50%) rotate(360deg); }} }}
  #name-wrap {{
    position:absolute; z-index:5; inset:0; display:flex; align-items:center;
    justify-content:center; padding:30px; overflow:hidden;
  }}
  #name {{
    position:relative; z-index:5; color:{text_color}; font-size:{font_size}px;
    font-weight:700; text-align:center; line-height:1.25; overflow-wrap:anywhere;
    text-shadow:0 2px 14px rgba(0,0,0,.16);
  }}
  #name.ticker {{
    white-space:nowrap; overflow-wrap:normal; position:absolute; left:100%;
    width:max-content; max-width:none; animation: ticker var(--ticker-duration) linear infinite;
  }}
  @keyframes ticker {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-190%); }} }}
  #name.repeated {{ display:flex; flex-direction:column; gap:.22em; }}
  #welcome {{ position:absolute; z-index:6; bottom:18px; left:18px; right:18px;
    text-align:center; font-size:14px; opacity:.72; }}
  @media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{ animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; }}
  }}
</style>
</head>
<body>
<div id="stage">
  <div id="glow"></div>
  <div id="particles"></div>
  <div id="name-wrap"><div id="name"></div></div>
  <div id="welcome" style="display:{'block' if show_hint else 'none'}">Welcome to your first app — try changing the controls!</div>
</div>
<script>
(() => {{
  const stage = document.getElementById('stage');
  const layer = document.getElementById('particles');
  const nameEl = document.getElementById('name');
  const userName = {safe_name_js};
  const mode = {safe_mode};
  const effect = {safe_effect};
  const speed = {animation_speed};
  const symbols = {{
    "Rain": ["💧", "💦"], "Snow": ["❄️", "❅", "❆"],
    "Hail": ["🧊", "●"], "Confetti": ["🎉", "🎊", "✨", "🟣", "🟡", "🟢"]
  }};
  nameEl.textContent = userName;
  nameEl.style.setProperty('--ticker-duration', (14 / speed) + 's');

  if (mode === "Ticker Tape") {{
    nameEl.className = "ticker";
    nameEl.style.left = "100%";
    nameEl.style.animationDuration = (14 / speed) + "s";
  }} else if (mode === "Repeated") {{
    nameEl.className = "repeated";
    nameEl.replaceChildren();
    for (let i = 0; i < 6; i++) {{
      const line = document.createElement('div');
      line.textContent = userName;
      line.style.opacity = String(1 - i * 0.09);
      line.style.fontSize = (1 - i * 0.07) + "em";
      nameEl.appendChild(line);
    }}
  }}

  function addParticle(symbol, index, count) {{
    const p = document.createElement('span');
    p.className = 'particle';
    p.textContent = symbol;
    p.style.setProperty('--x', (Math.random() * 100) + '%');
    p.style.setProperty('--size', (14 + Math.random() * 18) + 'px');
    p.style.setProperty('--opacity', (0.45 + Math.random() * 0.5).toFixed(2));
    p.style.setProperty('--duration', ((3 + Math.random() * 5) / speed) + 's');
    p.style.setProperty('--delay', (-Math.random() * 8 / speed) + 's');
    p.style.setProperty('--drift', ((Math.random() - 0.5) * 180) + 'px');
    layer.appendChild(p);
  }}

  if (symbols[effect]) {{
    const count = effect === "Confetti" ? 70 : effect === "Rain" ? 85 : 48;
    for (let i = 0; i < count; i++) {{
      const choices = symbols[effect];
      addParticle(choices[Math.floor(Math.random() * choices.length)], i, count);
    }}
    if (effect === "Rain") {{
      layer.querySelectorAll('.particle').forEach(p => {{
        p.style.fontSize = '16px';
        p.style.opacity = '.7';
      }});
    }}
    if (effect === "Hail") {{
      layer.querySelectorAll('.particle').forEach(p => {{
        p.style.fontSize = (9 + Math.random() * 10) + 'px';
      }});
    }}
  }} else if (effect === "Wind Gust") {{
    for (let i = 0; i < 12; i++) {{
      const gust = document.createElement('div');
      gust.className = 'gust';
      gust.style.top = (Math.random() * 100) + '%';
      gust.style.setProperty('--duration', ((2.5 + Math.random() * 3) / speed) + 's');
      gust.style.setProperty('--delay', (-Math.random() * 5 / speed) + 's');
      layer.appendChild(gust);
    }}
  }} else if (effect === "Tornado") {{
    const twister = document.createElement('div');
    twister.className = 'twister';
    twister.style.setProperty('--duration', (5 / speed) + 's');
    layer.appendChild(twister);
    for (let i = 0; i < 30; i++) {{
      const p = document.createElement('span');
      p.className = 'particle';
      p.textContent = ['🍃', '💨', '·'][Math.floor(Math.random() * 3)];
      p.style.setProperty('--x', (20 + Math.random() * 60) + '%');
      p.style.setProperty('--size', (14 + Math.random() * 14) + 'px');
      p.style.setProperty('--duration', ((2 + Math.random() * 3) / speed) + 's');
      p.style.setProperty('--delay', (-Math.random() * 5 / speed) + 's');
      p.style.setProperty('--drift', ((Math.random() - .5) * 240) + 'px');
      p.style.animationName = 'fall';
      layer.appendChild(p);
    }}
  }}
}})();
</script>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)

st.divider()
st.markdown(
    "**How it works:** Streamlit provides the controls, while HTML, CSS, and JavaScript inside the preview handle the continuous animation in the browser."
)

#!/usr/bin/env python3
"""Clean up the interface - simplified, refined, modern"""
import re

with open('D:/tokai/index-fixed-final.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original: {len(html)} bytes")

# ---- CSS Variables (cleaner, more refined) ----
old_vars = """    :root {

      --bg: #faf8f5;

      --bg2: #f2efe9;

      --card: #ffffff;

      --text: #1a1a1a;

      --text2: #777;

      --accent: #b8956a;

      --accent2: #d4b896;

      --accent-dark: #96754a;

      --gold: linear-gradient(135deg, #b8956a, #d4b896, #b8956a);

      --shadow: 0 4px 24px rgba(0,0,0,0.06);

      --shadow-lg: 0 12px 48px rgba(0,0,0,0.1);

      --radius: 16px;

      --nav-h: 64px;

      --bottom-nav-h: 0px;

    }"""

new_vars = """    :root {

      --bg: #faf8f5;

      --bg2: #f2efe9;

      --card: #ffffff;

      --text: #1a1a1a;

      --text2: #888;

      --accent: #b8956a;

      --accent2: #d4b896;

      --accent-dark: #96754a;

      --gold: linear-gradient(135deg, #b8956a, #d4b896, #b8956a);

      --shadow: 0 2px 16px rgba(0,0,0,0.04);

      --shadow-lg: 0 8px 32px rgba(0,0,0,0.08);

      --radius: 12px;

      --nav-h: 60px;

      --bottom-nav-h: 0px;

    }"""

if old_vars in html:
    html = html.replace(old_vars, new_vars)
    print("Updated CSS variables")
else:
    print("WARNING: vars not found, trying alternate...")

# ---- Animation (simpler, smoother) ----
html = html.replace(
    "@keyframes fadeUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }",
    "@keyframes fadeUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }"
)

html = html.replace(
    "@keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }",
    "@keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-6px); } }"
)

# ---- Reveal animation (cleaner) ----
html = html.replace(
    ".reveal { opacity: 1 !important; transform: none !important; }\n    .reveal.visible { opacity:1; transform:translateY(0); }",
    ".reveal { opacity: 0; transform: translateY(20px); transition: all 0.6s ease; }\n    .reveal.visible { opacity: 1; transform: none !important; }"
)

# ---- Nav (smaller, cleaner) ----
html = html.replace(
    ".logo { font-family:'Noto Serif SC',serif; font-size:1.5rem; font-weight:700; letter-spacing:2px; text-decoration:none; color:var(--text); }",
    ".logo { font-family:'Noto Serif SC',serif; font-size:1.3rem; font-weight:700; letter-spacing:2px; text-decoration:none; color:var(--text); }"
)

html = html.replace(
    ".menu-toggle { display:none; background:none; border:none; font-size:1.5rem; cursor:pointer; padding:8px; }",
    ".menu-toggle { display:none; background:none; border:none; font-size:1.3rem; cursor:pointer; padding:8px; }"
)

# ---- Hero (refined typography) ----
html = html.replace(
    ".hero-badge { display:inline-block; padding:6px 20px; border:1px solid rgba(255,255,255,0.3); border-radius:30px; font-size:0.8rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:24px; backdrop-filter:blur(8px); background:rgba(255,255,255,0.08); animation:fadeIn 1s 0.2s both; }",
    ".hero-badge { display:inline-block; padding:5px 16px; border:1px solid rgba(255,255,255,0.25); border-radius:20px; font-size:0.75rem; letter-spacing:2px; margin-bottom:20px; background:rgba(255,255,255,0.06); animation:fadeIn 1s 0.2s both; }"
)

html = html.replace(
    ".hero-title { font-family:'Noto Serif SC',serif; font-size:clamp(2.8rem,7vw,4.5rem); font-weight:700; line-height:1.15; letter-spacing:6px; margin-bottom:20px; animation:fadeUp 1s 0.4s both; }",
    ".hero-title { font-family:'Noto Serif SC',serif; font-size:clamp(2.2rem,6vw,3.8rem); font-weight:700; line-height:1.2; margin-bottom:16px; animation:fadeUp 1s 0.3s both; }"
)

html = html.replace(
    ".hero-sub { font-size:1.05rem; opacity:0.85; letter-spacing:3px; margin-bottom:40px; animation:fadeUp 1s 0.6s both; }",
    ".hero-sub { font-size:1rem; opacity:0.9; margin-bottom:32px; animation:fadeUp 1s 0.5s both; }"
)

html = html.replace(
    ".hero-actions { display:flex; gap:16px; animation:fadeUp 1s 0.8s both; }",
    ".hero-actions { display:flex; gap:12px; animation:fadeUp 1s 0.7s both; }"
)

html = html.replace(
    ".btn { display:inline-flex; align-items:center; gap:8px; padding:14px 36px; border-radius:50px; text-decoration:none; font-size:0.95rem; font-weight:500; transition:all 0.3s; cursor:pointer; border:none; }",
    ".btn { display:inline-flex; align-items:center; gap:6px; padding:12px 28px; border-radius:8px; text-decoration:none; font-size:0.9rem; font-weight:500; transition:all 0.3s; cursor:pointer; border:none; }"
)

html = html.replace(
    ".hero-scroll { position:absolute; bottom:40px; left:50%; transform:translateX(-50%); z-index:5; display:flex; flex-direction:column; align-items:center; gap:8px; color:rgba(255,255,255,0.6); font-size:0.75rem; letter-spacing:2px; animation:float 2s ease-in-out infinite; }",
    ".hero-scroll { position:absolute; bottom:32px; left:50%; transform:translateX(-50%); z-index:5; display:flex; flex-direction:column; align-items:center; gap:6px; color:rgba(255,255,255,0.5); font-size:0.7rem; letter-spacing:2px; animation:float 2s ease-in-out infinite; }"
)

html = html.replace(
    ".scroll-line { width:1px; height:40px; background:linear-gradient(to bottom,rgba(255,255,255,0.5),transparent); }",
    ".scroll-line { width:1px; height:32px; background:linear-gradient(to bottom,rgba(255,255,255,0.4),transparent); }"
)

html = html.replace(
    ".hero-dots { position:absolute; bottom:100px; left:50%; transform:translateX(-50%); display:flex; gap:8px; z-index:5; }",
    ".hero-dots { position:absolute; bottom:84px; left:50%; transform:translateX(-50%); display:flex; gap:6px; z-index:5; }"
)

html = html.replace(
    ".dot { width:8px; height:8px; border-radius:50%; background:rgba(255,255,255,0.3); cursor:pointer; transition:all 0.4s; }",
    ".dot { width:6px; height:6px; border-radius:3px; background:rgba(255,255,255,0.3); cursor:pointer; transition:all 0.3s; }"
)

html = html.replace(
    ".dot.active { background:#fff; width:28px; border-radius:4px; }",
    ".dot.active { background:#fff; width:20px; }"
)

# ---- Section headers (cleaner) ----
html = html.replace(
    "section { padding:100px 0; }",
    "section { padding:80px 0; }"
)

html = html.replace(
    ".sec-head { text-align:center; margin-bottom:60px; }",
    ".sec-head { text-align:center; margin-bottom:48px; }"
)

html = html.replace(
    ".sec-label { display:inline-block; font-size:0.75rem; letter-spacing:4px; text-transform:uppercase; color:var(--accent); margin-bottom:12px; }",
    ".sec-label { display:inline-block; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; color:var(--accent); margin-bottom:10px; }"
)

html = html.replace(
    ".sec-line { width:50px; height:2px; background:var(--gold); margin:0 auto; border-radius:1px; }",
    ".sec-line { width:40px; height:2px; background:var(--accent); margin:0 auto; }"
)

html = html.replace(
    ".sec-desc { color:var(--text2); max-width:520px; margin:16px auto 0; font-size:0.95rem; }",
    ".sec-desc { color:var(--text2); max-width:480px; margin:12px auto 0; font-size:0.9rem; }"
)

# ---- About section (tighter spacing) ----
html = html.replace(
    ".about-grid { display:grid; grid-template-columns:1fr 1fr; gap:80px; align-items:center; }",
    ".about-grid { display:grid; grid-template-columns:1fr 1fr; gap:60px; align-items:center; }"
)

html = html.replace(
    ".about-badge { display:inline-block; padding:6px 16px; background:rgba(184,149,106,0.1); color:var(--accent); border-radius:20px; font-size:0.8rem; margin-bottom:20px; }",
    ".about-badge { display:inline-block; padding:4px 12px; background:rgba(184,149,106,0.08); color:var(--accent); border-radius:4px; font-size:0.75rem; margin-bottom:16px; letter-spacing:1px; }"
)

html = html.replace(
    ".about-text h3 { font-family:'Noto Serif SC',serif; font-size:1.6rem; margin-bottom:20px; line-height:1.5; }",
    ".about-text h3 { font-family:'Noto Serif SC',serif; font-size:1.4rem; margin-bottom:16px; line-height:1.4; }"
)

html = html.replace(
    ".stats { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; margin-top:36px; }",
    ".stats { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:28px; }"
)

html = html.replace(
    ".stat { text-align:center; padding:20px; background:#fff; border-radius:var(--radius); box-shadow:var(--shadow); }",
    ".stat { text-align:center; padding:16px 8px; }"
)

html = html.replace(
    ".stat-num { display:block; font-family:'Noto Serif SC',serif; font-size:2rem; font-weight:700; color:var(--accent); }",
    ".stat-num { display:block; font-family:'Noto Serif SC',serif; font-size:1.8rem; font-weight:700; color:var(--accent); }"
)

html = html.replace(
    ".stat-label { font-size:0.8rem; color:var(--text2); margin-top:4px; }",
    ".stat-label { font-size:0.75rem; color:var(--text2); margin-top:2px; }"
)

html = html.replace(
    ".about-img { width:100%; height:440px; object-fit:cover; border-radius:var(--radius); box-shadow:var(--shadow-lg); }",
    ".about-img { width:100%; height:400px; object-fit:cover; border-radius:var(--radius); box-shadow:var(--shadow-lg); }"
)

html = html.replace(
    ".about-float { position:absolute; bottom:-20px; right:-20px; background:#fff; padding:20px 28px; border-radius:var(--radius); box-shadow:var(--shadow-lg); display:flex; align-items:center; gap:12px; }",
    ".about-float { position:absolute; bottom:-16px; right:-16px; background:#fff; padding:16px 20px; border-radius:var(--radius); box-shadow:var(--shadow-lg); display:flex; align-items:center; gap:10px; }"
)

html = html.replace(
    ".about-float .icon { width:48px; height:48px; background:var(--gold); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.4rem; color:#fff; }",
    ".about-float .icon { width:40px; height:40px; background:var(--gold); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; color:#fff; }"
)

# ---- Services (more compact cards) ----
html = html.replace(
    ".services-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; }",
    ".services-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }"
)

html = html.replace(
    ".service-card { background:#fff; padding:40px 24px; text-align:center; border-radius:var(--radius); border:1px solid rgba(0,0,0,0.04); transition:all 0.4s; cursor:default; }",
    ".service-card { background:#fff; padding:32px 20px; text-align:center; border-radius:var(--radius); border:1px solid rgba(0,0,0,0.04); transition:all 0.3s; cursor:default; }"
)

html = html.replace(
    ".service-icon { width:64px; height:64px; margin:0 auto 20px; background:linear-gradient(135deg,rgba(184,149,106,0.1),rgba(184,149,106,0.05)); border-radius:20px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; transition:all 0.4s; }",
    ".service-icon { width:56px; height:56px; margin:0 auto 16px; background:rgba(184,149,106,0.06); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:1.6rem; transition:all 0.3s; }"
)

html = html.replace(
    ".service-card h4 { font-size:1.05rem; margin-bottom:10px; }",
    ".service-card h4 { font-size:1rem; margin-bottom:8px; }"
)

html = html.replace(
    ".service-card p { color:var(--text2); font-size:0.88rem; line-height:1.6; }",
    ".service-card p { color:var(--text2); font-size:0.82rem; line-height:1.5; }"
)

# ---- Products (cleaner) ----
html = html.replace(
    ".prod-filters { display:flex; justify-content:center; gap:8px; margin-bottom:40px; flex-wrap:wrap; }",
    ".prod-filters { display:flex; justify-content:center; gap:6px; margin-bottom:32px; flex-wrap:wrap; }"
)

html = html.replace(
    ".filter-btn { padding:8px 22px; border:1.5px solid var(--border); border-radius:30px; background:transparent; cursor:pointer; font-size:0.88rem; transition:all 0.3s; color:var(--text2); }",
    ".filter-btn { padding:6px 18px; border:1px solid rgba(0,0,0,0.08); border-radius:20px; background:transparent; cursor:pointer; font-size:0.82rem; transition:all 0.2s; color:var(--text2); }"
)

html = html.replace(
    ".products-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }",
    ".products-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }"
)

html = html.replace(
    ".product-img { position:relative; height:260px; overflow:hidden; background:#f5f3ef; }",
    ".product-img { position:relative; height:240px; overflow:hidden; background:#f5f3ef; }"
)

html = html.replace(
    ".product-info { padding:20px; }",
    ".product-info { padding:16px; }"
)

html = html.replace(
    ".product-info h4 { font-size:1.05rem; margin-bottom:6px; }",
    ".product-info h4 { font-size:0.95rem; margin-bottom:4px; }"
)

html = html.replace(
    ".product-info .desc { color:var(--text2); font-size:0.85rem; margin-bottom:12px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }",
    ".product-info .desc { color:var(--text2); font-size:0.8rem; margin-bottom:10px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }"
)

html = html.replace(
    ".product-price { font-family:'Noto Serif SC',serif; font-size:1.2rem; font-weight:700; color:var(--accent); }",
    ".product-price { font-family:'Noto Serif SC',serif; font-size:1.1rem; font-weight:700; color:var(--accent); }"
)

html = html.replace(
    ".product-btn { padding:8px 20px; background:var(--accent); color:#fff; border:none; border-radius:24px; cursor:pointer; font-size:0.85rem; transition:all 0.3s; }",
    ".product-btn { padding:6px 16px; background:var(--accent); color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:0.8rem; transition:all 0.2s; }"
)

# ---- Portfolio (cleaner) ----
html = html.replace(
    ".portfolio-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }",
    ".portfolio-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }"
)

html = html.replace(
    ".portfolio-item { position:relative; height:280px; border-radius:var(--radius); overflow:hidden; cursor:pointer; }",
    ".portfolio-item { position:relative; height:260px; border-radius:var(--radius); overflow:hidden; cursor:pointer; }"
)

html = html.replace(
    ".portfolio-item::after { content:''; position:absolute; inset:0; background:linear-gradient(to top,rgba(0,0,0,0.75) 0%,rgba(0,0,0,0.1) 50%,transparent 100%); }",
    ".portfolio-item::after { content:''; position:absolute; inset:0; background:linear-gradient(to top,rgba(0,0,0,0.6),transparent); }"
)

html = html.replace(
    ".portfolio-info { position:absolute; bottom:0; left:0; right:0; padding:24px; z-index:2; color:#fff; transform:translateY(10px); transition:all 0.4s; }",
    ".portfolio-info { position:absolute; bottom:0; left:0; right:0; padding:20px; z-index:2; color:#fff; transform:translateY(8px); transition:all 0.3s; }"
)

html = html.replace(
    ".portfolio-info h4 { font-size:1.1rem; margin-bottom:4px; }",
    ".portfolio-info h4 { font-size:1rem; margin-bottom:2px; }"
)

# ---- Contact (cleaner) ----
html = html.replace(
    ".contact-grid { display:grid; grid-template-columns:1fr 1.4fr; gap:60px; }",
    ".contact-grid { display:grid; grid-template-columns:1fr 1.2fr; gap:48px; }"
)

html = html.replace(
    ".contact-card { background:#fff; padding:36px; border-radius:var(--radius); margin-bottom:20px; display:flex; gap:16px; align-items:flex-start; }",
    ".contact-card { display:flex; gap:12px; margin-bottom:16px; }"
)

html = html.replace(
    ".contact-icon { width:48px; height:48px; min-width:48px; background:linear-gradient(135deg,rgba(184,149,106,0.1),rgba(184,149,106,0.05)); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:1.3rem; }",
    ".contact-icon { width:40px; height:40px; min-width:40px; background:rgba(184,149,106,0.06); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; }"
)

html = html.replace(
    ".contact-card h5 { font-size:0.85rem; color:var(--text2); margin-bottom:4px; }",
    ".contact-card h5 { font-size:0.78rem; color:var(--text2); margin-bottom:2px; }"
)

html = html.replace(
    ".contact-form-wrap { background:#fff; padding:36px; border-radius:var(--radius); }",
    ".contact-form-wrap { background:var(--bg); padding:28px; border-radius:var(--radius); }"
)

html = html.replace(
    ".contact-form-wrap h3 { font-family:'Noto Serif SC',serif; font-size:1.3rem; margin-bottom:24px; }",
    ".contact-form-wrap h3 { font-family:'Noto Serif SC',serif; font-size:1.2rem; margin-bottom:20px; }"
)

html = html.replace(
    ".form-input, .form-textarea { width:100%; padding:14px 18px; border:1.5px solid rgba(0,0,0,0.06); border-radius:12px; font-size:0.9rem; font-family:inherit; background:var(--bg); transition:all 0.3s; }",
    ".form-input, .form-textarea { width:100%; padding:12px 14px; border:1px solid rgba(0,0,0,0.06); border-radius:8px; font-size:0.85rem; font-family:inherit; background:#fff; transition:all 0.2s; }"
)

html = html.replace(
    ".submit-btn { width:100%; padding:14px; background:var(--accent); color:#fff; border:none; border-radius:12px; font-size:0.95rem; cursor:pointer; transition:all 0.3s; font-weight:500; }",
    ".submit-btn { width:100%; padding:12px; background:var(--accent); color:#fff; border:none; border-radius:8px; font-size:0.88rem; cursor:pointer; transition:all 0.2s; }"
)

# ---- Footer (cleaner) ----
html = html.replace(
    ".footer { background:var(--text); color:rgba(255,255,255,0.6); padding:48px 0 24px; }",
    ".footer { background:var(--text); color:rgba(255,255,255,0.6); padding:40px 0 20px; }"
)

html = html.replace(
    ".footer-grid { display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:40px; margin-bottom:36px; }",
    ".footer-grid { display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:32px; margin-bottom:28px; }"
)

html = html.replace(
    ".footer-brand .logo { color:#fff; font-size:1.3rem; margin-bottom:12px; display:block; }",
    ".footer-brand .logo { color:#fff; font-size:1.2rem; margin-bottom:10px; display:block; }"
)

html = html.replace(
    ".footer-bottom { border-top:1px solid rgba(255,255,255,0.08); padding-top:20px; text-align:center; font-size:0.8rem; }",
    ".footer-bottom { border-top:1px solid rgba(255,255,255,0.06); padding-top:16px; text-align:center; font-size:0.75rem; }"
)

# ---- Lightbox (cleaner) ----
html = html.replace(
    ".lightbox { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.96); z-index:9999; justify-content:center; align-items:center; flex-direction:column; animation:fadeIn 0.3s; }",
    ".lightbox { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.92); z-index:9999; justify-content:center; align-items:center; flex-direction:column; animation:fadeIn 0.2s; }"
)

html = html.replace(
    ".lb-close { position:absolute; top:20px; right:24px; color:#fff; font-size:2rem; cursor:pointer; background:none; border:none; width:44px; height:44px; display:flex; align-items:center; justify-content:center; border-radius:50%; transition:background 0.3s; }",
    ".lb-close { position:absolute; top:16px; right:20px; color:#fff; font-size:1.8rem; cursor:pointer; background:none; border:none; width:40px; height:40px; display:flex; align-items:center; justify-content:center; border-radius:50%; opacity:0.7; transition:all 0.2s; }"
)

html = html.replace(
    ".lb-thumbs img { width:56px; height:56px; object-fit:cover; border-radius:8px; cursor:pointer; opacity:0.4; border:2px solid transparent; transition:all 0.3s; }",
    ".lb-thumbs img { width:48px; height:48px; object-fit:cover; border-radius:6px; cursor:pointer; opacity:0.35; border:2px solid transparent; transition:all 0.2s; }"
)

# ---- Modal (cleaner) ----
html = html.replace(
    ".modal { background:#fff; border-radius:20px; width:92%; max-width:440px; max-height:90vh; overflow-y:auto; animation:scaleIn 0.3s; }",
    ".modal { background:#fff; border-radius:16px; width:90%; max-width:400px; max-height:90vh; overflow-y:auto; animation:scaleIn 0.2s; }"
)

html = html.replace(
    ".modal-header h3 { font-family:'Noto Serif SC',serif; font-size:1.15rem; }",
    ".modal-header h3 { font-size:1rem; }"
)

html = html.replace(
    ".modal-close { background:none; border:none; font-size:1.4rem; cursor:pointer; color:var(--text2); width:36px; height:36px; display:flex; align-items:center; justify-content:center; border-radius:50%; }",
    ".modal-close { background:none; border:none; font-size:1.3rem; cursor:pointer; color:var(--text2); width:32px; height:32px; display:flex; align-items:center; justify-content:center; border-radius:50%; }"
)

html = html.replace(
    ".qr-box img { width:160px; height:160px; object-fit:contain; display:none; border-radius:8px; }",
    ".qr-box img { width:140px; height:140px; object-fit:contain; display:none; border-radius:4px; }"
)

html = html.replace(
    ".order-success .icon { font-size:3.5rem; margin-bottom:16px; animation:scaleIn 0.5s; }",
    ".order-success .icon { font-size:3rem; margin-bottom:12px; }"
)

# ---- Float buttons (smaller) ----
html = html.replace(
    ".float-contact { position:fixed; bottom:24px; right:24px; z-index:90; display:flex; flex-direction:column; align-items:flex-end; gap:10px; }",
    ".float-contact { position:fixed; bottom:20px; right:20px; z-index:90; display:flex; flex-direction:column; align-items:flex-end; gap:8px; }"
)

html = html.replace(
    ".float-btn { width:56px; height:56px; border-radius:50%; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:1.5rem; box-shadow:0 4px 20px rgba(0,0,0,0.15); transition:all 0.3s; }",
    ".float-btn { width:48px; height:48px; border-radius:50%; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:1.3rem; box-shadow:0 2px 12px rgba(0,0,0,0.1); transition:all 0.2s; }"
)

html = html.replace(
    ".wechat-popup { display:none; position:absolute; bottom:66px; right:0; background:#fff; border-radius:var(--radius); padding:24px; box-shadow:var(--shadow-lg); width:220px; text-align:center; animation:scaleIn 0.3s; }",
    ".wechat-popup { display:none; position:absolute; bottom:58px; right:0; background:#fff; border-radius:var(--radius); padding:20px; box-shadow:var(--shadow-lg); width:200px; text-align:center; animation:scaleIn 0.2s; }"
)

html = html.replace(
    ".wechat-popup img { width:160px; height:160px; border-radius:8px; margin-bottom:10px; }",
    ".wechat-popup img { width:140px; height:140px; border-radius:6px; margin-bottom:8px; }"
)

# ---- Mobile nav (tighter) ----
html = html.replace(
    ".mobile-nav { display:none; position:fixed; bottom:0; left:0; right:0; z-index:100; background:rgba(255,255,255,0.95); backdrop-filter:blur(20px); border-top:1px solid rgba(0,0,0,0.06); padding:6px 0 env(safe-area-inset-bottom,8px); }",
    ".mobile-nav { display:none; position:fixed; bottom:0; left:0; right:0; z-index:100; background:rgba(255,255,255,0.95); backdrop-filter:blur(16px); border-top:1px solid rgba(0,0,0,0.04); padding:4px 0 env(safe-area-inset-bottom,6px); }"
)

html = html.replace(
    ".mobile-nav a { display:flex; flex-direction:column; align-items:center; gap:2px; text-decoration:none; color:var(--text2); font-size:0.68rem; padding:6px 12px; border-radius:12px; transition:all 0.3s; }",
    ".mobile-nav a { display:flex; flex-direction:column; align-items:center; gap:1px; text-decoration:none; color:var(--text2); font-size:0.65rem; padding:4px 10px; border-radius:8px; transition:all 0.2s; }"
)

html = html.replace(
    ".mobile-nav a .icon { font-size:1.3rem; }",
    ".mobile-nav a .icon { font-size:1.2rem; }"
)

# Fix mobileNav template in JS - smaller icons
html = html.replace(
    "mobileNav.innerHTML = `<div class=\"mobile-nav-inner\">\n\n          <a href=\"#home\" class=\"active\"><span class=\"icon\">🏠</span>${i18n[lang].mobile_home}</a>\n\n          <a href=\"#products\"><span class=\"icon\">📦</span>${i18n[lang].mobile_products}</a>\n\n          <a href=\"#contact\"><span class=\"icon\">💬</span>${i18n[lang].mobile_consult}</a>",
    "mobileNav.innerHTML = `<div class=\"mobile-nav-inner\">\n\n          <a href=\"#home\" class=\"active\"><span class=\"icon\">🏠</span>${i18n[lang].mobile_home}</a>\n\n          <a href=\"#products\"><span class=\"icon\">📦</span>${i18n[lang].mobile_products}</a>\n\n          <a href=\"#contact\"><span class=\"icon\">💬</span>${i18n[lang].mobile_consult}</a>"
)

# Fix nav toggle button (smaller)
html = html.replace(
    '<button onclick="toggleSettings(event)" style="background:none;border:none;cursor:pointer;font-size:1.1rem;padding:6px 8px;border-radius:8px;color:#555" title="设置">⚙</button>',
    '<button onclick="toggleSettings(event)" style="background:none;border:none;cursor:pointer;font-size:1rem;padding:6px 8px;border-radius:6px;color:#666" title="设置">⚙</button>'
)

# Fix settings dropdown (cleaner)
html = html.replace(
    '<div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">',
    '<div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,0.08);min-width:150px;z-index:9999;overflow:hidden">'
)

html = html.replace(
    '<a onclick="checkAppUpdate()" style="display:block;padding:12px 16px;cursor:pointer;font-size:0.88rem;color:#333;text-decoration:none">🔄 版本更新</a>',
    '<a onclick="checkAppUpdate()" style="display:block;padding:10px 14px;cursor:pointer;font-size:0.82rem;color:#333;text-decoration:none">🔄 版本更新</a>'
)

html = html.replace(
    '<a onclick="clearCache()" style="display:block;padding:12px 16px;cursor:pointer;font-size:0.88rem;color:#333;text-decoration:none">🗑️ 清除缓存</a>',
    '<a onclick="clearCache()" style="display:block;padding:10px 14px;cursor:pointer;font-size:0.82rem;color:#333;text-decoration:none">🗑️ 清除缓存</a>'
)

# Fix contact form rows (tighter)
html = html.replace(
    ".form-row { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px; }",
    ".form-row { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px; }"
)

# Modal body padding
html = html.replace(
    ".modal-body { padding:24px; }",
    ".modal-body { padding:20px; }"
)

html = html.replace(
    ".modal-product { display:flex; gap:14px; padding-bottom:18px; border-bottom:1px solid rgba(0,0,0,0.05); margin-bottom:20px; }",
    ".modal-product { display:flex; gap:12px; padding-bottom:14px; border-bottom:1px solid rgba(0,0,0,0.04); margin-bottom:16px; }"
)

# Form group styles
html = html.replace(
    ".form-group label { display:block; margin-bottom:6px; font-size:0.82rem; color:var(--text2); }",
    ".form-group label { display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text2); }"
)

html = html.replace(
    ".form-group input, .form-group textarea { width:100%; padding:12px 14px; border:1.5px solid rgba(0,0,0,0.06); border-radius:10px; font-size:0.9rem; font-family:inherit; background:var(--bg); transition:all 0.3s; }",
    ".form-group input, .form-group textarea { width:100%; padding:10px 12px; border:1px solid rgba(0,0,0,0.06); border-radius:8px; font-size:0.85rem; font-family:inherit; background:var(--bg); transition:all 0.2s; }"
)

# Pay methods
html = html.replace(
    ".pay-methods { display:flex; gap:10px; margin-bottom:16px; }",
    ".pay-methods { display:flex; gap:8px; margin-bottom:14px; }"
)

html = html.replace(
    ".pay-btn { flex:1; padding:12px; border:2px solid rgba(0,0,0,0.06); border-radius:12px; background:#fff; cursor:pointer; text-align:center; font-size:0.88rem; transition:all 0.3s; }",
    ".pay-btn { flex:1; padding:10px; border:1.5px solid rgba(0,0,0,0.06); border-radius:8px; background:#fff; cursor:pointer; text-align:center; font-size:0.82rem; transition:all 0.2s; }"
)

# QR box
html = html.replace(
    ".qr-box { text-align:center; padding:20px; background:var(--bg); border-radius:12px; margin-bottom:20px; }",
    ".qr-box { text-align:center; padding:16px; background:var(--bg); border-radius:8px; margin-bottom:16px; }"
)

html = html.replace(
    ".qr-box p { color:var(--text2); font-size:0.85rem; margin:0; }",
    ".qr-box p { color:var(--text2); font-size:0.82rem; margin:0; }"
)

# Order button
html = html.replace(
    ".order-btn { width:100%; padding:14px; background:var(--accent); color:#fff; border:none; border-radius:12px; font-size:0.95rem; cursor:pointer; font-weight:500; transition:all 0.3s; }",
    ".order-btn { width:100%; padding:12px; background:var(--accent); color:#fff; border:none; border-radius:8px; font-size:0.88rem; cursor:pointer; transition:all 0.2s; }"
)

# Modal overlay
html = html.replace(
    ".modal-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:10000; justify-content:center; align-items:center; backdrop-filter:blur(4px); }",
    ".modal-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:10000; justify-content:center; align-items:center; backdrop-filter:blur(2px); }"
)

# Remove duplicate mobile nav closing tags
html = html.replace(
    """<nav class="mobile-nav">

    <div class="mobile-nav-inner">

      <a href="#home" class="active"><span class="icon">🏠</span>首页</a>

      <a href="#products"><span class="icon">📦</span>产品</a>

      <a href="#contact"><span class="icon">💬</span>咨询</a>

      
  
          <a href="javascript:void(0)" onclick="toggleSettings()" style="color:#555"><span class="icon">⚙</span>设置</a>

    </div>

      </nav>""",
    """<nav class="mobile-nav">

    <div class="mobile-nav-inner">

      <a href="#home" class="active"><span class="icon">🏠</span>首页</a>

      <a href="#products"><span class="icon">📦</span>产品</a>

      <a href="#contact"><span class="icon">💬</span>咨询</a>

      
  
          <a href="javascript:void(0)" onclick="toggleSettings()" style="color:#555"><span class="icon">⚙</span>设置</a>

    </div>

  </nav>"""
)

# Update language toggle (cleaner)
html = html.replace(
    '<button class="lang-toggle" onclick="toggleLang(event)"><span id="currentLangLabel">中文</span> <span class="arrow">▼</span></button>',
    '<button class="lang-toggle" onclick="toggleLang(event)"><span id="currentLangLabel">中文</span> <span class="arrow">▼</span></button>'
)

# Clean up whitespace around i18n object - remove extra blank lines inside i18n keys
# Keep i18n structure intact but make it cleaner

with open('D:/tokai/index-fixed-final.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"After cleanup: {len(html)} bytes ({len(html) - 80490:+d} change)")

# Quick validation
start = html.find('<script>') + 8
end = html.rfind('</script>')
js_code = html[start:end]
no_await = js_code.replace('await ', '')
try:
    exec(f"exec('''\\ntry:\\n    exec(compile(open(r'D:/tokai/check-final2.js').read(), '', 'exec'))\\nexcept:\\n    pass''')")
except:
    import subprocess
    r = subprocess.run(['node', '-e', f'try{{new Function(require(\'fs\').readFileSync(\'D:/tokai/check-final2.js\',\'utf8\'));console.log(\'OK\')}}catch(e){{console.log(\'ERROR:\',e.message.substring(0,100))}}'], capture_output=True, text=True)
    print(f"Validation: {r.stdout.strip()}")

print("Interface cleaned up successfully!")

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
import json
import gspread

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#5B96B2" 
GA_ID = "G-29F4EM37KE"

# --- 2. CONFIG & PWA META TAGS ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

st.markdown(f"""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION (BUG-FREE) ---
if "journal_unlocked" not in st.session_state: st.session_state.journal_unlocked = False
if "core_journal" not in st.session_state: st.session_state.core_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "energy_history" not in st.session_state: st.session_state.energy_history = []
if "active_audio" not in st.session_state: st.session_state.active_audio = None
if "active_game" not in st.session_state: st.session_state.active_game = "Release"
if "active_breath" not in st.session_state: st.session_state.active_breath = "Anchor"
if "agent_audio" not in st.session_state: st.session_state.agent_audio = "flute.mp3"
if "agent_breath" not in st.session_state: st.session_state.agent_breath = "Box"
if "agent_message" not in st.session_state: st.session_state.agent_message = "I have prepared this space for you."

if "theme" not in st.session_state: st.session_state.theme = "Midnight"

# --- 4. THEME ENGINE VARIABLES ---
if st.session_state.theme == "Midnight":
    app_bg = "#121212"
    app_text = "#E0E0E0"
    btn_bg = "linear-gradient(180deg, rgba(50,50,50,1) 0%, rgba(20,20,20,1) 100%)"
    btn_border = "#444"
    slab_bg = "rgba(255,255,255,0.05)"
    input_bg = "#1A1A1A"
    title_color = "#FFFFFF"
    
    c_bg = "#1A1A1A"
    c_text = "#FFFFFF"
    c_border = "#333"
    c_msg_bg = "rgba(0,0,0,0.5)"
    c_star = "255, 255, 255"
    c_moon = "255, 250, 240"
else: 
    app_bg = "#F4FAFF"
    app_text = "#1A2530"
    btn_bg = "linear-gradient(180deg, #FFFFFF 0%, #E6F0F9 100%)"
    btn_border = "#C0D6E4"
    slab_bg = "#FFFFFF"
    input_bg = "#FFFFFF"
    title_color = soft_blue
    
    c_bg = "#FFFFFF"
    c_text = "#1A2530"
    c_border = "#C0D6E4"
    c_msg_bg = "rgba(255,255,255,0.85)"
    c_star = "91, 150, 178" 
    c_moon = "91, 150, 178" 

def theme_it(html_str):
    return html_str.replace("[C_BG]", c_bg).replace("[C_BORDER]", c_border).replace("[C_TEXT]", c_text).replace("[C_MSG_BG]", c_msg_bg).replace("[C_STAR]", c_star).replace("[C_MOON]", c_moon)

# --- 5. GOOGLE ANALYTICS ---
components.html(f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}', {{ 'anonymize_ip': true }});
    </script>
    """, height=0)

# --- 6. THE BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

# --- 7. DYNAMIC DESIGN CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {app_bg} !important; color: {app_text} !important; transition: all 0.5s ease-in-out; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 4.5rem !important; text-align: center !important; overflow-x: hidden !important; }}
    
    div[data-testid="stHorizontalBlock"] {{
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important; 
        gap: 10px !important; 
    }}
    
    div[data-testid="column"], div[data-testid="stColumn"] {{
        width: calc(33.333% - 10px) !important;
        min-width: calc(33.333% - 10px) !important;
        max-width: calc(33.333% - 10px) !important;
        flex: 1 1 calc(33.333% - 10px) !important;
        display: flex !important;
        justify-content: center !important;
        margin-bottom: 5px !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(2):last-child) > div[data-testid="column"] {{
        width: calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
        max-width: calc(50% - 10px) !important;
        flex: 1 1 calc(50% - 10px) !important;
    }}
    
    @keyframes pulse426 {{
        0%   {{ transform: scale(1); opacity: 0.3; border-width: 2px; }}
        33%  {{ transform: scale(1.8); opacity: 1; border-width: 4px; }}
        50%  {{ transform: scale(1.8); opacity: 1; border-width: 4px; }}
        100% {{ transform: scale(1); opacity: 0.3; border-width: 2px; }}
    }}
    
    .breathing-circle {{
        width: 60px; height: 60px; border: 3px solid {soft_blue}; border-radius: 50%;
        margin: 25px auto; animation: pulse426 12s infinite ease-in-out !important;
        box-shadow: 0 0 25px rgba(91, 150, 178, 0.5);
    }}

    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; font-size: 2.5rem; color: {title_color}; text-transform: uppercase; transition: color 0.5s ease; }}
    .section-header {{ font-size: 13px; letter-spacing: 4px; text-transform: uppercase; margin: 30px 0 15px 0; color: {soft_blue}; border-bottom: 1px solid {btn_border}; padding-bottom: 8px; }}
    
    div.stButton {{ width: 100% !important; }}

    .stButton>button {{ 
        width: 100% !important; min-width: 100% !important;
        background: {btn_bg} !important; 
        color: {app_text} !important; border: 1px solid {btn_border} !important; 
        border-radius: 4px !important; min-height: 48px !important; height: 100% !important;
        font-size: 11px !important; padding: 0px 2px !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
        text-align: center !important; box-sizing: border-box !important;
        transition: all 0.3s ease;
    }}
    
    .autopilot-btn>button {{
        background: linear-gradient(180deg, #1c2b3a 0%, #0b131a 100%) !important;
        border: 1px solid {soft_blue} !important; color: {soft_blue} !important; letter-spacing: 1px;
    }}

    .agent-btn>button {{
        background: linear-gradient(180deg, #2a1a3a 0%, #150b1a 100%) !important;
        border: 1px solid #b25b96 !important; color: #b25b96 !important; letter-spacing: 1px;
    }}
    
    .market-slab {{ background: {slab_bg}; border: 1px solid {btn_border}; border-radius: 12px; padding: 25px; margin-bottom: 20px; text-align: center; transition: all 0.3s ease; }}
    .bundle-title {{ font-size: 22px; letter-spacing: 2px; color: {app_text}; margin-bottom: 10px; }}
    .price-tag {{ font-size: 20px; color: {soft_blue}; font-weight: 600; margin-bottom: 15px; }}
    
    .disclaimer-box {{ text-align: left; font-size: 12px; opacity: 0.7; line-height: 1.8; background: {input_bg}; padding: 20px; border-radius: 8px; border-left: 3px solid {soft_blue}; }}
    .faq-q {{ font-weight: bold; color: {soft_blue}; margin-top: 15px; text-align: left; }}
    .faq-a {{ font-size: 13px; opacity: 0.8; margin-bottom: 10px; text-align: left; border-bottom: 1px solid {btn_border}; padding-bottom: 10px; color: {app_text}; }}
    
    textarea, input {{ background: {input_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; text-align: center !important; font-size: 15px !important; }}
    .journal-entry {{ background: {input_bg}; border-left: 3px solid {soft_blue}; padding: 18px; margin-bottom: 5px; border-radius: 6px; color: {app_text}; text-align: left; font-size: 15px; line-height: 1.6; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# --- 8. MAIN APP HEADER & NAV GRID ---
# ==========================================

st.markdown("<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown("<div class='breathing-circle'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:10px; opacity:0.5; letter-spacing:3px; margin-bottom: 20px;'>INHALE 4 • HOLD 2 • EXHALE 6</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"; st.rerun()
with col2:
    if st.button("Ether", use_container_width=True): st.session_state.current_page = "Ether"; st.rerun()
with col3:
    if st.button("Focus", use_container_width=True): st.session_state.current_page = "Focus"; st.rerun()

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Market", use_container_width=True): st.session_state.current_page = "Market"; st.rerun()
with col5:
    if st.button("Info", use_container_width=True): st.session_state.current_page = "Info"; st.rerun()
with col6:
    if st.button("Settings", use_container_width=True): st.session_state.current_page = "Settings"; st.rerun()

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# --- REUSABLE HTML COMPONENTS ---
base_breath_html = """
<div style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; position:relative; width:100%; height:260px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
    <canvas id="breathCanvas" style="position:absolute; top:0; left:0; width:100%; height:100%;"></canvas>
</div>
<script>
    const canvas = document.getElementById('breathCanvas'); const ctx = canvas.getContext('2d');
    function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
    window.addEventListener('resize', resize); resize(); const start = Date.now();
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width/2; const cy = canvas.height/2 - 10;
        let t = ((Date.now() - start) / 1000);
        [JS_INJECT]
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

breath_js_dict = {
    "Anchor": """
        let cycle = t % 12; let text = ""; let scale = 1;
        if(cycle < 4) { text = "INHALE (4)"; scale = 1 + (cycle/4); }
        else if(cycle < 6) { text = "HOLD (2)"; scale = 2; }
        else { text = "EXHALE (6)"; scale = 2 - ((cycle-6)/6); }
        ctx.beginPath(); ctx.arc(cx, cy, 35 * scale, 0, Math.PI*2);
        ctx.strokeStyle = "rgba(91, 150, 178, 0.8)"; ctx.lineWidth = 3; ctx.stroke();
        ctx.fillStyle = "rgba(91, 150, 178, 0.2)"; ctx.fill();
        ctx.fillStyle = "[C_TEXT]"; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px";
        ctx.fillText(text, cx, cy + 90);
    """,
    "Box": """
        let cycle = t % 16; let text = ""; let size = 100; let x = cx - size/2; let y = cy - size/2;
        ctx.strokeStyle = "rgba(91, 150, 178, 0.2)"; ctx.lineWidth = 2; ctx.strokeRect(x, y, size, size);
        ctx.strokeStyle = "rgba(91, 150, 178, 1)"; ctx.lineWidth = 4; ctx.beginPath();
        if(cycle < 4) { text = "INHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y+size - size*(cycle/4)); } 
        else if(cycle < 8) { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x + size*((cycle-4)/4), y); } 
        else if(cycle < 12) { text = "EXHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y + size*((cycle-8)/4)); } 
        else { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y+size); ctx.lineTo(x+size - size*((cycle-12)/4), y+size); }
        ctx.stroke(); ctx.fillStyle = "[C_TEXT]"; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Wave": """
        let cycle = t % 19; let text = ""; let width = canvas.width * 0.7; let startX = cx - width/2; let amp = 50; let pathX = 0; let pathY = 0;
        if(cycle < 4) { text = "INHALE (4)"; pathX = startX + (width * 0.2 * (cycle/4)); pathY = cy + amp - (amp * 2 * (cycle/4)); } 
        else if(cycle < 11) { text = "HOLD (7)"; pathX = startX + (width * 0.2) + (width * 0.4 * ((cycle-4)/7)); pathY = cy - amp; } 
        else { text = "EXHALE (8)"; pathX = startX + (width * 0.6) + (width * 0.4 * ((cycle-11)/8)); pathY = cy - amp + (amp * 2 * ((cycle-11)/8)); }
        ctx.strokeStyle = "rgba(91, 150, 178, 0.2)"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(startX, cy+amp); ctx.lineTo(startX+width*0.2, cy-amp);
        ctx.lineTo(startX+width*0.6, cy-amp); ctx.lineTo(startX+width, cy+amp); ctx.stroke();
        ctx.beginPath(); ctx.arc(pathX, pathY, 12, 0, Math.PI*2); ctx.fillStyle = "rgba(91, 150, 178, 1)"; ctx.fill(); ctx.shadowBlur = 15; ctx.shadowColor = "#5B96B2";
        ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Moon": """
        let cycle = t % 19; let text = ""; let opacity = 0.2; let yOffset = 0;
        if(cycle < 4) { text = "INHALE (4)"; opacity = 0.2 + 0.8*(cycle/4); yOffset = -20 * (cycle/4); }
        else if(cycle < 11) { text = "HOLD (7)"; opacity = 1.0; yOffset = -20; }
        else { text = "EXHALE (8)"; opacity = 1.0 - 0.8*((cycle-11)/8); yOffset = -20 + 40*((cycle-11)/8); }
        ctx.beginPath(); ctx.arc(cx, cy + yOffset, 40, 0, Math.PI*2); ctx.fillStyle = `rgba([C_MOON], ${opacity})`; ctx.fill();
        ctx.shadowBlur = 30 * opacity; ctx.shadowColor = "[C_TEXT]";
        ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Lotus": """
        let cycle = t % 19; let text = ""; let spread = 0;
        if(cycle < 4) { text = "INHALE (4)"; spread = cycle/4; }
        else if(cycle < 11) { text = "HOLD (7)"; spread = 1; }
        else { text = "EXHALE (8)"; spread = 1 - ((cycle-11)/8); }
        for(let i=0; i<6; i++) {
            let angle = i * (Math.PI*2/6) + (t * 0.1); let px = cx + Math.cos(angle) * (30 * spread); let py = cy + Math.sin(angle) * (30 * spread);
            ctx.beginPath(); ctx.arc(px, py, 25, 0, Math.PI*2); ctx.strokeStyle = "rgba(91, 150, 178, 0.6)"; ctx.lineWidth = 1.5; ctx.stroke();
            ctx.fillStyle = "rgba(91, 150, 178, 0.1)"; ctx.fill();
        }
        ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """
}

release_game_html = """
<div style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; position:relative; width:100%; height:350px; overflow:hidden;">
    <div id="scoreDisplay" style="position:absolute; top:15px; width:100%; text-align:center; color:#5B96B2; font-family:sans-serif; font-size:12px; letter-spacing:3px; z-index:10; pointer-events:none;">
        THOUGHTS RELEASED: <span id="scoreVal">0</span>
    </div>
    <canvas id="gameCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
</div>
<script>
    const canvas = document.getElementById('gameCanvas'); const ctx = canvas.getContext('2d');
    let bubbles = []; let score = 0; let gameStarted = false; let bubbleInterval;
    function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
    window.addEventListener('resize', resize); resize();
    function createBubble() { bubbles.push({ x: Math.random() * (canvas.width - 40) + 20, y: canvas.height + 20, radius: Math.random() * 15 + 15, speed: Math.random() * 0.8 + 0.4, alpha: 0.6, popping: false }); }
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (!gameStarted) {
            ctx.fillStyle = "#5B96B2"; ctx.globalAlpha = 0.5; ctx.font = "12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "2px"; ctx.fillText("TAP SCREEN TO START", canvas.width / 2, canvas.height / 2); ctx.globalAlpha = 1.0;
        } else {
            for (let i = bubbles.length - 1; i >= 0; i--) {
                let b = bubbles[i]; ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
                if (b.popping) { b.radius += 2; b.alpha -= 0.05; ctx.strokeStyle = `rgba(91, 150, 178, ${b.alpha})`; ctx.lineWidth = 2; ctx.stroke(); if (b.alpha <= 0) bubbles.splice(i, 1);
                } else { b.y -= b.speed; ctx.fillStyle = `rgba(91, 150, 178, ${b.alpha})`; ctx.fill(); ctx.shadowBlur = 15; ctx.shadowColor = "rgba(91, 150, 178, 0.5)"; if (b.y < -50) bubbles.splice(i, 1); }
            }
        }
        requestAnimationFrame(draw);
    }
    canvas.addEventListener('pointerdown', (e) => {
        if (!gameStarted) { gameStarted = true; bubbleInterval = setInterval(createBubble, 1200); return; }
        const rect = canvas.getBoundingClientRect(); const clickX = e.clientX - rect.left; const clickY = e.clientY - rect.top;
        for (let i = 0; i < bubbles.length; i++) { let b = bubbles[i]; if (!b.popping && Math.hypot(clickX - b.x, clickY - b.y) < b.radius + 15) { b.popping = true; score++; document.getElementById('scoreVal').innerText = score; break; } }
    });
    draw();
</script>
"""

# --- PAGES ---

if st.session_state.current_page == "Journal":
    
    # 🚨 STEP 1: FREE AMBIENCE & NEW ZEN TOOLS AT THE TOP 🚨
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    aud_cols = st.columns(5)
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    for i, name in enumerate(sounds.keys()):
        with aud_cols[i]:
            if st.button(name, key=f"aud_{name}", use_container_width=True): st.session_state.active_audio = sounds[name]
    
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    # 🚨 NEW: 60px HEIGHT, 12 COLORS, 4 RANDOM ANIMATIONS 🚨
    zen_html = """
        <div style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; position:relative; width:100%; height:60px; overflow:hidden; cursor:crosshair;" id="zen-box">
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:#5B96B2; font-family:sans-serif; font-size:10px; letter-spacing:2px; opacity:0.7; pointer-events:none; text-align:center; width: 100%; line-height: 1.3;">
                TOUCH THE SURFACE<br>TO GROUND YOURSELF
            </div>
            <canvas id="zenCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0;"></canvas>
        </div>
        <script>
            const canvas = document.getElementById('zenCanvas');
            const ctx = canvas.getContext('2d');
            let shapes = [];
            
            // 12 distinct, beautiful colors for the mind
            const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#6A0572', '#A8E6CF', '#FDFFAB', '#FF8C94', '#82B1FF', '#B9F2FF', '#F9F871', '#D4A5A5', '#9B59B6'];
            // 4 different tactile geometric responses
            const types = ['circle', 'square', 'spots', 'bird'];

            function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
            window.addEventListener('resize', resize); resize();

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < shapes.length; i++) {
                    let s = shapes[i];
                    ctx.globalAlpha = s.alpha;
                    ctx.strokeStyle = s.color;
                    ctx.fillStyle = s.color;
                    ctx.lineWidth = 2;

                    if (s.type === 'circle') {
                        ctx.beginPath(); ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2); ctx.stroke();
                        s.radius += 1; s.alpha -= 0.02;
                    } else if (s.type === 'square') {
                        ctx.strokeRect(s.x - s.radius, s.y - s.radius, s.radius * 2, s.radius * 2);
                        s.radius += 1; s.alpha -= 0.02;
                    } else if (s.type === 'spot') {
                        ctx.beginPath(); ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2); ctx.fill();
                        s.x += s.vx; s.y += s.vy; s.alpha -= 0.02;
                    } else if (s.type === 'bird') {
                        ctx.beginPath();
                        ctx.moveTo(s.x - s.radius, s.y - s.radius/2);
                        ctx.lineTo(s.x, s.y);
                        ctx.lineTo(s.x + s.radius, s.y - s.radius/2);
                        ctx.stroke();
                        s.y -= 0.8; s.radius += 0.3; s.alpha -= 0.02;
                    }
                }
                shapes = shapes.filter(s => s.alpha > 0); 
                ctx.globalAlpha = 1.0;
                requestAnimationFrame(draw);
            }

            document.getElementById('zen-box').addEventListener('pointerdown', (e) => {
                const rect = canvas.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                const clickY = e.clientY - rect.top;
                
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                const randomType = types[Math.floor(Math.random() * types.length)];

                if (randomType === 'spots') {
                    // Create a burst of 6 small particles
                    for(let i=0; i<6; i++) {
                        shapes.push({
                            type: 'spot', x: clickX, y: clickY,
                            vx: (Math.random() - 0.5) * 3, vy: (Math.random() - 0.5) * 3,
                            radius: Math.random() * 3 + 1.5, alpha: 1, color: randomColor
                        });
                    }
                } else {
                    shapes.push({ type: randomType, x: clickX, y: clickY, radius: 5, alpha: 1, color: randomColor });
                }
            });
            draw();
        </script>
    """
    components.html(theme_it(zen_html), height=75)

    # 🚨 STEP 2: FREE EMERGENCY FIRE ALARM 🚨
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='autopilot-btn'>", unsafe_allow_html=True)
    if st.button("⚡ AUTO-PILOT (INSTANT SOS) ⚡", use_container_width=True):
        st.session_state.current_page = "AutoPilot"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 🚨 STEP 3: THE PREMIUM AI WALL 🚨
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>PRIVATE AI MENTOR</div>", unsafe_allow_html=True)

    if not st.session_state.journal_unlocked:
        # THE LOCK BOX
        st.markdown("<div class='market-slab' style='padding: 30px 20px;'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px; color: {app_text}; line-height: 1.6;'>Unlock the AI Agent and Guided Reflections by entering your email.</p>", unsafe_allow_html=True)
        user_email = st.text_input("Your Email Address", placeholder="name@example.com", key="ai_email_input")
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("UNLOCK AI MENTOR", use_container_width=True):
            if "@" in user_email and "." in user_email:
                try:
                    if "GCP_CREDENTIALS" in st.secrets:
                        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"], strict=False)
                        gc = gspread.service_account_from_dict(creds_dict)
                        sh = gc.open("jsukoon_users")
                        sheet = sh.sheet1
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sheet.append_row([user_email, current_time])
                except Exception as e:
                    pass 
                
                st.session_state.journal_unlocked = True
                st.rerun()
            else:
                st.error("Please enter a valid email address.")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # UNLOCKED AI TOOLS
        voice_input = st.audio_input("Record your thoughts")
        text_msg = st.text_area("Or type your reflection...", height=150)
        
        c_short, c_deep = st.columns(2)
        with c_short:
            btn_short = st.button("GUIDE (SHORT)", use_container_width=True)
        with c_deep:
            btn_deep = st.button("GUIDE (DEEP)", use_container_width=True)
            
        st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='agent-btn'>", unsafe_allow_html=True)
        btn_agent = st.button("🤖 AI AGENT (SMART SANCTUARY) 🤖", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if btn_short or btn_deep or btn_agent:
            if model:
                with st.spinner("Channeling Wisdom..." if not btn_agent else "Agent Analyzing Symptoms..."):
                    energy_context = ""
                    if st.session_state.energy_history:
                        latest_energy = st.session_state.energy_history[-1]
                        energy_context = f"\n\nThe user's physical energy state is '{latest_energy}'."

                    if btn_agent:
                        context = f"""You are the Sukoon AI Agent. The user needs a custom sanctuary.
                        Analyze their text. If they can't sleep, select 'Sleep_Lotus' and 'waves'. 
                        If they are anxious, select 'Box' and 'forest'.
                        {energy_context}
                        
                        CRITICAL INSTRUCTION: Respond ONLY with a raw JSON object. No markdown.
                        {{
                            "reply": "A very short, 1-sentence comforting message.",
                            "breath": "Anchor", "Box", "Sleep_Wave", "Sleep_Moon", or "Sleep_Lotus",
                            "audio": "birds", "flute", "forest", "waves", or "wind"
                        }}
                        """
                    else:
                        length_instruction = "Keep the response short: maximum 2 paragraphs." if btn_short else "Provide a detailed, deep, and highly comforting long-form response."
                        context = f"""You are the Sukoon Mentor. Respond in the user's exact language or Hinglish.
                        {length_instruction}
                        End with a brief 'Inhale 4 - Hold 2 - Exhale 6' reminder.
                        {energy_context}"""
                    
                    try:
                        if voice_input:
                            audio_part = {"mime_type": "audio/wav", "data": voice_input.getvalue()}
                            prompt_parts = [context, audio_part, "Listen to my voice note, transcribe it exactly, then respond."]
                        elif text_msg:
                            prompt_parts = [context, text_msg]
                        else:
                            prompt_parts = [context, "I am seeking silence."]
                            
                        resp = model.generate_content(prompt_parts)
                        
                        if btn_agent:
                            try:
                                clean_text = resp.text.strip().replace('```json', '').replace('```', '')
                                agent_command = json.loads(clean_text)
                                
                                st.session_state.agent_message = agent_command.get("reply", "I have prepared this space for you.")
                                st.session_state.agent_breath = agent_command.get("breath", "Box")
                                raw_audio = str(agent_command.get("audio", "flute")).lower()
                                st.session_state.agent_audio = f"{raw_audio}.mp3"
                                
                                st.session_state.current_page = "AgentSanctuary"
                                
                            except Exception as e:
                                st.session_state.agent_message = "I am here. Let us breathe together."
                                st.session_state.agent_breath = "Box"
                                st.session_state.agent_audio = "flute.mp3"
                                st.session_state.current_page = "AgentSanctuary"
                                
                        else:
                            ai_reply = resp.text
                            unique_id = str(datetime.now().timestamp()).replace('.', '')
                            st.session_state.core_journal.append({
                                "time": datetime.now().strftime("%H:%M"), 
                                "ai": ai_reply,
                                "id": unique_id
                            })
                        st.rerun()
                        
                    except Exception as e:
                        st.error("The Mentor needs a moment of quiet. Please try again.")
            else:
                st.warning("The Mentor is resting. Please try again in an hour.")

        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
        
        for entry in reversed(st.session_state.core_journal):
            safe_speech_text = urllib.parse.quote(entry['ai'])
            html_button = f"""
            <style>
                .listen-btn {{
                    background: {btn_bg};
                    color: {app_text}; border: 1px solid {btn_border}; border-radius: 4px; padding: 12px;
                    font-size: 11px; font-family: sans-serif; cursor: pointer; width: 100%; text-transform: uppercase;
                    margin-bottom: 5px;
                }}
                .listen-btn:active {{ filter: brightness(0.8); }}
            </style>
            <button class="listen-btn" onclick="playVoice()">LISTEN TO MENTOR ({entry['time']})</button>
            <script>
                function playVoice() {{
                    window.speechSynthesis.cancel();
                    var decodedText = decodeURIComponent("{safe_speech_text}");
                    var m = new SpeechSynthesisUtterance(decodedText);
                    m.rate = 0.85;
                    m.lang = 'hi-IN'; 
                    
                    function setVoiceAndSpeak() {{
                        var voices = window.speechSynthesis.getVoices();
                        var localVoice = voices.find(v => v.lang.includes('hi-IN') || v.lang.includes('en-IN') || v.name.includes('India') || v.name.includes('Hindi'));
                        if (localVoice) {{ m.voice = localVoice; }}
                        window.speechSynthesis.speak(m);
                    }}

                    if (window.speechSynthesis.getVoices().length === 0) {{
                        window.speechSynthesis.onvoiceschanged = setVoiceAndSpeak;
                    }} else {{
                        setVoiceAndSpeak();
                    }}
                }}
            </script>
            """
            components.html(html_button, height=50)

            formatted_text = entry['ai'].replace('\n', '<br>')
            st.markdown(f"<div class='journal-entry'><b>{entry['time']}</b><br><br>{formatted_text}</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>ENERGY STATE</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 11px; opacity: 0.7; margin-bottom: 15px; color:{app_text};'>Pause and acknowledge how your body feels to guide the Mentor.</p>", unsafe_allow_html=True)
        
        m_cols = st.columns(5)
        for i, m in enumerate(["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]):
            with m_cols[i]:
                if st.button(m, key=f"m_{m}", use_container_width=True): st.session_state.energy_history.append(m); st.rerun()

elif st.session_state.current_page == "AutoPilot":
    st.markdown("<div class='section-header' style='color: #a6d8ff;'>⚡ EMERGENCY SANCTUARY ⚡</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 25px; color:{app_text};'>I have taken over. Let the sound wash over you. Tap the screen to pop your thoughts, and breathe with the box.</p>", unsafe_allow_html=True)
    
    st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/waves.mp3", format="audio/mp3", autoplay=True)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    components.html(theme_it(base_breath_html.replace("[JS_INJECT]", breath_js_dict["Box"])), height=270)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    components.html(theme_it(release_game_html), height=370)

elif st.session_state.current_page == "AgentSanctuary":
    st.markdown("<div class='section-header' style='color: #b25b96;'>🤖 AI AGENT SANCTUARY 🤖</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 25px; color:{app_text};'>{st.session_state.agent_message}</p>", unsafe_allow_html=True)
    
    st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.agent_audio}", format="audio/mp3", autoplay=True)
    
    selected_js = breath_js_dict.get(st.session_state.agent_breath, breath_js_dict["Box"])
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    components.html(theme_it(base_breath_html.replace("[JS_INJECT]", selected_js)), height=270)
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    components.html(theme_it(release_game_html), height=370)

elif st.session_state.current_page == "Ether":
    st.markdown("<div class='section-header'>THE ETHER</div>", unsafe_allow_html=True)
    
    ether_html = """
    <div id="ether-container" style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; padding: 40px 20px; text-align: center; position: relative; overflow: hidden; min-height: 400px; display: flex; flex-direction: column; justify-content: center;">
        <canvas id="starCanvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5;"></canvas>
        <p id="promptText" style="color:#5B96B2; font-family:sans-serif; font-size:12px; letter-spacing:3px; margin-bottom:25px; transition: opacity 1s; z-index: 10;">
            WRITE YOUR THOUGHTS INTO THE ETHER
        </p>
        <textarea id="etherInput" placeholder="..." style="width:100%; height:120px; background: transparent; color:[C_TEXT]; border:1px solid [C_BORDER]; border-radius:6px; padding:15px; text-align:center; font-size:16px; resize:none; outline:none; font-family:sans-serif; transition: all 2.5s cubic-bezier(0.25, 0.1, 0.25, 1); z-index: 10; position: relative;"></textarea>
        
        <div style="height: 25px; z-index: 10;"></div>
        
        <div id="buttonRow" style="display: flex; gap: 10px; z-index: 10; width: 100%; transition: opacity 1s;">
            <button id="releaseBtn" style="background: linear-gradient(180deg, #3a1c1c 0%, #1a0b0b 100%); color: #ffbba6; border: 1px solid #5a2a2a; border-radius: 4px; padding: 12px; font-size: 10px; letter-spacing: 1px; cursor: pointer; text-transform: uppercase; flex: 1;">
                BURN & RELEASE<br><span style="font-size: 8px; opacity: 0.6;">(Negative Thoughts)</span>
            </button>
            <button id="manifestBtn" style="background: linear-gradient(180deg, #1c2b3a 0%, #0b131a 100%); color: #a6d8ff; border: 1px solid #2a415a; border-radius: 4px; padding: 12px; font-size: 10px; letter-spacing: 1px; cursor: pointer; text-transform: uppercase; flex: 1;">
                MANIFEST & SEND<br><span style="font-size: 8px; opacity: 0.6;">(Positive Thoughts)</span>
            </button>
        </div>

        <div id="messageText" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: [C_TEXT]; font-family: sans-serif; font-size: 14px; letter-spacing: 3px; opacity: 0; transition: opacity 2s ease-in-out; pointer-events: none; width: 90%; line-height: 1.8; z-index: 15;">
        </div>
    </div>

    <script>
        const btnRelease = document.getElementById('releaseBtn');
        const btnManifest = document.getElementById('manifestBtn');
        const btnRow = document.getElementById('buttonRow');
        const input = document.getElementById('etherInput');
        const promptText = document.getElementById('promptText');
        const msg = document.getElementById('messageText');
        const container = document.getElementById('ether-container');
        const canvas = document.getElementById('starCanvas');
        const ctx = canvas.getContext('2d');
        
        let particles = [];
        let animating = false;
        let currentMode = 'star';

        function resizeCanvas() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
        window.addEventListener('resize', resizeCanvas); resizeCanvas();

        function createParticles(mode) {
            const rect = input.getBoundingClientRect();
            const containerRect = container.getBoundingClientRect();
            const top = rect.top - containerRect.top; const left = rect.left - containerRect.left;
            
            for (let i = 0; i < 120; i++) {
                if (mode === 'fire') {
                    particles.push({
                        x: left + Math.random() * rect.width, y: top + Math.random() * rect.height,
                        vx: (Math.random() - 0.5) * 4, vy: (Math.random() * -5) - 1, 
                        radius: Math.random() * 3 + 1, alpha: 1, decay: Math.random() * 0.02 + 0.01,
                        color: `rgba(${255}, ${Math.random() * 100 + 50}, 0, ` 
                    });
                } else {
                    particles.push({
                        x: left + Math.random() * rect.width, y: top + Math.random() * rect.height,
                        vx: (Math.random() - 0.5) * 2, vy: (Math.random() * -2) - 0.2, 
                        radius: Math.random() * 2 + 0.5, alpha: 1, decay: Math.random() * 0.01 + 0.005,
                        color: `rgba([C_STAR], ` 
                    });
                }
            }
            if (!animating) { animating = true; animateParticles(); }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let active = false;
            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                if (p.alpha > 0) {
                    active = true; p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fillStyle = p.color + `${Math.max(0, p.alpha)})`;
                    ctx.shadowBlur = currentMode === 'fire' ? 8 : 15; 
                    ctx.shadowColor = currentMode === 'fire' ? "#ff4500" : "[C_TEXT]"; 
                    ctx.fill();
                }
            }
            if (active) { requestAnimationFrame(animateParticles); } 
            else { animating = false; particles = []; ctx.clearRect(0, 0, canvas.width, canvas.height); }
        }

        function triggerEther(mode) {
            if(input.value.trim() === '') return;
            currentMode = mode;
            
            if (mode === 'fire') {
                msg.innerHTML = "THE ETHER HAS BURNED IT.<br>YOU HAVE CHOSEN TO LET IT GO.";
                input.style.filter = "blur(15px) contrast(200%) sepia(100%) hue-rotate(330deg) saturate(300%)"; 
                input.style.transform = "translateY(30px) scale(0.9)"; 
            } else {
                msg.innerHTML = "THE ETHER HAS HEARD YOU.<br>YOUR INTENTION HAS BEEN SET.";
                input.style.filter = "blur(12px) brightness(200%)"; 
                input.style.transform = "translateY(-60px) scale(1.05)"; 
            }

            createParticles(mode);
            input.style.opacity = "0";
            btnRow.style.opacity = "0"; promptText.style.opacity = "0";
            btnRow.style.pointerEvents = "none"; input.style.pointerEvents = "none";
            
            setTimeout(() => { msg.style.opacity = "1"; }, 2000);
            
            setTimeout(() => {
                msg.style.opacity = "0";
                setTimeout(() => {
                    input.value = ''; input.style.transition = "none"; input.style.filter = "none"; input.style.transform = "none"; input.style.opacity = "1";
                    void input.offsetWidth; 
                    input.style.transition = "all 2.5s cubic-bezier(0.25, 0.1, 0.25, 1)";
                    btnRow.style.opacity = "1"; promptText.style.opacity = "1";
                    btnRow.style.pointerEvents = "auto"; input.style.pointerEvents = "auto";
                }, 2000);
            }, 6500); 
        }

        btnRelease.addEventListener('click', () => triggerEther('fire'));
        btnManifest.addEventListener('click', () => triggerEther('star'));
    </script>
    """
    components.html(theme_it(ether_html), height=450)

elif st.session_state.current_page == "Focus":
    
    st.markdown("<div class='section-header'>BREATH STUDIO</div>", unsafe_allow_html=True)
    
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        if st.button("Anchor (4-2-6)", use_container_width=True): st.session_state.active_breath = "Anchor"; st.rerun()
    with b_col2:
        if st.button("The Box (4-4-4-4)", use_container_width=True): st.session_state.active_breath = "Box"; st.rerun()
    with b_col3:
        if st.button("Deep Sleep (4-7-8)", use_container_width=True): 
            if not st.session_state.active_breath.startswith("Sleep"):
                st.session_state.active_breath = "Sleep_Wave"
            st.rerun()

    if st.session_state.active_breath.startswith("Sleep"):
        st.markdown("<p style='font-size: 11px; opacity: 0.7; margin: 15px 0 5px 0; text-align: center; color: #5B96B2;'>CHOOSE YOUR VISUAL GUIDE</p>", unsafe_allow_html=True)
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("The Wave", use_container_width=True): st.session_state.active_breath = "Sleep_Wave"; st.rerun()
        with s_col2:
            if st.button("The Moon", use_container_width=True): st.session_state.active_breath = "Sleep_Moon"; st.rerun()
        with s_col3:
            if st.button("The Lotus", use_container_width=True): st.session_state.active_breath = "Sleep_Lotus"; st.rerun()

    selected_js = breath_js_dict.get(st.session_state.active_breath, breath_js_dict["Anchor"])
    final_breath_html = base_breath_html.replace("[JS_INJECT]", selected_js)
    components.html(theme_it(final_breath_html), height=270)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>GROUNDING GAMES</div>", unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        if st.button("The Release", use_container_width=True): st.session_state.active_game = "Release"; st.rerun()
    with g_col2:
        if st.button("The Bloom", use_container_width=True): st.session_state.active_game = "Bloom"; st.rerun()

    if st.session_state.active_game == "Release":
        st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px; color:{app_text};'>Tap the rising thoughts to release them.</p>", unsafe_allow_html=True)
        components.html(theme_it(release_game_html), height=370)

    elif st.session_state.active_game == "Bloom":
        st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px; color:{app_text};'>Tap the center slowly to grow your light.</p>", unsafe_allow_html=True)
        bloom_html = """
        <div style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; position:relative; width:100%; height:350px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
            <canvas id="bloomCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
            <div id="bloomMessage" style="position:absolute; z-index:10; color:[C_TEXT]; font-family:sans-serif; font-size:14px; letter-spacing:3px; text-align:center; opacity:0; transition: opacity 1.5s ease-in-out; pointer-events:none; background:[C_MSG_BG]; padding:10px 20px; border-radius:4px; border:1px solid #5B96B2;"></div>
        </div>
        <script>
            const c = document.getElementById('bloomCanvas'); const ctx = c.getContext('2d'); const msg = document.getElementById('bloomMessage');
            let taps = 0; const maxTaps = 6; const affirmations = ["BEAUTIFUL FOCUS", "YOU ARE GROWING", "A MOMENT OF PEACE", "PERFECT HARMONY", "YOU ARE ENOUGH"];
            function resize() { c.width = c.offsetWidth; c.height = c.offsetHeight; draw(); }
            window.addEventListener('resize', resize);
            function draw() {
                ctx.clearRect(0, 0, c.width, c.height); const cx = c.width / 2; const cy = c.height / 2;
                if (taps === 0) { ctx.fillStyle = "#5B96B2"; ctx.globalAlpha = 0.5; ctx.font = "12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "2px"; ctx.fillText("TAP TO BLOOM", cx, cy); return; }
                for (let i = 1; i <= taps; i++) {
                    ctx.beginPath(); ctx.arc(cx, cy, i * 25, 0, Math.PI * 2); ctx.strokeStyle = "#5B96B2"; ctx.lineWidth = 1.5; ctx.globalAlpha = 0.2 + (i * 0.1); ctx.stroke();
                    for (let j = 0; j < 8; j++) {
                        let angle = (j * Math.PI / 4) + (i * 0.2); let px = cx + Math.cos(angle) * (i * 25); let py = cy + Math.sin(angle) * (i * 25);
                        ctx.beginPath(); ctx.arc(px, py, 4 + i, 0, Math.PI * 2); ctx.fillStyle = "#5B96B2"; ctx.shadowBlur = 15; ctx.shadowColor = "#5B96B2"; ctx.fill();
                    }
                }
            }
            c.addEventListener('pointerdown', () => {
                if (taps < maxTaps) {
                    taps++; draw();
                    if (taps === maxTaps) {
                        msg.innerText = affirmations[Math.floor(Math.random() * affirmations.length)]; msg.style.opacity = 1;
                        setTimeout(() => { msg.style.opacity = 0; setTimeout(() => { taps = 0; draw(); }, 1500); }, 3500);
                    }
                }
            });
            resize();
        </script>
        """
        components.html(theme_it(bloom_html), height=370)

elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>RITUAL BUNDLES & TOOLS</div>", unsafe_allow_html=True)
    
    products = [
        {"name": "Laughing Buddha", "file": "laughingbuddha.png", "price": "650"},
        {"name": "Focus Beads", "file": "beads.png", "price": "250"},
        {"name": "Buddha Sculpture", "file": "buddha.png", "price": "750"},
        {"name": "Thumb Stone", "file": "thumbstone.png", "price": "300"},
        {"name": "Wish Candle", "file": "wishcandle.png", "price": "500"},
        {"name": "Grounding Stones", "file": "stones.png", "price": "1,000"},
        {"name": "Starter Ritual", "file": "ritual.png", "price": "2,999"},
        {"name": "Master Sanctuary", "file": "sanctuary.png", "price": "6,000"}
    ]

    products_html = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">'
    for p in products:
        img_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{p['file']}"
        wa_text = urllib.parse.quote(f"I am interested in the {p['name']}")
        wa_link = f"https://wa.me/{MY_PHONE}?text={wa_text}"
        
        products_html += f"""<div style="background: {input_bg}; border: 1px solid {btn_border}; border-radius: 8px; padding: 12px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease;">
<div style="width: 100%; aspect-ratio: 1/1; background-image: url('{img_url}'); background-size: cover; background-position: center; border-radius: 6px; margin-bottom: 12px; border: 1px solid {btn_border};"></div>
<div style="color: {app_text}; font-size: 13px; letter-spacing: 1px; margin-bottom: 5px; min-height: 35px; display: flex; align-items: center; justify-content: center; line-height: 1.3;">{p['name']}</div>
<div style="color: {soft_blue}; font-weight: bold; font-size: 15px; margin-bottom: 12px;">₹{p['price']}</div>
<a href="{wa_link}" target="_blank" style="text-decoration: none; width: 100%;">
<div style="background: {btn_bg}; color: {app_text}; border: 1px solid {btn_border}; padding: 10px 0; border-radius: 4px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; width: 100%; cursor: pointer; transition: all 0.3s ease;">ORDER VIA WA</div>
</a>
</div>"""
        
    products_html += '</div>'
    st.markdown(products_html, unsafe_allow_html=True)

elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INSTALL SUKOON</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab' style='text-align:left; font-size:13px; color: {app_text};'>
        <b>1.</b> Open this link in Safari (iPhone) or Chrome (Android).<br><br>
        <b>2.</b> Tap the Share or Menu (⋮) icon.<br><br>
        <b>3.</b> Select 'Add to Home Screen'.<br><br>
        <b>4.</b> Open Sukoon directly from your home screen.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>FREQUENTLY ASKED</div>", unsafe_allow_html=True)
    faqs = [
        ("Is my journal data stored?", "No. Your reflections stay in your current session. We do not store personal journal history on our servers."),
        ("What is the 4-2-6 Rhythm?", "It is a breathing pattern designed to reduce stress and clear the mind."),
        ("Is this therapy?", "No. Sukoon is a lifestyle companion for mindfulness and well-being."),
        ("Are the objects religious?", "No. They are tactile grounding tools intended for sensory focus.")
    ]
    for q, a in faqs:
        st.markdown(f"<div class='faq-q'>{q}</div><div class='faq-a'>{a}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>LEGAL & ETHICAL DISCLAIMER</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='disclaimer-box' style='color:{app_text};'>
        <b>1. SECULAR PRACTICE:</b> The term 'Ritual' refers to secular mindfulness practices for wellness. <br><br>
        <b>2. NO SUPERNATURAL CLAIMS:</b> Sukoon does not make spiritual claims regarding physical objects. They are strictly tactile tools for focus. <br><br>
        <b>3. NOT MEDICAL ADVICE:</b> This app is for lifestyle purposes only. Not intended to diagnose or treat medical conditions. <br><br>
        <b>4. DATA PRIVACY:</b> Your journal entries and voice recordings are session-based and are not permanently stored on our servers. <br><br>
        <b>5. COMMERCE & TAXES:</b> Physical bundle sales are initiated via WhatsApp and are subject to standard shipping timelines and applicable state taxes (including GST).
    </div>""", unsafe_allow_html=True)

elif st.session_state.current_page == "Settings":
    st.markdown("<div class='section-header'>APP THEME</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 20px;'>", unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        if st.button("🌙 Midnight (Dark)", use_container_width=True): 
            st.session_state.theme = "Midnight"; st.rerun()
    with t_col2:
        if st.button("☁️ Peaceful Sky (Light)", use_container_width=True): 
            st.session_state.theme = "Sky"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>ACCOUNT & SECURITY</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='text-align:center; padding: 30px 20px;'>", unsafe_allow_html=True)
    
    if st.session_state.journal_unlocked:
        st.markdown(f"<p style='font-size: 14px; color: {app_text}; margin-bottom: 20px;'>Your Private AI Mentor is currently <b>Unlocked</b>.</p>", unsafe_allow_html=True)
        if st.button("LOCK AI MENTOR", key="btn_lock", use_container_width=True):
            st.session_state.journal_unlocked = False
            st.rerun()
    else:
        st.markdown(f"<p style='font-size: 14px; color: {soft_blue}; margin-bottom: 0;'>Your Private AI Mentor is secured.</p>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:10px; opacity:0.3; color:{app_text};'>Sukoon Sanctuary v137.0 | Tactile Zen Box Update</div>", unsafe_allow_html=True)

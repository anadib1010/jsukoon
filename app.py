import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
import json

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

# --- 3. SESSION STATE INITIALIZATION ---
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
if "ui_language" not in st.session_state: st.session_state.ui_language = "English"

# --- 4. ZERO-COST UI DICTIONARY (THE TOGGLE) ---
LANG = {
    "English": {
        "nav_journal": "Journal", "nav_ether": "Ether", "nav_focus": "Focus", 
        "nav_market": "Market", "nav_info": "Info", "nav_settings": "Settings",
        "subtitle": "INHALE 4 • HOLD 2 • EXHALE 6",
        "h_ambience": "AMBIENCE", "h_mentor": "PRIVATE AI MENTOR", "h_energy": "ENERGY STATE",
        "zen_box": "TOUCH 3 TIMES<br>TO GROUND YOURSELF",
        "sos_btn": "⚡ AUTO-PILOT (INSTANT SOS) ⚡",
        "agent_btn": "🤖 AI AGENT (SMART SANCTUARY) 🤖",
        "btn_short": "GUIDE (SHORT)", "btn_deep": "GUIDE (DEEP)",
        "record": "Record your thoughts", "type_here": "Or type your reflection...",
        "energy_prompt": "Pause and acknowledge how your body feels to guide the Mentor.",
        "e_quiet": "Quiet", "e_heavy": "Heavier", "e_neutral": "Neutral", "e_steady": "Steady", "e_vibrant": "Vibrant",
        "h_ether": "THE ETHER", "h_breath": "BREATH STUDIO", "h_games": "GROUNDING GAMES",
        "b_anchor": "Anchor (4-2-6)", "b_box": "The Box (4-4-4-4)", "b_sleep": "Deep Sleep (4-7-8)",
        "choose_visual": "CHOOSE YOUR VISUAL GUIDE", "v_wave": "The Wave", "v_moon": "The Moon", "v_lotus": "The Lotus",
        "game_release": "The Release", "game_bloom": "The Bloom",
        "release_desc": "Tap the rising thoughts to release them.", "bloom_desc": "Tap the center slowly to grow your light.",
        "h_market": "RITUAL BUNDLES & TOOLS",
        "order_wa": "ORDER VIA WA", "free_shipping": "+ FREE SHIPPING",
        "h_theme": "APP THEME", "h_lang": "UI LANGUAGE",
        "theme_dark": "🌙 Midnight (Dark)", "theme_light": "☁️ Peaceful Sky (Light)"
    },
    "Hindi": {
        "nav_journal": "जर्नल", "nav_ether": "आकाश", "nav_focus": "ध्यान", 
        "nav_market": "बाज़ार", "nav_info": "जानकारी", "nav_settings": "सेटिंग्स",
        "subtitle": "सांस लें 4 • रोकें 2 • छोड़ें 6",
        "h_ambience": "माहौल", "h_mentor": "निजी एआई मेंटर", "h_energy": "ऊर्जा की स्थिति",
        "zen_box": "खुद को शांत करने के लिए<br>3 बार छुएं",
        "sos_btn": "⚡ ऑटो-पायलट (आपातकालीन) ⚡",
        "agent_btn": "🤖 एआई एजेंट (स्मार्ट अभयारण्य) 🤖",
        "btn_short": "मार्गदर्शन (संक्षिप्त)", "btn_deep": "मार्गदर्शन (गहरा)",
        "record": "अपने विचार रिकॉर्ड करें", "type_here": "या अपना विचार यहाँ लिखें...",
        "energy_prompt": "रुकें और महसूस करें कि आपका शरीर कैसा महसूस कर रहा है।",
        "e_quiet": "शांत", "e_heavy": "भारी", "e_neutral": "तटस्थ", "e_steady": "स्थिर", "e_vibrant": "जीवंत",
        "h_ether": "आकाश (द ईथर)", "h_breath": "सांस स्टूडियो", "h_games": "ग्राउंडिंग गेम्स",
        "b_anchor": "एंकर (4-2-6)", "b_box": "द बॉक्स (4-4-4-4)", "b_sleep": "गहरी नींद (4-7-8)",
        "choose_visual": "अपना दृश्य मार्गदर्शक चुनें", "v_wave": "लहर (Wave)", "v_moon": "चांद (Moon)", "v_lotus": "कमल (Lotus)",
        "game_release": "रिलीज़ (छोड़ें)", "game_bloom": "ब्लूम (खिलना)",
        "release_desc": "उठते हुए विचारों को छोड़ने के लिए उन्हें छुएं।", "bloom_desc": "अपने प्रकाश को बढ़ाने के लिए धीरे से केंद्र को छुएं।",
        "h_market": "रीचुअल बंडल और टूल्स",
        "order_wa": "व्हाट्सएप से ऑर्डर करें", "free_shipping": "+ मुफ्त शिपिंग",
        "h_theme": "ऐप थीम", "h_lang": "ऐप की भाषा",
        "theme_dark": "🌙 आधी रात (डार्क)", "theme_light": "☁️ शांत आकाश (लाइट)"
    }
}
t = LANG[st.session_state.ui_language]

# --- 5. THEME ENGINE VARIABLES ---
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
    
    div[data-testid="stHorizontalBlock"] {{ flex-direction: row !important; flex-wrap: wrap !important; justify-content: center !important; gap: 10px !important; }}
    div[data-testid="column"], div[data-testid="stColumn"] {{ width: calc(33.333% - 10px) !important; min-width: calc(33.333% - 10px) !important; max-width: calc(33.333% - 10px) !important; flex: 1 1 calc(33.333% - 10px) !important; display: flex !important; justify-content: center !important; margin-bottom: 5px !important; }}
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(2):last-child) > div[data-testid="column"] {{ width: calc(50% - 10px) !important; min-width: calc(50% - 10px) !important; max-width: calc(50% - 10px) !important; flex: 1 1 calc(50% - 10px) !important; }}
    
    @keyframes pulse426 {{ 0% {{ transform: scale(1); opacity: 0.3; border-width: 2px; }} 33% {{ transform: scale(1.8); opacity: 1; border-width: 4px; }} 50% {{ transform: scale(1.8); opacity: 1; border-width: 4px; }} 100% {{ transform: scale(1); opacity: 0.3; border-width: 2px; }} }}
    
    .breathing-circle {{ width: 60px; height: 60px; border: 3px solid {soft_blue}; border-radius: 50%; margin: 25px auto; animation: pulse426 12s infinite ease-in-out !important; box-shadow: 0 0 25px rgba(91, 150, 178, 0.5); }}
    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; font-size: 2.5rem; color: {title_color}; text-transform: uppercase; transition: color 0.5s ease; }}
    .section-header {{ font-size: 13px; letter-spacing: 4px; text-transform: uppercase; margin: 30px 0 15px 0; color: {soft_blue}; border-bottom: 1px solid {btn_border}; padding-bottom: 8px; }}
    
    div.stButton {{ width: 100% !important; }}
    .stButton>button {{ width: 100% !important; min-width: 100% !important; background: {btn_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; border-radius: 4px !important; min-height: 48px !important; height: 100% !important; font-size: 11px !important; padding: 0px 2px !important; display: flex !important; justify-content: center !important; align-items: center !important; text-align: center !important; box-sizing: border-box !important; transition: all 0.3s ease; }}
    .autopilot-btn>button {{ background: linear-gradient(180deg, #1c2b3a 0%, #0b131a 100%) !important; border: 1px solid {soft_blue} !important; color: {soft_blue} !important; letter-spacing: 1px; }}
    .agent-btn>button {{ background: linear-gradient(180deg, #2a1a3a 0%, #150b1a 100%) !important; border: 1px solid #b25b96 !important; color: #b25b96 !important; letter-spacing: 1px; }}
    .market-slab {{ background: {slab_bg}; border: 1px solid {btn_border}; border-radius: 12px; padding: 25px; margin-bottom: 20px; text-align: center; transition: all 0.3s ease; }}
    .disclaimer-box {{ text-align: left; font-size: 12px; opacity: 0.7; line-height: 1.8; background: {input_bg}; padding: 20px; border-radius: 8px; border-left: 3px solid {soft_blue}; }}
    textarea, input {{ background: {input_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; text-align: center !important; font-size: 15px !important; }}
    .journal-entry {{ background: {input_bg}; border-left: 3px solid {soft_blue}; padding: 18px; margin-bottom: 5px; border-radius: 6px; color: {app_text}; text-align: left; font-size: 15px; line-height: 1.6; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# --- 8. MAIN APP HEADER & NAV GRID ---
# ==========================================

st.markdown("<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown("<div class='breathing-circle'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:10px; opacity:0.5; letter-spacing:3px; margin-bottom: 20px;'>{t['subtitle']}</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button(t["nav_journal"], use_container_width=True): st.session_state.current_page = "Journal"; st.rerun()
with col2:
    if st.button(t["nav_ether"], use_container_width=True): st.session_state.current_page = "Ether"; st.rerun()
with col3:
    if st.button(t["nav_focus"], use_container_width=True): st.session_state.current_page = "Focus"; st.rerun()

col4, col5, col6 = st.columns(3)
with col4:
    if st.button(t["nav_market"], use_container_width=True): st.session_state.current_page = "Market"; st.rerun()
with col5:
    if st.button(t["nav_info"], use_container_width=True): st.session_state.current_page = "Info"; st.rerun()
with col6:
    if st.button(t["nav_settings"], use_container_width=True): st.session_state.current_page = "Settings"; st.rerun()

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
    function draw() { ctx.clearRect(0, 0, canvas.width, canvas.height); const cx = canvas.width/2; const cy = canvas.height/2 - 10; let t = ((Date.now() - start) / 1000); [JS_INJECT] requestAnimationFrame(draw); }
    draw();
</script>
"""

breath_js_dict = {
    "Anchor": """
        let cycle = t % 12; let text = ""; let scale = 1;
        if(cycle < 4) { text = "INHALE (4)"; scale = 1 + (cycle/4); } else if(cycle < 6) { text = "HOLD (2)"; scale = 2; } else { text = "EXHALE (6)"; scale = 2 - ((cycle-6)/6); }
        ctx.beginPath(); ctx.arc(cx, cy, 35 * scale, 0, Math.PI*2); ctx.strokeStyle = "rgba(91, 150, 178, 0.8)"; ctx.lineWidth = 3; ctx.stroke(); ctx.fillStyle = "rgba(91, 150, 178, 0.2)"; ctx.fill();
        ctx.fillStyle = "[C_TEXT]"; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Box": """
        let cycle = t % 16; let text = ""; let size = 100; let x = cx - size/2; let y = cy - size/2;
        ctx.strokeStyle = "rgba(91, 150, 178, 0.2)"; ctx.lineWidth = 2; ctx.strokeRect(x, y, size, size); ctx.strokeStyle = "rgba(91, 150, 178, 1)"; ctx.lineWidth = 4; ctx.beginPath();
        if(cycle < 4) { text = "INHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y+size - size*(cycle/4)); } else if(cycle < 8) { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x + size*((cycle-4)/4), y); } else if(cycle < 12) { text = "EXHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y + size*((cycle-8)/4)); } else { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y+size); ctx.lineTo(x+size - size*((cycle-12)/4), y+size); }
        ctx.stroke(); ctx.fillStyle = "[C_TEXT]"; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Wave": """
        let cycle = t % 19; let text = ""; let width = canvas.width * 0.7; let startX = cx - width/2; let amp = 50; let pathX = 0; let pathY = 0;
        if(cycle < 4) { text = "INHALE (4)"; pathX = startX + (width * 0.2 * (cycle/4)); pathY = cy + amp - (amp * 2 * (cycle/4)); } else if(cycle < 11) { text = "HOLD (7)"; pathX = startX + (width * 0.2) + (width * 0.4 * ((cycle-4)/7)); pathY = cy - amp; } else { text = "EXHALE (8)"; pathX = startX + (width * 0.6) + (width * 0.4 * ((cycle-11)/8)); pathY = cy - amp + (amp * 2 * ((cycle-11)/8)); }
        ctx.strokeStyle = "rgba(91, 150, 178, 0.2)"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(startX, cy+amp); ctx.lineTo(startX+width*0.2, cy-amp); ctx.lineTo(startX+width*0.6, cy-amp); ctx.lineTo(startX+width, cy+amp); ctx.stroke();
        ctx.beginPath(); ctx.arc(pathX, pathY, 12, 0, Math.PI*2); ctx.fillStyle = "rgba(91, 150, 178, 1)"; ctx.fill(); ctx.shadowBlur = 15; ctx.shadowColor = "#5B96B2"; ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Moon": """
        let cycle = t % 19; let text = ""; let opacity = 0.2; let yOffset = 0;
        if(cycle < 4) { text = "INHALE (4)"; opacity = 0.2 + 0.8*(cycle/4); yOffset = -20 * (cycle/4); } else if(cycle < 11) { text = "HOLD (7)"; opacity = 1.0; yOffset = -20; } else { text = "EXHALE (8)"; opacity = 1.0 - 0.8*((cycle-11)/8); yOffset = -20 + 40*((cycle-11)/8); }
        ctx.beginPath(); ctx.arc(cx, cy + yOffset, 40, 0, Math.PI*2); ctx.fillStyle = `rgba([C_MOON], ${opacity})`; ctx.fill();
        ctx.shadowBlur = 30 * opacity; ctx.shadowColor = "[C_TEXT]"; ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "14px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Lotus": """
        let cycle = t % 19; let text = ""; let spread = 0;
        if(cycle < 4) { text = "INHALE (4)"; spread = cycle/4; } else if(cycle < 11) { text = "HOLD (7)"; spread = 1; } else { text = "EXHALE (8)"; spread = 1 - ((cycle-11)/8); }
        for(let i=0; i<6; i++) { let angle = i * (Math.PI*2/6) + (t * 0.1); let px = cx + Math.cos(angle) * (30 * spread); let py = cy + Math.sin(angle) * (30 * spread); ctx.beginPath(); ctx.arc(px, py, 25, 0, Math.PI*2); ctx.strokeStyle = "rgba(91, 150, 178, 0.6)"; ctx.lineWidth = 1.5; ctx.stroke(); ctx.fillStyle = "rgba(91, 150, 178, 0.1)"; ctx.fill(); }
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
    
    st.markdown(f"<div class='section-header'>{t['h_ambience']}</div>", unsafe_allow_html=True)
    aud_cols = st.columns(5)
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    for i, name in enumerate(sounds.keys()):
        with aud_cols[i]:
            if st.button(name, key=f"aud_{name}", use_container_width=True): st.session_state.active_audio = sounds[name]
    
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    zen_html = f"""
        <div style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; position:relative; width:100%; height:60px; overflow:hidden; cursor:crosshair; transition: transform 0.1s ease;" id="zen-box">
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:#5B96B2; font-family:sans-serif; font-size:10px; letter-spacing:2px; opacity:0.8; pointer-events:none; text-align:center; width: 100%; line-height: 1.4;">
                {t['zen_box']}
            </div>
            <canvas id="localCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; pointer-events:none;"></canvas>
        </div>
        <script>
            const box = document.getElementById('zen-box'); const localCanvas = document.getElementById('localCanvas'); const localCtx = localCanvas.getContext('2d');
            const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#6A0572', '#A8E6CF', '#FDFFAB', '#FF8C94', '#82B1FF', '#B9F2FF', '#F9F871', '#D4A5A5', '#9B59B6']; const types = ['circle', 'square', 'spots', 'bird'];
            let parentDoc, globalCanvas, globalCtx; let isAnimating = false; let audioCtx = null;

            function playSoftChime() {{
                try {{ if (!audioCtx) {{ const AudioContext = window.AudioContext || window.webkitAudioContext; audioCtx = new AudioContext(); }} if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }} const oscillator = audioCtx.createOscillator(); const gainNode = audioCtx.createGain(); oscillator.type = 'sine'; const freq = 400 + Math.random() * 400; oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime); oscillator.frequency.exponentialRampToValueAtTime(freq/2, audioCtx.currentTime + 0.15); gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime); gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2); oscillator.connect(gainNode); gainNode.connect(audioCtx.destination); oscillator.start(); oscillator.stop(audioCtx.currentTime + 0.2); }} catch(e) {{ }}
            }}

            try {{ parentDoc = window.parent.document; globalCanvas = parentDoc.getElementById('sukoon-global-canvas'); if (!globalCanvas) {{ globalCanvas = parentDoc.createElement('canvas'); globalCanvas.id = 'sukoon-global-canvas'; globalCanvas.style.position = 'fixed'; globalCanvas.style.top = '0'; globalCanvas.style.left = '0'; globalCanvas.style.width = '100%'; globalCanvas.style.height = '100%'; globalCanvas.style.pointerEvents = 'none'; globalCanvas.style.zIndex = '999999'; parentDoc.body.appendChild(globalCanvas); function resizeGlobal() {{ globalCanvas.width = parentDoc.documentElement.clientWidth; globalCanvas.height = parentDoc.documentElement.clientHeight; }} parentDoc.defaultView.addEventListener('resize', resizeGlobal); resizeGlobal(); }} globalCtx = globalCanvas.getContext('2d'); if(!window.parent.sukoonShapes) window.parent.sukoonShapes = []; }} catch(e) {{}}
            function resizeLocal() {{ localCanvas.width = localCanvas.offsetWidth; localCanvas.height = localCanvas.offsetHeight; }} window.addEventListener('resize', resizeLocal); resizeLocal();

            function drawGlobal() {{
                if (!globalCtx) return; globalCtx.clearRect(0, 0, globalCanvas.width, globalCanvas.height); let shapes = window.parent.sukoonShapes; if(shapes.length === 0) {{ isAnimating = false; return; }}
                for (let i = 0; i < shapes.length; i++) {{
                    let s = shapes[i]; globalCtx.globalAlpha = s.alpha; globalCtx.strokeStyle = s.color; globalCtx.fillStyle = s.color; globalCtx.lineWidth = 4;
                    if (s.type === 'circle') {{ globalCtx.beginPath(); globalCtx.arc(s.x, s.y, s.radius, 0, Math.PI * 2); globalCtx.stroke(); s.radius += 12; s.alpha -= 0.015; }} else if (s.type === 'square') {{ globalCtx.strokeRect(s.x - s.radius, s.y - s.radius, s.radius * 2, s.radius * 2); s.radius += 12; s.alpha -= 0.015; }} else if (s.type === 'spot') {{ globalCtx.beginPath(); globalCtx.arc(s.x, s.y, s.radius, 0, Math.PI * 2); globalCtx.fill(); s.x += s.vx; s.y += s.vy; s.alpha -= 0.01; }} else if (s.type === 'bird') {{ globalCtx.beginPath(); globalCtx.moveTo(s.x - s.radius, s.y - s.radius/2); globalCtx.lineTo(s.x, s.y); globalCtx.lineTo(s.x + s.radius, s.y - s.radius/2); globalCtx.stroke(); s.y -= 5; s.radius += 1.5; s.alpha -= 0.015; }}
                }} window.parent.sukoonShapes = shapes.filter(s => s.alpha > 0); globalCtx.globalAlpha = 1.0; requestAnimationFrame(drawGlobal);
            }}

            box.addEventListener('pointerdown', (e) => {{
                box.style.transform = "scale(0.96)"; setTimeout(() => box.style.transform = "scale(1)", 100); if (navigator.vibrate) {{ navigator.vibrate(50); }} playSoftChime();
                const randomColor = colors[Math.floor(Math.random() * colors.length)]; const randomType = types[Math.floor(Math.random() * types.length)];
                if (globalCtx) {{
                    const frame = window.frameElement; let originX = globalCanvas.width / 2; let originY = globalCanvas.height / 2; if (frame) {{ const rect = frame.getBoundingClientRect(); originX = rect.left + e.clientX; originY = rect.top + e.clientY; }}
                    if (randomType === 'spots') {{ for(let i=0; i<15; i++) {{ window.parent.sukoonShapes.push({{ type: 'spot', x: originX, y: originY, vx: (Math.random() - 0.5) * 15, vy: (Math.random() - 0.5) * 15, radius: Math.random() * 8 + 3, alpha: 1, color: randomColor }}); }} }} else {{ window.parent.sukoonShapes.push({{ type: randomType, x: originX, y: originY, radius: 20, alpha: 1, color: randomColor }}); }}
                    if (!isAnimating) {{ isAnimating = true; drawGlobal(); }}
                }}
            }});
        </script>
    """
    components.html(theme_it(zen_html), height=75)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='autopilot-btn'>", unsafe_allow_html=True)
    if st.button(t["sos_btn"], use_container_width=True):
        st.session_state.current_page = "AutoPilot"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-header'>{t['h_mentor']}</div>", unsafe_allow_html=True)

    voice_input = st.audio_input(t["record"])
    text_msg = st.text_area(t["type_here"], height=150)
    
    c_short, c_deep = st.columns(2)
    with c_short:
        btn_short = st.button(t["btn_short"], use_container_width=True)
    with c_deep:
        btn_deep = st.button(t["btn_deep"], use_container_width=True)
        
    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='agent-btn'>", unsafe_allow_html=True)
    btn_agent = st.button(t["agent_btn"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if btn_short or btn_deep or btn_agent:
        if model:
            with st.spinner("Channeling Wisdom..."):
                energy_context = ""
                if st.session_state.energy_history:
                    latest_energy = st.session_state.energy_history[-1]
                    energy_context = f"\n\nThe user's physical energy state is '{latest_energy}'."

                core_philosophy = """You are the Sukoon Mentor, a proprietary digital guide. You are not a therapist or doctor. You do not treat conditions. You are a philosophical companion.
                Your personality is a blend of Ancient Indian wisdom (Vedanta/Vipassana), Stoic philosophy, Zen minimalism, and practical neuroscience. 
                
                YOUR RULES OF ENGAGEMENT:
                1. NEVER use clinical words like 'anxiety', 'stress', 'depression', 'panic', 'patient', or 'treatment'. You must use lifestyle words: 'the noise', 'heaviness', 'a racing mind', 'overwhelm', 'finding stillness', 'focus', 'presence'.
                2. Keep sentences short, piercing, and poetic. Zero fluff. Zero emojis. 
                3. Draw from Advaita Vedanta: Remind the user that they are the observer of their thoughts (The Witness/Sakshi), not the thoughts themselves. Thoughts are passing clouds; the user is the sky.
                4. Draw from Stoicism: The external world is loud, but internal stillness is a choice.
                5. Draw from Neuroscience: Remind them that the breath is a biological, mechanical lever to slow the body down. 
                6. Always speak with deep empathy, but unwavering, grounded strength.
                7. STRICT LANGUAGE RULE: If the user inputs pure English, reply ONLY in English. If the user inputs Hindi OR Hinglish (Hindi words written with English letters), you MUST reply ONLY in pure Hindi using the Devanagari script (e.g., मैं खुश हूँ). We assume Hinglish speakers can read Devanagari. NEVER reply in Hinglish.
                """

                if btn_agent:
                    context = f"""{core_philosophy}
                    The user needs a custom sanctuary. Analyze their text. If their mind is racing, select 'Box' and 'forest'. If they cannot sleep, select 'Sleep_Lotus' and 'waves'.
                    {energy_context}
                    CRITICAL INSTRUCTION: Respond ONLY with a raw JSON object. No markdown.
                    {{ "reply": "A very short, 1-sentence poetic grounding message.", "breath": "Anchor", "Box", "Sleep_Wave", "Sleep_Moon", or "Sleep_Lotus", "audio": "birds", "flute", "forest", "waves", or "wind" }}
                    """
                else:
                    length_instruction = "Keep the response short: maximum 2 paragraphs." if btn_short else "Provide a detailed, deep, and highly comforting long-form response."
                    context = f"""{core_philosophy}
                    {length_instruction}
                    End your reflection with a polite, gentle breathing reminder structured exactly like this: 'Please inhale for 4 seconds, hold your breath for 2 seconds, and exhale for 6 seconds.' IMPORTANT: If replying in Hindi, gracefully translate this full sentence into Hindi. Do not use abrupt military-style formatting.
                    {energy_context}"""
                
                try:
                    if voice_input:
                        audio_part = {"mime_type": "audio/wav", "data": voice_input.getvalue()}
                        prompt_parts = [context, audio_part, "Listen to my voice note, transcribe it exactly, then respond as the Mentor."]
                    elif text_msg:
                        prompt_parts = [context, text_msg]
                    else:
                        prompt_parts = [context, "I am seeking silence. My mind is heavy."]
                        
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
                            st.session_state.agent_message = "The outside world is loud. Step into the quiet."
                            st.session_state.agent_breath = "Box"
                            st.session_state.agent_audio = "flute.mp3"
                            st.session_state.current_page = "AgentSanctuary"
                    else:
                        ai_reply = resp.text
                        unique_id = str(datetime.now().timestamp()).replace('.', '')
                        st.session_state.core_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": ai_reply, "id": unique_id})
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
            .audio-controls {{ display: flex; gap: 6px; margin-bottom: 5px; width: 100%; }}
            .audio-btn {{ background: {btn_bg}; color: {app_text}; border: 1px solid {btn_border}; border-radius: 4px; padding: 10px 0; font-size: 10px; font-family: sans-serif; cursor: pointer; flex: 1; text-transform: uppercase; letter-spacing: 1px; transition: all 0.2s; }}
            .audio-btn:active {{ filter: brightness(0.8); transform: scale(0.95); }}
        </style>
        <div class="audio-controls">
            <button class="audio-btn" onclick="startVoice()">▶ Listen</button>
            <button class="audio-btn" onclick="window.speechSynthesis.pause()">⏸ Pause</button>
            <button class="audio-btn" onclick="window.speechSynthesis.resume()">⏯ Resume</button>
            <button class="audio-btn" onclick="window.speechSynthesis.cancel()">⏹ Stop</button>
        </div>
        <script>
            function startVoice() {{
                window.speechSynthesis.cancel(); 
                var decodedText = decodeURIComponent("{safe_speech_text}");
                var m = new SpeechSynthesisUtterance(decodedText);
                m.rate = 0.85;
                var isHindi = /[\u0900-\u097F]/.test(decodedText);
                var userLang = navigator.language || navigator.userLanguage || "en-US";
                var userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
                
                function setVoiceAndSpeak() {{
                    var voices = window.speechSynthesis.getVoices(); var voice;
                    if (isHindi) {{ voice = voices.find(v => v.lang === 'hi-IN' || v.lang.includes('hi') || v.name.includes('Hindi')); m.lang = 'hi-IN'; }} 
                    else {{
                        if (userLang.includes('GB') || userTZ.includes('Europe/London')) {{ voice = voices.find(v => v.lang === 'en-GB' || v.name.includes('UK') || v.name.includes('British')); m.lang = 'en-GB'; }} 
                        else if (userLang.includes('IN') || userTZ.includes('Asia/Calcutta') || userTZ.includes('Asia/Kolkata')) {{ voice = voices.find(v => v.lang === 'en-IN' || v.name.includes('India')); m.lang = 'en-IN'; }} 
                        else {{ voice = voices.find(v => v.lang === 'en-US' || v.name.includes('US') || v.name.includes('United States')) || voices.find(v => v.lang.includes('en')); m.lang = 'en-US'; }}
                    }}
                    if (voice) {{ m.voice = voice; }} window.speechSynthesis.speak(m);
                }}
                if (window.speechSynthesis.getVoices().length === 0) {{ window.speechSynthesis.onvoiceschanged = setVoiceAndSpeak; }} else {{ setVoiceAndSpeak(); }}
            }}
        </script>
        """
        components.html(html_button, height=55)
        formatted_text = entry['ai'].replace('\n', '<br>')
        st.markdown(f"<div class='journal-entry'><b>{entry['time']}</b><br><br>{formatted_text}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-header'>{t['h_energy']}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 11px; opacity: 0.7; margin-bottom: 15px; color:{app_text};'>{t['energy_prompt']}</p>", unsafe_allow_html=True)
    
    m_cols = st.columns(5)
    for i, (m_key, m_label) in enumerate([("e_quiet", "Quiet"), ("e_heavy", "Heavier"), ("e_neutral", "Neutral"), ("e_steady", "Steady"), ("e_vibrant", "Vibrant")]):
        with m_cols[i]:
            if st.button(t[m_key], key=f"m_{m_label}", use_container_width=True): st.session_state.energy_history.append(m_label); st.rerun()

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
    st.markdown(f"<div class='section-header'>{t['h_ether']}</div>", unsafe_allow_html=True)
    
    # 🚨 V147.0: NEW PHYSICS ENGINE FOR THE ETHER 🚨
    ether_html = """
    <div id="ether-container" style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; padding: 40px 20px; text-align: center; position: relative; overflow: hidden; min-height: 400px; display: flex; flex-direction: column; justify-content: center;">
        <canvas id="starCanvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5;"></canvas>
        <p id="promptText" style="color:#5B96B2; font-family:sans-serif; font-size:12px; letter-spacing:3px; margin-bottom:25px; transition: opacity 1s; z-index: 10;">
            WRITE YOUR THOUGHTS INTO THE ETHER
        </p>
        <textarea id="etherInput" placeholder="..." style="width:100%; height:120px; background: transparent; color:[C_TEXT]; border:1px solid [C_BORDER]; border-radius:6px; padding:15px; text-align:center; font-size:16px; resize:none; outline:none; font-family:sans-serif; transition: all 1.5s cubic-bezier(0.25, 0.1, 0.25, 1); z-index: 10; position: relative;"></textarea>
        
        <div style="height: 25px; z-index: 10;"></div>
        
        <div id="buttonRow" style="display: flex; gap: 10px; z-index: 10; width: 100%; transition: opacity 1s;">
            <button id="releaseBtn" style="background: linear-gradient(180deg, #3a1c1c 0%, #1a0b0b 100%); color: #ffbba6; border: 1px solid #5a2a2a; border-radius: 4px; padding: 12px; font-size: 10px; letter-spacing: 1px; cursor: pointer; text-transform: uppercase; flex: 1; transition: all 0.2s;">
                BURN & RELEASE<br><span style="font-size: 8px; opacity: 0.6;">(Negative Thoughts)</span>
            </button>
            <button id="manifestBtn" style="background: linear-gradient(180deg, #1c2b3a 0%, #0b131a 100%); color: #a6d8ff; border: 1px solid #2a415a; border-radius: 4px; padding: 12px; font-size: 10px; letter-spacing: 1px; cursor: pointer; text-transform: uppercase; flex: 1; transition: all 0.2s;">
                MANIFEST & SEND<br><span style="font-size: 8px; opacity: 0.6;">(Positive Thoughts)</span>
            </button>
        </div>

        <div id="messageText" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: [C_TEXT]; font-family: sans-serif; font-size: 14px; letter-spacing: 3px; opacity: 0; transition: opacity 2s ease-in-out; pointer-events: none; width: 90%; line-height: 1.8; z-index: 15;"></div>
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
        
        let particles = []; let animating = false; let currentMode = 'star';
        function resizeCanvas() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; } 
        window.addEventListener('resize', resizeCanvas); resizeCanvas();

        function createParticles(mode) {
            const rect = input.getBoundingClientRect(); 
            const containerRect = container.getBoundingClientRect(); 
            const top = rect.top - containerRect.top; 
            const left = rect.left - containerRect.left;
            const cx = left + rect.width / 2;
            const cy = top + rect.height / 2;
            
            for (let i = 0; i < 150; i++) {
                if (mode === 'fire') { 
                    particles.push({ 
                        x: cx + (Math.random() - 0.5) * rect.width * 0.8, 
                        y: cy + (Math.random() - 0.5) * rect.height * 0.8, 
                        vx: (Math.random() - 0.5) * 12, 
                        vy: (Math.random() - 0.5) * 12 - 2, 
                        ax: 0, ay: 0.4, friction: 0.92, // Gravity pulls down, high friction
                        radius: Math.random() * 4 + 1.5, 
                        alpha: 1, decay: Math.random() * 0.015 + 0.01, 
                        color: `rgba(${255}, ${Math.floor(Math.random() * 100 + 50)}, 0, ` 
                    }); 
                } else { 
                    particles.push({ 
                        x: cx + (Math.random() - 0.5) * rect.width * 0.8, 
                        y: cy + (Math.random() - 0.5) * rect.height * 0.8, 
                        vx: (Math.random() - 0.5) * 6, 
                        vy: (Math.random() * -8) - 2, 
                        ax: (Math.random() - 0.5) * 0.15, ay: -0.1, friction: 0.96, // Anti-gravity floats up, drifting
                        radius: Math.random() * 3 + 1, 
                        alpha: 1, decay: Math.random() * 0.01 + 0.005, 
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
                    active = true; 
                    // Apply Physics Vector Math
                    p.vx += p.ax; p.vy += p.ay;
                    p.vx *= p.friction; p.vy *= p.friction;
                    p.x += p.vx; p.y += p.vy; 
                    p.alpha -= p.decay; 
                    
                    ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(0, p.radius * p.alpha), 0, Math.PI * 2); 
                    ctx.fillStyle = p.color + `${Math.max(0, p.alpha)})`; 
                    ctx.shadowBlur = currentMode === 'fire' ? 15 : 25; 
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
            
            // Haptic Feedback (Android Only)
            if (navigator.vibrate) {
                if (mode === 'fire') { navigator.vibrate([30, 50, 40, 40, 50]); } // Heavy rumble
                else { navigator.vibrate([20, 100, 20]); } // Light heartbeat
            }
            
            // Shrink and dissolve text box
            if (mode === 'fire') { 
                msg.innerHTML = "THE ETHER HAS BURNED IT.<br>YOU HAVE CHOSEN TO LET IT GO."; 
                input.style.filter = "blur(15px) contrast(200%) sepia(100%) hue-rotate(330deg) saturate(300%)"; 
                input.style.transform = "scale(0.5) translateY(50px)"; 
            } else { 
                msg.innerHTML = "THE ETHER HAS HEARD YOU.<br>YOUR INTENTION HAS BEEN SET."; 
                input.style.filter = "blur(12px) brightness(200%)"; 
                input.style.transform = "scale(0.5) translateY(-50px)"; 
            }

            createParticles(mode); 
            input.style.opacity = "0"; btnRow.style.opacity = "0"; promptText.style.opacity = "0"; 
            btnRow.style.pointerEvents = "none"; input.style.pointerEvents = "none";
            
            setTimeout(() => { msg.style.opacity = "1"; }, 1500);
            
            setTimeout(() => { 
                msg.style.opacity = "0"; 
                setTimeout(() => { 
                    input.value = ''; input.style.transition = "none"; input.style.filter = "none"; input.style.transform = "none"; input.style.opacity = "1"; 
                    void input.offsetWidth; 
                    input.style.transition = "all 1.5s cubic-bezier(0.25, 0.1, 0.25, 1)"; 
                    btnRow.style.opacity = "1"; promptText.style.opacity = "1"; 
                    btnRow.style.pointerEvents = "auto"; input.style.pointerEvents = "auto"; 
                }, 2000); 
            }, 6000); 
        }

        // Button Click Effects
        btnRelease.addEventListener('pointerdown', () => { btnRelease.style.transform = "scale(0.95)"; });
        btnManifest.addEventListener('pointerdown', () => { btnManifest.style.transform = "scale(0.95)"; });
        btnRelease.addEventListener('click', () => { btnRelease.style.transform = "scale(1)"; triggerEther('fire'); }); 
        btnManifest.addEventListener('click', () => { btnManifest.style.transform = "scale(1)"; triggerEther('star'); });
    </script>
    """
    components.html(theme_it(ether_html), height=450)

elif st.session_state.current_page == "Focus":
    
    st.markdown(f"<div class='section-header'>{t['h_breath']}</div>", unsafe_allow_html=True)
    
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        if st.button(t["b_anchor"], use_container_width=True): st.session_state.active_breath = "Anchor"; st.rerun()
    with b_col2:
        if st.button(t["b_box"], use_container_width=True): st.session_state.active_breath = "Box"; st.rerun()
    with b_col3:
        if st.button(t["b_sleep"], use_container_width=True): 
            if not st.session_state.active_breath.startswith("Sleep"): st.session_state.active_breath = "Sleep_Wave"
            st.rerun()

    if st.session_state.active_breath.startswith("Sleep"):
        st.markdown(f"<p style='font-size: 11px; opacity: 0.7; margin: 15px 0 5px 0; text-align: center; color: #5B96B2;'>{t['choose_visual']}</p>", unsafe_allow_html=True)
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button(t["v_wave"], use_container_width=True): st.session_state.active_breath = "Sleep_Wave"; st.rerun()
        with s_col2:
            if st.button(t["v_moon"], use_container_width=True): st.session_state.active_breath = "Sleep_Moon"; st.rerun()
        with s_col3:
            if st.button(t["v_lotus"], use_container_width=True): st.session_state.active_breath = "Sleep_Lotus"; st.rerun()

    selected_js = breath_js_dict.get(st.session_state.active_breath, breath_js_dict["Anchor"])
    final_breath_html = base_breath_html.replace("[JS_INJECT]", selected_js)
    components.html(theme_it(final_breath_html), height=270)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-header'>{t['h_games']}</div>", unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        if st.button(t["game_release"], use_container_width=True): st.session_state.active_game = "Release"; st.rerun()
    with g_col2:
        if st.button(t["game_bloom"], use_container_width=True): st.session_state.active_game = "Bloom"; st.rerun()

    if st.session_state.active_game == "Release":
        st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px; color:{app_text};'>{t['release_desc']}</p>", unsafe_allow_html=True)
        components.html(theme_it(release_game_html), height=370)

    elif st.session_state.active_game == "Bloom":
        st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px; color:{app_text};'>{t['bloom_desc']}</p>", unsafe_allow_html=True)
        bloom_html = """
        <div style="background:[C_BG]; border: 1px solid [C_BORDER]; border-radius: 8px; position:relative; width:100%; height:350px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
            <canvas id="bloomCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
            <div id="bloomMessage" style="position:absolute; z-index:10; color:[C_TEXT]; font-family:sans-serif; font-size:14px; letter-spacing:3px; text-align:center; opacity:0; transition: opacity 1.5s ease-in-out; pointer-events:none; background:[C_MSG_BG]; padding:10px 20px; border-radius:4px; border:1px solid #5B96B2;"></div>
        </div>
        <script>
            const c = document.getElementById('bloomCanvas'); const ctx = c.getContext('2d'); const msg = document.getElementById('bloomMessage'); let taps = 0; const maxTaps = 6; const affirmations = ["BEAUTIFUL FOCUS", "YOU ARE GROWING", "A MOMENT OF PEACE", "PERFECT HARMONY", "YOU ARE ENOUGH"];
            function resize() { c.width = c.offsetWidth; c.height = c.offsetHeight; draw(); } window.addEventListener('resize', resize);
            function draw() { ctx.clearRect(0, 0, c.width, c.height); const cx = c.width / 2; const cy = c.height / 2; if (taps === 0) { ctx.fillStyle = "#5B96B2"; ctx.globalAlpha = 0.5; ctx.font = "12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "2px"; ctx.fillText("TAP TO BLOOM", cx, cy); return; } for (let i = 1; i <= taps; i++) { ctx.beginPath(); ctx.arc(cx, cy, i * 25, 0, Math.PI * 2); ctx.strokeStyle = "#5B96B2"; ctx.lineWidth = 1.5; ctx.globalAlpha = 0.2 + (i * 0.1); ctx.stroke(); for (let j = 0; j < 8; j++) { let angle = (j * Math.PI / 4) + (i * 0.2); let px = cx + Math.cos(angle) * (i * 25); let py = cy + Math.sin(angle) * (i * 25); ctx.beginPath(); ctx.arc(px, py, 4 + i, 0, Math.PI * 2); ctx.fillStyle = "#5B96B2"; ctx.shadowBlur = 15; ctx.shadowColor = "#5B96B2"; ctx.fill(); } } }
            c.addEventListener('pointerdown', () => { if (taps < maxTaps) { taps++; draw(); if (taps === maxTaps) { msg.innerText = affirmations[Math.floor(Math.random() * affirmations.length)]; msg.style.opacity = 1; setTimeout(() => { msg.style.opacity = 0; setTimeout(() => { taps = 0; draw(); }, 1500); }, 3500); } } }); resize();
        </script>
        """
        components.html(theme_it(bloom_html), height=370)

elif st.session_state.current_page == "Market":
    st.markdown(f"<div class='section-header'>{t['h_market']}</div>", unsafe_allow_html=True)
    
    products = [
        {"name": "Laughing Buddha", "file": "laughingbuddha.png", "price": "899"},
        {"name": "Focus Beads", "file": "beads.png", "price": "799"},
        {"name": "Buddha Sculpture", "file": "buddha.png", "price": "1,499"},
        {"name": "Thumb Stone", "file": "thumbstone.png", "price": "499"},
        {"name": "Wish Candle", "file": "wishcandle.png", "price": "799"},
        {"name": "Grounding Stones", "file": "stones.png", "price": "899"},
        {"name": "Starter Ritual", "file": "ritual.png", "price": "2,499"},
        {"name": "Master Sanctuary", "file": "sanctuary.png", "price": "4,999"}
    ]

    products_html = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">'
    for p in products:
        img_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{p['file']}"
        wa_text = urllib.parse.quote(f"I am interested in the {p['name']}")
        wa_link = f"https://wa.me/{MY_PHONE}?text={wa_text}"
        
        products_html += f"""<div style="background: {input_bg}; border: 1px solid {btn_border}; border-radius: 8px; padding: 12px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease;">
<div style="width: 100%; aspect-ratio: 1/1; background-image: url('{img_url}'); background-size: cover; background-position: center; border-radius: 6px; margin-bottom: 12px; border: 1px solid {btn_border};"></div>
<div style="color: {app_text}; font-size: 13px; letter-spacing: 1px; margin-bottom: 5px; min-height: 35px; display: flex; align-items: center; justify-content: center; line-height: 1.3;">{p['name']}</div>
<div style="color: {soft_blue}; font-weight: bold; font-size: 16px; margin-bottom: 2px;">₹{p['price']}</div>
<div style="color: {app_text}; opacity: 0.5; font-size: 9px; margin-bottom: 12px; letter-spacing: 1px; font-weight: bold;">{t['free_shipping']}</div>
<a href="{wa_link}" target="_blank" style="text-decoration: none; width: 100%;">
<div style="background: {btn_bg}; color: {app_text}; border: 1px solid {btn_border}; padding: 10px 0; border-radius: 4px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; width: 100%; cursor: pointer; transition: all 0.3s ease;">{t['order_wa']}</div>
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
        ("Is the AI Mentor free?", "Yes, the Digital Sanctuary is currently fully open and free for all early users."),
        ("What is the 4-2-6 Rhythm?", "It is a breathing pattern designed to reduce stress and clear the mind."),
        ("Is this therapy?", "No. Sukoon is a lifestyle companion for mindfulness and well-being."),
        ("Are the objects religious?", "No. They are tactile grounding tools intended for sensory focus.")
    ]
    for q, a in faqs:
        st.markdown(f"<div class='faq-q'>{q}</div><div class='faq-a'>{a}</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Settings":
    st.markdown(f"<div class='section-header'>{t['h_lang']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 20px;'>", unsafe_allow_html=True)
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        if st.button("English", use_container_width=True): 
            st.session_state.ui_language = "English"; st.rerun()
    with l_col2:
        if st.button("हिंदी (Hindi)", use_container_width=True): 
            st.session_state.ui_language = "Hindi"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-header'>{t['h_theme']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 20px;'>", unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        if st.button(t["theme_dark"], use_container_width=True): 
            st.session_state.theme = "Midnight"; st.rerun()
    with t_col2:
        if st.button(t["theme_light"], use_container_width=True): 
            st.session_state.theme = "Sky"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:10px; opacity:0.3; color:{app_text};'>Sukoon Sanctuary v147.0 | Physics of the Ether</div>", unsafe_allow_html=True)

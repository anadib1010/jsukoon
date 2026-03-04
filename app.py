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

# Ensure valid theme
valid_themes = ["The Void", "Sage Sanctuary", "Terracotta Earth", "Social Blue", "First Light", "Sea Glass", 
                "Deep Sage", "Ocean Blue", "Ocean Green", "Red Amber", "Maroon", "Twilight Blue", "Liquid Gold"]
if "theme" not in st.session_state or st.session_state.theme not in valid_themes: 
    st.session_state.theme = "The Void"
    
if "ui_language" not in st.session_state: st.session_state.ui_language = "English"

# VIP Unlocks
if "unlocked_mala" not in st.session_state: st.session_state.unlocked_mala = False
if "unlocked_flame" not in st.session_state: st.session_state.unlocked_flame = False
if "unlocked_nirvana" not in st.session_state: st.session_state.unlocked_nirvana = False

# --- 4. ZERO-COST UI DICTIONARY ---
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
        "th_light": "LIGHT SANCTUARY", "th_dark": "DEEP SANCTUARY",
        "t_void": "The Void", "t_sage_l": "Sage Sanctuary", "t_terra": "Terracotta",
        "t_abyss": "Social Blue", "t_dawn": "First Light", "t_sea": "Sea Glass",
        "t_sage_d": "Deep Sage", "t_oblue": "Ocean Blue", "t_ogreen": "Ocean Green",
        "t_amber": "Red Amber", "t_maroon": "Maroon", "t_tblue": "Twilight Blue",
        "t_gold": "Liquid Gold (VIP)", "b_flame": "The Flame (VIP)", "game_mala": "Haptic Mala (VIP)",
        "vault_h": "SANCTUARY VAULT", "vault_p": "Have a Sanctuary Code?"
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
        "th_light": "हल्का अभयारण्य (Light)", "th_dark": "गहरा अभयारण्य (Deep)",
        "t_void": "शून्य (The Void)", "t_sage_l": "सेज वन (Sage)", "t_terra": "मिट्टी (Terracotta)",
        "t_abyss": "सोशल ब्लू (FB Blue)", "t_dawn": "पहली किरण (Dawn)", "t_sea": "समुद्री कांच (Sea Glass)",
        "t_sage_d": "गहरा सेज (Deep Sage)", "t_oblue": "समुद्री नीला (Blue)", "t_ogreen": "समुद्री हरा (Green)",
        "t_amber": "लाल एम्बर (Amber)", "t_maroon": "मैरून (Maroon)", "t_tblue": "गहरा नीला (Twilight)",
        "t_gold": "तरल सोना (VIP)", "b_flame": "लौ (VIP)", "game_mala": "स्पर्श माला (VIP)",
        "vault_h": "गुप्त तिजोरी", "vault_p": "क्या आपके पास कोड है?"
    }
}
t = LANG[st.session_state.ui_language]

# --- 5. THE ULTIMATE 13-THEME ENGINE ---
# LIGHT THEMES
if st.session_state.theme == "First Light":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#FDFBF7", "#4A4A4A", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.05)", "#D4A373", "212,163,115"
elif st.session_state.theme == "Sea Glass":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#E5EDF0", "#4A5D66", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#7A9EA8", "122,158,168"
elif st.session_state.theme == "Terracotta Earth":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#F2ECE7", "#5C4033", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#B07D62", "176,125,98"
elif st.session_state.theme == "Sage Sanctuary":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#E3E7E0", "#3E4735", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#6B765F", "107,118,95"

# DEEP THEMES
elif st.session_state.theme == "The Void":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#000000", "#E0E0E0", "rgba(20,20,20,0.6)", "rgba(255,255,255,0.08)", "#888888", "136,136,136"
elif st.session_state.theme == "Social Blue":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#1877F2", "#FFFFFF", "rgba(255,255,255,0.15)", "rgba(255,255,255,0.3)", "#FFFFFF", "255,255,255"
elif st.session_state.theme == "Deep Sage":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#1E2720", "#D3DDD0", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#7B9075", "123,144,117"
elif st.session_state.theme == "Ocean Blue":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#122840", "#CFE2F3", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#5D93C4", "93,147,196"
elif st.session_state.theme == "Ocean Green":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#0F2926", "#CDE3DF", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#4A9D93", "74,157,147"
elif st.session_state.theme == "Red Amber":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#38180D", "#F3D9CE", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#B35835", "179,88,53"
elif st.session_state.theme == "Maroon":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#2A0E13", "#EFD1D6", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#9B3D4F", "155,61,79"
elif st.session_state.theme == "Twilight Blue":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#181830", "#D6D5F2", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#726FBA", "114,111,186"

# VIP
elif st.session_state.theme == "Liquid Gold":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#000000", "#F5E6BA", "rgba(212,175,55,0.08)", "rgba(212,175,55,0.25)", "#D4AF37", "212,175,55"
else:
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#000000", "#E0E0E0", "rgba(20,20,20,0.6)", "rgba(255,255,255,0.08)", "#888888", "136,136,136"

def theme_it(html_str):
    return html_str.replace("[C_BG]", "transparent").replace("[C_GLASS]", glass_bg).replace("[C_BORDER]", btn_border).replace("[C_TEXT]", app_text).replace("[C_ACCENT]", c_accent).replace("[C_RGB]", c_rgb)

# --- 6. THE BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

# --- 7. MINIMALIST COMMAND CENTER CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    .stApp {{ background-color: {app_bg} !important; color: {app_text} !important; font-family: 'Inter', sans-serif; transition: background-color 0.8s ease; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 3.5rem !important; text-align: center !important; overflow-x: hidden !important; }}
    div[data-testid="stHorizontalBlock"] {{ flex-direction: row !important; flex-wrap: wrap !important; justify-content: center !important; gap: 8px !important; }}
    div[data-testid="column"], div[data-testid="stColumn"] {{ width: calc(33.333% - 8px) !important; min-width: calc(33.333% - 8px) !important; max-width: calc(33.333% - 8px) !important; flex: 1 1 calc(33.333% - 8px) !important; display: flex !important; justify-content: center !important; margin-bottom: 5px !important; }}
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(2):last-child) > div[data-testid="column"] {{ width: calc(50% - 8px) !important; min-width: calc(50% - 8px) !important; max-width: calc(50% - 8px) !important; flex: 1 1 calc(50% - 8px) !important; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 0.2; border-width: 1px; }} 50% {{ transform: scale(1.6); opacity: 0.8; border-width: 3px; }} 100% {{ transform: scale(1); opacity: 0.2; border-width: 1px; }} }}
    .breathing-circle {{ width: 50px; height: 50px; border: 2px solid {c_accent}; border-radius: 50%; margin: 15px auto 25px auto; animation: pulse 12s infinite ease-in-out !important; box-shadow: 0 0 20px rgba({c_rgb}, 0.3); transition: all 0.8s ease; }}
    .main-title {{ text-align: center; letter-spacing: 14px; font-weight: 300; font-size: 2.2rem; color: {app_text}; text-transform: uppercase; margin-bottom: 5px; }}
    .section-header {{ font-size: 11px; letter-spacing: 5px; font-weight: 500; text-transform: uppercase; margin: 35px 0 15px 0; color: {c_accent}; padding-bottom: 8px; opacity: 0.8; }}
    .theme-group-header {{ font-size: 9px; letter-spacing: 3px; font-weight: 400; text-transform: uppercase; margin: 20px 0 10px 0; color: {app_text}; opacity: 0.5; text-align: left; padding-left: 5px; }}
    div.stButton {{ width: 100% !important; }}
    .stButton>button {{ width: 100% !important; min-width: 100% !important; background: {glass_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; border-radius: 30px !important; backdrop-filter: blur(12px) !important; -webkit-backdrop-filter: blur(12px) !important; min-height: 44px !important; height: 100% !important; font-size: 11px !important; font-weight: 400 !important; letter-spacing: 1px !important; display: flex !important; justify-content: center !important; align-items: center !important; text-align: center !important; transition: all 0.3s ease; }}
    .stButton>button:active {{ transform: scale(0.96); opacity: 0.7; }}
    .autopilot-btn>button {{ border: 1px solid rgba({c_rgb}, 0.5) !important; color: {c_accent} !important; letter-spacing: 2px; font-weight: 500 !important; }}
    .agent-btn>button {{ border: 1px solid rgba({c_rgb}, 0.5) !important; color: {c_accent} !important; letter-spacing: 2px; font-weight: 500 !important; }}
    .market-slab {{ background: {glass_bg}; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid {btn_border}; padding: 20px; margin-bottom: 15px; text-align: center; transition: all 0.5s ease; }}
    .disclaimer-box {{ text-align: left; font-size: 11px; opacity: 0.6; line-height: 1.8; background: transparent; padding: 15px; border-radius: 12px; border: 1px solid {btn_border}; }}
    textarea, input {{ background: {glass_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; border-radius: 16px !important; backdrop-filter: blur(12px) !important; text-align: center !important; font-size: 14px !important; font-weight: 300 !important; font-family: 'Inter', sans-serif !important; padding: 15px !important; box-shadow: none !important; }}
    textarea:focus, input:focus {{ border-color: {c_accent} !important; outline: none !important; }}
    .journal-entry {{ background: {glass_bg}; backdrop-filter: blur(12px); border-left: 2px solid {c_accent}; padding: 20px; margin-bottom: 10px; border-radius: 12px; color: {app_text}; text-align: left; font-size: 14px; line-height: 1.6; font-weight: 300; border-top: 1px solid {btn_border}; border-right: 1px solid {btn_border}; border-bottom: 1px solid {btn_border}; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# --- 8. MAIN APP HEADER & NAV GRID ---
# ==========================================

st.markdown("<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown("<div class='breathing-circle'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:9px; opacity:0.5; letter-spacing:4px; margin-bottom: 25px; text-transform: uppercase;'>{t['subtitle']}</div>", unsafe_allow_html=True)

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

st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

# --- REUSABLE HTML COMPONENTS ---
base_breath_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:260px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
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
        ctx.beginPath(); ctx.arc(cx, cy, 35 * scale, 0, Math.PI*2); ctx.strokeStyle = "rgba([C_RGB], 0.6)"; ctx.lineWidth = 2; ctx.stroke(); ctx.fillStyle = "rgba([C_RGB], 0.1)"; ctx.fill();
        ctx.fillStyle = "[C_TEXT]"; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Box": """
        let cycle = t % 16; let text = ""; let size = 100; let x = cx - size/2; let y = cy - size/2;
        ctx.strokeStyle = "rgba([C_RGB], 0.15)"; ctx.lineWidth = 1; ctx.strokeRect(x, y, size, size); ctx.strokeStyle = "rgba([C_RGB], 0.8)"; ctx.lineWidth = 3; ctx.beginPath();
        if(cycle < 4) { text = "INHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y+size - size*(cycle/4)); } else if(cycle < 8) { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x + size*((cycle-4)/4), y); } else if(cycle < 12) { text = "EXHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y + size*((cycle-8)/4)); } else { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y+size); ctx.lineTo(x+size - size*((cycle-12)/4), y+size); }
        ctx.stroke(); ctx.fillStyle = "[C_TEXT]"; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Wave": """
        let cycle = t % 19; let text = ""; let width = canvas.width * 0.7; let startX = cx - width/2; let amp = 50; let pathX = 0; let pathY = 0;
        if(cycle < 4) { text = "INHALE (4)"; pathX = startX + (width * 0.2 * (cycle/4)); pathY = cy + amp - (amp * 2 * (cycle/4)); } else if(cycle < 11) { text = "HOLD (7)"; pathX = startX + (width * 0.2) + (width * 0.4 * ((cycle-4)/7)); pathY = cy - amp; } else { text = "EXHALE (8)"; pathX = startX + (width * 0.6) + (width * 0.4 * ((cycle-11)/8)); pathY = cy - amp + (amp * 2 * ((cycle-11)/8)); }
        ctx.strokeStyle = "rgba([C_RGB], 0.15)"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(startX, cy+amp); ctx.lineTo(startX+width*0.2, cy-amp); ctx.lineTo(startX+width*0.6

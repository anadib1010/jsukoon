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
if "active_game" not in st.session_state: st.session_state.active_game = "Convergence"
if "active_breath" not in st.session_state: st.session_state.active_breath = "Anchor"
if "agent_audio" not in st.session_state: st.session_state.agent_audio = "flute.mp3"
if "agent_breath" not in st.session_state: st.session_state.agent_breath = "Box"
if "agent_message" not in st.session_state: st.session_state.agent_message = "I have prepared this space for you."

# Ensure valid theme
valid_themes = ["The Void", "Sage Sanctuary", "Terracotta Earth", "Social Blue", "First Light", "Sea Glass", 
                "Deep Sage", "Ocean Blue", "Ocean Green", "Red Amber", "Maroon", "Twilight Blue", 
                "Champagne Gold", "Pink Champagne", "Liquid Gold"]

# ==========================================
# 🚨 DYNAMIC CIRCADIAN DEFAULT INJECTION 🚨
# ==========================================
if "theme" not in st.session_state or st.session_state.theme not in valid_themes: 
    current_hour = datetime.now().hour
    is_daytime = 6 <= current_hour < 18  # 6 AM to 6 PM
    # Pink Champagne for Day (Warmth), The Void for Night (Melatonin Protection)
    st.session_state.theme = "Pink Champagne" if is_daytime else "The Void"
    
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
        "game_release": "The Release", "game_bloom": "The Bloom", "game_convergence": "The Convergence",
        "release_desc": "Tap the rising thoughts to release them.", "bloom_desc": "Tap the center slowly to grow your light.",
        "convergence_desc": "Your mind is the swarm. Hold to overpower the resistance.",
        "h_market": "RITUAL BUNDLES & TOOLS",
        "order_wa": "ORDER VIA WA", "free_shipping": "+ FREE SHIPPING",
        "h_theme": "APP THEME", "h_lang": "UI LANGUAGE",
        "th_light": "LIGHT SANCTUARY", "th_dark": "DEEP SANCTUARY",
        "t_void": "The Void", "t_sage_l": "Sage Sanctuary", "t_terra": "Terracotta",
        "t_abyss": "Social Blue", "t_dawn": "First Light", "t_sea": "Sea Glass",
        "t_champagne": "Champagne Gold", "t_pink_champ": "Pink Champagne",
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
        "game_release": "रिलीज़ (छोड़ें)", "game_bloom": "ब्लूम (खिलना)", "game_convergence": "कन्वर्जेंस (संकेंद्रण)",
        "release_desc": "उठते हुए विचारों को छोड़ने के लिए उन्हें छुएं।", "bloom_desc": "अपने प्रकाश को बढ़ाने के लिए धीरे से केंद्र को छुएं।",
        "convergence_desc": "आपका मन यह झुंड है। इसे शांत करने के लिए स्क्रीन को दबाकर रखें।",
        "h_market": "रीचुअल बंडल और टूल्स",
        "order_wa": "व्हाट्सएप से ऑर्डर करें", "free_shipping": "+ मुफ्त शिपिंग",
        "h_theme": "ऐप थीम", "h_lang": "ऐप की भाषा",
        "th_light": "हल्का अभयारण्य (Light)", "th_dark": "गहरा अभयारण्य (Deep)",
        "t_void": "शून्य (The Void)", "t_sage_l": "सेज वन (Sage)", "t_terra": "मिट्टी (Terracotta)",
        "t_abyss": "सोशल ब्लू (FB Blue)", "t_dawn": "पहली किरण (Dawn)", "t_sea": "समुद्री कांच (Sea Glass)",
        "t_champagne": "शैंपेन गोल्ड (Champagne)", "t_pink_champ": "पिंक शैंपेन (Pink)",
        "t_sage_d": "गहरा सेज (Deep Sage)", "t_oblue": "समुद्री नीला (Blue)", "t_ogreen": "समुद्री हरा (Green)",
        "t_amber": "लाल एम्बर (Amber)", "t_maroon": "मैरून (Maroon)", "t_tblue": "गहरा नीला (Twilight)",
        "t_gold": "तरल सोना (VIP)", "b_flame": "लौ (VIP)", "game_mala": "स्पर्श माला (VIP)",
        "vault_h": "गुप्त तिजोरी", "vault_p": "क्या आपके पास कोड है?"
    }
}
t = LANG[st.session_state.ui_language]

# --- 5. THE ULTIMATE 14-THEME ENGINE ---
if st.session_state.theme == "First Light":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#FDFBF7", "#4A4A4A", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.05)", "#D4A373", "212,163,115"
elif st.session_state.theme == "Sea Glass":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#E5EDF0", "#4A5D66", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#7A9EA8", "122,158,168"
elif st.session_state.theme == "Terracotta Earth":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#F2ECE7", "#5C4033", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#B07D62", "176,125,98"
elif st.session_state.theme == "Sage Sanctuary":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#E3E7E0", "#3E4735", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#6B765F", "107,118,95"
elif st.session_state.theme == "Champagne Gold":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#FBF5ED", "#4A4036", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.06)", "#C5A059", "197,160,89"
elif st.session_state.theme == "Pink Champagne":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#F8DECD", "#5A3A42", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.06)", "#C88A8E", "200,138,142"
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
elif st.session_state.

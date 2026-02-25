import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#5B96B2" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "theme" not in st.session_state: st.session_state.theme = "Midnight"
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. THEME COLORS ---
bg, txt = "#121212", "#E0E0E0"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. THE HARD-CENTER OVERRIDE CSS ---
st.markdown(f"""
    <style>
    /* 1. Force the entire screen container to center EVERYTHING */
    .stApp {{ 
        background-color: {bg} !important; 
        color: {txt} !important; 
    }}
    
    .block-container {{
        max-width: 600px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }}

    /* 2. Title & Headers - Full Width Centering */
    .main-title {{
        letter-spacing: 12px; font-weight: 200; 
        margin-bottom: 25px; font-size: 2.8rem; color: #FFFFFF;
        text-transform: uppercase; width: 100%; text-align: center;
    }}

    .section-header {{
        font-size: 16px !important; font-weight: 400 !important; letter-spacing: 4px !important;
        text-transform: uppercase; margin-top: 25px !important; margin-bottom: 12px !important;
        color: {soft_blue} !important; width: 100%; text-align: center;
    }}

    /* 3. THE GRID FIX: Force-centering the row of columns */
    [data-testid="stHorizontalBlock"] {{
        gap: 2px !important; 
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        max-width: 580px !important;
        margin: 0 auto !important;
    }}
    
    div[data-testid="column"] {{
        padding: 0px !important; margin: 0px !important;
        flex: 1 1 0% !important;
        display: flex !important;
        justify-content: center !important;
    }}

    /* 4. THE BUTTON: Absolute internal centering */
    .stButton {{ width: 100% !important; }}
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(45,45,45,1) 0%, rgba(30,30,30,1) 100%) !important; 
        color: {txt} !important; 
        border: 1px solid #333 !important; 
        border-radius: 4px !important; 
        height: 42px !important;
        width: 100% !important; 
        font-size: 12px !important; 
        
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 2px 4px rgba(0,0,0,0.3) !important;
    }}

    .stButton>button:hover {{ border-color: {soft_blue} !important; }}

    /* 5. Center-align the Breather */
    .breather-wrapper {{ width: 100%; display: flex; flex-direction: column; align-items: center; margin: 25px 0; }}
    .breather-circle {{
        width: 45px; height: 45px; border: 2px solid {soft_blue};
        border-radius: 50%; margin-bottom: 15px;
        animation: breathe-426 12s infinite ease-in-out;
    }}
    .breather-text {{ font-size: 14px; letter-spacing: 2px; color: #FFFFFF; font-weight: 300; opacity: 0.9; }}
    
    @keyframes breathe-426 {{
        0% {{ transform: scale(0.95); opacity: 0.4; }}
        33% {{ transform: scale(1.5); opacity: 1; }}   
        50% {{ transform: scale(1.5); opacity: 1; }}   
        100% {{ transform: scale(0.95); opacity: 0.4; }}    
    }}

    textarea {{ width: 100% !important; background: #1A1A1A !important; color: {soft_blue} !important; border: 1px solid #333 !important; border-radius: 8px !important; }}
    .footer-text {{ font-size: 10px; opacity: 0.4; margin-top: 40px; border-top: 1px solid #333; padding: 20px; width: 100%; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown(f"<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
nav_row = st.columns(3)
nav_list = [("Journal", "Journal"), ("Market", "Market"), ("Vision", "Vision"), ("FAQ", "FAQ"), ("Info", "Info")]

for i, (label, target) in enumerate(nav_list):
    with nav_row[i % 3]:
        if st.button(label, key=f"n_{label}"):
            st.session_state.current_page = target; st.rerun()

# --- 7. PAGES ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='section-header'>ENERGY</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight"; st.rerun()

    st.markdown(f"""<div class='breather-wrapper'><div class='breather-circle'></div><div class='breather-text'>4-2-6 RHYTHM</div></div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    aud_cols = st.columns(3)
    sound_list = list(sounds.keys())
    for i, name in enumerate(sound_list):
        with aud_cols[i % 3]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]; st.session_state.audio_label = name

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Record reflection...", height=90)
    
    if st.button("CONSULT GUIDE", key="brain_btn", use_container_width=True):
        if model:
            with st.spinner("..."):
                try:
                    prompt = "Mindfulness mentor. Calm reflection. No clinical terms."
                    parts = [prompt]
                    if audio_rec: parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                    else: parts.append(text_msg)
                    resp = model.generate_content(parts).text
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp})
                    st.rerun()
                except: st.error("Resting.")

    for entry in reversed(st.session_state.private_journal):
        st.info(f"{entry['time']} | {entry['ai']}")

elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>MARKET</div>", unsafe_allow_html=True)
    st.write("### Grounding Objects")
    st.write("**Starter Ritual:** ₹2,499  \n**Master Sanctuary:** ₹4,999")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>WhatsApp Order</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("### Ground | Release | Reflect")
    st.write("A bridge between technology and stillness.")

st.markdown("<div class='footer-text'>Wellness tool. Not medical.</div>", unsafe_allow_html=True)

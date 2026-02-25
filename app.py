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
bg, txt, btn_bg = "#121212", "#E0E0E0", "#1E1E1E"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. "SLEEK SLAB" CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    .block-container {{
        max-width: 550px !important;
        margin: auto;
        padding-top: 3.5rem !important; 
    }}

    @media (max-width: 640px) {{
        .block-container {{ max-width: 98% !important; padding-top: 3.5rem !important; }}
    }}

    .main-title {{
        text-align: center; letter-spacing: 10px; font-weight: 200; 
        margin-top: 10px; margin-bottom: 20px; font-size: 2.5rem; color: #FFFFFF;
        text-transform: uppercase;
    }}

    .section-header {{
        font-size: 13px !important; font-weight: 300 !important; letter-spacing: 3px !important;
        text-transform: uppercase; margin-top: 20px !important; margin-bottom: 5px !important;
        text-align: center; width: 100%; color: {soft_blue} !important;
    }}

    /* THE GRID: Ultra-Tight Horizontal Spacing */
    [data-testid="stHorizontalBlock"] {{
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 2px !important; 
        width: 100% !important;
    }}

    /* SLENDER RECTANGULAR BUTTONS */
    .stButton>button {{ 
        background-color: {btn_bg} !important; 
        color: {txt} !important; 
        border: 1px solid #2A2A2A !important; 
        border-radius: 2px !important; /* Sharper corners for a slab look */
        width: 100% !important;
        
        /* THE FIX: Reduced Height & Sideways Width */
        padding: 4px 0px !important; 
        min-height: 32px !important; 
        
        font-size: 11px !important; 
        font-weight: 400 !important;
        white-space: nowrap !important;
        margin: 0px !important;
        transition: all 0.2s ease;
    }}

    .stButton>button:hover {{
        border-color: {soft_blue} !important;
        background-color: #252525 !important;
    }}

    /* BREATHER RING */
    .breather-wrapper {{ text-align: center; margin: 20px 0; }}
    .breather-circle {{
        width: 40px; height: 40px;
        border: 2px solid {soft_blue};
        border-radius: 50%;
        margin: 0 auto 10px auto;
        animation: breathe-426 12s infinite ease-in-out;
    }}
    .breather-text {{ font-size: 8px; letter-spacing: 2px; color: {txt}; opacity: 0.5; }}
    
    @keyframes breathe-426 {{
        0% {{ transform: scale(0.95); opacity: 0.4; }}
        33% {{ transform: scale(1.4); opacity: 1; }}   
        50% {{ transform: scale(1.4); opacity: 1; }}   
        100% {{ transform: scale(0.95); opacity: 0.4; }}    
    }}

    textarea {{ 
        background: {btn_bg} !important; 
        color: {soft_blue} !important; 
        border: 1px solid #2A2A2A !important; 
        text-align: center !important;
        border-radius: 4px !important;
    }}
    
    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 0.1rem !important; }}
    .footer-text {{ font-size: 9px; opacity: 0.4; margin-top: 40px; border-top: 1px solid #2A2A2A; padding: 15px; width: 100%; }}
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

st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

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
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    aud_cols = st.columns(3)
    sound_list = list(sounds.keys())
    for i, name in enumerate(sound_list):
        with aud_cols[i % 3]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]; st.session_state.audio_label = name

    if st.session_state.active_audio:
        st.write(f"~ {st.session_state.audio_label} ~")
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    audio_rec = st.audio_input("Voice")
    text_msg = st.text_area("Record reflection...", height=80)
    
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

# Pages below remain safe and formatted
elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>MARKET</div>", unsafe_allow_html=True)
    st.write("Starter Ritual | Master Sanctuary")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Order</a>", unsafe_allow_html=True)
elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("Ground | Release | Reflect")
elif st.session_state.current_page == "FAQ":
    st.markdown("<div class='section-header'>FAQ</div>", unsafe_allow_html=True)
    st.write("Privacy focus.")
elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INFO</div>", unsafe_allow_html=True)
    st.write("Wellness companion.")

st.markdown("<div class='footer-text'>Sukoon is a wellness tool. Not a medical substitute.</div>", unsafe_allow_html=True)

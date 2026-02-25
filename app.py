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

# --- 5. "NANA BANANA" PRECISION CSS ---
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
        text-transform: uppercase; margin-top: 25px !important; margin-bottom: 8px !important;
        text-align: center; width: 100%; color: {soft_blue} !important;
    }}

    /* THE GRID: Ultra-Tight 2px Gaps */
    [data-testid="stHorizontalBlock"] {{
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 2px !important; /* Precision gap as requested */
        width: 100% !important;
    }}

    /* EQUAL SIZE RECTANGULAR BUTTONS */
    .stButton>button {{ 
        background-color: {btn_bg} !important; 
        color: {txt} !important; 
        border: 1px solid #2A2A2A !important; 
        border-radius: 4px !important; /* Subtle rounding for a rectangular feel */
        width: 100% !important;
        padding: 12px 2px !important; 
        min-height: 45px !important;
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

    /* SYNCED COLORS FOR INPUTS */
    textarea {{ 
        background: {btn_bg} !important; 
        color: {soft_blue} !important; /* Synced color */
        border: 1px solid #2A2A2A !important; 
        text-align: center !important;
        border-radius: 4px !important;
        margin-top: 5px;
    }}
    
    /* Voice Input Styling Sync */
    [data-testid="stAudioInput"] {{
        border: 1px solid #2A2A2A !important;
        border-radius: 4px !important;
        background: {btn_bg} !important;
    }}

    /* SMALLER BREATHER RING */
    .breather-wrapper {{ text-align: center; margin: 25px 0; }}
    .breather-circle {{
        width: 45px; height: 45px;
        border: 2px solid {soft_blue};
        border-radius: 50%;
        margin: 0 auto 15px auto;
        animation: breathe-426 12s infinite ease-in-out;
        box-shadow: 0 0 10px rgba(91, 150, 178, 0.2);
    }}
    .breather-text {{ font-size: 9px; letter-spacing: 2px; color: {txt}; opacity: 0.5; }}
    
    @keyframes breathe-426 {{
        0% {{ transform: scale(0.95); opacity: 0.4; }}
        33% {{ transform: scale(1.4); opacity: 1; }}   
        50% {{ transform: scale(1.4); opacity: 1; }}   
        100% {{ transform: scale(0.95); opacity: 0.4; }}    
    }}

    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 0.2rem !important; }}
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

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# --- 7. PAGES ---

if st.session_state.current_page == "Journal":
    # Energy
    st.markdown("<div class='section-header'>ENERGY</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight"; st.rerun()

    # BREATHER
    st.markdown(f"""
        <div class='breather-wrapper'>
            <div class='breather-circle'></div>
            <div class='breather-text'>INHALE 4s • HOLD 2s • EXHALE 6s</div>
        </div>
    """, unsafe_allow_html=True)

    # Ambience
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

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # INPUTS
    audio_rec = st.audio_input("Voice")
    text_msg = st.text_area("Record reflection...", height=100)
    
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

# Other pages (Preserved with the same deck style)
elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>MARKET</div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1: st.info("Starter Ritual")
    with m2: st.info("Master Sanctuary")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Connect to Order</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("Ground | Release | Reflect")

elif st.session_state.current_page == "FAQ":
    st.markdown("<div class='section-header'>FAQ</div>", unsafe_allow_html=True)
    st.write("Data is session-only.")

elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INFO</div>", unsafe_allow_html=True)
    st.write("Wellness companion.")

st.markdown("<div class='footer-text'>Sukoon is a wellness tool. Not a medical substitute.</div>", unsafe_allow_html=True)

import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"

# UPDATED: The perfect "one tone down" blue - calm and professional
soft_blue = "#5B96B2" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "theme" not in st.session_state: st.session_state.theme = "Midnight" # Default to premium dark
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. PREMIUM THEME COLORS ---
# We are now using a rich Charcoal/Midnight base for that premium feel
bg, txt, btn_bg = "#121212", "#E0E0E0", "#1E1E1E"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. THE "PREMIUM" CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    .block-container {{
        max-width: 550px !important;
        margin: auto;
        padding-top: 4rem !important; 
    }}

    @media (max-width: 640px) {{
        .block-container {{ max-width: 98% !important; padding-top: 3.5rem !important; }}
    }}

    /* Sukoon Title - Minimalist & Airy */
    .main-title {{
        text-align: center; letter-spacing: 10px; font-weight: 200; 
        margin-top: 10px; margin-bottom: 20px; font-size: 2.5rem; color: #FFFFFF;
        text-transform: uppercase;
    }}

    .section-header {{
        font-size: 14px !important; font-weight: 300 !important; letter-spacing: 3px !important;
        text-transform: uppercase; margin-top: 30px !important; margin-bottom: 15px !important;
        text-align: center; width: 100%; color: {soft_blue} !important;
        opacity: 0.8;
    }}

    /* SMALLER, ELEGANT BREATHER */
    .breather-wrapper {{
        text-align: center; margin: 30px 0;
    }}
    .breather-circle {{
        width: 55px; height: 55px; /* Smaller, as requested */
        border: 3px solid {soft_blue}; /* Using a ring/border look for premium feel */
        border-radius: 50%;
        margin: 0 auto 20px auto;
        animation: breathe-426 12s infinite ease-in-out;
        box-shadow: 0 0 15px rgba(91, 150, 178, 0.3);
    }}
    .breather-text {{
        font-size: 10px; letter-spacing: 2px; color: {txt}; opacity: 0.6;
    }}
    
    @keyframes breathe-426 {{
        0% {{ transform: scale(0.9); opacity: 0.4; }}
        33% {{ transform: scale(1.6); opacity: 1; }}   
        50% {{ transform: scale(1.6); opacity: 1; }}   
        100% {{ transform: scale(0.9); opacity: 0.4; }}    
    }}

    /* Minimalist Word Buttons */
    .stButton>button {{ 
        background: transparent !important; color: {txt} !important; 
        border: none !important; box-shadow: none !important;
        width: 100% !important; padding: 10px 0px !important;
        font-size: 12px !important; font-weight: 300 !important;
        white-space: nowrap !important;
        text-decoration: underline; text-decoration-color: rgba(91, 150, 178, 0.4);
        transition: all 0.4s ease;
    }}

    .stButton>button:hover {{
        color: {soft_blue} !important;
        text-decoration-color: {soft_blue};
    }}

    [data-testid="stHorizontalBlock"] {{
        display: grid !important; grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important; width: 100% !important; align-items: center;
    }}

    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 0.5rem !important; }}
    
    textarea {{ 
        background: #1A1A1A !important; color: {txt} !important; 
        border: 0.5px solid #333 !important; text-align: center !important;
        border-radius: 8px !important; margin-top: 20px;
    }}

    .footer-text {{ font-size: 9px; opacity: 0.4; margin-top: 50px; border-top: 0.5px solid #333; padding: 20px; width: 100%; }}
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

st.markdown("<hr style='border: 0.5px solid #333; margin: 10px 0;'>", unsafe_allow_html=True)

# --- 7. PAGES ---

if st.session_state.current_page == "Journal":
    # Energy
    st.markdown("<div class='section-header'>ENERGY</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(lab, key=f"m_{lab}"):
                # Mood logic preserved
                st.session_state.theme = "Midnight"; st.rerun()

    # THE PREMIUM BREATHER
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

    st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)
    audio_rec = st.audio_input("Voice")
    text_msg = st.text_area("Record reflection...", height=100)
    
    if st.button("CONSULT GUIDE", key="brain_btn"):
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
    m1, m2 = st.columns(2)
    with m1: st.write("**Starter Ritual**"); st.write("₹2,499")
    with m2: st.write("**Master Sanctuary**"); st.write("₹4,999")
    st.markdown(f"<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Connect to Order</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("### Ground | Release | Reflect")
    st.write("A bridge between high-technology and inner stillness.")

elif st.session_state.current_page == "FAQ":
    st.markdown("<div class='section-header'>FAQ</div>", unsafe_allow_html=True)
    st.write("Data is session-only. Frequencies for focus.")

elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INFO</div>", unsafe_allow_html=True)
    st.write("Wellness companion. No medical or psychiatric advice provided.")

st.markdown("<div class='footer-text'>Sukoon is a wellness tool. Not a medical substitute.</div>", unsafe_allow_html=True)

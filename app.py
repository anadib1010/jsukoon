import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "theme" not in st.session_state: st.session_state.theme = "Peaceful"
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. THEME ---
bg, txt, btn_bg = ("#0A0E0B", "#AEC6CF", "#1E1E1E") if st.session_state.theme == "Midnight" else ("#F9FDF9", "#2E4032", "white")

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. CENTERED TYPOGRAPHY CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    .block-container {{
        max-width: 550px !important;
        margin: auto;
        padding-top: 1.5rem !important;
    }}

    @media (max-width: 640px) {{
        .block-container {{ max-width: 98% !important; }}
    }}

    /* Section Header Styling */
    .section-header {{
        font-size: 20px !important;
        font-weight: 300 !important;
        letter-spacing: 4px !important;
        text-transform: uppercase;
        margin-top: 25px !important;
        margin-bottom: 10px !important;
        text-align: center;
        width: 100%;
        color: {txt};
        opacity: 0.9;
    }}

    /* Word-Only Buttons */
    .stButton>button {{ 
        background: transparent !important; 
        color: {txt} !important; 
        border: none !important; 
        box-shadow: none !important;
        width: 100% !important;
        padding: 8px 0px !important;
        font-size: clamp(10px, 3vw, 13px) !important; 
        font-weight: 400 !important;
        white-space: nowrap !important;
        text-decoration: underline;
        text-decoration-color: {soft_blue};
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{ color: {soft_blue} !important; }}

    /* Grid Layout */
    [data-testid="stHorizontalBlock"] {{
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 5px !important;
        width: 100% !important;
        align-items: center;
    }}

    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 0.2rem !important; }}
    
    textarea {{ 
        background: transparent !important; 
        color: {txt} !important; 
        border: 0.5px solid {soft_blue} !important; 
        text-align: center !important; 
        margin-top: 15px !important;
    }}

    .footer-text {{ font-size: 9px; opacity: 0.5; margin-top: 35px; border-top: 0.5px solid {soft_blue}; padding: 10px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h1 style='text-align: center; letter-spacing: 6px; font-weight: 200; margin-bottom: 0px;'>SUKOON</h1>", unsafe_allow_html=True)
nav_row = st.columns(3)
nav_list = [("Journal", "Journal"), ("Market", "Market"), ("Vision", "Vision"), ("FAQ", "FAQ"), ("Info", "Info")]

for i, (label, target) in enumerate(nav_list):
    with nav_row[i % 3]:
        if st.button(label, key=f"n_{label}"):
            st.session_state.current_page = target; st.rerun()

st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    # CENTERED LARGE HEADER: ENERGY
    st.markdown("<div class='section-header'>ENERGY</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # CENTERED LARGE HEADER: AMBIENCE
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    aud_cols = st.columns(3)
    sound_list = list(sounds.keys())
    for i, name in enumerate(sound_list):
        with aud_cols[i % 3]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        st.write(f"~ {st.session_state.audio_label} ~")
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
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

# (Pages handled minimally)
elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>MARKET</div>", unsafe_allow_html=True)
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>WhatsApp Order</a>", unsafe_allow_html=True)
elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("Ground | Release | Reflect")
elif st.session_state.current_page == "FAQ":
    st.markdown("<div class='section-header'>FAQ</div>", unsafe_allow_html=True)
elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INFO</div>", unsafe_allow_html=True)

st.markdown("<div class='footer-text'>Wellness tool. Not medical.</div>", unsafe_allow_html=True)

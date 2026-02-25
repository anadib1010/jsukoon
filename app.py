import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import requests

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "manavprakash" 
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

for key in ["private_journal", "current_page", "theme", "active_audio"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful" if key == "theme" else None

# --- 3. THEME ---
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
brain_online = False
try:
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        brain_online = True
except: brain_online = False

# --- 5. AUDIO HELPER (The "Bypass" Engine) ---
def get_audio_data(file_name):
    # This fetches the file directly to avoid the 'grey button' glitch
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/{file_name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

# --- 6. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; text-align: center !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {soft_blue} !important; border-radius: 10px !important; width: 100%; font-size: 12px !important; }}
    .breather-circle {{ width: 60px; height: 60px; background: {soft_blue}; border-radius: 50%; margin: 15px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 7. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nj"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nm"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nv"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 8. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    m_cols = st.columns(5)
    for i, lab in enumerate(["Low", "Drained", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(lab, key=f"md_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # --- HORIZONTAL AUDIO BUTTONS ---
    st.write("#### Nature Ambience")
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    aud_cols = st.columns(5)
    for idx, (name, file) in enumerate(sounds.items()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = file
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        audio_data = get_audio_data(st.session_state.active_audio)
        if audio_data:
            st.write(f"🔊 Playing: **{st.session_state.audio_label}**")
            st.audio(audio_data, format="audio/mp3", autoplay=True)
        else:
            st.error("Audio file not found. Check GitHub privacy/filenames.")

    st.markdown("---")
    # (AI Logic and History remains here...)
    # [Microphone and Consult Guide Button Code]

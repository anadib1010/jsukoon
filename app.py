import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "manavprakash" 
# This is the most reliable way to link to GitHub raw files
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
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

# --- 4. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; text-align: center !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {soft_blue} !important; border-radius: 10px !important; width: 100%; font-size: 11px !important; }}
    .breather-circle {{ width: 60px; height: 60px; background: {soft_blue}; border-radius: 50%; margin: 15px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nj"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nm"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nv"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 6. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    m_cols = st.columns(5)
    for i, lab in enumerate(["Low", "Drained", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(lab, key=f"md_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # --- HORIZONTAL AUDIO BUTTONS ---
    st.write("#### Nature Ambience")
    sounds = {
        "Birds": "birds.mp3", 
        "Flute": "flute.mp3", 
        "Forest": "forest.mp3", 
        "Waves": "waves.mp3", 
        "Wind": "wind.mp3"
    }
    
    aud_cols = st.columns(5)
    for idx, name in enumerate(sounds.keys()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        file_url = f"{BASE_URL}{st.session_state.active_audio}"
        st.write(f"🔊 Playing: **{st.session_state.audio_label}**")
        # Direct URL streaming
        st.audio(file_url, format="audio/mp3", autoplay=True)
        
        # DEBUG LINK: If it fails, clicking this will show us why
        with st.expander("Connection Troubles?"):
            st.write("If you hear nothing, tap the link below. If it opens a music player, the app is fine. If it says 404, the filename is wrong.")
            st.link_button("Test Direct File Link", file_url)

    st.markdown("---")
    # ... rest of AI code ...

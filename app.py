import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
# CHANGE THIS TO YOUR ACTUAL GITHUB USERNAME
GITHUB_USER = "manavprakash" 
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# Initialize state properly
if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "theme" not in st.session_state: st.session_state.theme = "Peaceful"

# --- 3. THEME LOGIC (FORCE REFRESH) ---
if st.session_state.theme == "Midnight":
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A"
else:
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"

# --- 4. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; text-align: center !important; }}
    h1, h2, h3, h4, p, li {{ color: {txt} !important; font-weight: 200 !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {soft_blue} !important; border-radius: 12px !important; width: 100%; }}
    .breather-circle {{ width: 70px; height: 70px; background: {soft_blue}; border-radius: 50%; margin: 20px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .mkt-box {{ border: 1px solid {soft_blue}; padding: 15px; border-radius: 15px; margin-bottom: 15px; background: rgba(174, 198, 207, 0.05); }}
    .wa-link {{ display: block; background: {soft_blue}; color: #0A0E0B; padding: 10px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nav_j"): 
        st.session_state.current_page = "Journal"
        st.rerun()
with n2: 
    if st.button("Market", key="nav_m"): 
        st.session_state.current_page = "Marketplace"
        st.rerun()
with n3: 
    if st.button("Vision", key="nav_v"): 
        st.session_state.current_page = "Vision"
        st.rerun()
st.markdown("---")

# --- 6. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check-In")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"mood_{i}"):
                # FORCE THEME UPDATE
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({
                    "time": datetime.now().strftime("%H:%M"), 
                    "diary": f"[{label} Energy]", 
                    "ai": f"Acknowledging that {label.lower()} energy. Let's find center."
                })
                st.rerun() # This is critical to change colors immediately

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    st.write("#### Nature Ambience")
    # THE FIX: Ensuring the URL points to the RAW file
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    
    # Check these filenames exactly in your GitHub
    sounds = {"Waves": "waves.mp3", "Birds": "birds.mp3", "Rain": "rain.mp3", "Forest": "forest.mp3", "Flute": "flute.mp3"}
    
    for name, file in sounds.items():
        col1, col2 = st.columns([1, 4])
        with col1: st.write(f"**{name}**")
        with col2: st.audio(base_url + file, format="audio/mp3")

    st.markdown("---")
    # ... rest of your code for AI consultation ...
    # (AI logic remains the same as previous stable versions)

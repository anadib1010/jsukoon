import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
# VITAL: Ensure this matches your GitHub username exactly
GITHUB_USER = "manavprakash" 
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "theme" not in st.session_state: st.session_state.theme = "Peaceful"

# --- 3. THEME LOGIC ---
if st.session_state.theme == "Midnight":
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A"
else:
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"

# --- 4. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; text-align: center !important; }}
    h1, h2, h3, h4, p, li {{ color: {txt} !important; font-weight: 200 !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {soft_blue} !important; border-radius: 12px !important; }}
    .breather-circle {{ width: 70px; height: 70px; background: {soft_blue}; border-radius: 50%; margin: 20px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .mkt-box {{ border: 1px solid {soft_blue}; padding: 15px; border-radius: 15px; margin-bottom: 15px; background: rgba(174, 198, 207, 0.05); }}
    .wa-link {{ display: block; background: {soft_blue}; color: #0A0E0B; padding: 10px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
    
    /* Center Audio Widgets */
    div[data-testid="stAudio"] {{ display: flex; justify-content: center; margin-bottom: 5px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nav_j"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nav_m"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nav_v"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 6. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check-In")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"mood_{i}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": f"[{label} Energy]", "ai": f"Acknowledging your {label.lower()} energy."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # --- UPDATED NATURE AMBIENCE SECTION ---
    st.write("#### Nature Ambience")
    
    # Path construction
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    
    # Names MUST match your GitHub files exactly (case sensitive)
    sounds = {
        "Waves": "waves.mp3", 
        "Birds": "birds.mp3", 
        "Rain": "rain.mp3", 
        "Forest": "forest.mp3", 
        "Flute": "flute.mp3"
    }

    # Creating a clean layout for audio
    for name, file in sounds.items():
        st.write(f"_{name}_")
        st.audio(base_url + file)

    st.markdown("---")
    # ... AI Input and History logic follows ...

# --- 7. MARKETPLACE (RE-CENTERED & FIXED) ---
elif st.session_state.current_page == "Marketplace":
    st.write("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"<div class='mkt-box'><h4>Starter Ritual</h4><p>₹2,499</p><a href='https://wa.me/{MY_PHONE}?text=Starter' class='wa-link'>Order</a></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='mkt-box'><h4>Master Sanctuary</h4><p>₹4,999</p><a href='https://wa.me/{MY_PHONE}?text=Master' class='wa-link'>Order</a></div>", unsafe_allow_html=True)
    
    st.write("#### Individual Items")
    i1, i2, i3 = st.columns(3)
    items = ["Stones", "Buddha", "Art"]
    for idx, item in enumerate(items):
        with [i1, i2, i3][idx]:
            st.markdown(f"<div class='mkt-box'><h5>{item}</h5><a href='https://wa.me/{MY_PHONE}?text={item}' class='wa-link'>Inquire</a></div>", unsafe_allow_html=True)

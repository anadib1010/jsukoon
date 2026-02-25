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
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. THE "GRID" CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    [data-testid="stVerticalBlock"] {{ display: flex; flex-direction: column; align-items: center !important; text-align: center !important; }}
    
    /* Navigation Bar: Force Horizontal */
    div[data-testid="column"] {{
        min-width: 0px !important;
        flex: 1 1 0% !important;
    }}

    /* The Secret Sauce: Flex-Grid for Audio Buttons */
    .button-container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        width: 100%;
        max-width: 500px;
        margin: 10px auto;
    }}

    /* Styling the buttons to look like 2-per-row on mobile */
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 10px !important; 
        padding: 8px 5px !important; min-height: 40px !important;
        font-size: 11px !important; font-weight: 500 !important;
        white-space: nowrap !important;
    }}

    /* Mobile specific: Force buttons to take 45% width to make a 2-column grid */
    @media (max-width: 640px) {{
        div[data-testid="stHorizontalBlock"] > div {{
            flex: 1 1 45% !important;
            min-width: 45% !important;
        }}
    }}

    .footer-text {{ font-size: 10px; opacity: 0.6; text-align: center; margin-top: 20px; padding: 10px; border-top: 0.5px solid {soft_blue}; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>Sukoon</h1>", unsafe_allow_html=True)
nav_cols = st.columns(5)
nav_items = [("Journal", "Journal"), ("Market", "Marketplace"), ("Vision", "Vision"), ("FAQ", "FAQ"), ("Info", "Disclaimer")]
for i, (label, target) in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(label, key=f"nav_{label}"):
            st.session_state.current_page = target; st.rerun()

st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check")
    m_cols = st.columns(5)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # Nature Ambience - Forced Grid of 2 on Mobile
    st.write("#### Nature Ambience")
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    # We use a nested column structure that the CSS will force into a grid
    a_row1 = st.columns(2)
    with a_row1[0]:
        if st.button("Birds", key="aud_b"): st.session_state.active_audio = "birds.mp3"; st.session_state.audio_label = "Birds"
    with a_row1[1]:
        if st.button("Flute", key="aud_f"): st.session_state.active_audio = "flute.mp3"; st.session_state.audio_label = "Flute"
        
    a_row2 = st.columns(2)
    with a_row2[0]:
        if st.button("Forest", key="aud_fo"): st.session_state.active_audio = "forest.mp3"; st.session_state.audio_label = "Forest"
    with a_row2[1]:
        if st.button("Waves", key="aud_w"): st.session_state.active_audio = "waves.mp3"; st.session_state.audio_label = "Waves"
        
    a_row3 = st.columns(1) # Center the 5th one
    with a_row3[0]:
        if st.button("Wind", key="aud_wi"): st.session_state.active_audio = "wind.mp3"; st.session_state.audio_label = "Wind"

    if st.session_state.active_audio:
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Record reflection...", height=80)
    
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
                try:
                    prompt = "You are a mindfulness mentor. Provide a calm reflection. Avoid clinical terms."
                    parts = [prompt]
                    if audio_rec: parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                    else: parts.append(text_msg)
                    resp = model.generate_content(parts).text
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp})
                    st.rerun()
                except: st.error("The Guide is pausing.")

    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")

# --- 8. OTHER PAGES ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div class='mkt-box'>Starter Ritual<br>₹2,499<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue}; text-decoration:none;'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='mkt-box'>Master Sanctuary<br>₹4,999<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue}; text-decoration:none;'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### The Ritual: Ground | Release | Reflect")
    st.markdown(f"<br><a href='https://wa.me/{MY_PHONE}' class='mkt-box' style='display:block; text-decoration:none; color:{soft_blue}; font-weight:bold;'>Connect with Founder</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "FAQ":
    st.write("### FAQ")
    st.write("**Privacy:** Data is session-only.")
    st.write("**Purpose:** Wellness companion.")

elif st.session_state.current_page == "Disclaimer":
    st.write("### Information")
    st.write("Sukoon is a self-help tool, not for medical use.")

st.markdown("<div class='footer-text'>Wellness tool. Not a medical substitute.</div>", unsafe_allow_html=True)

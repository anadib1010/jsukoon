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

# --- 5. MOBILE-FIRST CSS (FLUID FONTS) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    /* Center vertical blocks */
    [data-testid="stVerticalBlock"] {{
        display: flex;
        flex-direction: column;
        align-items: center !important;
        text-align: center !important;
    }}

    /* Buttons: Wider and Fluid Font */
    .stButton {{ display: flex; justify-content: center; width: 100%; }}
    .stButton>button {{ 
        background-color: {btn_bg} !important; 
        color: {txt} !important; 
        border: 1px solid {soft_blue} !important; 
        border-radius: 10px !important; 
        width: 100% !important; 
        padding: 5px 2px !important;
        font-size: clamp(10px, 3vw, 14px) !important; /* Shrinks text to fit */
        white-space: nowrap !important; /* Prevents 2-line break */
        overflow: hidden;
        margin: 2px auto !important;
    }}
    
    /* Center Audio */
    div[data-testid="stAudio"] {{ display: flex; justify-content: center; width: 100%; }}
    
    /* Text Input Alignment */
    textarea {{ text-align: center !important; border-radius: 12px !important; border: 1px solid {soft_blue} !important; }}

    .breather-circle {{ width: 65px; height: 65px; background: {soft_blue}; border-radius: 50%; margin: 20px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nj"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nm"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nv"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check")
    m_cols = st.columns(5)
    moods = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # Nature Ambience
    st.write("#### Nature Ambience")
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    aud_cols = st.columns(5)
    for idx, name in enumerate(sounds.keys()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        st.write(f"🔊 Playing: **{st.session_state.audio_label}**")
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    
    # AI INPUT
    audio_rec = st.audio_input("Record")
    text_msg = st.text_area("Share your heart...", placeholder="Type here...")
    
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Respond in 1 calm paragraph."]
                    if audio_rec: parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                    else: parts.append(text_msg)
                    resp = model.generate_content(parts).text
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp})
                    st.rerun()
                except: st.error("The Brain is pausing. Wait a minute.")
        else: st.warning("Guide Offline.")

    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")
        st.write("---")

# --- 8. OTHER PAGES ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div style='border:1px solid {soft_blue}; padding:10px; border-radius:10px;'>Starter Ritual<br>₹2,499<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue}; text-decoration:none;'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div style='border:1px solid {soft_blue}; padding:10px; border-radius:10px;'>Master Sanctuary<br>₹4,999<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue}; text-decoration:none;'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.markdown(f"<div style='display:flex; justify-content:center; width:100%;'><a href='https://wa.me/{MY_PHONE}' style='display:block; border:1px solid {soft_blue}; padding:15px; border-radius:12px; text-decoration:none; color:{soft_blue}; font-weight:bold;'>Connect</a></div>", unsafe_allow_html=True)

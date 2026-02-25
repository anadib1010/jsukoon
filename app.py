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

# --- 5. SMART RESPONSIVE CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    [data-testid="stVerticalBlock"] {{ display: flex; flex-direction: column; align-items: center !important; text-align: center !important; }}
    
    /* Buttons: Smaller Font & Flexible Grid */
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 10px !important; 
        width: 100% !important; padding: 6px 10px !important; min-height: 38px !important;
        margin: 2px auto !important; font-size: 12px !important; font-weight: 500 !important;
        white-space: nowrap !important;
    }}
    
    /* Marketplace Boxes */
    .mkt-box {{ border: 1px solid {soft_blue}; padding: 15px; border-radius: 12px; background: {btn_bg}; width: 100%; }}
    
    /* Footer */
    .footer-text {{ font-size: 10px; opacity: 0.6; text-align: center; margin-top: 30px; padding: 10px; width: 100%; border-top: 0.5px solid {soft_blue}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. TOP NAVIGATION (Adaptive) ---
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>Sukoon</h1>", unsafe_allow_html=True)
# Using 5 columns for the menu to keep them on one line on desktop
nav_cols = st.columns(5)
nav_items = [("Journal", "Journal"), ("Market", "Marketplace"), ("Vision", "Vision"), ("FAQ", "FAQ"), ("Info", "Disclaimer")]

for i, (label, target) in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(label, key=f"nav_{label}"):
            st.session_state.current_page = target; st.rerun()

st.markdown("---")

# --- 7. JOURNAL PAGE (Space-Saving Grid) ---
if st.session_state.current_page == "Journal":
    # Energy Selection in a single row
    st.write("#### Energy Check")
    m_cols = st.columns(5)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # Nature Ambience in a 3+2 Grid to save vertical space
    st.write("#### Nature Ambience")
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    # We use 3 columns here so buttons wrap naturally
    aud_cols = st.columns(3)
    sound_keys = list(sounds.keys())
    for i in range(3):
        with aud_cols[i]:
            if st.button(sound_keys[i], key=f"aud_{sound_keys[i]}"):
                st.session_state.active_audio = sounds[sound_keys[i]]
                st.session_state.audio_label = sound_keys[i]
    
    aud_cols2 = st.columns(2)
    for i in range(3, 5):
        with aud_cols2[i-3]:
            if st.button(sound_keys[i], key=f"aud_{sound_keys[i]}"):
                st.session_state.active_audio = sounds[sound_keys[i]]
                st.session_state.audio_label = sound_keys[i]

    if st.session_state.active_audio:
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    
    # INPUT SECTION (Brought higher up)
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Record reflection...", placeholder="How is your presence?", height=100)
    
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
                try:
                    prompt = "You are a mindfulness mentor. Provide a calm, supportive reflection. Avoid clinical terms."
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
    st.write("### The Sukoon Ritual")
    st.markdown("**1. Ground** | **2. Release** | **3. Reflect**")
    st.markdown(f"<br><a href='https://wa.me/{MY_PHONE}' class='mkt-box' style='display:block; text-decoration:none; color:{soft_blue}; font-weight:bold;'>Connect with Founder</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "FAQ":
    st.write("### FAQ")
    st.write("**Privacy:** Data stays in your current session.")
    st.write("**Sounds:** Natural frequencies for calm focus.")

elif st.session_state.current_page == "Disclaimer":
    st.write("### Information")
    st.write("Sukoon is a self-help companion. It is not for medical or psychiatric use.")

st.markdown("<div class='footer-text'>Wellness tool. Not a medical substitute.</div>", unsafe_allow_html=True)

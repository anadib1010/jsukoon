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

# --- 5. COMPREHENSIVE CSS (Including Breather) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    .block-container {{
        max-width: 550px !important;
        margin: auto;
        padding-top: 3.5rem !important; 
    }}

    @media (max-width: 640px) {{
        .block-container {{ max-width: 98% !important; padding-top: 3rem !important; }}
    }}

    .main-title {{
        text-align: center; letter-spacing: 7px; font-weight: 200; 
        margin-top: 10px; margin-bottom: 5px; font-size: 2.2rem; color: {txt};
    }}

    .section-header {{
        font-size: 17px !important; font-weight: 300 !important; letter-spacing: 4px !important;
        text-transform: uppercase; margin-top: 25px !important; margin-bottom: 12px !important;
        text-align: center; width: 100%; color: {soft_blue} !important;
    }}

    /* BREATHE ANIMATION */
    .breather-container {{
        display: flex; justify-content: center; align-items: center;
        height: 120px; width: 100%; margin: 10px 0;
    }}
    .breather-circle {{
        width: 50px; height: 50px;
        background: {soft_blue};
        border-radius: 50%;
        animation: breathe 8s infinite ease-in-out;
        opacity: 0.7;
        filter: blur(8px);
    }}
    @keyframes breathe {{
        0%, 100% {{ transform: scale(1); opacity: 0.3; }}
        50% {{ transform: scale(1.8); opacity: 0.8; }}
    }}

    /* Minimalist Word Buttons */
    .stButton>button {{ 
        background: transparent !important; color: {txt} !important; 
        border: none !important; box-shadow: none !important;
        width: 100% !important; padding: 8px 0px !important;
        font-size: clamp(10.5px, 3.2vw, 13px) !important; 
        font-weight: 400 !important; white-space: nowrap !important;
        text-decoration: underline; text-decoration-color: {soft_blue};
        transition: all 0.3s ease;
    }}

    [data-testid="stHorizontalBlock"] {{
        display: grid !important; grid-template-columns: repeat(3, 1fr) !important;
        gap: 5px !important; width: 100% !important; align-items: center;
    }}

    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 0.4rem !important; }}
    
    textarea {{ 
        background: transparent !important; color: {txt} !important; 
        border: 0.5px solid {soft_blue} !important; text-align: center !important;
        border-radius: 0px !important;
    }}

    .footer-text {{ font-size: 9px; opacity: 0.5; margin-top: 40px; border-top: 0.5px solid {soft_blue}; padding: 15px; width: 100%; }}
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

st.markdown("---")

# --- 7. PAGES ---

# JOURNAL PAGE
if st.session_state.current_page == "Journal":
    # 1. Energy
    st.markdown("<div class='section-header'>ENERGY</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # 2. THE BREATHER (Restored)
    st.markdown("<div class='breather-container'><div class='breather-circle'></div></div>", unsafe_allow_html=True)

    # 3. Ambience
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

# MARKET PAGE (Locked & Restored)
elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>MARKET</div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1: st.write("**Starter Ritual**"); st.write("₹2,499")
    with m2: st.write("**Master Sanctuary**"); st.write("₹4,999")
    st.markdown("---")
    st.write("Authentic beads, yantras, and grounding stones.")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Connect to Order</a>", unsafe_allow_html=True)

# VISION PAGE (Locked & Restored)
elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("### The Sukoon Ritual")
    st.markdown("**Ground:** Frequencies. | **Release:** Reflection. | **Reflect:** Presence.")
    st.write("A bridge between technology and stillness.")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Talk to the Founder</a>", unsafe_allow_html=True)

# FAQ & INFO (Locked & Restored)
elif st.session_state.current_page == "FAQ":
    st.markdown("<div class='section-header'>FAQ</div>", unsafe_allow_html=True)
    st.write("Data is session-only. Frequencies for focus.")
elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INFO</div>", unsafe_allow_html=True)
    st.write("### Disclaimer")
    st.write("Wellness companion. No medical, psychological, or psychiatric advice provided.")

st.markdown("<div class='footer-text'>Wellness tool. Not medical substitute.</div>", unsafe_allow_html=True)

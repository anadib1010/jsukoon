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

# --- 5. THE FORCED GRID CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    /* Force 3 Columns on Mobile & Desktop */
    [data-testid="stHorizontalBlock"] {{
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 8px !important;
        width: 100% !important;
    }}

    /* Make buttons slim but sturdy */
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 10px !important; 
        padding: 6px 2px !important; min-height: 40px !important;
        font-size: 11px !important; font-weight: 500 !important;
        width: 100% !important;
        margin: 0px !important;
    }}

    /* Center text and elements */
    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 1rem !important; }}
    
    .footer-text {{ font-size: 9px; opacity: 0.6; margin-top: 20px; border-top: 0.5px solid {soft_blue}; padding: 10px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. TOP NAVIGATION (3-Column Grid) ---
st.markdown("<h2 style='margin-bottom:0px;'>Sukoon</h2>", unsafe_allow_html=True)
# This will now show 3 buttons on row 1, 2 buttons on row 2
nav_row = st.columns(3)
nav_list = [("Journal", "Journal"), ("Market", "Marketplace"), ("Vision", "Vision"), ("FAQ", "FAQ"), ("Info", "Disclaimer")]

for i, (label, target) in enumerate(nav_list):
    with nav_row[i % 3]: # The %3 forces the wrap into 3 columns
        if st.button(label, key=f"n_{label}"):
            st.session_state.current_page = target; st.rerun()

st.markdown("---")

# --- 7. PAGES ---
if st.session_state.current_page == "Journal":
    # Energy Section (3-Column Grid)
    st.write("Energy Check")
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # Nature Ambience (3-Column Grid)
    st.write("Nature Ambience")
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
        st.write(f"🔊 {st.session_state.audio_label}")
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    # Voice Note and Box - Now much higher up the screen!
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Reflection...", height=80)
    
    if st.button("Consult Guide", use_container_width=True):
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
                except: st.error("Pausing.")

    for entry in reversed(st.session_state.private_journal):
        st.info(f"{entry['time']} | {entry['ai']}")

elif st.session_state.current_page == "Marketplace":
    st.write("### Grounding Objects")
    m_row = st.columns(2)
    with m_row[0]: st.info("Starter Ritual")
    with m_row[1]: st.info("Master Sanctuary")
    st.markdown(f"<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>WhatsApp Order</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Ground | Release | Reflect")
    st.markdown(f"<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Connect with Founder</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "FAQ":
    st.write("### FAQ")
    st.write("Data is session-only. Sounds for focus.")

elif st.session_state.current_page == "Disclaimer":
    st.write("### Information")
    st.write("Wellness companion. Not medical.")

st.markdown("<div class='footer-text'>Wellness tool. Not medical.</div>", unsafe_allow_html=True)

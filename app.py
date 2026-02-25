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

# --- 5. REFINED SPACIAL CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    /* Centering and Row Spacing (Horizontal Cladding) */
    [data-testid="stVerticalBlock"] {{ 
        align-items: center !important; 
        text-align: center !important; 
        gap: 1.5rem !important; /* Increased space between different rows/sections */
    }}

    /* Compact Buttons with Tight Column Gaps */
    .stButton {{ display: flex; justify-content: center; }}
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 8px !important; 
        padding: 4px 8px !important; min-height: 34px !important;
        font-size: 11px !important; font-weight: 500 !important;
        width: 100% !important;
        margin: 0px !important; /* Remove individual margins to allow tight columns */
    }}

    /* Tightening the columns specifically */
    div[data-testid="column"] {{
        padding: 0px 2px !important; /* This is the secret to decreasing column space */
    }}
    
    div[data-testid="stHorizontalBlock"] {{
        gap: 4px !important; /* Controls the horizontal gap between buttons */
    }}

    textarea {{ text-align: center !important; border-radius: 12px !important; border: 1px solid {soft_blue} !important; }}
    .footer-text {{ font-size: 9px; opacity: 0.6; margin-top: 30px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION (Tight Horizontal Row) ---
st.markdown("<h2 style='margin-bottom:0px;'>Sukoon</h2>", unsafe_allow_html=True)
nav_cols = st.columns(5)
nav_items = [("Journal", "Journal"), ("Market", "Marketplace"), ("Vision", "Vision"), ("FAQ", "FAQ"), ("Info", "Disclaimer")]
for i, (label, target) in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(label, key=f"n_{label}"):
            st.session_state.current_page = target; st.rerun()

st.markdown("---")

# --- 7. PAGES ---
if st.session_state.current_page == "Journal":
    # Energy Section
    st.write("Energy Balance")
    m_cols = st.columns(5)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # Nature Ambience
    st.write("Nature Ambience")
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    aud_cols = st.columns(5)
    for idx, (name, file) in enumerate(sounds.items()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = file
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        st.write(f"🔊 {st.session_state.audio_label}")
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    # Voice Note and Box
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Record reflection...", height=80)
    
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
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
    st.write("Session-only privacy. Natural focus sounds.")

elif st.session_state.current_page == "Disclaimer":
    st.write("### Information")
    st.write("Wellness companion. Not medical.")

st.markdown("<div class='footer-text'>Wellness tool. Not medical.</div>", unsafe_allow_html=True)

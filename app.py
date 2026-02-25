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

for key in ["private_journal", "current_page", "theme", "active_audio"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful" if key == "theme" else None

# --- 3. THEME ---
bg, txt, btn_bg = ("#0A0E0B", "#AEC6CF", "#1E1E1E") if st.session_state.theme == "Midnight" else ("#F9FDF9", "#2E4032", "white")

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. ULTRA-COMPACT CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    /* Center the main block */
    [data-testid="stVerticalBlock"] {{ align-items: center !important; text-align: center !important; gap: 0.5rem !important; }}

    /* THE KEY: Horizontal Flex Container */
    .flex-container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 6px;
        width: 100%;
        margin-bottom: 15px;
    }}

    /* Compact Button Styling */
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 8px !important; 
        padding: 4px 10px !important; min-height: 32px !important;
        font-size: 11px !important; font-weight: 500 !important;
        width: auto !important; /* Let buttons shrink to text size */
    }}

    /* Remove extra Streamlit padding */
    .block-container {{ padding-top: 1rem !important; padding-bottom: 1rem !important; }}
    div[data-testid="stHorizontalBlock"] {{ gap: 0px !important; }}
    
    .footer-text {{ font-size: 9px; opacity: 0.6; margin-top: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION (One Tight Line) ---
st.markdown("<h2 style='margin-bottom:0px;'>Sukoon</h2>", unsafe_allow_html=True)
nav_cols = st.columns([1,1,1,1,1])
with nav_cols[0]: 
    if st.button("Journal", key="n1"): st.session_state.current_page="Journal"; st.rerun()
with nav_cols[1]: 
    if st.button("Market", key="n2"): st.session_state.current_page="Marketplace"; st.rerun()
with nav_cols[2]: 
    if st.button("Vision", key="n3"): st.session_state.current_page="Vision"; st.rerun()
with nav_cols[3]: 
    if st.button("FAQ", key="n4"): st.session_state.current_page="FAQ"; st.rerun()
with nav_cols[4]: 
    if st.button("Info", key="n5"): st.session_state.current_page="Disclaimer"; st.rerun()

# --- 7. PAGES ---
if st.session_state.current_page == "Journal":
    # Energy Section (Tight Horizontal Row)
    st.write("Energy Check")
    m_cols = st.columns(5)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(moods):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    # Nature Ambience (Tight Horizontal Row)
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
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    # Voice Note and Box
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Record reflection...", height=70)
    
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
    m1, m2 = st.columns(2)
    with m1: st.info("Starter Ritual - ₹2,499")
    with m2: st.info("Master Sanctuary - ₹4,999")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>WhatsApp Order</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Ritual: Ground | Release | Reflect")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Connect with Founder</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "FAQ":
    st.write("### FAQ")
    st.write("Data is session-only. Sounds for focus.")

elif st.session_state.current_page == "Disclaimer":
    st.write("### Information")
    st.write("Wellness companion. Not medical.")

st.markdown("<div class='footer-text'>Wellness tool. Not medical.</div>", unsafe_allow_html=True)

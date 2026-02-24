import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# --- AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # Discovery Logic
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in models if 'flash' in m), models[0])
        super_brain = genai.GenerativeModel(target_model)
    except:
        super_brain = None
else:
    super_brain = None

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"

def get_daily_quote():
    # Only call AI if we have a brain, otherwise use a default to save quota
    if super_brain:
        try:
            return super_brain.generate_content("Give a 1-sentence mindfulness quote.").text
        except:
            pass
    return "Peace begins with a single, conscious breath."

# --- NAVIGATION ---
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Sukoon</h2>", unsafe_allow_html=True)
nav1, nav2, nav3, nav4 = st.columns([1, 1, 1, 1])

with nav1:
    if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"
with nav2:
    if st.button("Market", use_container_width=True): st.session_state.current_page = "Marketplace"
with nav3:
    if st.button("Vision", use_container_width=True): st.session_state.current_page = "Vision"
with nav4:
    theme_choice = st.radio("Vibe", ["Peaceful", "Midnight"], horizontal=True, label_visibility="collapsed")

# --- THEME COLORS ---
if theme_choice == "Peaceful":
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"
else:
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#333333"

st.markdown(f"""
<style>
    html, body, .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    h1, h2, h3, h4, label, p {{ color: {txt} !important; font-weight: 200 !important; }}
    textarea {{ background-color: {input_bg} !important; color: {txt} !important; border: 1px solid #444 !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {txt} !important; border-radius: 10px; }}
    hr {{ border-top: 1px solid {txt} !important; opacity: 0.3; }}
</style>
""", unsafe_allow_html=True)
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown(f"<div style='text-align: center;'><h3><i>{get_daily_quote()}</i></h3></div>", unsafe_allow_html=True)
    
    st.markdown("#### 🎵 Ambient Sounds")
    audio_type = st.radio("Format", ["Silent", "Library", "YouTube"], horizontal=True)
    if audio_type == "Library":
        choice = st.radio("Sound:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
        # Corrected dictionary format
        files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
        target = files.get(choice)
        if target and os.path.exists(target): st.audio(target)
    
    st.markdown("---")
    with st.form("diary_form", clear_on_submit=True):
        diary_entry = st.text_area("What is on your mind today?")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_entry:
                with st.spinner("Listening..."):
                    try:
                        resp = super_brain.generate_content(diary_entry).text
                        st.success(resp)
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_entry, "ai": resp})
                    except Exception as e:
                        st.error("The Guide is at capacity for today. Please try again tomorrow.")
            else:
                st.warning("The Guide is resting.")

    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- OTHER PAGES ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("## The Marketplace")
    st.write("Grounding items for your journey.")

elif st.session_state.current_page == "Vision":
    st.markdown("## Our Vision")
    st.write("Sukoon exists to provide peace in a loud world.")

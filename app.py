import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# --- USER PHONE ---
MY_PHONE = "918882850790"

# --- AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in models if 'flash' in m), models[0])
        super_brain = genai.GenerativeModel(target_model)
    except:
        super_brain = None
else:
    super_brain = None

# --- UI STATE ---
if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"
if "theme" not in st.session_state:
    st.session_state.theme = "Peaceful"

# --- THEME COLORS ---
soft_blue = "#AEC6CF" 
if st.session_state.theme == "Peaceful":
    bg, txt, input_bg, btn_bg, card_hover = "#F9FDF9", "#2E4032", "white", "transparent", "rgba(74, 112, 85, 0.15)"
else:
    bg, txt, input_bg, btn_bg, card_hover = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A", "rgba(255, 255, 255, 0.05)"

# --- CSS ---
css_code = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; }
    h1, h2, h3, h4, label, p, li { color: V_TXT !important; font-weight: 200 !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; }
    button[kind="secondaryFormSubmit"], .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
    @keyframes breathe {
        0% { transform: scale(1); opacity: 0.4; }
        40% { transform: scale(1.4); opacity: 1; }
        60% { transform: scale(1.4); opacity: 1; }
        100% { transform: scale(1); opacity: 0.4; }
    }
    .breather-circle {
        width: 80px; height: 80px; background: V_BLUE; border-radius: 50%;
        margin: 20px auto; animation: breathe 10s infinite ease-in-out;
        box-shadow: 0 0 25px V_BLUE;
    }
    .ritual-box { padding: 20px; border: 1px solid V_BLUE; border-radius: 15px; background: rgba(174, 198, 207, 0.1); margin: 20px 0; }
    img { border-radius: 15px; margin-bottom: 10px; }
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns([1,1,1])
with n1: 
    if st.button("Journal", use_container_width=True, key="n1"):
        st.session_state.current_page = "Journal"
        st.rerun()
with n2: 
    if st.button("Market", use_container_width=True, key="n2"):
        st.session_state.current_page = "Marketplace"
        st.rerun()
with n3: 
    if st.button("Vision", use_container_width=True, key="n3"):
        st.session_state.current_page = "Vision"
        st.rerun()
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='ritual-box'><b>✨ Ritual:</b> Hold your Natural Stone in your left hand for 3 minutes.</div>", unsafe_allow_html=True)
    st.write("#### How is your energy?")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i in range(5):
        with mood_cols[i]:
            if st.button(mood_labels[i], key=f"m_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                msg = "I see you're in a " + mood_labels[i].lower() + " energy space."
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Energy Check]", "ai": msg})
                st.rerun()
    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("---")
    if hasattr(st, "audio_input"): st.audio_input("Voice Note")
    with st.form(key="j_form", clear_on_submit=True):
        diary_in = st.text_area("Share your heart...")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_in:
                st.session_state.theme = "Midnight" if "sad" in diary_in.lower() else "Peaceful"
                resp = super_brain.generate_content("Mentor response: " + diary_in).text
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_in, "ai": resp})
                st.rerun()
    for entry in reversed(st.session_state.private_journal):
        st.write("🕒 " + entry['time'] + " | " + entry['diary']); st.info(entry['ai'])

# --- PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h2 style='text-align: center;'>Market</h2>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if os.path.exists("buddha.jpg"): st.image("buddha.

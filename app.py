import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# --- AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key is missing! Please check Streamlit Cloud Secrets.")
else:
    genai.configure(api_key=api_key)
    # We use gemini-pro as it's the most globally stable name for v1/v1beta
    try:
        super_brain = genai.GenerativeModel('gemini-1.5-flash')
    except:
        super_brain = genai.GenerativeModel('gemini-pro')

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"

def get_daily_quote():
    try:
        q_prompt = "Create a short, unique 1-sentence mindfulness quote."
        return super_brain.generate_content(q_prompt).text
    except:
        return "Peace begins with a single, conscious breath."

# --- NAVIGATION & THEME ---
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
    bg, txt, accent, card_hover = "#F9FDF9", "#2E4032", "#4A7055", "rgba(74, 112, 85, 0.15)"
    input_bg, btn_bg = "white", "transparent"
else:
    bg, txt, accent, card_hover = "#0A0E0B", "#AEC6CF", "#AEC6CF", "rgba(255, 255, 255, 0.05)"
    input_bg, btn_bg = "#1E1E1E", "#333333"

custom_style = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400&display=swap');
    html, body, .stApp {{ background-color: {bg} !important; color: {txt} !important; font-family: 'Inter', sans-serif !important; }}
    h1, h2, h3, h4, label, p, span {{ color: {txt} !important; font-weight: 200 !important; }}
    hr {{ border-top: 1px solid {txt} !important; opacity: 0.3; }}
    textarea {{ background-color: {input_bg} !important; color: {txt} !important; border: 1px solid #444 !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {txt} !important; border-radius: 10px; }}
    div[data-testid="stColumn"] {{ transition: all 0.4s ease; padding: 10px; border-radius: 20px; }}
    div[data-testid="stColumn"]:hover {{ transform: translateY(-8px); box-shadow: 0px 15px 30px {card_hover}; }}
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], svg {{ display: none !important; }}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)
st.markdown("---")

# --- PAGES ---
if st.session_state.current_page == "Journal":
    st.markdown(f"<div style='text-align: center;'><h3><i>{get_daily_quote()}</i></h3></div>", unsafe_allow_html=True)
    st.markdown("#### 🎵 Ambient Sounds")
    audio_type = st.radio("Format", ["Silent", "Library", "YouTube"], horizontal=True)
    
    if audio_type == "Library":
        choice = st.radio("Sound:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
    elif audio_type == "YouTube":
        v_choice = st.radio("Video:", ["Rain", "Ocean", "Zen"], horizontal=True)
        v_links = {{"Rain": "https://www.youtube.com/watch?v=BIcl7DrBcjg", "Ocean": "https://www.youtube.com/watch?v=unvd_fjiiAQ", "Zen": "https://www.youtube.com/watch?v=UF5H3EfvXTk"}}
        st.video(v_links[v_choice])
        
    st.markdown("---")
    with st.form("diary_form", clear_on_submit=True):
        diary_entry = st.text_area("What is on your mind today?")
        submitted = st.form_submit_button("Consult Guide")
        if submitted:
            if not api_key:
                st.warning("Please set your GEMINI_API_KEY in Secrets.")
            elif diary_entry:
                with st.spinner("Listening..."):
                    try:
                        # Simplified call
                        response = super_brain.generate_content(f"Be a kind mindfulness coach. Respond to: {diary_entry}")
                        ai_text = response.text
                        st.success(ai_text)
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_entry, "ai": ai_text})
                    except Exception as e:
                        st.error(f"The Guide is resting. (Error: {str(e)})")
    
    for entry in reversed(st.session_state.private_journal):
        st.markdown(f"🕒 **{entry['time']}**")
        st.write(f"💭 {entry['diary']}")
        st.write(f"✨ {entry['ai']}")
        st.markdown("---")

elif st.session_state.current_page == "Marketplace":
    st.markdown("## The Marketplace")
    # Marketplace content... (omitted for brevity but kept in your file)

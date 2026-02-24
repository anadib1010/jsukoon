import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# --- AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-1.5-flash')

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "emergency_lock" not in st.session_state:
    st.session_state.emergency_lock = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"

def get_daily_quote():
    try:
        q_prompt = "Create a short, unique 1-sentence mindfulness quote."
        return super_brain.generate_content(q_prompt).text
    except:
        return "Peace begins with a single, conscious breath."

def save_journal(user_text, ai_response):
    now = datetime.now()
    st.session_state.private_journal.append({
        "time": now.strftime("%H:%M"),
        "diary": user_text,
        "ai_advice": ai_response
    })

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

# --- CENTRALIZED CSS (No more syntax errors) ---
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
    if st.session_state.emergency_lock:
        st.error("🚨 CRISIS ALERT")
    else:
        st.markdown(f"<div style='text-align: center;'><h3><i>{get_daily_quote()}</i></h3></div>", unsafe_allow_html=True)
        st.markdown("#### 🎵 Ambient Sounds")
        audio_type = st.radio("Format", ["Silent", "Library", "YouTube"], horizontal=True)
        
        if audio_type == "Library":
            choice = st.radio("Sound:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
            files = {{"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}}
            if os.path.exists(files.get(choice, "")): st.audio(files[choice])
        elif audio_type == "YouTube":
            v_choice = st.radio("Video:", ["Rain", "Ocean", "Zen"], horizontal=True)
            v_links = {{"Rain": "https://www.youtube.com/watch?v=BIcl7DrBcjg", "Ocean": "https://www.youtube.com/watch?v=unvd_fjiiAQ", "Zen": "https://www.youtube.com/watch?v=UF5H3EfvXTk"}}
            st.video(v_links[v_choice])
            
        st.markdown("---")
        with st.form("diary_form"):
            diary_entry = st.text_area("What is on your mind today?")
            if st.form_submit_button("Consult Guide"):
                if diary_entry:
                    with st.spinner("Listening..."):
                        try:
                            response = super_brain.generate_content(f"Empathy for: {diary_entry}").text
                            st.success(response)
                            save_journal(diary_entry, response)
                        except:
                            st.error("Guide is resting.")
        for entry in reversed(st.session_state.private_journal):
            st.write(f"🕒 {entry['time']} | {entry['diary']}")

elif st.session_state.current_page == "Marketplace":
    st.markdown("## The Marketplace")
    def display_product(label, img_file, desc):
        st.markdown(f"#### {label}")
        if os.path.exists(img_file): st.image(img_file, use_container_width=True)
        st.write(desc)
        wa_url = "https://wa.me/919876543210?text=" + urllib.parse.quote(f"Interest: {label}")
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:12px; padding:12px; background-color:#25D366; color:white; border:none; font-weight:bold; cursor:pointer;">💬 WhatsApp</button></a>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: display_product("Natural Stones", "stones.jpg", "Grounding.")
    with c2: display_product("Crafted Beads", "beads.jpg", "Tactile.")
    with c3: display_product("Geometric Yantras", "yantras.jpg", "Focal points.")

elif st.session_state.current_page == "Vision":
    st.markdown("## Our Vision")
    st.write("Sukoon exists to provide peace in a loud world.")
    st.markdown('<a href="https://wa.me/919876543210" target="_blank"><button style="border-radius:10px; padding:12px; background-color:#25D366; color:white; border:none; cursor:pointer;">Message Founder</button></a>', unsafe_allow_html=True)

import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
from google.api_core import exceptions

# --- THE CONFIG (Sidebar hidden, Wide layout) ---
st.set_page_config(page_title="Sukoon", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# WAKE UP THE SUPER BRAIN
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-1.5-flash')

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "emergency_lock" not in st.session_state:
    st.session_state.emergency_lock = False

def get_daily_quote():
    try:
        q_prompt = "Create a unique 1-sentence mindfulness quote."
        q_response = super_brain.generate_content(q_prompt)
        return q_response.text
    except:
        return "Peace begins with a single, conscious breath."

def save_journal(user_text, ai_response, hidden_mood):
    now = datetime.now()
    today = now.strftime("%H:%M")
    entry = {"time": today, "diary": user_text, "ai_advice": ai_response, "mood": hidden_mood}
    st.session_state.private_journal.append(entry)

# ==========================================
# THE TOP NAVIGATION BAR (No Sidebars)
# ==========================================
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([2, 1, 1, 1, 1])

with nav_col1:
    st.markdown("<h2 style='margin-top: -10px;'>Sukoon</h2>", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"

with nav_col2:
    if st.button("Journal 📖", use_container_width=True):
        st.session_state.current_page = "Journal"
with nav_col3:
    if st.button("Marketplace 🛍️", use_container_width=True):
        st.session_state.current_page = "Marketplace"
with nav_col4:
    if st.button("Vision 🕊️", use_container_width=True):
        st.session_state.current_page = "Vision"
with nav_col5:
    # Replaced selectbox with a simple radio toggle to avoid the arrow glitch
    theme_choice = st.radio("Vibe", ["Peaceful", "Midnight"], horizontal=True, label_visibility="collapsed")

# ==========================================
# THE CSS "GLITCH-KILLER"
# ==========================================
font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif !important; }
h1, h2, h3, h4 { font-weight: 200 !important; letter-spacing: -1px !important; }

/* Remove ALL internal Streamlit icons and arrows globally */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], 
svg, span[data-baseweb="icon"], [data-testid="stExpanderChevron"] {
    display: none !important;
}

.stButton>button { 
    font-weight: 300 !important; 
    border-radius: 12px !important; 
    border: 1px solid rgba(0,0,0,0.1);
    height: 45px;
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

if theme_choice == "Peaceful":
    css = """<style>.stApp { background-color: #F9FDF9; color: #2E4032; } h1, h2, h3, h4 { color: #4A7055 !important; } .stButton>button { background-color: transparent; color: #4A7055; border: 1px solid #4A7055; }</style>"""
else: # Midnight
    css = """<style>.stApp { background-color: #121212; color: #E0E0E0; } h1, h2, h3, h4 { color: #AEC6CF !important; } .stButton>button { background-color: transparent; color: #AEC6CF; border: 1px solid #AEC6CF; }</style>"""

st.markdown(css, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# PAGE LOGIC
# ==========================================
if st.session_state.current_page == "Journal":
    if st.session_state.emergency_lock:
        st.error("🚨 CRISIS ALERT: Please seek help.")
    else:
        st.markdown(f"### *{get_daily_quote()}*")
        
        # Audio Section: Using Buttons/Radio instead of Dropdowns
        st.markdown("#### 🎵 Ambient Sounds")
        audio_type = st.radio("Format", ["Silent", "App Library", "YouTube"], horizontal=True, label_visibility="collapsed")
        
        if audio_type == "App Library":
            # Using radio buttons as 'pills' - no arrows!
            choice = st.radio("Choose sound:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
            files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
            if os.path.exists(files[choice]): st.audio(files[choice])
        
        elif audio_type == "YouTube":
            v_choice = st.radio("Choose video:", ["Forest Rain", "Ocean Sunset", "Zen Flute"], horizontal=True)
            v_links = {"Forest Rain": "https://www.youtube.com/watch?v=BIcl7DrBcjg", "Ocean Sunset": "https://www.youtube.com/watch?v=unvd_fjiiAQ", "Zen Flute": "https://www.youtube.com/watch?v=UF5H3EfvXTk"}
            st.video(v_links[v_choice])

        st.markdown("---")
        with st.form("diary_form"):
            diary_entry = st.text_area("Write freely...")
            if st.form_submit_button("Consult Guide"):
                if diary_entry:
                    with st.spinner("Processing..."):
                        try:
                            instr = f"User: '{diary_entry}'. Celebrate joy, soft empathy for grief, or 3 professional tips for office stress. End with a breathing exercise."
                            response = super_brain.generate_content(instr)
                            st.success(response.text)
                            save_journal(diary_entry, response.text, "Processed")
                        except:
                            st.error("The Guide is resting. Try again soon.")

        for entry in reversed(st.session_state.private_journal):
            st.write(f"🕒 {entry['time']} | {entry['diary']}")

elif st.session_state.current_page == "Marketplace":
    st.markdown("## The Marketplace")
    MY_NUMBER = "919876543210" # Your number
    def display_product(label, img_file, desc):
        st.markdown(f"#### {label}")
        if os.path.exists(img_file): st.image(img_file)
        st.write(desc)
        wa_url = f"https://wa.me/{MY_NUMBER}?text=" + urllib.parse.quote(f"Interest: {label}")
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; background-color:#25D366; color:white; border:none; font-weight:bold;">💬 Buy via WhatsApp</button></a>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: display_product("Natural Stones", "stones.jpg", "Grounding stones.")
    with c2: display_product("Crafted Beads", "beads.jpg", "Tactile wooden beads.")
    with c3: display_product("Geometric Yantras", "yantras.jpg", "Focal points.")

elif st.session_state.current_page == "Vision":
    st.markdown("## Our Vision")
    st.write("Sukoon exists to provide peace in a loud world.")
    wa_support = f"https://wa.me/919876543210?text=Support"
    st.markdown(f'<a href="{wa_support}" target="_blank"><button style="border-radius:5px; padding:10px; background-color:#25D366; color:white; border:none;">Message on WhatsApp</button></a>', unsafe_allow_html=True)

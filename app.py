import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
from google.api_core import exceptions

# --- THE CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

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
        q_prompt = "Create a short, unique 1-sentence mindfulness quote."
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
# DYNAMIC STYLING (CSS)
# ==========================================
font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif !important; }
h1, h2, h3, h4 { font-weight: 200 !important; letter-spacing: -1px !important; }

/* Hide Sidebar elements */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], 
svg, span[data-baseweb="icon"], [data-testid="stExpanderChevron"] {
    display: none !important;
}

/* Nav Buttons */
div[data-testid="stHorizontalBlock"] button {
    height: 40px !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
    min-width: 120px !important;
    white-space: nowrap !important;
    font-size: 15px !important;
    border-radius: 10px !important;
}

/* Marketplace Hover */
div[data-testid="stColumn"] {
    padding: 15px;
    transition: all 0.4s ease;
    border-radius: 20px;
}
div[data-testid="stColumn"]:hover {
    transform: translateY(-8px);
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"

# ==========================================
# THE TOP NAVIGATION BAR
# ==========================================
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Sukoon</h2>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])

with nav_col1:
    if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"
with nav_col2:
    if st.button("Marketplace", use_container_width=True): st.session_state.current_page = "Marketplace"
with nav_col3:
    if st.button("Our Vision", use_container_width=True): st.session_state.current_page = "Vision"
with nav_col4:
    theme_choice = st.radio("Vibe", ["Peaceful", "Midnight"], horizontal=True, label_visibility="collapsed")

# Apply Theme Colors
if theme_choice == "Peaceful":
    css = """<style>
    .stApp { background-color: #F9FDF9; color: #2E4032; } 
    h1, h2, h3, h4 { color: #4A7055 !important; } 
    .stButton>button { background-color: transparent; color: #4A7055; border: 1px solid #4A7055; } 
    div[data-testid="stColumn"]:hover { box-shadow: 0px 15px 30px rgba(74, 112, 85, 0.15); background-color: rgba(255,255,255,0.5); }
    </style>"""
else:
    css = """<style>
    .stApp { background-color: #0A0E0B; color: #E0E0E0; } 
    h1, h2, h3, h4, label, .stMarkdown p { color: #AEC6CF !important; } 
    div[data-testid="stRadio"] label p { color: #AEC6CF !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label { color: #AEC6CF !important; }
    textarea { background-color: #1E1E1E !important; color: #E0E0E0 !important; border: 1px solid #333 !important; }
    div.stForm button { background-color: #333333 !important; color: #AEC6CF !important; border: 1px solid #444 !important; }
    div.stForm button:hover { background-color: #444444 !important; }
    .stButton>button { background-color: transparent; color: #AEC6CF; border: 1px solid #AEC6CF; } 
    div[data-testid="stColumn"]:hover { box-shadow: 0px 15px 30px rgba(255, 255, 255, 0.05); background-color: rgba(255,255,255,0.02); }
    </style>"""
st.markdown(css, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# PAGE LOGIC
# ==========================================
if st.session_state.current_page == "Journal":
    if st.session_state.emergency_lock:
        st.error("🚨 CRISIS ALERT")
    else:
        st.markdown(f"<div style='text-align: center; padding: 10px;'><h3><i>{get_daily_quote()}</i></h3></div>", unsafe_allow_html=True)
        st.markdown("#### 🎵 Ambient Sounds")
        audio_type = st.radio("Format", ["Silent", "Library", "YouTube"], horizontal=True)
        if audio_type == "Library":
            choice = st.radio("Sound:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
            files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
            if os.path.exists(files[choice]): st.audio(files[choice])
        elif audio_type == "YouTube":
            v_choice = st.radio("Video:", ["Rain", "Ocean", "Zen"], horizontal=True)
            v_links = {"Rain": "https://www.youtube.com/watch?v=BIcl7DrBcjg", "Ocean": "https://www.youtube.com/watch?v=unvd_fjiiAQ", "Zen": "https://www.youtube.com/watch?v=UF5H3EfvXTk"}
            st.video(v_links[v_choice])
        st.markdown("---")
        with st.form("diary_form"):
            diary_entry = st.text_area("What is on your mind today?")
            if st.form_submit_button("Consult Guide"):
                if diary_entry:
                    with st.spinner("Listening..."):
                        try:
                            instr = f"User: '{diary_entry}'. Empathy for grief, celebrate joy, or office stress tips. End with a breathing exercise."
                            response = super_brain.generate_content(instr)
                            st.success(

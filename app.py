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

/* Hide Sidebar and Glitches */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], 
svg, span[data-baseweb="icon"], [data-testid="stExpanderChevron"] {
    display: none !important;
}

/* Navigation Buttons */
div[data-testid="stHorizontalBlock"] button {
    height: 40px !important;
    padding-left: 15px !important;
    padding-right: 15px !important;
    min-width: 100px !important;
    white-space: nowrap !important;
    font-size: 14px !important;
    border-radius: 10px !important;
}

/* Marketplace Hover Effect */
div[data-testid="stColumn"] {
    padding: 10px;
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
    if st.button("Journal", use_container_width=True): 
        st.session_state.current_page = "Journal"
with nav_col2:
    if st.button("Marketplace", use_container_width=True): 
        st.session_state.current_page = "Marketplace"
with nav_col3:
    if st.button("Our Vision", use_container_width=True): 
        st.session_state.current_page = "Vision"
with nav_col4:
    theme_choice = st.radio("Vibe", ["Peaceful", "Midnight"], horizontal=True, label_visibility="collapsed")

# Apply Theme Colors
if theme_choice == "Peaceful":
    css = """<style>
    .stApp { background-color: #F9FDF9; color: #2E4032; } 
    h1, h2, h3, h4 { color: #4A7055 !important; } 
    hr { border-top: 1px solid #4A7055 !important; opacity: 0.2; }
    .stButton>button { background-color: transparent; color: #4A7055; border: 1px solid #4A7055; } 
    div[data-testid="stColumn"]:hover { box-shadow: 0px 15px 30px rgba(74, 112, 85, 0.15); background-color: rgba(255,255,255,0.5); }
    </style>"""
else:
    css = """<style>
    .stApp { background-color: #0A0E0B; color: #E0E0E0; } 
    h1, h2, h3, h4, label, .stMarkdown p { color: #AEC6CF !

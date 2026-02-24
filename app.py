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

/* Hide Sidebar glitches */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], 
svg, span[data-baseweb="icon"], [data-testid="stExpanderChevron"] {
    display: none !important;
}

/* Navigation Button Styling */
div[data-testid="stHorizontalBlock"] button {
    height: 40px !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
    min-width: 120px !important;
    white-space: nowrap !important;
    font-size: 15px !important;
    border-radius: 10px !important;
}

/* Marketplace Hover Effect */
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
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Suk

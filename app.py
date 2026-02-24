import st
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

/* Marketplace Hover Effect */
div[data-testid="stColumn"] {
    padding: 15px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 15px;
}

div[data-testid="stColumn"]:hover {
    transform: translateY(-5px);
}

.stButton>button { 
    font-weight: 300 !important; 
    border-radius: 12px !important; 
    border: 1px solid rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"

# ==========================================
# THE TOP NAVIGATION BAR
# ==========================================
nav_left, nav_mid, nav_right = st.columns([1, 2, 1])

with nav_left:
    st.markdown("<h2 style='margin-top: -10px;'>Sukoon</h2>", unsafe_allow_html=True)

with nav_mid:
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"
    with btn_col2:
        if st.button("Market", use_container_width=True): st.session_state.current_page = "Marketplace"
    with btn_col3:
        if st.button("Vision", use_container_width=True): st.session_state.current_page = "Vision"

with nav_right:
    theme_choice = st.radio("Vibe", ["Peaceful", "Midnight"], horizontal=True, label_visibility="collapsed")

if theme_choice == "Peaceful":
    css = """<style>.stApp { background-color: #F9FDF9; color: #2E4032; } h1, h2, h3, h4 { color: #4A7055 !important; } .stButton

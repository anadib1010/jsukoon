import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
from google.api_core import exceptions

# --- THE CONFIG ---
st.set_page_config(page_title="Sukoon", initial_sidebar_state="auto")

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
        q_prompt = "Generate a unique 1-sentence mindfulness quote."
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
# THE SIDEBAR
# ==========================================
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio("Go to:", ["Journal", "Marketplace", "Vision"], label_visibility="collapsed")

MY_NUMBER = "919876543210" # Your number

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Atmosphere")
theme = st.sidebar.selectbox("Vibe", ["Peaceful", "Midnight", "Psychedelic"], label_visibility="collapsed")

# --- THE REINFORCED "GLITCH-KILLER" CSS ---
font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif !important; }
h1, h2, h3 { font-weight: 200 !important; letter-spacing: -1px !important; }

/* 1. THE NUCLEAR OPTION: Target the actual text content */
span:contains("keyboard"), 
span:contains("arrow"),
div:contains("keyboard"),
[data-testid="stSidebarCollapseIcon"] {
    visibility: hidden !important;
    display: none !important;
    font-size: 0 !important;
    color: transparent !important;
    width: 0 !important;
    height: 0 !important;
}

/* 2. STYLE THE BUTTON WITHOUT THE TEXT */
button[kind="headerNoPadding"] {
    background-color: rgba(74, 112, 85, 0.1) !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
}

/* 3. ADD A STABLE ICON MANUALLY */
button[kind="headerNoPadding"]::after {
    content: "☰";
    font-size: 20px !important;
    visibility: visible !important;
    display: block !important;
    color: inherit;
    position: absolute;
    left: 10px;
    top: 4px;
}

.stButton>button { font-weight: 300 !important; border-radius: 10px !important; }
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

if theme == "Peaceful":
    css = """<style>.stApp { background-color: #F9FDF9; color: #2E4032; } h1, h2, h3 { color: #4A7055 !important; } .stButton>button { background-color: #4A7055 !important; color: white !important; }</style>"""
elif theme == "Midnight":
    css = """<style>.stApp { background-color: #121212; color: #E0E0E0; } h1, h2, h3 { color: #AEC6CF !important; } .stButton>button { background-color: #AEC6CF !important; color: #121212 !important; }</style>"""
else:
    css = """<style>.stApp { background-image: linear-gradient(120deg, #ff00cc, #3333ff, #00ffcc); background-size: 400% 400%; color: white; } h1, h2, h3 { color: #FFFFFF !important; } .stButton>button { background-color: #0A0520 !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; }</style>"""

st.markdown(css, unsafe_allow_html=True)

wa_support = f"https://wa.me/{MY_NUMBER}?text=Support"
st.sidebar.markdown(f'<a href="{wa_support}" target="_blank"><button style="width:100%; border-radius:5px; padding:8px; background-color:#25D366; color:white; border:none; cursor:pointer;">Contact Founder</button></a>', unsafe_allow_html=True)

# ==========================================
# ROOM 1: THE JOURNAL
# ==========================================
if page == "Journal":
    st.title("Sukoon")
    
    if st.session_state.emergency_lock:
        st.error("🚨 CRISIS ALERT")
    else:
        st.markdown(f"### *{get_daily_quote()}*")
        st.markdown("---")
        st.markdown("#### 🎵 Soundscape")
        
        sound_type = st.radio("Type", ["Silent", "Local Audio", "YouTube"], horizontal=True, label_visibility="collapsed")
        
        if sound_type == "Local Audio":
            choice = st.radio("Select:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
            files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
            if os.path.exists(files[choice]): st.audio(files[choice])
        
        elif sound_type == "YouTube":
            v_choice = st.radio("Select:", ["Rain", "Ocean", "Zen"], horizontal=True)
            v_links = {"Rain": "https://www.youtube.com/watch?v=BIcl7DrBcjg", "Ocean": "https://www.youtube.com/watch?v=unvd_fjiiAQ", "Zen": "https://www.youtube.com/watch?v=UF5H3EfvXTk"}
            st.video(v_links[v_choice])

        st.markdown("---")
        with st.form("diary_form"):
            diary_entry = st.text_area("What is on your mind?")
            if st.form_submit_button("Share with Guide"):
                if diary_entry:
                    with st.spinner("Listening..."):
                        try:
                            instr = f"User: '{diary_entry}'. Celebrate joy, soft empathy for grief, or 3 professional tips for office stress. End with a breathing exercise."
                            response = super_brain.generate_content(instr)
                            st.success(response.text)
                            save_journal(diary_entry, response.text, "Processed")
                        except:
                            st.error("The Guide is in silence. Try again shortly.")

        for entry in reversed(st.session_state.private_journal):
            st.write(f"🕒 {entry['time']} | {entry['diary']}")

# ==========================================
# ROOM 2: THE MARKETPLACE
# ==========================================
elif page == "Marketplace":
    st.title("The Marketplace")
    def display_product(label, img_file, desc):
        st.markdown(f"#### {label}")
        if os.path.exists(img_file): st.image(img_file)
        st.write(desc)
        wa_url = f"https://wa.me/{MY_NUMBER}?text=Interest:{label}"
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:5px; padding:10px; background-color:#25D366; color:white; border:none;">Buy on WhatsApp</button></a>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: display_product("Stones", "stones.jpg", "Grounding naturally sourced stones.")
    with c2: display_product("Beads", "beads.jpg", "Tactile wooden beads.")
    with c3: display_product("Yantras", "yantras.jpg", "Focal points.")
    
# ==========================================
# ROOM 3: OUR VISION
# ==========================================
elif page == "Vision":
    st.title("The Story of Sukoon")
    st.write("Sukoon was born out of a realization: in an increasingly loud world, true luxury is silence and mental clarity.")

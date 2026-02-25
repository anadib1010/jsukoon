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
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in models if 'flash' in m), models[0])
        super_brain = genai.GenerativeModel(target_model)
    except:
        super_brain = None
else:
    super_brain = None

# --- UI STATE & PERSISTENCE ---
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

# --- CSS (With Breath Animation) ---
css_template = """
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
    div[data-testid="stColumn"] { transition: all 0.4s ease; padding: 15px; border-radius: 20px; border: 1px solid rgba(128,128,128,0.1); margin-bottom: 10px; }
    div[data-testid="stColumn"]:hover { transform: translateY(-8px); box-shadow: 0px 15px 30px V_HOV; border: 1px solid V_BLUE; }
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], svg { display: none !important; }
</style>
"""
clean_css = css_template.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_HOV", card_hover).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
nav_cols = st.columns([1,1,1])
with nav_cols[0]:
    if st.button("Journal", use_container_width=True, key="btn_journal"):
        st.session_state.current_page = "Journal"
        st.rerun()
with nav_cols[1]:
    if st.button("Market", use_container_width=True, key="btn_market"):
        st.session_state.current_page = "Marketplace"
        st.rerun()
with nav_cols[2]:
    if st.button("Vision", use_container_width=True, key="btn_vision"):
        st.session_state.current_page = "Vision"
        st.rerun()
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div style='text-align: center;'><h3>Welcome to your sanctuary.</h3></div>", unsafe_allow_html=True)
    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7; letter-spacing: 2px;'>INHALE • HOLD • EXHALE</p>", unsafe_allow_html=True)
    
    st.markdown("#### 🎵 Ambient Sounds")
    choice = st.radio("Select Vibe:", ["Silent", "Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
    if choice != "Silent":
        files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
        target = files.get(choice)
        if target and os.path.exists(target): st.audio(target)
    
    st.markdown("---")
    with st.form(key="journal_entry_form", clear_on_submit=True):
        diary_in = st.text_area("What is on your mind today?")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_in:
                stressors = ["sad", "anxious", "stress", "tired", "dark", "heavy", "pain", "exhausted"]
                st.session_state.theme = "Midnight" if any(w in diary_in.lower() for w in stressors) else "Peaceful"
                with st.spinner("Listening..."):
                    try:
                        resp = super_brain.generate_content("Respond as a mindfulness mentor: " + diary_in).text
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_in, "ai": resp})
                        st.rerun()
                    except:
                        st.error("The Guide is resting.")

    for entry in reversed(st.session_state.private_journal):
        st.write("🕒 " + entry['time'] + " | " + entry['diary'])
        st.info(entry['ai'])

# --- PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h2 style='text-align: center;'>The Marketplace</h2>", unsafe_allow_html=True)
    
    st.markdown("### ✨ Grounding Bundles")
    b_col1, b_col2 = st.columns(2)
    
    bundles = [
        ("The Starter Ritual (3 Items)", "Stones, Buddha, & Beads. ₹2,499", "Ritual Box"),
        ("The Master Sanctuary (5 Items)", "Stones, Buddha, Art, Vaastu, & Journal. ₹4,999", "Ritual Box")
    ]
    
    for i, (name, desc, btype) in enumerate(bundles):
        with (b_col1 if i==0 else b_col2):
            st.markdown(f"#### {name}")
            st.write(desc)
            url = "https://wa.me/919876543210?text=" + urllib.parse.quote("Interest: " + name)
            st.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; cursor:pointer; background-color:{soft_blue}; color:#0A0E0B;">Order {btype}</button></a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏺 Individual Objects")
    items = [
        ("Natural Stones", "Grounding energy."), ("Sacred Buddha", "Stillness focal point."), ("Artic Art", "Visual tranquility."),
        ("Vaastu Objects", "Spatial harmony."), ("Crafted Beads", "Focus through touch."), ("Insight Journals", "Inner clarity.")
    ]
    
    rows = [st.columns(3), st.columns(3)]
    for idx, (iname, idesc) in enumerate(items):
        with rows[idx // 3][idx % 3]:
            st.markdown(f"#### {iname}")
            st.write(idesc)
            i_url = "https://wa.me/919876543210?text=" + urllib.parse.quote("Interest: " + iname)
            st.markdown(f'<a href="{i_url}" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; cursor:pointer; background-color:{soft_blue}; color:#0A0E0B;">Inquire</button></a>', unsafe_allow_html=True)

# --- PAGE: VISION ---
elif st.session_state.current_page == "Vision":
    st.markdown("<h2 style='text-align: center;'>Our Vision</h2>", unsafe_allow_html=True)
    st.write("### Silence in a Loud World")
    st.write("Sukoon is an ecosystem designed to bridge the gap between digital AI guidance and tangible physical grounding. We believe that technology should be a gateway to tranquility, not a source of distraction.")
    st.write("---")
    st.write("### The Journey")
    st.write("We are integrating affective computing to understand human emotion and provide support when it is needed most. This app is the first step toward a personalized, responsive sanctuary.")
    
    wa_v = "https://wa.me/919876543210?text=" + urllib.parse.quote("Support Sukoon")
    st.markdown(f'<div style="text-align: center;"><br><a href="{wa_v}" target="_blank"><button style="padding:10px 25px; border-radius:10px; border:none; font-weight:bold; cursor:pointer; background-color:{soft_blue}; color:#0A0E0B;">💬 Connect with Founder</button></a></div>', unsafe_allow_html=True)

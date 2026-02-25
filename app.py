import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
import time

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

# --- CSS (With Breath Animation) ---
css_template = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; }
    h1, h2, h3, h4, label, p, li { color: V_TXT !important; font-weight: 200 !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; }
    button[kind="secondaryFormSubmit"], .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
    
    /* Breathing Animation (4s Inhale, 2s Hold, 4s Exhale) */
    @keyframes breathe {
        0% { transform: scale(1); opacity: 0.4; }
        40% { transform: scale(1.5); opacity: 1; } /* Inhale (40% of 10s = 4s) */
        60% { transform: scale(1.5); opacity: 1; } /* Hold (20% of 10s = 2s) */
        100% { transform: scale(1); opacity: 0.4; } /* Exhale (40% of 10s = 4s) */
    }
    .breather-circle {
        width: 80px; height: 80px; background: V_BLUE; border-radius: 50%;
        margin: 30px auto; animation: breathe 10s infinite ease-in-out;
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
n1, n2, n3 = st.columns([1,1,1])
with n1: 
    if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"
with n2: 
    if st.button("Market", use_container_width=True): st.session_state.current_page = "Marketplace"
with n3: 
    if st.button("Vision", use_container_width=True): st.session_state.current_page = "Vision"
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div style='text-align: center;'><h3>Welcome to your sanctuary.</h3></div>", unsafe_allow_html=True)
    
    # BREATHWORK VISUAL
    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7; letter-spacing: 2px;'>INHALE • HOLD • EXHALE</p>", unsafe_allow_html=True)
    
    # RESTORED AUDIO LIBRARY
    st.markdown("#### 🎵 Ambient Sounds")
    choice = st.radio("Select Vibe:", ["Silent", "Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
    if choice != "Silent":
        files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
        target = files.get(choice)
        if target and os.path.exists(target): 
            st.audio(target)
        else:
            st.info(f"Playing {choice}... (Ensure {target} is in your GitHub repo)")

    st.markdown("---")
    with st.form("diary_form", clear_on_submit=True):
        diary_entry = st.text_area("What is on your mind today?")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_entry:
                # AFFECTIVE THEME LOGIC
                stress_words = ["sad", "anxious", "stress", "tired", "dark", "exhausted", "heavy", "pain", "angry", "lonely"]
                if any(word in diary_entry.lower() for word in stress_words):
                    st.session_state.theme = "Midnight"
                else:
                    st.session_state.theme = "Peaceful"
                
                with st.spinner("Listening..."):
                    try:
                        resp = super_brain.generate_content("Respond as a calm mindfulness mentor: " + diary_entry).text
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_entry, "ai": resp})
                        st.rerun()
                    except:
                        st.error("The Guide is resting.")

    for entry in reversed(st.session_state.private_journal):
        st.write("🕒 " + entry['time'] + " | " + entry['diary'])
        st.info(entry['ai'])

# --- PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h2 style='text-align: center;'>Grounding Bundles</h2>", unsafe_allow_html=True)
    def display_bundle(title, items, price, desc):
        st.markdown(f"### {title}")
        st.write(desc)
        st.write(f"**Includes:** {items}")
        st.write(f"**Investment:** {price}")
        wa_url = "https://wa.me/919876543210?text=" + urllib.parse.quote(f"I'm interested in {title}")
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:10px; padding:12px; background-color:{soft_blue}; color:#0A0E0B; border:none; font-weight:bold; cursor:pointer;">Order Ritual Box</button></a>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        display_bundle("The Starter Ritual", "Natural Stones, Sacred Buddha, & Crafted Beads.", "₹2,499", "A perfect entry point for daily grounding.")
    with col2:
        display_bundle("The Master Sanctuary", "Stones, Buddha, Art, Vaastu Object, & Insight Journal.", "₹4,999", "A complete overhaul for your physical peace.")

# --- PAGE: VISION ---
elif st.session_state.current_page == "Vision":
    st.markdown("<h2 style='text-align: center;'>Our Vision</h2>", unsafe_allow_html=True)
    st.write("### Silence in a Loud World")
    st.write("Sukoon is an ecosystem designed to bridge the gap between digital AI guidance and tangible physical grounding.")
    wa_support = "https://wa.me/919876543210?text=" + urllib.parse.quote("Hi, I'd like to support the Sukoon vision.")
    st.markdown(f'<div style="text-align: center;"><br><a href="{wa_support}" target="_blank"><button style="padding:10px 25px; border-radius:10px; background-color:{soft_blue}; color:#0A0E0B; border:none; font-weight:bold; cursor:pointer;">💬 Connect with Founder</button></a></div>', unsafe_allow_html=True)

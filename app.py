import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#5B96B2" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "energy_history" not in st.session_state: st.session_state.energy_history = []
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. THEME ---
bg, txt = "#121212", "#E0E0E0"

# --- 4. THE AUTO-WAKE BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None

if api_key:
    genai.configure(api_key=api_key)
    # List of models to try in order of preference
    for m_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]:
        try:
            temp_model = genai.GenerativeModel(m_name)
            # Try a tiny test call
            temp_model.generate_content("Ping", generation_config={"max_output_tokens": 1})
            model = temp_model
            st.toast(f"✅ Sanctuary Brain Awake ({m_name})", icon="🧘")
            break 
        except:
            continue
    
    if not model:
        st.error("🌘 The brain is in deep rest (Quota reached). It will wake up soon.")

# --- 5. THE DESIGN CSS (Centered & Body-Positive) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    .block-container {{
        max-width: 600px !important;
        margin: auto;
        padding-top: 2.5rem !important;
        text-align: center !important;
    }}

    .main-title {{
        text-align: center; letter-spacing: 12px; font-weight: 200; 
        margin-top: 5px; margin-bottom: 5px; font-size: 2.8rem; color: #FFFFFF;
        text-transform: uppercase; width: 100%;
    }}

    .section-header {{
        font-size: 15px !important; font-weight: 400 !important; letter-spacing: 4px !important;
        text-transform: uppercase; margin-top: 25px !important; margin-bottom: 12px !important;
        text-align: center; width: 100%; color: {soft_blue} !important;
    }}

    /* GRID: Balanced Center Alignment */
    [data-testid="stHorizontalBlock"] {{
        gap: 2px !important; 
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }}
    
    div[data-testid="column"] {{
        padding: 0px !important; margin: 0px !important;
        flex: 1 1 0% !important;
        display: flex !important;
        justify-content: center !important;
    }}

    /* GLASSY SLAB BUTTONS */
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(45,45,45,1) 0%, rgba(30,30,30,1) 100%) !important; 
        color: {txt} !important; 
        border: 1px solid #333 !important; 
        border-radius: 4px !important; 
        padding: 0 12px !important;
        min-height: 42px !important; height: 42px !important;
        width: 100% !important; 
        font-size: 12px !important; 
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 2px 4px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{ border-color: {soft_blue} !important; }}

    /* RITUAL COMPONENTS */
    .ritual-prompt {{ font-size: 14px; font-style: italic; color: {soft_blue}; text-align: center; margin: 15px 0; letter-spacing: 1px; }}
    .energy-dot {{ height: 10px; width: 10px; background-color: {soft_blue}; border-radius: 50%; display: inline-block; margin: 0 6px; box-shadow: 0 0 8px {soft_blue}; }}
    
    textarea {{ background: #1A1A1A !important; color: {soft_blue} !important; border: 1px solid #333 !important; border-radius: 8px !important; text-align: center !important; }}
    .footer-text {{ font-size: 10px; opacity: 0.4; margin-top: 50px; text-align: center; padding: 20px; border-top: 1px solid #333; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION & BREATHER ---
st.markdown(f"<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='width:45px; height:45px; border:2px solid {soft_blue}; border-radius:50%; margin:0 auto; animation: breathe 12s infinite ease-in-out;'></div>
        <div style='font-size:12px; margin-top:10px; opacity:0.7; letter-spacing: 2px;'>4-2-6 RHYTHM</div>
    </div>
""", unsafe_allow_html=True)

nav_row = st.columns(3)
nav_list = [("Journal", "Journal"), ("Market", "Market"), ("Vision", "Vision")]

for i, (label, target) in enumerate(nav_list):
    with nav_row[i % 3]:
        if st.button(label, key=f"n_{label}"):
            st.session_state.current_page = target; st.rerun()

# --- 7. PAGES ---
if st.session_state.current_page == "Journal":
    # AMBIENCE
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    aud_cols = st.columns(3)
    sound_list = list(sounds.keys())
    for i, name in enumerate(sound_list):
        with aud_cols[i % 3]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]; st.session_state.audio_label = name

    if st.session_state.active_audio:
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    # RITUAL PROMPT (Safe & Body-Positive)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    prompts = [
        "Close your eyes. Hold your stone.", 
        "Feel the beads between your fingers.", 
        "Observe your Yantra.", 
        "Sense the support of the surface beneath you."
    ]
    st.markdown(f"<div class='ritual-prompt'>— {prompts[datetime.now().second % 4]} —</div>", unsafe_allow_html=True)

    # INPUTS
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Release your thoughts...", height=100)
    
    # THE INTELLIGENT MENTOR RESPONSE (Compassion & Expansion Protocols)
    if st.button("CONSULT GUIDE", key="brain_btn", use_container_width=True):
        if model:
            with st.spinner("Refining..."):
                # Analyze Energy History
                recent = st.session_state.energy_history[-3:]
                is_heavy = len(recent) >= 3 and all(e == "Heavier" for e in recent)
                is_growth = len(recent) >= 3 and all(e in ["Steady", "Vibrant"] for e in recent)
                
                if is_heavy:
                    context = "The user is in a persistent heavy state. Be deeply compassionate and gentle. Suggest a very light grounding ritual. Max 3 sentences."
                elif is_growth:
                    context = "The user is in a state of sustained growth. Celebrate this subtly. Encourage them to 'seal' this calm energy into their physical objects. Max 3 sentences."
                else:
                    context = "You are a Sukoon Mentor. Use secular mindfulness language. Acknowledge grounding objects (beads/stones) if relevant. Max 3 sentences."

                try:
                    user_input = text_msg if text_msg else "I am present."
                    response = model.generate_content([context, user_input])
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": response.text})
                    st.rerun()
                except:
                    st.error("The sanctuary is resting.")

    # ENERGY CHECK & TRACKING
    st.markdown("<div class='section-header'>ENERGY STATE</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, m in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(m, key=f"mood_{m}"):
                st.session_state.energy_history.append(m)
                if len(st.session_state.energy_history) > 6: st.session_state.energy_history.pop(0)
                st.rerun()

    if st.session_state.energy_history:
        st.markdown("<div style='text-align:center; font-size:10px; opacity:0.5; margin-bottom:5px;'>JOURNEY PATH</div>", unsafe_allow_html=True)
        dots = "".join(["<span class='energy-dot'></span>" for _ in st.session_state.energy_history])
        st.markdown(f"<div style='text-align:center;'>{dots}</div>", unsafe_allow_html=True)

    for entry in reversed(st.session_state.private_journal):
        st.info(f"{entry['time']} | {entry['ai']}")

elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>GROUNDING TOOLS</div>", unsafe_allow_html=True)
    st.write("### The Physical Connection")
    st.write("Stones and beads are anchors for your focus and storage for your energy.")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Inquire on WhatsApp</a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>VISION</div>", unsafe_allow_html=True)
    st.write("### Ground | Release | Reflect")
    st.write("A bridge between technology and stillness.")

# FOOTER NAVIGATION
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
f_cols = st.columns(2)
with f_cols[0]:
    if st.button("FAQ", key="f_faq"): st.session_state.current_page = "FAQ"; st.rerun()
with f_cols[1]:
    if st.button("INFO", key="f_info"): st.session_state.current_page = "Info"; st.rerun()

st.markdown("<div class='footer-text'>Sukoon: A Digital & Physical Sanctuary. Not medical advice.</div>", unsafe_allow_html=True)

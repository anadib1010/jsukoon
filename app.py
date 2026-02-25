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

# --- 3. THEME & STYLING ---
bg, txt = "#121212", "#E0E0E0"

# --- 4. THE MODERN BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We try the newest models first (Gemini 3 and 2.5)
        # These are the current standards as of early 2026
        model_found = False
        for model_name in ["gemini-3-flash", "gemini-2.5-flash", "gemini-2.0-flash"]:
            try:
                model = genai.GenerativeModel(model_name)
                # Quick test to confirm access
                model.generate_content("Ping")
                st.toast(f"✅ Sanctuary Brain Active ({model_name})", icon="🧘")
                model_found = True
                break
            except:
                continue
        
        if not model_found:
            st.error("❌ Model Access Error: Your API key doesn't seem to have access to the latest Flash models.")
            model = None
            
    except Exception as e:
        st.error(f"❌ Connection Failed: {e}")
        model = None
else:
    st.warning("⚠️ Waiting for API Key in Secrets...")
    model = None

# --- 5. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 2rem !important; }}
    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; margin-bottom: 5px; font-size: 2.8rem; color: #FFFFFF; text-transform: uppercase; }}
    .section-header {{ font-size: 15px !important; font-weight: 400 !important; letter-spacing: 3px !important; text-transform: uppercase; margin-top: 20px; margin-bottom: 10px; text-align: center; color: {soft_blue} !important; }}
    
    /* GLASSY BUTTONS */
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(45,45,45,1) 0%, rgba(30,30,30,1) 100%) !important; 
        color: {txt} !important; border: 1px solid #333 !important; border-radius: 4px !important; 
        min-height: 42px !important; width: 100% !important; font-size: 12px !important; 
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 2px 4px rgba(0,0,0,0.3) !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
    }}
    
    .ritual-prompt {{ font-size: 13px; font-style: italic; color: {soft_blue}; opacity: 0.8; text-align: center; margin-bottom: 15px; }}
    .energy-dot {{ height: 8px; width: 8px; background-color: {soft_blue}; border-radius: 50%; display: inline-block; margin: 0 4px; opacity: 0.6; }}
    
    [data-testid="stHorizontalBlock"] {{ gap: 2px !important; }}
    textarea {{ background: #1A1A1A !important; color: {soft_blue} !important; border: 1px solid #333 !important; text-align: center !important; border-radius: 8px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. TOP NAVIGATION & BREATHER ---
st.markdown(f"<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><div style='width:45px; height:45px; border:2px solid {soft_blue}; border-radius:50%; margin:0 auto; animation: breathe 12s infinite ease-in-out;'></div><div style='font-size:12px; margin-top:10px; opacity:0.7;'>4-2-6 RHYTHM</div></div>", unsafe_allow_html=True)

nav_cols = st.columns(3)
pages = [("Journal", "Journal"), ("Market", "Market"), ("Vision", "Vision")]
for i, (lab, tar) in enumerate(pages):
    with nav_cols[i]:
        if st.button(lab, key=f"nav_{lab}"): st.session_state.current_page = tar; st.rerun()

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    aud_cols = st.columns(3)
    sounds = ["Birds", "Flute", "Forest", "Waves", "Wind"]
    for i, s in enumerate(sounds):
        with aud_cols[i % 3]:
            if st.button(s, key=f"s_{s}"): st.session_state.active_audio = s.lower() + ".mp3"

    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", autoplay=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ritual-prompt'>— Focus on your grounding object —</div>", unsafe_allow_html=True)

    audio_in = st.audio_input("Voice Note")
    text_in = st.text_area("Record reflection...", height=100)
    
    if st.button("CONSULT GUIDE", use_container_width=True):
        if model:
            with st.spinner("Connecting to Sukoon..."):
                try:
                    prompt = "You are a Sukoon Mentor. Encourage sensory grounding with physical objects. Keep it brief."
                    user_input = text_in if text_in else "I am here."
                    response = model.generate_content(user_input)
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Brain is resting: {e}")
        else:
            st.error("AI is not configured. Check API key.")

    st.markdown("<div class='section-header'>ENERGY STATE</div>", unsafe_allow_html=True)
    m_cols = st.columns(3)
    moods = ["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]
    for i, m in enumerate(moods):
        with m_cols[i % 3]:
            if st.button(m, key=f"mood_{m}"):
                st.session_state.energy_history.append(m)
                if len(st.session_state.energy_history) > 5: st.session_state.energy_history.pop(0)
                st.rerun()

    if st.session_state.energy_history:
        st.markdown("<div style='text-align:center; font-size:10px; opacity:0.5; margin-bottom:5px;'>RECENT ENERGY PATH</div>", unsafe_allow_html=True)
        history_dots = "".join(["<span class='energy-dot'></span>" for _ in st.session_state.energy_history])
        st.markdown(f"<div style='text-align:center;'>{history_dots}</div>", unsafe_allow_html=True)

    for entry in reversed(st.session_state.private_journal):
        st.info(f"{entry['time']} | {entry['ai']}")

# OTHER PAGES (Market/Vision) remain the same...
elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>GROUNDING OBJECTS</div>", unsafe_allow_html=True)
    st.write("Sustain your ritual with physical focus.")

st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
f_cols = st.columns(2)
with f_cols[0]:
    if st.button("FAQ", key="f_faq"): st.session_state.current_page = "FAQ"; st.rerun()
with f_cols[1]:
    if st.button("INFO", key="f_info"): st.session_state.current_page = "Info"; st.rerun()

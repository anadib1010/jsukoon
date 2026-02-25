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

# --- 4. THE ACTIVE BRAIN SETUP (v69.0) ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using the verified gemini-2.5-flash
        model = genai.GenerativeModel("gemini-2.5-flash")
    except:
        model = None

# --- 5. GLASSY SANCTUARY CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 2rem !important; }}
    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; font-size: 2.8rem; color: #FFFFFF; text-transform: uppercase; }}
    
    .section-header {{ font-size: 15px !important; font-weight: 400 !important; letter-spacing: 3px !important; text-transform: uppercase; margin-top: 25px; margin-bottom: 12px; text-align: center; color: {soft_blue} !important; }}
    
    /* GLASSY SLAB BUTTONS */
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(45,45,45,1) 0%, rgba(30,30,30,1) 100%) !important; 
        color: {txt} !important; border: 1px solid #333 !important; border-radius: 4px !important; 
        padding: 0 12px !important; min-height: 42px !important; width: 100% !important; font-size: 12px !important; 
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 2px 4px rgba(0,0,0,0.3) !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
    }}
    .stButton>button:hover {{ border-color: {soft_blue} !important; }}

    /* RITUAL PROMPT */
    .ritual-prompt {{ font-size: 14px; font-style: italic; color: {soft_blue}; text-align: center; margin: 15px 0; letter-spacing: 1px; }}
    
    /* ENERGY DOTS */
    .energy-dot {{ height: 10px; width: 10px; background-color: {soft_blue}; border-radius: 50%; display: inline-block; margin: 0 6px; box-shadow: 0 0 8px {soft_blue}; }}
    
    [data-testid="stHorizontalBlock"] {{ gap: 2px !important; }}
    textarea {{ background: #1A1A1A !important; color: {soft_blue} !important; border: 1px solid #333 !important; text-align: center !important; border-radius: 8px !important; }}
    .footer-text {{ font-size: 10px; opacity: 0.4; margin-top: 50px; text-align: center; padding: 20px; border-top: 1px solid #333; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. TOP SECTION ---
st.markdown(f"<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><div style='width:45px; height:45px; border:2px solid {soft_blue}; border-radius:50%; margin:0 auto; animation: breathe 12s infinite ease-in-out;'></div><div style='font-size:12px; margin-top:10px; opacity:0.7;'>4-2-6 RHYTHM</div></div>", unsafe_allow_html=True)

nav_cols = st.columns(3)
pages = [("Journal", "Journal"), ("Market", "Market"), ("Vision", "Vision")]
for i, (lab, tar) in enumerate(pages):
    with nav_cols[i]:
        if st.button(lab, key=f"n_{lab}"): st.session_state.current_page = tar; st.rerun()

# --- 7. JOURNAL PAGE (THE INFLUENCE LAYER) ---
if st.session_state.current_page == "Journal":
    # 1. AMBIENCE
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    aud_cols = st.columns(3)
    sounds = ["Birds", "Flute", "Forest", "Waves", "Wind"]
    for i, s in enumerate(sounds):
        with aud_cols[i % 3]:
            if st.button(s, key=f"s_{s}"): st.session_state.active_audio = s.lower() + ".mp3"

    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", autoplay=True)

    # 2. RITUAL GROUNDING
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    prompts = ["Close your eyes. Hold your stone.", "Feel the beads between your fingers.", "Observe your Yantra.", "Sense the weight of your body."]
    st.markdown(f"<div class='ritual-prompt'>— {prompts[datetime.now().second % 4]} —</div>", unsafe_allow_html=True)

    audio_in = st.audio_input("Voice Note")
    text_in = st.text_area("Release your thoughts...", height=100)
    
    # 3.UPDATED CONSULT GUIDE LOGIC (Surgical Change)

    if st.button("CONSULT GUIDE", use_container_width=True):
        if model:
            with st.spinner("Holding space..."):
                # Check for the "Heavier" pattern
                recent_energy = st.session_state.energy_history[-3:]
                is_persistent_heavy = len(recent_energy) >= 3 and all(e == "Heavier" for e in recent_energy)
            
                # Dynamic Context based on user's journey
                if is_persistent_heavy:
                    context = ("The user has been feeling 'Heavier' for several sessions. "
                               "Adopt a deeply compassionate, gentle tone. Acknowledge their persistence. "
                               "Suggest a very simple physical grounding task with their stone or beads. "
                               "Remind them that release takes time. Max 3 sentences.")
                else:
                    context = ("You are a Sukoon Mentor. Use secular mindfulness language. "
                               "Acknowledge grounding objects (beads/stones) if relevant. Max 3 sentences.")

                try:
                    user_input = text_in if text_in else "I am here."
                    response = model.generate_content([context, user_input])
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": response.text})
                    st.rerun()
                except Exception as e:
                    st.error("The sanctuary is quiet right now. Please try again.")

    # 4. ENERGY CHECK & TRACKING
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
    st.write("Stones and beads are not just objects; they are anchors for your focus.")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Inquire on WhatsApp</a>", unsafe_allow_html=True)

# FOOTER
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
f_cols = st.columns(2)
with f_cols[0]:
    if st.button("FAQ", key="f_faq"): st.session_state.current_page = "FAQ"; st.rerun()
with f_cols[1]:
    if st.button("INFO", key="f_info"): st.session_state.current_page = "Info"; st.rerun()

st.markdown("<div class='footer-text'>Sukoon: A Digital & Physical Sanctuary. Not medical advice.</div>", unsafe_allow_html=True)

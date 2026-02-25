import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# Initialize Session State
for key in ["private_journal", "current_page", "theme", "active_audio"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful" if key == "theme" else None

# --- 3. THEME ---
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # Using 1.5 Flash for the best balance of speed and reliability
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# --- 5. CSS (FORCE CENTER EVERYTHING) ---
st.markdown(f"""
    <style>
    /* Global alignment */
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .main .block-container {{ 
        display: flex; 
        flex-direction: column; 
        align-items: center !important; 
        text-align: center !important; 
        max-width: 500px !important;
    }}
    
    /* Center all buttons */
    .stButton {{ display: flex; justify-content: center; width: 100%; }}
    .stButton>button {{ 
        background-color: {btn_bg} !important; 
        color: {txt} !important; 
        border: 1px solid {soft_blue} !important; 
        border-radius: 12px !important; 
        width: 100% !important; 
        margin: 5px auto !important;
        display: block !important;
    }}
    
    /* Center Audio */
    div[data-testid="stAudio"] {{ display: flex; justify-content: center; width: 100%; }}
    
    /* Center Text Areas & Inputs */
    .stTextArea, .stAudioInput {{ width: 100% !important; display: flex; justify-content: center; }}
    textarea {{ text-align: center !important; border-radius: 12px !important; border: 1px solid {soft_blue} !important; }}

    .breather-circle {{ width: 70px; height: 70px; background: {soft_blue}; border-radius: 50%; margin: 25px auto; animation: breathe 8s infinite ease-in-out; box-shadow: 0 0 15px {soft_blue}; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION (Centered) ---
st.markdown("<h1 style='text-align: center;'>Sukoon</h1>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nav1"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nav2"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nav3"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    # Energy Buttons
    st.write("#### How is your energy?")
    m_cols = st.columns(5)
    for i, lab in enumerate(["Low", "Drained", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # Nature Ambience (Centered Row)
    st.write("#### Nature Ambience")
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    aud_cols = st.columns(5)
    for idx, name in enumerate(sounds.keys()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        st.markdown(f"🔊 Playing: **{st.session_state.audio_label}**")
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    
    # AI INPUT
    audio_rec = st.audio_input("Record a note")
    text_msg = st.text_area("Share your heart...", placeholder="Type here...")
    
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("The Guide is reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Respond in 1 calm paragraph."]
                    if audio_rec:
                        parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                    else:
                        parts.append(text_msg)
                    
                    response = model.generate_content(parts).text
                    st.session_state.private_journal.append({
                        "id": datetime.now().strftime("%H%M%S"), 
                        "time": datetime.now().strftime("%H:%M"), 
                        "ai": response
                    })
                    st.rerun()
                except:
                    st.error("The Brain is pausing. Please wait 60 seconds and try again.")
        else:
            st.warning("Guide is offline. Check your API Key.")

    # HISTORY
    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")
        st.write("---")

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div style='border:1px solid {soft_blue}; padding:15px; border-radius:12px;'>Starter Ritual<br>₹2,499<br><a href='https://wa.me/{MY_PHONE}?text=Starter' style='color:{soft_blue}; text-decoration:none; font-weight:bold;'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div style='border:1px solid {soft_blue}; padding:15px; border-radius:12px;'>Master Sanctuary<br>₹4,999<br><a href='https://wa.me/{MY_PHONE}?text=Master' style='color:{soft_blue}; text-decoration:none; font-weight:bold;'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}?text=Vision' style='display:block; border:1px solid {soft_blue}; padding:15px; border-radius:12px; text-decoration:none; color:{soft_blue}; font-weight:bold;'>Connect with Founder</a>", unsafe_allow_html=True)

st.markdown("<hr><div style='opacity:0.6; font-size:10px; text-align:center;'>Mindfulness Support. Not Medical Advice.</div>", unsafe_allow_html=True)

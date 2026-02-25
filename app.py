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
brain_online = False
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        brain_online = True
    except: model = None
else: model = None

# --- 5. CENTERED CSS ---
st.markdown(f"""
    <style>
    /* Global Centering */
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .main .block-container {{ display: flex; flex-direction: column; align-items: center !important; text-align: center !important; }}
    
    /* Button Centering & Styling */
    .stButton {{ display: flex; justify-content: center; width: 100%; }}
    .stButton>button {{ 
        background-color: {btn_bg} !important; 
        color: {txt} !important; 
        border: 1px solid {soft_blue} !important; 
        border-radius: 12px !important; 
        width: 90% !important; 
        margin: 5px auto !important;
    }}
    
    /* Audio Widget Centering */
    div[data-testid="stAudio"] {{ display: flex; justify-content: center; width: 100%; }}
    
    .breather-circle {{ width: 65px; height: 65px; background: {soft_blue}; border-radius: 50%; margin: 20px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .mkt-box {{ border: 1px solid {soft_blue}; padding: 15px; border-radius: 12px; margin-bottom: 10px; background: rgba(174, 198, 207, 0.05); width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION (Centered Columns) ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nj"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nm"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nv"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    # Mood Buttons
    m_cols = st.columns(5)
    for i, lab in enumerate(["Low", "Drained", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(lab, key=f"md_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # --- CENTERED AUDIO BUTTONS ---
    st.markdown("<p style='font-weight: bold;'>Nature Ambience</p>", unsafe_allow_html=True)
    cdn_base = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    aud_cols = st.columns(5)
    for idx, name in enumerate(sounds.keys()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]
                st.session_state.audio_label = name

    if st.session_state.active_audio:
        file_url = f"{cdn_base}{st.session_state.active_audio}"
        st.markdown(f"🔊 Playing: **{st.session_state.audio_label}**")
        st.audio(file_url, format="audio/mp3", autoplay=True)

    st.markdown("---")
    
    # AI INPUT (Centered)
    audio_data = st.audio_input("Record")
    text_in = st.text_area("Share your heart...", placeholder="Type here...")
    
    if st.button("Consult Guide", use_container_width=True, key="submit_brain"):
        if brain_online:
            with st.spinner("Reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Respond in 1 paragraph."]
                    if audio_data: parts.append({"mime_type": "audio/wav", "data": audio_data.read()})
                    else: parts.append(text_in)
                    response = model.generate_content(parts).text
                    st.session_state.private_journal.append({
                        "id": datetime.now().strftime("%H%M%S"), "time": datetime.now().strftime("%H:%M"), 
                        "diary": text_in if text_in else "🎙️ Voice Entry", "ai": response
                    })
                    st.rerun()
                except: st.error("The Brain is resting.")
        else: st.warning("Guide Status: Resting.")

    # HISTORY
    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")
        st.write("---")

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h3>✨ Grounding Objects</h3>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div class='mkt-box'>Starter Ritual<br>₹2,499<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='mkt-box'>Master Sanctuary<br>₹4,999<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.markdown("<h3>Silence in a Loud World</h3>", unsafe_allow_html=True)
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' class='mkt-box' style='display:block; text-decoration:none; color:{soft_blue};'>Connect with Founder</a>", unsafe_allow_html=True)

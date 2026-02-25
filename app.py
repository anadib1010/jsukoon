import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "manavprakash" 
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

for key in ["private_journal", "current_page", "theme", "active_audio"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful" if key == "theme" else None

# --- 3. THEME LOGIC ---
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
brain_online = False
try:
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        brain_online = True
except: brain_online = False

# --- 5. SCRIPTS & CSS ---
st.markdown(f"""
    <script>
    function speakNow(text) {{
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance(text);
        msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    }}
    </script>
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; text-align: center !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {soft_blue} !important; border-radius: 10px !important; width: 100%; }}
    .breather-circle {{ width: 60px; height: 60px; background: {soft_blue}; border-radius: 50%; margin: 15px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .status-light {{ height: 8px; width: 8px; border-radius: 50%; display: inline-block; margin-right: 5px; }}
    .mkt-box {{ border: 1px solid {soft_blue}; padding: 15px; border-radius: 12px; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
status_col = "#4CAF50" if brain_online else "#F44336"
st.markdown(f"<div style='font-size:10px;'><span class='status-light' style='background-color:{status_col};'></span>Guide: {'Ready' if brain_online else 'Resting'}</div>", unsafe_allow_html=True)

n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="n_j"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="n_m"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="n_v"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    # MOODS
    m_cols = st.columns(5)
    for i, lab in enumerate(["Low", "Drained", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(lab, key=f"md_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # --- HORIZONTAL AUDIO BUTTONS ---
    st.write("#### Nature Ambience")
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    
    # Horizontal Buttons
    aud_cols = st.columns(5)
    for idx, (name, file) in enumerate(sounds.items()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = name

    # Hidden Player that auto-plays when state changes
    if st.session_state.active_audio:
        st.write(f"🔊 Playing: **{st.session_state.active_audio}**")
        file_name = sounds[st.session_state.active_audio]
        st.audio(f"{base_url}{file_name}", autoplay=True)

    st.markdown("---")
    
    # AI INPUT
    audio_rec = st.audio_input("Record")
    text_in = st.text_area("Share your heart...")
    
    if st.button("Consult Guide", use_container_width=True):
        if brain_online:
            with st.spinner("Reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Respond in 1 paragraph."]
                    if audio_rec:
                        parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                        parts.append("Start with: 'I heard you say...'")
                    else: parts.append(text_in)
                    
                    response = model.generate_content(parts).text
                    st.session_state.private_journal.append({
                        "id": datetime.now().strftime("%H%M%S"),
                        "time": datetime.now().strftime("%H:%M"), 
                        "diary": text_in if text_in else "🎙️ Voice Entry", "ai": response
                    })
                    st.rerun()
                except: st.error("Guide is resting.")

    # HISTORY
    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")
        if st.button("🔊 Hear", key=f"h_{entry['id']}"):
            st.markdown(f"<script>speakNow({repr(entry['ai'])})</script>", unsafe_allow_html=True)
        st.write("---")

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.write("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div class='mkt-box'>Starter Ritual<br>₹2,499<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='mkt-box'>Master Sanctuary<br>₹4,999<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue};'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' class='wa-link' style='color:{soft_blue};'>Connect with Founder</a>", unsafe_allow_html=True)

st.markdown("<hr><div style='opacity:0.6; font-size:10px; text-align:center;'>Mindfulness support. Not medical advice.</div>", unsafe_allow_html=True)

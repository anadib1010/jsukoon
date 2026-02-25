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

for key in ["private_journal", "current_page", "theme"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful"

# --- 3. THEME LOGIC ---
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP & STATUS ---
api_key = os.environ.get("GEMINI_API_KEY")
brain_online = False
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Test if the model is responsive
        brain_online = True
    except:
        brain_online = False

# --- 5. CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; text-align: center !important; }}
    .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid {soft_blue} !important; border-radius: 12px !important; }}
    .breather-circle {{ width: 60px; height: 60px; background: {soft_blue}; border-radius: 50%; margin: 15px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .status-light {{ height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
status_color = "#4CAF50" if brain_online else "#F44336"
st.markdown(f"<div style='font-size:12px; margin-bottom:10px;'><span class='status-light' style='background-color:{status_color};'></span>Guide Status: {'Ready' if brain_online else 'Resting'}</div>", unsafe_allow_html=True)

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
    # Mood Selection
    m_cols = st.columns(5)
    m_labs = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(m_labs):
        with m_cols[i]:
            if st.button(lab, key=f"mood_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # --- UPDATED NATURE AMBIENCE (Confirmed Filenames) ---
    st.write("#### Nature Ambience")
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    
    # Precise filenames as per your confirmation
    sounds = {
        "Birds": "birds.mp3", 
        "Flute": "flute.mp3", 
        "Forest": "forest.mp3", 
        "Waves": "waves.mp3", 
        "Wind": "wind.mp3"
    }
    
    # Display audio players
    for name, file in sounds.items():
        st.write(f"_{name}_")
        st.audio(f"{base_url}{file}")

    st.markdown("---")
    
    # AI INPUT
    audio_data = st.audio_input("Record")
    text_in = st.text_area("Share your heart...")
    
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Give a calm 1-paragraph response."]
                    if audio_data:
                        parts.append({"mime_type": "audio/wav", "data": audio_data.read()})
                        parts.append("Include a transcription of what you heard.")
                    else:
                        parts.append(text_in)

                    response = model.generate_content(parts).text
                    uid = datetime.now().strftime("%H%M%S")
                    st.session_state.private_journal.append({
                        "id": uid, "time": datetime.now().strftime("%H:%M"), 
                        "diary": text_in if text_in else "🎙️ Voice Entry", "ai": response
                    })
                    st.rerun()
                except:
                    st.error("Brain is resting. Please breathe and try again later.")

    # HISTORY
    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")
        st.write("---")

# --- 8. MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.write("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div style='border:1px solid {soft_blue}; padding:10px; border-radius:12px;'>Starter Ritual<br>₹2,499<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue}; text-decoration:none; font-weight:bold;'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div style='border:1px solid {soft_blue}; padding:10px; border-radius:12px;'>Master Sanctuary<br>₹4,999<br><a href='https://wa.me/{MY_PHONE}' style='color:{soft_blue}; text-decoration:none; font-weight:bold;'>Order</a></div>", unsafe_allow_html=True)

st.markdown("<hr><div style='opacity:0.6; font-size:10px; text-align:center;'>This app offers mindfulness support and is not a substitute for medical advice.</div>", unsafe_allow_html=True)

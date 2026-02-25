import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import time

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
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A"
else:
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# --- 5. SCRIPTS ---
st.markdown(f"""
    <script>
    function speakNow(text) {{
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance(text);
        msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """, unsafe_allow_html=True)

css_code = """
<style>
    html, body, .stApp {{ background-color: V_BG !important; color: V_TXT !important; text-align: center !important; }}
    .stButton>button {{ background-color: V_BTN !important; color: V_TXT !important; border: 1px solid V_BLUE !important; border-radius: 12px !important; margin: 5px auto !important; }}
    .breather-circle {{ width: 60px; height: 60px; background: V_BLUE; border-radius: 50%; margin: 15px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .mkt-box {{ border: 1px solid V_BLUE; padding: 15px; border-radius: 12px; margin-bottom: 10px; }}
    .wa-link {{ display: block; background: V_BLUE; color: #0A0E0B; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; }}
    div[data-testid="stAudio"] {{ filter: grayscale(0) !important; }}
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nav_j_unique"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nav_m_unique"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nav_v_unique"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    m_cols = st.columns(5)
    m_labs = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(m_labs):
        with m_cols[i]:
            if st.button(lab, key=f"mood_btn_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    st.write("#### Nature Ambience")
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    sounds = {"Waves": "waves.mp3", "Birds": "birds.mp3", "Rain": "rain.mp3", "Forest": "forest.mp3", "Flute": "flute.mp3"}
    ac = st.columns(5)
    for idx, (name, file) in enumerate(sounds.items()):
        with ac[idx]:
            st.write(f"**{name}**")
            # Using the RAW domain which is more reliable for direct streaming
            st.audio(f"{base_url}{file}")

    st.markdown("---")
    
    # AI INPUT
    audio_data = st.audio_input("Record your thoughts")
    text_in = st.text_area("Or type here...", placeholder="How are you feeling?")
    
    if st.button("Consult Guide", use_container_width=True, key="main_submit_btn"):
        if model:
            with st.spinner("The Guide is reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Respond with warmth in 1 paragraph."]
                    if audio_data:
                        audio_bytes = audio_data.read()
                        parts.append({"mime_type": "audio/wav", "data": audio_bytes})
                        parts.append("Start by saying 'I heard you say:' followed by a transcription.")
                    else:
                        parts.append(text_in)

                    response = model.generate_content(parts).text
                    # Use unique ID based on seconds to avoid the 'Duplicate Key' error
                    uid = datetime.now().strftime("%H%M%S")
                    st.session_state.private_journal.append({
                        "id": uid,
                        "time": datetime.now().strftime("%H:%M"), 
                        "diary": text_in if text_in else "🎙️ Voice Entry", 
                        "ai": response
                    })
                    st.rerun()
                except Exception as e:
                    st.error("The Brain is resting. Breathe and try again in a moment.")

    # HISTORY DISPLAY
    for entry in reversed(st.session_state.private_journal):
        with st.container():
            st.write(f"🕒 **{entry['time']}**")
            st.write(f"_{entry['diary']}_")
            st.info(entry['ai'])
            if st.button("🔊 Hear", key=f"hear_{entry['id']}"):
                st.markdown(f"<script>speakNow({repr(entry['ai'])})</script>", unsafe_allow_html=True)
            st.write("---")

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.write("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div class='mkt-box'><h4>Starter Ritual</h4>₹2,499<br><br><a href='https://wa.me/{MY_PHONE}' class='wa-link'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='mkt-box'><h4>Master Sanctuary</h4>₹4,999<br><br><a href='https://wa.me/{MY_PHONE}' class='wa-link'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.write("Bridging the digital and physical for inner peace.")
    st.markdown(f"<br><br><a href='https://wa.me/{MY_PHONE}' class='wa-link' style='width:200px; margin:0 auto;'>Connect</a>", unsafe_allow_html=True)

st.markdown("<hr><div style='opacity:0.6; font-size:10px; text-align:center;'>This app provides mindfulness support, not medical advice.</div>", unsafe_allow_html=True)

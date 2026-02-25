import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
# Ensure this matches your GitHub username exactly
GITHUB_USER = "manavprakash" 
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# Initialize Session State
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
    # Using 1.5 Flash as it is the most stable for Multimodal
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
    .stButton>button {{ background-color: V_BTN !important; color: V_TXT !important; border: 1px solid V_BLUE !important; border-radius: 12px !important; }}
    .breather-circle {{ width: 60px; height: 60px; background: V_BLUE; border-radius: 50%; margin: 15px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    .mkt-box {{ border: 1px solid V_BLUE; padding: 15px; border-radius: 12px; margin-bottom: 10px; }}
    .wa-link {{ display: block; background: V_BLUE; color: #0A0E0B; padding: 8px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 5px; }}
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
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
    m_cols = st.columns(5)
    m_labs = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, lab in enumerate(m_labs):
        with m_cols[i]:
            if st.button(lab, key=f"m_{i}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)

    # NATURE AMBIENCE (Improved URL Format)
    st.write("#### Nature Ambience")
    # This format is more likely to work with Streamlit's audio widget
    base_url = f"https://github.com/{GITHUB_USER}/sukoon/blob/main/"
    sounds = {"Waves": "waves.mp3", "Birds": "birds.mp3", "Rain": "rain.mp3", "Forest": "forest.mp3", "Flute": "flute.mp3"}
    ac = st.columns(5)
    for idx, (name, file) in enumerate(sounds.items()):
        with ac[idx]:
            st.write(f"**{name}**")
            # Adding ?raw=true is a secret trick for GitHub audio
            st.audio(f"{base_url}{file}?raw=true")

    st.markdown("---")
    
    # AI INPUT
    audio_data = st.audio_input("Record")
    text_in = st.text_area("Share your heart...")
    
    if st.button("Consult Guide", use_container_width=True):
        if not model:
            st.error("API Key missing.")
        else:
            with st.spinner("Reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Give a calm 1-paragraph response."]
                    if audio_data:
                        parts.append({"mime_type": "audio/wav", "data": audio_data.read()})
                        parts.append("Also, start your reply by transcribing what you heard in one sentence.")
                    else:
                        parts.append(text_in)

                    response = model.generate_content(parts).text
                    st.session_state.private_journal.append({
                        "time": datetime.now().strftime("%H:%M"), 
                        "diary": text_in if text_in else "🎙️ Voice Note", 
                        "ai": response
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Brain is resting. Please try again in a moment.")

    # HISTORY
    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")
        if st.button("🔊 Hear", key=f"btn_{entry['time']}"):
            st.markdown(f"<script>speakNow({repr(entry['ai'])})</script>", unsafe_allow_html=True)
        st.write(f"---")

# --- 8. OTHER PAGES ---
elif st.session_state.current_page == "Marketplace":
    st.write("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1: st.markdown(f"<div class='mkt-box'><h4>Starter Ritual</h4>₹2,499<a href='https://wa.me/{MY_PHONE}' class='wa-link'>Order</a></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='mkt-box'><h4>Master Sanctuary</h4>₹4,999<a href='https://wa.me/{MY_PHONE}' class='wa-link'>Order</a></div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' class='wa-link'>Connect with Founder</a>", unsafe_allow_html=True)

st.markdown("<hr><div style='opacity: 0.6; font-size: 10px; text-align: center;'>Not medical advice.</div>", unsafe_allow_html=True)

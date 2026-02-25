import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import base64

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
soft_blue = "#AEC6CF" 

# --- 2. CONFIG & STATE ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"
if "theme" not in st.session_state:
    st.session_state.theme = "Peaceful"

# --- 3. THEME LOGIC ---
if st.session_state.theme == "Peaceful":
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"
else:
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    super_brain = genai.GenerativeModel("gemini-1.5-flash")
else:
    super_brain = None

# --- 5. CSS & VOICE SCRIPT ---
# This JavaScript allows the browser to speak the AI's response out loud
st.markdown("""
    <script>
    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9; // Slightly slower for peace
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
    </script>
    """, unsafe_allow_html=True)

css_code = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; }
    h1, h2, h3, h4, p, li { color: V_TXT !important; font-weight: 200 !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; }
    .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
    .breather-circle { width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; box-shadow: 0 0 25px V_BLUE; }
    @keyframes breathe { 0% { transform: scale(1); opacity: 0.4; } 40% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(1); opacity: 0.4; } }
    .ritual-box { padding: 15px; border: 1px solid V_BLUE; border-radius: 12px; background: rgba(174, 198, 207, 0.1); margin: 15px 0; }
    .mkt-btn { width:100%; padding:10px; background:V_BLUE; border:none; border-radius:10px; font-weight:bold; color:#0A0E0B; text-align:center; display:block; text-decoration:none; }
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nav_j"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nav_m"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nav_v"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='ritual-box'><b>✨ Ritual:</b> Hold your Natural Stone for 3 minutes.</div>", unsafe_allow_html=True)
    
    # ENERGY BUTTONS
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"m_{i}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Energy Check]", "ai": f"I see you're in a {label.lower()} energy space."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    
    # VOICE & TEXT INPUT
    st.write("#### Speak or Type")
    audio_file = st.audio_input("Record your voice")
    
    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("What's on your mind?")
        submit = st.form_submit_button("Consult Guide")
        
        if submit and super_brain:
            content_to_send = []
            user_display_text = ""

            if audio_file:
                # Processing Audio
                audio_bytes = audio_file.read()
                content_to_send.append({"mime_type": "audio/wav", "data": audio_bytes})
                user_display_text = "🎙️ Voice Note Sent"
            elif text_in:
                content_to_send.append(text_in)
                user_display_text = text_in

            if content_to_send:
                prompt = "You are a calm mindfulness mentor for the app Sukoon. If audio is provided, transcribe it first. Then, respond to the user's feelings with warmth and brevity (max 2 paragraphs). Speak directly to them."
                with st.spinner("Listening..."):
                    try:
                        response = super_brain.generate_content([prompt] + content_to_send)
                        ai_resp = response.text
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": user_display_text, "ai": ai_resp})
                        
                        # Trigger Voice Output
                        js_speak = f"<script>speak({repr(ai_resp)})</script>"
                        st.markdown(js_speak, unsafe_allow_html=True)
                        st.rerun()
                    except:
                        st.error("The Guide is resting. Please breathe and try in 60 seconds.")

    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- 8. PAGE: MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Bundles"); b1, b2 = st.columns(2)
    with b1: st.markdown(f'#### Starter\n₹2,499\n<a href="https://wa.me/{MY_PHONE}?text=Starter" class="mkt-btn">Order</a>', unsafe_allow_html=True)
    with b2: st.markdown(f'#### Master\n₹4,999\n<a href="https://wa.me/{MY_PHONE}?text=Master" class="mkt-btn">Order</a>', unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World\nSukoon bridges digital AI and physical grounding.")
    st.markdown(f'<br><a href="https://wa.me/{MY_PHONE}?text=Support" class="mkt-btn">Connect with Founder</a>', unsafe_allow_html=True)

# --- 10. GLOBAL FOOTER ---
st.markdown("---")
st.markdown("<div style='opacity: 0.6; font-size: 11px; text-align: center;'>“This app offers a quiet digital space. It does not provide therapy, counseling, medical advice, or emergency support.”</div>", unsafe_allow_html=True)

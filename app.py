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

# --- 5. CSS & SENSORY SCRIPTS ---
# Enhanced JavaScript for Voice Quality and Visual Feedback
st.markdown("""
    <script>
    function speakWithVisuals(text) {
        const msg = new SpeechSynthesisUtterance(text);
        
        // Voice Quality: Pick a more natural sounding voice if available
        const voices = window.speechSynthesis.getVoices();
        const naturalVoice = voices.find(v => v.name.contains('Google') || v.name.contains('Natural')) || voices[0];
        msg.voice = naturalVoice;
        msg.rate = 0.85; // Calmer pace
        msg.pitch = 1.0;

        const wave = document.getElementById('voice-wave');
        
        msg.onstart = function() {
            wave.style.display = 'block';
        };
        msg.onend = function() {
            wave.style.display = 'none';
        };
        
        window.speechSynthesis.speak(msg);
    }
    </script>
    """, unsafe_allow_html=True)

css_code = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; text-align: center !important; }
    h1, h2, h3, h4, p, li, label { color: V_TXT !important; font-weight: 200 !important; text-align: center !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; text-align: left !important; }
    .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; margin: 0 auto !important; display: block !important; }
    
    /* The Breathing Circle */
    .breather-circle { width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; box-shadow: 0 0 25px V_BLUE; }
    @keyframes breathe { 0% { transform: scale(1); opacity: 0.4; } 40% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(1); opacity: 0.4; } }
    
    /* NEW: Voice Waveform Feedback */
    #voice-wave { 
        display: none; width: 100px; height: 30px; margin: 10px auto;
        background: linear-gradient(90deg, transparent, V_BLUE, transparent);
        background-size: 200% 100%; animation: wave-pulse 1.5s infinite linear;
        border-radius: 15px;
    }
    @keyframes wave-pulse { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

    .ritual-box { padding: 15px; border: 1px solid V_BLUE; border-radius: 12px; background: rgba(174, 198, 207, 0.1); margin: 15px auto; max-width: 90%; }
    .mkt-btn { width: 80%; padding: 10px; background: V_BLUE; border:none; border-radius: 10px; font-weight: bold; color: #0A0E0B; text-align: center; display: block; margin: 10px auto; text-decoration: none; }
    div[data-testid="stAudioInput"] { display: flex; justify-content: center; }
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="nav_j", use_container_width=True): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="nav_m", use_container_width=True): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="nav_v", use_container_width=True): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='ritual-box'><b>✨ Ritual</b><br>Hold your Natural Stone for 3 minutes.</div>", unsafe_allow_html=True)
    
    # ENERGY CHECK
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"m_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Energy Check]", "ai": f"I see you're in a {label.lower()} energy space."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<div id='voice-wave'></div>", unsafe_allow_html=True) # Waveform element
    st.markdown("---")
    
    st.write("#### Speak or Type")
    audio_file = st.audio_input("Record your voice")
    
    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("What's on your mind?")
        submit = st.form_submit_button("Consult Guide")
        
        if submit and super_brain:
            content_to_send = []
            if audio_file:
                audio_bytes = audio_file.read()
                content_to_send.append({"mime_type": "audio/wav", "data": audio_bytes})
                display_label = "🎙️ Listening to your voice..."
            else:
                content_to_send.append(text_in)
                display_label = text_in

            if content_to_send:
                # UPDATED PROMPT: Requesting transcription echoing
                prompt = (
                    "You are a calm mindfulness mentor for Sukoon. "
                    "First, transcribe what the user said in a single line starting with 'TRANSCRIPTION: '. "
                    "Then, give a warm, brief response (max 2 paragraphs). "
                    "Speak directly to the user."
                )
                with st.spinner("Processing..."):
                    try:
                        response = super_brain.generate_content([prompt] + content_to_send)
                        raw_text = response.text
                        
                        # Separate Transcription from AI Response
                        if "TRANSCRIPTION:" in raw_text:
                            parts = raw_text.split("TRANSCRIPTION:", 1)[1].split("\n", 1)
                            user_said = parts[0].strip()
                            ai_wisdom = parts[1].strip() if len(parts) > 1 else "I hear you."
                        else:
                            user_said = display_label
                            ai_wisdom = raw_text

                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": user_said, "ai": ai_wisdom})
                        
                        # Use Enhanced Speak Function
                        js_speak = f"<script>speakWithVisuals({repr(ai_wisdom)})</script>"
                        st.markdown(js_speak, unsafe_allow_html=True)
                        st.rerun()
                    except:
                        st.error("The Guide is resting. Please try in 60 seconds.")

    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Grounding Bundles")
    b1, b2 = st.columns(2)
    with b1: st.markdown(f'#### Starter Ritual\n₹2,499\n<a href="https://wa.me/{MY_PHONE}?text=Starter" class="mkt-btn">Order</a>', unsafe_allow_html=True)
    with b2: st.markdown(f'#### Master Sanctuary\n₹4,999\n<a href="https://wa.me/{MY_PHONE}?text=Master" class="mkt-btn">Order</a>', unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.markdown(f'<br><a href="https://wa.me/{MY_PHONE}?text=Support" class="mkt-btn" style="width: 250px;">Connect</a>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='opacity: 0.6; font-size: 11px; text-align: center;'>“This app offers a quiet digital space. It does not provide therapy, counseling, medical advice, or emergency support.”</div>", unsafe_allow_html=True)

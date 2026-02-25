import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

for key in ["private_journal", "current_page", "theme"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful"

# --- 3. THEME ---
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

# --- 5. SENSORY SCRIPTS (Voice, Waveform, & Live Typing) ---
st.markdown(f"""
    <script>
    // 1. LIVE TYPING ENGINE
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    function startListening() {{
        recognition.start();
        document.getElementById('mic-status').innerText = '🎙️ Listening...';
    }}

    recognition.onresult = function(event) {{
        const text = event.results[0][0].transcript;
        const textArea = window.parent.document.querySelector('textarea');
        if(textArea) {{
            textArea.value = text;
            textArea.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        document.getElementById('mic-status').innerText = '✅ Transcribed';
    }};

    // 2. NATURAL VOICE & WAVEFORM ENGINE
    function speakWithVisuals(text) {{
        const msg = new SpeechSynthesisUtterance(text);
        const voices = window.speechSynthesis.getVoices();
        msg.voice = voices.find(v => v.name.includes('Google') || v.name.includes('Natural')) || voices[0];
        msg.rate = 0.85;
        
        const wave = document.getElementById('voice-wave');
        msg.onstart = () => wave.style.display = 'block';
        msg.onend = () => wave.style.display = 'none';
        
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """, unsafe_allow_html=True)

css_code = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; text-align: center !important; }
    h1, h2, h3, h4, p, li, label { color: V_TXT !important; font-weight: 200 !important; text-align: center !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
    .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; margin: 0 auto !important; display: block !important; }
    .breather-circle { width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; box-shadow: 0 0 25px V_BLUE; }
    @keyframes breathe { 0% { transform: scale(1); opacity: 0.4; } 40% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(1); opacity: 0.4; } }
    
    /* NEW: PURE WAVEFORM VISUAL */
    #voice-wave { display: none; width: 120px; height: 4px; background: V_BLUE; margin: 10px auto; border-radius: 2px; box-shadow: 0 0 15px V_BLUE; animation: glow 1s infinite alternate; }
    @keyframes glow { from { opacity: 0.3; width: 80px; } to { opacity: 1; width: 150px; } }

    .mkt-btn { width: 80%; padding: 10px; background: V_BLUE; border-radius: 10px; font-weight: bold; color: #0A0E0B; display: block; margin: 10px auto; text-decoration: none; }
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"; st.rerun()
with c2: 
    if st.button("Market", use_container_width=True): st.session_state.current_page = "Marketplace"; st.rerun()
with c3: 
    if st.button("Vision", use_container_width=True): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### How is your energy?")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"m_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Energy Check]", "ai": f"Acknowledging your {label.lower()} energy."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<div id='voice-wave'></div>", unsafe_allow_html=True)
    
    # LIVE TRANSCRIPTION BUTTON
    st.markdown('<p id="mic-status" style="font-size:12px; opacity:0.7;">Tap button below to speak</p>', unsafe_allow_html=True)
    if st.button("🎙️ Start Voice Typing", use_container_width=True):
        st.markdown('<script>startListening()</script>', unsafe_allow_html=True)

    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("The box will fill with your voice...")
        submit = st.form_submit_button("Consult Guide")
        
        if submit and super_brain and text_in:
            prompt = "You are a calm mindfulness mentor for Sukoon. Respond with warmth and wisdom (max 2 paragraphs)."
            with st.spinner("Reflecting..."):
                try:
                    response = super_brain.generate_content(prompt + text_in)
                    ai_resp = response.text
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": text_in, "ai": ai_resp})
                    st.markdown(f"<script>speakWithVisuals({repr(ai_resp)})</script>", unsafe_allow_html=True)
                    st.rerun()
                except:
                    st.error("The Guide is resting. Try in 60 seconds.")

    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Grounding Bundles")
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Starter" class="mkt-btn">Starter Ritual: ₹2,499</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Master" class="mkt-btn">Master Sanctuary: ₹4,999</a>', unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.markdown(f'<br><a href="https://wa.me/{MY_PHONE}?text=Support" class="mkt-btn" style="width: 250px;">Connect</a>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='opacity: 0.6; font-size: 11px; text-align: center;'>“This app offers a quiet digital space. It does not provide therapy, counseling, medical advice, or emergency support.”</div>", unsafe_allow_html=True)

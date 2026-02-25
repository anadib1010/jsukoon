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

# --- 5. CSS & SCRIPTS (Improved Spacing & Centering) ---
st.markdown(f"""
    <script>
    function speakWithVisuals(text) {{
        const msg = new SpeechSynthesisUtterance(text);
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
    
    /* Improved Journal Entry Spacing */
    .stInfo {{ 
        background-color: rgba(174, 198, 207, 0.1) !important; 
        border: 1px solid V_BLUE !important; 
        border-radius: 15px !important; 
        padding: 20px !important; 
        margin: 10px auto !important;
        max-width: 85% !important;
        color: V_TXT !important;
    }}
    
    /* Box Spacing */
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 12px !important; padding: 10px !important; }
    
    /* Button Layout */
    .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 12px !important; margin: 10px auto !important; display: block !important; padding: 10px 20px !important; }
    
    .breather-circle { width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; box-shadow: 0 0 25px V_BLUE; }
    @keyframes breathe { 0% { transform: scale(1); opacity: 0.4; } 40% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(1); opacity: 0.4; } }
    
    #voice-wave { display: none; width: 120px; height: 4px; background: V_BLUE; margin: 15px auto; border-radius: 2px; box-shadow: 0 0 15px V_BLUE; animation: glow 1s infinite alternate; }
    @keyframes glow { from { opacity: 0.3; width: 80px; } to { opacity: 1; width: 150px; } }
    
    .mkt-btn { width: 85%; padding: 12px; background: V_BLUE; border-radius: 12px; font-weight: bold; color: #0A0E0B; display: block; margin: 12px auto; text-decoration: none; border: none; }
    div[data-testid="stAudioInput"] { display: flex; justify-content: center; margin-bottom: 20px; }
    
    hr { border-top: 1px solid rgba(174, 198, 207, 0.3) !important; }
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h1 style='font-size: 2.2rem;'>Sukoon</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("Journal", key="nav_j", use_container_width=True): st.session_state.current_page = "Journal"; st.rerun()
with c2: 
    if st.button("Market", key="nav_m", use_container_width=True): st.session_state.current_page = "Marketplace"; st.rerun()
with c3: 
    if st.button("Vision", key="nav_v", use_container_width=True): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check-In")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"m_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Mood Check]", "ai": f"Acknowledging your {label.lower()} energy space. Breathe with me."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<div id='voice-wave'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("#### Voice Recording")
    audio_file = st.audio_input("Record")

    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("Journal Entry", placeholder="Speak or type your thoughts...")
        submit = st.form_submit_button("Consult Guide")
        
        if submit and super_brain:
            content = []
            if audio_file:
                content.append({"mime_type": "audio/wav", "data": audio_file.read()})
                prompt = "Transcribe exactly what is heard first in a line starting with 'You said: '. Then provide a calm, brief mindfulness response."
            else:
                content.append(text_in)
                prompt = "Respond as a calm mindfulness mentor in 1-2 brief paragraphs."
            
            with st.spinner("Reflecting..."):
                try:
                    response = super_brain.generate_content([prompt] + content).text
                    if "You said:" in response:
                        parts = response.split("You said:", 1)[1].split("\n", 1)
                        user_entry = "🎙️ " + parts[0].strip()
                        ai_entry = parts[1].strip() if len(parts) > 1 else "I hear you."
                    else:
                        user_entry = text_in if text_in else "🎙️ Voice Note"
                        ai_entry = response

                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": user_entry, "ai": ai_entry})
                    st.markdown(f"<script>speakWithVisuals({repr(ai_entry)})</script>", unsafe_allow_html=True)
                    st.rerun()
                except Exception as e:
                    st.error("The Guide is resting. Please breathe and try again shortly.")

    # HISTORY (Beautifully Centered)
    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 **{entry['time']}**")
        st.write(f"*{entry['diary']}*")
        st.info(entry['ai'])

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("### ✨ Ritual Bundles")
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Starter" class="mkt-btn">Starter Ritual: ₹2,499</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Master" class="mkt-btn">Master Sanctuary: ₹4,999</a>', unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.write("Sukoon bridges digital AI and physical grounding.")
    st.markdown(f'<br><a href="https://wa.me/{MY_PHONE}?text=Support" class="mkt-btn" style="width: 250px; margin: 0 auto;">Connect with Founder</a>', unsafe_allow_html=True)

st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<div style='opacity: 0.6; font-size: 11px; text-align: center; padding-bottom: 30px;'>“This app offers a quiet digital space. It does not provide therapy, counseling, medical advice, or emergency support.”</div>", unsafe_allow_html=True)

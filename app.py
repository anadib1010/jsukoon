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

# --- 4. MULTI-BRAIN AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
brains = []
if api_key:
    genai.configure(api_key=api_key)
    # List of models to try in order of preference
    model_names = ["gemini-3-flash", "gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"]
    for name in model_names:
        try:
            brains.append(genai.GenerativeModel(name))
        except:
            pass

# --- 5. SENSORY SCRIPTS ---
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
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 12px !important; }
    .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 12px !important; margin: 10px auto !important; display: block !important; }
    .breather-circle { width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; box-shadow: 0 0 25px V_BLUE; }
    @keyframes breathe { 0% { transform: scale(1); opacity: 0.4; } 40% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(1); opacity: 0.4; } }
    #voice-wave { display: none; width: 120px; height: 4px; background: V_BLUE; margin: 15px auto; border-radius: 2px; box-shadow: 0 0 15px V_BLUE; animation: glow 1s infinite alternate; }
    @keyframes glow { from { opacity: 0.3; width: 80px; } to { opacity: 1; width: 150px; } }
    .mkt-btn { width: 85%; padding: 12px; background: V_BLUE; border-radius: 12px; font-weight: bold; color: #0A0E0B; display: block; margin: 12px auto; text-decoration: none; border: none; }
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
    st.markdown("---")
    
    st.write("#### Record or Type")
    audio_file = st.audio_input("Record")

    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("What's on your mind?")
        submit = st.form_submit_button("Consult Guide")
        
        if submit and brains:
            content = []
            if audio_file:
                content.append({"mime_type": "audio/wav", "data": audio_file.read()})
                prompt = "TRANScribe what you hear first in a line starting with 'You said: '. Then give a calm 1-paragraph response."
            else:
                content.append(text_in)
                prompt = "Respond as a calm mindfulness mentor in 1 paragraph."
            
            with st.spinner("Reflecting..."):
                response_received = False
                for brain in brains:
                    try:
                        resp = brain.generate_content([prompt] + content).text
                        response_received = True
                        
                        if "You said:" in resp:
                            parts = resp.split("You said:", 1)[1].split("\n", 1)
                            user_entry = "🎙️ " + parts[0].strip()
                            ai_entry = parts[1].strip() if len(parts) > 1 else "I hear you."
                        else:
                            user_entry = text_in if text_in else "🎙️ Voice Note"
                            ai_entry = resp

                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": user_entry, "ai": ai_entry})
                        st.markdown(f"<script>speakWithVisuals({repr(ai_entry)})</script>", unsafe_allow_html=True)
                        st.rerun()
                        break
                    except:
                        continue
                
                if not response_received:
                    st.error("The Sanctuary is in deep silence (Quota Exceeded). Please breathe and try again tomorrow.")

    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 **{entry['time']}**")
        st.write(f"*{entry['diary']}*")
        st.info(entry['ai'])

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Starter" class="mkt-btn">Starter Ritual</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Master" class="mkt-btn">Master Sanctuary</a>', unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("Sukoon bridges digital AI and physical grounding.")
    st.markdown(f'<br><a href="https://wa.me/{MY_PHONE}?text=Support" class="mkt-btn">Connect</a>', unsafe_allow_html=True)

st.markdown("<hr><div style='opacity: 0.6; font-size: 11px; text-align: center;'>“This app offers a quiet digital space. It does not provide medical advice.”</div>", unsafe_allow_html=True)

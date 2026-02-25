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
    model_names = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]
    for name in model_names:
        try:
            brains.append(genai.GenerativeModel(name))
        except:
            pass

# --- 5. ENHANCED VOICE SCRIPT ---
st.markdown(f"""
    <script>
    function manualSpeak() {{
        const text = document.querySelector('.ai-response-text').innerText;
        const msg = new SpeechSynthesisUtterance(text);
        msg.rate = 0.85;
        msg.pitch = 1.0;
        
        // Find a calm voice
        const voices = window.speechSynthesis.getVoices();
        msg.voice = voices.find(v => v.name.includes('Google') || v.name.includes('Natural')) || voices[0];
        
        const wave = document.getElementById('voice-wave');
        msg.onstart = () => wave.style.display = 'block';
        msg.onend = () => wave.style.display = 'none';
        
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """, unsafe_allow_html=True)

css_code = """
<style>
    html, body, .stApp {{ background-color: V_BG !important; color: V_TXT !important; text-align: center !important; }}
    h1, h2, h3, h4, p, li, label {{ color: V_TXT !important; font-weight: 200 !important; text-align: center !important; }}
    textarea {{ background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 12px !important; }}
    .stButton>button {{ background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 12px !important; margin: 10px auto !important; display: block !important; }}
    .breather-circle {{ width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; box-shadow: 0 0 25px V_BLUE; }}
    @keyframes breathe {{ 0% {{ transform: scale(1); opacity: 0.4; }} 40% {{ transform: scale(1.4); opacity: 1; }} 100% {{ transform: scale(1); opacity: 0.4; }} }}
    #voice-wave {{ display: none; width: 120px; height: 4px; background: V_BLUE; margin: 15px auto; border-radius: 2px; box-shadow: 0 0 15px V_BLUE; animation: glow 1s infinite alternate; }}
    @keyframes glow {{ from {{ opacity: 0.3; width: 80px; }} to {{ opacity: 1; width: 150px; }} }}
    .mkt-btn {{ width: 85%; padding: 12px; background: V_BLUE; border-radius: 12px; font-weight: bold; color: #0A0E0B; display: block; margin: 12px auto; text-decoration: none; border: none; }}
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
    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<div id='voice-wave'></div>", unsafe_allow_html=True)
    
    audio_file = st.audio_input("Record your voice")

    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("Share your heart...")
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
                for brain in brains:
                    try:
                        resp = brain.generate_content([prompt] + content).text
                        if "You said:" in resp:
                            parts = resp.split("You said:", 1)[1].split("\n", 1)
                            u_entry, a_entry = "🎙️ " + parts[0].strip(), parts[1].strip()
                        else:
                            u_entry, a_entry = text_in if text_in else "🎙️ Voice Note", resp

                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": u_entry, "ai": a_entry})
                        st.rerun()
                        break
                    except: continue

    # RECENT RESPONSE WITH "LISTEN" BUTTON
    if st.session_state.private_journal:
        latest = st.session_state.private_journal[-1]
        st.markdown(f"🕒 **{latest['time']}**")
        st.write(f"*{latest['diary']}*")
        st.markdown(f"<div class='ai-response-text' style='background: rgba(174,198,207,0.1); padding:15px; border-radius:10px; border:1px solid {soft_blue}; margin-bottom:10px;'>{latest['ai']}</div>", unsafe_allow_html=True)
        
        # This button forces the browser to play the audio
        if st.button("🔊 Hear the Mentor", use_container_width=True):
            st.markdown("<script>manualSpeak()</script>", unsafe_allow_html=True)

    st.markdown("---")
    for entry in reversed(st.session_state.private_journal[:-1]):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- 8. MARKETPLACE & VISION ---
elif st.session_state.current_page == "Marketplace":
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Starter" class="mkt-btn">Starter Ritual</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/{MY_PHONE}?text=Master" class="mkt-btn">Master Sanctuary</a>', unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.write("Sukoon bridges digital AI and physical grounding.")
    st.markdown(f'<br><a href="https://wa.me/{MY_PHONE}?text=Support" class="mkt-btn">Connect</a>', unsafe_allow_html=True)

st.markdown("<hr><div style='opacity: 0.6; font-size: 11px; text-align: center;'>“This app offers a quiet digital space. It does not provide medical advice.”</div>", unsafe_allow_html=True)

import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "YOUR_GITHUB_USERNAME" # Replace this with your GitHub username
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

# --- 4. MULTI-BRAIN AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
brains = []
if api_key:
    genai.configure(api_key=api_key)
    # Using 1.5 Flash as primary for speed/multimodal
    for name in ["gemini-1.5-flash", "gemini-pro"]:
        try: brains.append(genai.GenerativeModel(name))
        except: pass

# --- 5. SCRIPTS ---
st.markdown(f"""
    <script>
    function speakNow(text) {{
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance(text);
        msg.rate = 0.8;
        const wave = document.getElementById('voice-wave');
        msg.onstart = () => {{ if(wave) wave.style.display = 'block'; }};
        msg.onend = () => {{ if(wave) wave.style.display = 'none'; }};
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """, unsafe_allow_html=True)

css_code = """
<style>
    html, body, .stApp {{ background-color: V_BG !important; color: V_TXT !important; text-align: center !important; }}
    .stButton>button {{ background-color: V_BTN !important; color: V_TXT !important; border: 1px solid V_BLUE !important; border-radius: 12px !important; }}
    .breather-circle {{ width: 80px; height: 80px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 10s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    #voice-wave {{ display: none; width: 100px; height: 4px; background: V_BLUE; margin: 10px auto; animation: glow 1s infinite alternate; }}
    @keyframes glow {{ from {{ opacity: 0.3; }} to {{ opacity: 1; }} }}
    .mkt-btn {{ width: 90%; padding: 12px; background: V_BLUE; border-radius: 12px; font-weight: bold; color: #0A0E0B; display: block; margin: 10px auto; text-decoration: none; }}
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
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
    # 5 MOOD BUTTONS
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"m_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": f"[{label} Energy Check]", "ai": f"Acknowledging your {label.lower()} energy."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<div id='voice-wave'></div>", unsafe_allow_html=True)

    # NATURE AMBIENCE (YOUR FILES)
    st.write("#### Nature Ambience")
    # Change 'birds.mp3' etc. to match your EXACT file names in GitHub
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.write("Waves")
        st.audio(base_url + "waves.mp3", format="audio/mp3")
    with sc2:
        st.write("Birds")
        st.audio(base_url + "birds.mp3", format="audio/mp3")
    with sc3:
        st.write("Rain")
        st.audio(base_url + "rain.mp3", format="audio/mp3")

    st.markdown("---")
    audio_file = st.audio_input("Record a voice note")

    with st.form("input_form", clear_on_submit=True):
        text_in = st.text_area("Share your heart...")
        submit = st.form_submit_button("Consult Guide")
        
        if submit and brains:
            content = []
            if audio_file:
                content.append({"mime_type": "audio/wav", "data": audio_file.read()})
                prompt = "Transcribe exactly what is heard first in a line starting with 'You said: '. Then give a calm 1-paragraph response."
            else:
                content.append(text_in)
                prompt = "Respond as a calm mindfulness mentor in 1 paragraph."
            
            with st.spinner("Reflecting..."):
                for brain in brains:
                    try:
                        resp = brain.generate_content([prompt] + content).text
                        if "You said:" in resp:
                            parts = resp.split("You said:", 1)[1].split("\n", 1)
                            u_e, a_e = "🎙️ " + parts[0].strip(), parts[1].strip()
                        else:
                            u_e, a_e = text_in if text_in else "🎙️ Voice Note", resp
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": u_e, "ai": a_e})
                        st.rerun()
                        break
                    except: continue

    if st.session_state.private_journal:
        latest = st.session_state.private_journal[-1]
        st.info(f"🕒 {latest['time']} | {latest['ai']}")
        if st.button("🔊 Play Mentor's Voice", use_container_width=True):
            st.markdown(f"<script>speakNow({repr(latest['ai'])})</script>", unsafe_allow_html=True)

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

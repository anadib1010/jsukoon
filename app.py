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
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A"
else:
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
brains = []
if api_key:
    genai.configure(api_key=api_key)
    for name in ["gemini-1.5-flash", "gemini-pro"]:
        try: brains.append(genai.GenerativeModel(name))
        except: pass

# --- 5. SCRIPTS ---
st.markdown(f"""
    <script>
    function speakNow(text) {{
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance(text);
        msg.rate = 0.85;
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
    h1, h2, h3, h4, p, li {{ color: V_TXT !important; font-weight: 200 !important; }}
    .stButton>button {{ background-color: V_BTN !important; color: V_TXT !important; border: 1px solid V_BLUE !important; border-radius: 12px !important; width: 100%; }}
    .breather-circle {{ width: 70px; height: 70px; background: V_BLUE; border-radius: 50%; margin: 20px auto; animation: breathe 8s infinite ease-in-out; }}
    @keyframes breathe {{ 0%, 100% {{ transform: scale(1); opacity: 0.4; }} 50% {{ transform: scale(1.3); opacity: 1; }} }}
    #voice-wave {{ display: none; width: 100px; height: 4px; background: V_BLUE; margin: 10px auto; border-radius: 2px; animation: glow 1s infinite alternate; }}
    @keyframes glow {{ from {{ opacity: 0.3; }} to {{ opacity: 1; }} }}
    .mkt-box {{ border: 1px solid V_BLUE; padding: 15px; border-radius: 15px; margin-bottom: 15px; background: rgba(174, 198, 207, 0.05); }}
    .wa-link {{ display: block; background: V_BLUE; color: #0A0E0B; padding: 10px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
    textarea {{ background-color: V_IN !important; color: V_TXT !important; border: 1px solid V_BLUE !important; border-radius: 10px !important; }}
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1: 
    if st.button("Journal", key="n1"): st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", key="n2"): st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", key="n3"): st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    # MOOD BUTTONS
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i, label in enumerate(mood_labels):
        with mood_cols[i]:
            if st.button(label, key=f"mood_{i}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": f"[{label} Energy]", "ai": f"Acknowledging that {label.lower()} energy."})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("<div id='voice-wave'></div>", unsafe_allow_html=True)

    # HORIZONTAL NATURE SOUNDS
    st.write("#### Nature Ambience")
    base_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/sukoon/main/"
    sounds = {"Waves": "waves.mp3", "Birds": "birds.mp3", "Rain": "rain.mp3", "Forest": "forest.mp3", "Flute": "flute.mp3"}
    ac = st.columns(5)
    for idx, (name, file) in enumerate(sounds.items()):
        with ac[idx]:
            st.write(f"**{name}**")
            st.audio(base_url + file)

    st.markdown("---")
    # AI INPUT SECTION
    audio_file = st.audio_input("Record your heart")
    with st.form("ai_form", clear_on_submit=True):
        text_in = st.text_area("Share your thoughts...")
        if st.form_submit_button("Consult Guide"):
            content = []
            if audio_file:
                content.append({"mime_type": "audio/wav", "data": audio_file.read()})
                prompt = "Transcribe what you hear first in a line starting with 'You said: '. Then give a calm response."
            else:
                content.append(text_in)
                prompt = "Respond as a calm mindfulness mentor in 1 paragraph."
            
            if brains:
                with st.spinner("Reflecting..."):
                    for brain in brains:
                        try:
                            resp = brain.generate_content([prompt] + content).text
                            if "You said:" in resp:
                                parts = resp.split("You said:", 1)[1].split("\n", 1)
                                u_e, a_e = "🎙️ " + parts[0].strip(), parts[1].strip()
                            else: u_e, a_e = text_in if text_in else "Voice Note", resp
                            st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": u_e, "ai": a_e})
                            st.rerun()
                            break
                        except: continue

    # RECENT HISTORY & VOICE SPEAKER
    if st.session_state.private_journal:
        latest = st.session_state.private_journal[-1]
        st.info(f"🕒 {latest['time']} | {latest['ai']}")
        if st.button("🔊 Hear the Mentor"):
            st.markdown(f"<script>speakNow({repr(latest['ai'])})</script>", unsafe_allow_html=True)

    for entry in reversed(st.session_state.private_journal[:-1]):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- 8. MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.write("### ✨ Grounding Objects")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"<div class='mkt-box'><h4>Starter Ritual</h4><p>₹2,499</p><a href='https://wa.me/{MY_PHONE}?text=Starter' class='wa-link'>Order</a></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='mkt-box'><h4>Master Sanctuary</h4><p>₹4,999</p><a href='https://wa.me/{MY_PHONE}?text=Master' class='wa-link'>Order</a></div>", unsafe_allow_html=True)
    
    i1, i2, i3 = st.columns(3)
    items = ["Stones", "Buddha", "Art"]
    for idx, item in enumerate(items):
        with [i1, i2, i3][idx]:
            st.markdown(f"<div class='mkt-box'><h5>{item}</h5><a href='https://wa.me/{MY_PHONE}?text={item}' class='wa-link'>Inquire</a></div>", unsafe_allow_html=True)

# --- 9. VISION ---
elif st.session_state.current_page == "Vision":
    st.write("### Silence in a Loud World")
    st.write("Sukoon bridges digital AI and physical grounding.")
    st.markdown(f"<br><a href='https://wa.me/{MY_PHONE}?text=Support' class='wa-link' style='width:200px; margin: 0 auto;'>Connect</a>", unsafe_allow_html=True)

# --- 10. DISCLAIMER (Always Visible) ---
st.markdown("<hr><div style='opacity: 0.6; font-size: 11px; text-align: center; padding-bottom: 50px;'>“This app offers a quiet digital space. It does not provide medical advice, therapy, or emergency support.”</div>", unsafe_allow_html=True)

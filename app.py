import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

# --- USER PHONE ---
MY_PHONE = "918882850790"

# --- AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in models if 'flash' in m), models[0])
        super_brain = genai.GenerativeModel(target_model)
    except:
        super_brain = None
else:
    super_brain = None

# --- UI STATE ---
if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Journal"
if "theme" not in st.session_state:
    st.session_state.theme = "Peaceful"

# --- THEME COLORS ---
soft_blue = "#AEC6CF" 
if st.session_state.theme == "Peaceful":
    bg, txt, input_bg, btn_bg, card_hover = "#F9FDF9", "#2E4032", "white", "transparent", "rgba(74, 112, 85, 0.15)"
else:
    bg, txt, input_bg, btn_bg, card_hover = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A", "rgba(255, 255, 255, 0.05)"

# --- CSS (STRATEGY: NO F-STRINGS TO PREVENT ERRORS) ---
css_template = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; }
    h1, h2, h3, h4, label, p, li { color: V_TXT !important; font-weight: 200 !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; }
    button[kind="secondaryFormSubmit"], .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
    @keyframes breathe {
        0% { transform: scale(1); opacity: 0.4; }
        40% { transform: scale(1.4); opacity: 1; }
        60% { transform: scale(1.4); opacity: 1; }
        100% { transform: scale(1); opacity: 0.4; }
    }
    .breather-circle {
        width: 80px; height: 80px; background: V_BLUE; border-radius: 50%;
        margin: 20px auto; animation: breathe 10s infinite ease-in-out;
        box-shadow: 0 0 25px V_BLUE;
    }
    .ritual-box { padding: 20px; border: 1px solid V_BLUE; border-radius: 15px; background: rgba(174, 198, 207, 0.1); margin: 20px 0; }
    img { border-radius: 15px; margin-bottom: 10px; }
</style>
"""
clean_css = css_template.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns([1,1,1])
with n1: 
    if st.button("Journal", use_container_width=True, key="n1"):
        st.session_state.current_page = "Journal"; st.rerun()
with n2: 
    if st.button("Market", use_container_width=True, key="n2"):
        st.session_state.current_page = "Marketplace"; st.rerun()
with n3: 
    if st.button("Vision", use_container_width=True, key="n3"):
        st.session_state.current_page = "Vision"; st.rerun()
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='ritual-box'><b>✨ Ritual of the Week:</b> Hold your Natural Stone in your left hand while listening to 'Waves' for 3 minutes to ground your center.</div>", unsafe_allow_html=True)
    st.write("#### How is your energy?")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i in range(5):
        with mood_cols[i]:
            if st.button(mood_labels[i], key=f"m_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                msg = "I see you're in a " + mood_labels[i].lower() + " energy space. Let's just breathe for a moment."
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Energy Check: " + mood_labels[i] + "]", "ai": msg})
                st.rerun()

    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("#### 🎵 Ambient Sounds")
    choice = st.radio("Vibe:", ["Silent", "Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
    if choice != "Silent":
        files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
        target = files.get(choice)
        if target and os.path.exists(target): st.audio(target)

    st.markdown("---")
    st.write("#### Journal & Voice")
    if hasattr(st, "audio_input"): st.audio_input("Tap to Record Voice Note")
    with st.form(key="journal_form", clear_on_submit=True):
        diary_in = st.text_area("Share your heart...")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_in:
                stressors = ["sad", "anxious", "stress", "tired", "dark", "heavy", "pain", "exhausted"]
                st.session_state.theme = "Midnight" if any(w in diary_in.lower() for w in stressors) else "Peaceful"
                with st.spinner("Listening..."):
                    try:
                        resp = super_brain.generate_content("Respond as a mindfulness mentor: " + diary_in).text
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_in, "ai": resp})
                        st.rerun()
                    except:
                        st.error("The Guide is resting.")
    for entry in reversed(st.session_state.private_journal):
        st.write("🕒 " + entry['time'] + " | " + entry['diary'])
        st.info(entry['ai'])

# --- PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h2 style='text-align: center;'>The Marketplace</h2>", unsafe_allow_html=True)
    st.markdown("### ✨ Grounding Bundles")
    b1, b2 = st.columns(2)
    with b1:
        if os.path.exists("buddha.jpg"): st.image("buddha.jpg", use_container_width=True)
        st.markdown("#### The Starter Ritual (3 Items)")
        st.write("Stones, Buddha, & Beads. ₹2,499")
        u1 = "https://wa.me/" + MY_PHONE + "?text=Interest:StarterRitual"
        st.markdown('<a href="'+u1+'" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; cursor:pointer; background-color:'+soft_blue+'; color:#0A0E0B;">Order Ritual Box</button></a>', unsafe_allow_html=True)
    with b2:
        if os.path.exists("vaastu.jpg"): st.image("vaastu.jpg", use_container_width=True)
        st.markdown("#### The Master Sanctuary (5 Items)")
        st.write("Stones, Buddha, Art, Vaastu, & Journal. ₹4,999")
        u2 = "https://wa.me/" + MY_PHONE + "?text=Interest:MasterSanctuary"
        st.markdown('<a href="'+u2+'" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; cursor:pointer; background-color:'+soft_blue+'; color:#0A0E0B;">Order Ritual Box</button></a>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🏺 Individual Objects")
    c1, c2, c3 = st.columns(3)
    with c1:
        if os.path.exists("stones.jpg"): st.image("stones.jpg", use_container_width=True)
        st.markdown("#### Natural Stones")
        l1 = "https://wa.me/" + MY_PHONE + "?text=Stones"
        st.markdown('<a href="'+l1+'" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; background-color:'+soft_blue+';">Inquire</button></a>', unsafe_allow_html=True)
    with c2:
        if os.path.exists("buddha.jpg"): st.image("buddha.jpg", use_container_width=True)
        st.markdown("#### Sacred Buddha")
        l2 = "https://wa.me/" + MY_PHONE + "?text=Buddha"
        st.markdown('<a href="'+l2+'" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; background-color:'+soft_blue+';">Inquire</button></a>', unsafe_allow_html=True)
    with c3:
        if os.path.exists("art.jpg"): st.image("art.jpg", use_container_width=True)
        st.markdown("#### Artic Art")
        l3 = "https://wa.me/" + MY_PHONE + "?text=Art"
        st.markdown('<a href="'+l3+'" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; background-color:'+soft_blue+';">Inquire</button></a>', unsafe_allow_html=True)

# --- PAGE: VISION ---
elif st.session_state.current_page == "Vision":
    st.markdown("<h2 style='text-align: center;'>Our Vision</h2>", unsafe_allow_html=True)
    st.write("Sukoon is an ecosystem designed to bridge the gap between digital AI guidance and tangible physical grounding.")
    wa_v = "https://wa.me/" + MY_PHONE + "?text=SupportSukoon"
    st.markdown('<div style="text-align: center;"><br><a href="' + wa_v + '" target="_blank"><button style="padding:10px 25px; border-radius:10px; border:none; font-weight:bold; cursor:pointer; background-color:' + soft_blue + '; color:#0A0E0B;">💬 Connect with Founder</button

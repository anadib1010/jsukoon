import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

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
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in models if 'flash' in m), models[0])
        super_brain = genai.GenerativeModel(target_model)
    except:
        super_brain = None
else:
    super_brain = None

# --- 5. CSS ---
css_code = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; }
    h1, h2, h3, h4, p, li { color: V_TXT !important; font-weight: 200 !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; }
    .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
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
    .ritual-box { padding: 15px; border: 1px solid V_BLUE; border-radius: 12px; background: rgba(174, 198, 207, 0.1); margin: 15px 0; }
    .mkt-btn { width:100%; padding:10px; background:V_BLUE; border:none; border-radius:10px; font-weight:bold; color:#0A0E0B; cursor:pointer; text-align:center; display:block; text-decoration:none; }
</style>
"""
clean_css = css_code.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h2 style='text-align: center;'>Sukoon</h2>", unsafe_allow_html=True)
n1, n2, n3 = st.columns([1,1,1])
with n1: 
    if st.button("Journal", use_container_width=True, key="nav_j"):
        st.session_state.current_page = "Journal"
        st.rerun()
with n2: 
    if st.button("Market", use_container_width=True, key="nav_m"):
        st.session_state.current_page = "Marketplace"
        st.rerun()
with n3: 
    if st.button("Vision", use_container_width=True, key="nav_v"):
        st.session_state.current_page = "Vision"
        st.rerun()
st.markdown("---")

# --- 7. PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div class='ritual-box'><b>✨ Ritual:</b> Hold your Natural Stone for 3 minutes.</div>", unsafe_allow_html=True)
    st.write("#### How is your energy?")
    mood_cols = st.columns(5)
    mood_labels = ["Low", "Drained", "Neutral", "Steady", "Vibrant"]
    for i in range(5):
        with mood_cols[i]:
            if st.button(mood_labels[i], key=f"mood_{i}", use_container_width=True):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"
                msg = "I see you're in a " + mood_labels[i].lower() + " energy space."
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": "[Energy Check]", "ai": msg})
                st.rerun()
    st.markdown("<div class='breather-circle'></div>", unsafe_allow_html=True)
    st.markdown("---")
    if hasattr(st, "audio_input"): st.audio_input("Voice Note")
    with st.form(key="journal_form", clear_on_submit=True):
        diary_in = st.text_area("Share your heart...")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_in:
                st.session_state.theme = "Midnight" if "sad" in diary_in.lower() else "Peaceful"
                resp = super_brain.generate_content("Mentor response: " + diary_in).text
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_in, "ai": resp})
                st.rerun()
    for entry in reversed(st.session_state.private_journal):
        st.write("🕒 " + entry['time'] + " | " + entry['diary'])
        st.info(entry['ai'])

# --- 8. PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h2 style='text-align: center;'>Marketplace</h2>", unsafe_allow_html=True)
    st.markdown("### ✨ Grounding Bundles")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("#### The Starter Ritual")
        st.write("3 Items: ₹2,499")
        link1 = "https://wa.me/" + MY_PHONE + "?text=StarterRitual"
        st.markdown('<a href="' + link1 + '" class="mkt-btn">Order Box</a>', unsafe_allow_html=True)
    with b2:
        st.markdown("#### Master Sanctuary")
        st.write("5 Items: ₹4,999")
        link2 = "https://wa.me/" + MY_PHONE + "?text=MasterSanctuary"
        st.markdown('<a href="' + link2 + '" class="mkt-btn">Order Box</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🏺 Individual Objects")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### Stones")
        link_s = "https://wa.me/" + MY_PHONE + "?text=Stones"
        st.markdown('<a href="' + link_s + '" class="mkt-btn">Inquire</a>', unsafe_allow_html=True)
    with c2:
        st.markdown("#### Buddha")
        link_b = "https://wa.me/" + MY_PHONE + "?text=Buddha"
        st.markdown('<a href="' + link_b + '" class="mkt-btn">Inquire</a>', unsafe_allow_html=True)
    with c3:
        st.markdown("#### Art")
        link_a = "https://wa.me/" + MY_PHONE + "?text=Art"
        st.markdown('<a href="' + link_a + '" class="mkt-btn">Inquire</a>', unsafe_allow_html=True)

# --- 9. PAGE: VISION ---
elif st.session_state.current_page == "Vision":
    st.markdown("<h2 style='text-align: center;'>Vision</h2>", unsafe_allow_html=True)
    st.write("### Silence in a Loud World")
    st.write("Sukoon bridges digital AI guidance and tangible physical grounding.")
    st.write("---")
    st.write("### The Journey")
    st.write("We are integrating affective computing to understand human emotion.")
    wa_v = "https://wa.me/" + MY_PHONE + "?text=SupportSukoon"
    st.markdown('<div style="text-align:center;"><a href="' + wa_v + '" class="mkt-btn">Connect</a></div>', unsafe_allow_html=True)

# --- 10. GLOBAL FOOTER ---
st.markdown("---")
st.markdown("""
<div style='opacity: 0.6; font-size: 11px; text-align: center; padding: 10px; line-height: 1.6;'>
“This app offers a quiet digital space.<br>
It does not provide therapy, counseling, medical advice, or emergency support.”
</div>
""", unsafe_allow_html=True)

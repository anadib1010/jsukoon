import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#AEC6CF" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "theme" not in st.session_state: st.session_state.theme = "Peaceful"
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. THEME ---
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. UI STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    [data-testid="stVerticalBlock"] {{ display: flex; flex-direction: column; align-items: center !important; text-align: center !important; }}
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 14px !important; 
        width: 100% !important; padding: 10px 15px !important; min-height: 45px !important;
        margin: 5px auto !important; font-size: 13px !important; font-weight: 500 !important;
    }}
    .footer-text {{ font-size: 10px; opacity: 0.7; text-align: center; margin-top: 50px; padding: 15px; border-top: 0.5px solid {soft_blue}; width: 100%; }}
    .faq-q {{ font-weight: bold; color: {soft_blue}; margin-top: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
st.markdown("<h1 style='text-align: center;'>Sukoon</h1>", unsafe_allow_html=True)
r1_1, r1_2, r1_3 = st.columns(3)
with r1_1: 
    if st.button("Journal", key="n1"): st.session_state.current_page = "Journal"; st.rerun()
with r1_2: 
    if st.button("Market", key="n2"): st.session_state.current_page = "Marketplace"; st.rerun()
with r1_3: 
    if st.button("Vision", key="n3"): st.session_state.current_page = "Vision"; st.rerun()

r2_1, r2_2 = st.columns(2)
with r2_1: 
    if st.button("FAQ", key="n4"): st.session_state.current_page = "FAQ"; st.rerun()
with r2_2: 
    if st.button("Disclaimer", key="n5"): st.session_state.current_page = "Disclaimer"; st.rerun()
st.markdown("---")

# --- 7. JOURNAL PAGE ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check")
    m_cols = st.columns(5)
    for i, lab in enumerate(["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(lab, key=f"m_{lab}"):
                st.session_state.theme = "Midnight" if i < 2 else "Peaceful"; st.rerun()

    st.markdown("<div style='width:60px; height:60px; background:"+soft_blue+"; border-radius:50%; margin:20px auto; opacity:0.6;'></div>", unsafe_allow_html=True)
    
    st.write("#### Nature Ambience")
    cdn = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/"
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    aud_cols = st.columns(5)
    for idx, name in enumerate(sounds.keys()):
        with aud_cols[idx]:
            if st.button(name, key=f"aud_{name}"):
                st.session_state.active_audio = sounds[name]
                st.session_state.audio_label = name
    if st.session_state.active_audio:
        st.audio(f"{cdn}{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("---")
    audio_rec = st.audio_input("Voice Note")
    text_msg = st.text_area("Record your reflection...")
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
                try:
                    # System Instruction modified to be legally safe
                    prompt = "You are a mindfulness mentor. Provide a calm, supportive reflection. Avoid medical advice or clinical terms."
                    parts = [prompt]
                    if audio_rec: parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                    else: parts.append(text_msg)
                    resp = model.generate_content(parts).text
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp})
                    st.rerun()
                except: st.error("The Guide is pausing.")

    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")

# --- 8. VISION ---
elif st.session_state.current_page == "Vision":
    st.write("### The Sukoon Ritual")
    st.write("Sukoon is a digital sanctuary designed to cultivate inner stillness and balance.")
    st.markdown("""
    **1. Ground:** Select a nature frequency to settle your focus.  
    **2. Release:** Share your current reflections to clear mental noise.  
    **3. Reflect:** Receive a supportive mirror to help maintain presence.
    """)
    st.write("For inquiries regarding the philosophy or grounding tools:")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='display:block; border:1px solid {soft_blue}; padding:15px; border-radius:12px; text-decoration:none; color:{soft_blue}; font-weight:bold;'>Talk to the Founder</a>", unsafe_allow_html=True)

# --- 9. FAQ ---
elif st.session_state.current_page == "FAQ":
    st.write("### Common Inquiries")
    faqs = {
        "Is my data private?": "Your reflections stay in your current session. We do not store personal journal history on our servers.",
        "How do the nature sounds help?": "Natural frequencies are used to encourage a state of calm focus and relaxation.",
        "Is this a therapy tool?": "No. Sukoon is a lifestyle companion for mindfulness and general well-being.",
        "What are the grounding objects?": "We offer physical items like beads and stones designed for sensory focus and ritual."
    }
    for q, a in faqs.items():
        st.markdown(f"<div class='faq-q'>{q}</div><div>{a}</div>", unsafe_allow_html=True)

# --- 10. DISCLAIMER ---
elif st.session_state.current_page == "Disclaimer":
    st.write("### Information & Use")
    st.write("Sukoon is an AI-supported companion for mindfulness and relaxation. It does not provide medical, psychological, or psychiatric advice. It is not intended to treat or manage any health condition. By using this app, you acknowledge that it is a self-help tool used at your own discretion.")

# --- UNIVERSAL FOOTER ---
st.markdown("<div class='footer-text'>Sukoon is a wellness tool for mindfulness and is not a medical substitute.</div>", unsafe_allow_html=True)

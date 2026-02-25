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

# Session States
for key in ["private_journal", "current_page", "theme", "active_audio"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "private_journal" else "Journal" if key == "current_page" else "Peaceful" if key == "theme" else None

# --- 3. THEME ---
if st.session_state.theme == "Midnight":
    bg, txt, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E"
else:
    bg, txt, btn_bg = "#F9FDF9", "#2E4032", "white"

# --- 4. AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash") if api_key else None
if api_key: genai.configure(api_key=api_key)

# --- 5. CSS (Symmetry & Mobile Optimization) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    [data-testid="stVerticalBlock"] {{ display: flex; flex-direction: column; align-items: center !important; text-align: center !important; }}
    
    .stButton {{ display: flex; justify-content: center; width: 100%; }}
    .stButton>button {{ 
        background-color: {btn_bg} !important; color: {txt} !important; 
        border: 1px solid {soft_blue} !important; border-radius: 14px !important; 
        width: 100% !important; padding: 10px 15px !important; min-height: 45px !important;
        margin: 5px auto !important; font-size: 13px !important; font-weight: 500 !important;
        white-space: nowrap !important;
    }}
    
    .mkt-box {{ border: 1px solid {soft_blue}; padding: 20px; border-radius: 15px; background: {btn_bg}; width: 100%; margin-bottom: 15px; }}
    .disclaimer-bar {{ font-size: 10px; opacity: 0.6; text-align: center; margin-top: 40px; padding: 10px; border-top: 0.5px solid {soft_blue}; width: 100%; }}
    .faq-q {{ font-weight: bold; color: {soft_blue}; margin-top: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NEW NAVIGATION GRID ---
st.markdown("<h1 style='text-align: center;'>Sukoon</h1>", unsafe_allow_html=True)
row1_1, row1_2, row1_3 = st.columns(3)
with row1_1: 
    if st.button("Journal", key="n1"): st.session_state.current_page = "Journal"; st.rerun()
with row1_2: 
    if st.button("Market", key="n2"): st.session_state.current_page = "Marketplace"; st.rerun()
with row1_3: 
    if st.button("Vision", key="n3"): st.session_state.current_page = "Vision"; st.rerun()

row2_1, row2_2 = st.columns(2)
with row2_1: 
    if st.button("FAQ", key="n4"): st.session_state.current_page = "FAQ"; st.rerun()
with row2_2: 
    if st.button("Disclaimer", key="n5"): st.session_state.current_page = "Disclaimer"; st.rerun()
st.markdown("---")

# --- 7. PAGES ---

# --- JOURNAL ---
if st.session_state.current_page == "Journal":
    st.write("#### Energy Check")
    m_cols = st.columns(5)
    for i, lab in enumerate(["Low", "Drained", "Neutral", "Steady", "Vibrant"]):
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
    audio_rec = st.audio_input("Record")
    text_msg = st.text_area("Share your heart...")
    if st.button("Consult Guide", use_container_width=True):
        if model:
            with st.spinner("Reflecting..."):
                try:
                    parts = ["You are a mindfulness mentor. Respond in 1 calm paragraph."]
                    if audio_rec: parts.append({"mime_type": "audio/wav", "data": audio_rec.read()})
                    else: parts.append(text_msg)
                    resp = model.generate_content(parts).text
                    st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp})
                    st.rerun()
                except: st.error("Brain is resting.")

    for entry in reversed(st.session_state.private_journal):
        st.info(f"🕒 {entry['time']} | {entry['ai']}")

# --- VISION ---
elif st.session_state.current_page == "Vision":
    st.write("### The Sukoon Ritual")
    st.write("Sukoon is designed as a bridge between high-tech AI and the quiet human soul.")
    st.markdown("""
    **1. Ground:** Select a nature sound to settle your nervous system.  
    **2. Release:** Speak or type your honest thoughts without judgment.  
    **3. Reflect:** Receive guidance that acts as a mirror to your inner peace.
    """)
    st.write("Questions? I am here to help.")
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='display:block; border:1px solid {soft_blue}; padding:15px; border-radius:12px; text-decoration:none; color:{soft_blue}; font-weight:bold;'>Talk to the Founder</a>", unsafe_allow_html=True)

# --- FAQ ---
elif st.session_state.current_page == "FAQ":
    st.write("### Common Inquiries")
    faqs = {
        "Is my data private?": "Your journal entries are stored only in your current session and are not saved permanently on our servers.",
        "How do the nature sounds help?": "Binaural and nature frequencies are scientifically proven to lower cortisol (stress) levels.",
        "How often should I use the Guide?": "Even 3 minutes a day can build significant mental resilience over time.",
        "Can I purchase physical items?": "Yes, our Marketplace connects you directly to the founder for authentic grounding tools."
    }
    for q, a in faqs.items():
        st.markdown(f"<div class='faq-q'>{q}</div><div>{a}</div>", unsafe_allow_html=True)

# --- DISCLAIMER PAGE ---
elif st.session_state.current_page == "Disclaimer":
    st.write("### Official Disclaimer")
    st.write("Sukoon is a wellness tool designed for mindfulness and self-reflection. It is not a medical device, nor does it provide clinical therapy or psychiatric diagnosis. If you are in a crisis, please contact professional emergency services immediately.")

# --- UNIVERSAL FOOTER ---
st.markdown("<div class='disclaimer-bar'>Sukoon is a mindfulness tool, not a medical substitute.</div>", unsafe_allow_html=True)

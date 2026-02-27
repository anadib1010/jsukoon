import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#5B96B2" 
GA_ID = "G-29F4EM37KE"

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "energy_history" not in st.session_state: st.session_state.energy_history = []
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. GOOGLE ANALYTICS INJECTION ---
st.markdown(f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
    </script>
    """, unsafe_allow_html=True)

# --- 4. THE BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None
if api_key:
    genai.configure(api_key=api_key)
    for m_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]:
        try:
            temp_model = genai.GenerativeModel(m_name)
            temp_model.generate_content("Ping", generation_config={"max_output_tokens": 1})
            model = temp_model
            break 
        except: continue

# --- 5. DESIGN CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #121212 !important; color: #E0E0E0 !important; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 4rem !important; text-align: center !important; }}
    
    @keyframes pulse426 {{
        0%   {{ transform: scale(1); opacity: 0.3; border-width: 2px; }}
        33%  {{ transform: scale(1.8); opacity: 1; border-width: 4px; }}
        50%  {{ transform: scale(1.8); opacity: 1; border-width: 4px; }}
        100% {{ transform: scale(1); opacity: 0.3; border-width: 2px; }}
    }}
    
    .breathing-circle {{
        width: 60px; height: 60px; border: 3px solid {soft_blue}; border-radius: 50%;
        margin: 25px auto; animation: pulse426 12s infinite ease-in-out !important;
        box-shadow: 0 0 25px rgba(91, 150, 178, 0.5);
    }}

    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; font-size: 2.5rem; color: #FFFFFF; text-transform: uppercase; }}
    .section-header {{ font-size: 13px; letter-spacing: 4px; text-transform: uppercase; margin: 30px 0 15px 0; color: {soft_blue}; border-bottom: 1px solid #333; padding-bottom: 8px; }}
    
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(50,50,50,1) 0%, rgba(20,20,20,1) 100%) !important; 
        color: #E0E0E0 !important; border: 1px solid #444 !important; border-radius: 4px !important; 
        min-height: 45px !important; width: 100% !important; font-size: 11px !important;
    }}
    
    .market-slab {{ background: rgba(255,255,255,0.05); border: 1px solid #444; border-radius: 12px; padding: 25px; margin-bottom: 20px; text-align: center; }}
    .bundle-title {{ font-size: 22px; letter-spacing: 2px; color: #FFF; margin-bottom: 10px; }}
    .price-tag {{ font-size: 20px; color: {soft_blue}; font-weight: 600; margin-bottom: 15px; }}
    
    .disclaimer-box {{ text-align: left; font-size: 12px; opacity: 0.7; line-height: 1.8; background: #1A1A1A; padding: 20px; border-radius: 8px; border-left: 3px solid {soft_blue}; }}
    .faq-q {{ font-weight: bold; color: {soft_blue}; margin-top: 15px; text-align: left; }}
    .faq-a {{ font-size: 13px; opacity: 0.8; margin-bottom: 10px; text-align: left; border-bottom: 1px solid #222; padding-bottom: 10px; }}
    
    textarea {{ background: #1A1A1A !important; color: {soft_blue} !important; border: 1px solid #333 !important; text-align: center !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. HEADER ---
st.markdown("<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown("<div class='breathing-circle'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:10px; opacity:0.5; letter-spacing:3px;'>INHALE 4 • HOLD 2 • EXHALE 6</div>", unsafe_allow_html=True)

nav_row = st.columns(3)
nav_list = [("Journal", "Journal"), ("Market", "Market"), ("Info & FAQ", "Info")]
for i, (lab, tar) in enumerate(nav_list):
    with nav_row[i]:
        if st.button(lab, key=f"nav_{lab}"): st.session_state.current_page = tar; st.rerun()

# --- 7. PAGES ---

if st.session_state.current_page == "Journal":
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    aud_cols = st.columns(5)
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    for i, name in enumerate(sounds.keys()):
        with aud_cols[i]:
            if st.button(name, key=f"aud_{name}"): st.session_state.active_audio = sounds[name]
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    voice_input = st.audio_input("Record your thoughts")
    text_msg = st.text_area("Or type your reflection...", height=150)
    
    if st.button("CONSULT GUIDE", key="brain_btn", use_container_width=True):
        if model:
            with st.spinner("Channeling Wisdom..."):
                context = (
                    "You are the Sukoon Mentor. If a user shares a struggle regarding money, health, love, or career, "
                    "validate their specific pain. Provide a thoughtful, long-form, practical perspective. "
                    "Explain that a stable mind is necessary for right action. End by guiding them to hold "
                    "their beads/stone and follow the 4-2-6 breathing rhythm to clear their mindset."
                )
                user_content = text_msg if text_msg else "I am seeking silence."
                resp = model.generate_content([context, user_content])
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp.text})
                
                # VOICE SYNTHESIS
                clean_text = resp.text.replace('"', "'").replace("\n", " ")
                st.markdown(f"""
                    <script>
                        var msg = new SpeechSynthesisUtterance("{clean_text}");
                        msg.rate = 0.85; 
                        msg.pitch = 0.9;
                        window.speechSynthesis.speak(msg);
                    </script>
                """, unsafe_allow_html=True)
                st.rerun()

    st.markdown("<div class='section-header'>ENERGY STATE</div>", unsafe_allow_html=True)
    m_cols = st.columns(5)
    for i, m in enumerate(["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(m, key=f"m_{m}"): st.session_state.energy_history.append(m); st.rerun()

    for entry in reversed(st.session_state.private_journal):
        st.info(f"{entry['time']} | {entry['ai']}")
        if st.button(f"Listen Again ({entry['time']})", key=f"sp_{entry['time']}"):
            clean_hist = entry['ai'].replace('"', "'").replace("\n", " ")
            st.markdown(f"""<script>var m=new SpeechSynthesisUtterance("{clean_hist}");m.rate=0.85;window.speechSynthesis.speak(m);</script>""", unsafe_allow_html=True)

elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>RITUAL BUNDLES</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab'>
        <div class='bundle-title'>Starter Ritual</div>
        <div class='bundle-desc'>Selection of Grounding Stones, Buddha Sculpture, and Hand-crafted Beads.</div>
        <div class='price-tag'>₹2,499</div>
        <a href='https://wa.me/{MY_PHONE}?text=I am interested in the Starter Ritual' style='text-decoration:none;'><div style='background:{soft_blue}; color:white; padding:12px; border-radius:5px; font-weight:bold;'>ORDER VIA WHATSAPP</div></a>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab'>
        <div class='bundle-title'>Master Sanctuary</div>
        <div class='bundle-desc'>Full 5-Item Set including Art pieces and premium ritual objects.</div>
        <div class='price-tag'>₹4,999</div>
        <a href='https://wa.me/{MY_PHONE}?text=I am interested in the Master Sanctuary' style='text-decoration:none;'><div style='background:{soft_blue}; color:white; padding:12px; border-radius:5px; font-weight:bold;'>ORDER VIA WHATSAPP</div></a>
    </div>""", unsafe_allow_html=True)

elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>FREQUENTLY ASKED</div>", unsafe_allow_html=True)
    faqs = [
        ("Is my journal data stored?", "No. Your reflections stay in your current session. We do not store personal journal history on our servers."),
        ("What is the 4-2-6 Rhythm?", "It is a breathing pattern designed to reduce stress and clear the mind."),
        ("Is this therapy?", "No. Sukoon is a lifestyle companion for mindfulness and well-being."),
        ("Are the objects religious?", "No. They are tactile grounding tools intended for sensory focus.")
    ]
    for q, a in faqs:
        st.markdown(f"<div class='faq-q'>{q}</div><div class='faq-a'>{a}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>LEGAL & ETHICAL DISCLAIMER</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='disclaimer-box'>
        <b>SECULAR PRACTICE:</b> The term 'Ritual' refers to secular mindfulness practices for wellness. 
        <br><br>
        <b>NO SUPERNATURAL CLAIMS:</b> Sukoon does not make spiritual claims regarding physical objects. They are tactile tools for focus.
        <br><br>
        <b>NOT MEDICAL ADVICE:</b> This app is for lifestyle purposes only. Not intended to diagnose or treat medical conditions.
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:10px; opacity:0.3;'>Sukoon v81.0 | Google Analytics: {GA_ID}</div>", unsafe_allow_html=True)

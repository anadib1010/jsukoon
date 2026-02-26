import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#5B96B2" 

# --- 2. CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

if "private_journal" not in st.session_state: st.session_state.private_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "energy_history" not in st.session_state: st.session_state.energy_history = []
if "active_audio" not in st.session_state: st.session_state.active_audio = None

# --- 3. THEME ---
bg, txt = "#121212", "#E0E0E0"

# --- 4. BRAIN SETUP ---
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

# --- 5. DESIGN CSS (With Precise 4-2-6 Animation) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 2rem !important; text-align: center !important; }}
    
    /* 4-2-6 BREATHING MATH (Total 12s) */
    @keyframes breathe426 {{
        0%   {{ transform: scale(1); opacity: 0.3; }}      /* Start Inhale */
        33%  {{ transform: scale(1.7); opacity: 1; }}    /* 4s: Full Inhale (33% of 12s) */
        50%  {{ transform: scale(1.7); opacity: 1; }}    /* 2s: Hold (to 50% of 12s) */
        100% {{ transform: scale(1); opacity: 0.3; }}      /* 6s: Full Exhale (to 100%) */
    }}
    
    .breathing-circle {{
        width: 50px; height: 50px; border: 2px solid {soft_blue}; border-radius: 50%;
        margin: 0 auto; animation: breathe426 12s infinite ease-in-out;
        box-shadow: 0 0 20px rgba(91, 150, 178, 0.4);
    }}

    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; font-size: 2.8rem; color: #FFFFFF; text-transform: uppercase; }}
    .section-header {{ font-size: 14px; letter-spacing: 4px; text-transform: uppercase; margin: 30px 0 15px 0; color: {soft_blue}; border-bottom: 1px solid #333; padding-bottom: 5px; }}
    
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(45,45,45,1) 0%, rgba(30,30,30,1) 100%) !important; 
        color: {txt} !important; border: 1px solid #333 !important; border-radius: 4px !important; 
        min-height: 44px !important; width: 100% !important; font-size: 12px !important;
    }}
    
    .market-card {{ background: rgba(255,255,255,0.03); border: 1px solid #333; border-radius: 8px; padding: 20px; margin-bottom: 15px; text-align: left; }}
    .price-tag {{ color: {soft_blue}; font-weight: bold; font-size: 18px; }}
    .ritual-prompt {{ font-size: 14px; font-style: italic; color: {soft_blue}; text-align: center; margin: 20px 0; opacity: 0.8; }}
    textarea {{ background: #1A1A1A !important; color: {soft_blue} !important; border: 1px solid #333 !important; text-align: center !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. HEADER ---
st.markdown(f"<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown(f"<div class='breathing-circle'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:11px; margin-top:15px; opacity:0.6; letter-spacing:3px;'>INHALE (4) • HOLD (2) • EXHALE (6)</div>", unsafe_allow_html=True)

nav_row = st.columns(3)
for i, (lab, tar) in enumerate([("Journal", "Journal"), ("Market", "Market"), ("Vision", "Vision")]):
    with nav_row[i]:
        if st.button(lab, key=f"n_{lab}"): st.session_state.current_page = tar; st.rerun()

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

    st.markdown("<div class='ritual-prompt'>— Sense the support of the surface beneath you —</div>", unsafe_allow_html=True)
    text_msg = st.text_area("Release your thoughts...", height=100)
    
    if st.button("CONSULT GUIDE", key="brain_btn"):
        if model:
            with st.spinner("Processing..."):
                recent = st.session_state.energy_history[-3:]
                is_heavy = len(recent) >= 3 and all(e == "Heavier" for e in recent)
                context = "You are a Sukoon Mentor. Max 3 sentences. Focus on physical grounding."
                if is_heavy: context += " User is persistent heavy, be deeply gentle."
                resp = model.generate_content([context, text_msg if text_msg else "Silence."])
                st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": resp.text})
                st.rerun()

    st.markdown("<div class='section-header'>ENERGY STATE</div>", unsafe_allow_html=True)
    m_cols = st.columns(5)
    for i, m in enumerate(["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(m, key=f"m_{m}"): st.session_state.energy_history.append(m); st.rerun()

    for entry in reversed(st.session_state.private_journal):
        st.info(f"{entry['time']} | {entry['ai']}")
        if st.button(f"Speak ({entry['time']})", key=f"sp_{entry['time']}"):
            st.markdown(f'<script>var m=new SpeechSynthesisUtterance("{entry["ai"]}");m.rate=0.85;window.speechSynthesis.speak(m);</script>', unsafe_allow_html=True)

elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>RITUAL BUNDLES</div>", unsafe_allow_html=True)
    
    # Bundle 1
    st.markdown(f"""<div class='market-card'>
        <div style='font-size:20px; margin-bottom:5px;'>The Starter Ritual</div>
        <div style='font-size:13px; opacity:0.7; margin-bottom:10px;'>Includes: Grounding Stones, Buddha Statue, and Meditation Beads.</div>
        <div class='price-tag'>₹2,499</div>
    </div>""", unsafe_allow_html=True)
    
    # Bundle 2
    st.markdown(f"""<div class='market-card'>
        <div style='font-size:20px; margin-bottom:5px;'>The Master Sanctuary</div>
        <div style='font-size:13px; opacity:0.7; margin-bottom:10px;'>Complete 5-Item Set for a fully immersive ritual space.</div>
        <div class='price-tag'>₹4,999</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown(f"<a href='https://wa.me/{MY_PHONE}' style='text-decoration:none;'><div style='background:{soft_blue}; color:white; padding:15px; border-radius:5px; text-align:center;'>WHATSAPP TO ORDER</div></a>", unsafe_allow_html=True)

elif st.session_state.current_page == "Vision":
    st.markdown("<div class='section-header'>THE VISION</div>", unsafe_allow_html=True)
    st.write("Sukoon is a bridge between the digital and the physical. We believe that true mindfulness requires both mental presence and physical anchors.")

# --- FOOTER & INFO ---
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
f_cols = st.columns(2)
with f_cols[0]:
    if st.button("FAQ"): st.session_state.current_page = "FAQ"; st.rerun()
with f_cols[1]:
    if st.button("INFO"): st.session_state.current_page = "Info"; st.rerun()

if st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>LEGAL DISCLAIMER</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='text-align:left; font-size:12px; opacity:0.6; line-height:1.6;'>
        The term 'Ritual' as used in Sukoon refers to secular mindfulness practices and habit-stacking for personal wellness. 
        <br><br>
        Sukoon does not make any spiritual, religious, or supernatural claims regarding the physical objects (beads, stones, yantras) sold. 
        These items are intended as tactile grounding tools only. 
        <br><br>
        This app and its contents are not intended to diagnose, treat, or cure any medical or mental health conditions. 
        Always seek the advice of a qualified health provider with any questions regarding a medical condition.
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='footer-text'>Sukoon: A Sanctuary for the Modern Mind.</div>", unsafe_allow_html=True)

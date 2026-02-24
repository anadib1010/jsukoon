import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- CONFIG ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

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

# --- NAVIGATION ---
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Sukoon</h2>", unsafe_allow_html=True)
nav1, nav2, nav3, nav4 = st.columns([1, 1, 1, 1])

with nav1:
    if st.button("Journal", use_container_width=True): st.session_state.current_page = "Journal"
with nav2:
    if st.button("Market", use_container_width=True): st.session_state.current_page = "Marketplace"
with nav3:
    if st.button("Vision", use_container_width=True): st.session_state.current_page = "Vision"
with nav4:
    theme_choice = st.radio("Vibe", ["Peaceful", "Midnight"], horizontal=True, label_visibility="collapsed")

# --- THEME COLORS ---
soft_blue = "#AEC6CF" 
if theme_choice == "Peaceful":
    bg, txt, input_bg, btn_bg, card_hover = "#F9FDF9", "#2E4032", "white", "transparent", "rgba(74, 112, 85, 0.15)"
else:
    bg, txt, input_bg, btn_bg, card_hover = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A", "rgba(255, 255, 255, 0.05)"

# --- CSS ---
st.markdown(f"""
<style>
    html, body, .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    h1, h2, h3, h4, label, p, li {{ color: {txt} !important; font-weight: 200 !important; }}
    textarea {{ background-color: {input_bg} !important; color: {txt} !important; border: 1px solid #444 !important; }}
    button[kind="secondaryFormSubmit"], .stButton>button {{ background-color: {btn_bg} !important; color: {txt} !important; border: 1px solid #444 !important; border-radius: 10px !important; }}
    hr {{ border-top: 1px solid {txt} !important; opacity: 0.3; }}
    div[data-testid="stColumn"] {{ transition: all 0.4s ease; padding: 15px; border-radius: 20px; border: 1px solid rgba(128,128,128,0.1); margin-bottom: 10px; }}

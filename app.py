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
if theme_choice == "Peaceful":
    bg, txt, input_bg, btn_bg = "#F9FDF9", "#2E4032", "white", "transparent"
    card_hover = "rgba(74, 112, 85, 0.15)"
else:
    # MIDNIGHT COLORS
    bg, txt, input_bg, btn_bg = "#0A0E0B", "#AEC6CF", "#1E1E1E", "#2A2A2A"
    card_hover = "rgba(255, 255, 255, 0.05)"

# --- HEAVY DUTY CSS ---
custom_style = f"""
<style>
    html, body, .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    h1, h2, h3, h4, label, p {{ color: {txt} !important; font-weight: 200 !important; }}
    textarea {{ background-color: {input_bg} !important; color: {txt} !important; border: 1px solid #444 !important; }}
    
    /* Target all buttons including the Form 'Consult' button */
    button[kind="secondaryFormSubmit"], .stButton>button {{ 
        background-color: {btn_bg} !important; 
        color: {txt} !important; 
        border: 1px solid #444 !important; 
        border-radius: 10px !important;
    }}

    /* Hover State for all buttons */
    button[kind="secondaryFormSubmit"]:hover, .stButton>button:hover {{ 
        background-color: #3D3D3D !important; 
        border: 1px solid {txt} !important;
        color: white !important;
    }}

    hr {{ border-top: 1px solid {txt} !important; opacity: 0.3; }}
    
    /* Marketplace Grid Hover */
    div[data-testid="stColumn"] {{ transition: all 0.4s ease; padding: 10px; border-radius: 20px; }}
    div[data-testid="stColumn"]:hover {{ transform: translateY(-8px); box-shadow: 0px 15px 30px {card_hover}; }}
    
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], svg {{ display: none !important; }}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div style='text-align: center; padding: 20px;'><h3>Welcome to your sanctuary.</h3></div>", unsafe_allow_html=True)
    
    st.markdown("#### 🎵 Ambient Sounds")
    audio_type = st.radio("Format", ["Silent", "Library", "YouTube"], horizontal=True)
    if audio_type == "Library":
        choice = st.radio("Sound:", ["Forest", "Waves", "Birds", "Wind", "Flute"], horizontal=True)
        files = {"Forest": "forest.mp3", "Waves": "waves.mp3", "Birds": "birds.mp3", "Wind": "wind.mp3", "Flute": "flute.mp3"}
        target = files.get(choice)
        if target and os.path.exists(target): st.audio(target)
    elif audio_type == "YouTube":
        v_choice = st.radio("Video:", ["Rain", "Ocean", "Zen"], horizontal=True)
        v_links = {"Rain": "https://www.youtube.com/watch?v=BIcl7DrBcjg", "Ocean": "https://www.youtube.com/watch?v=unvd_fjiiAQ", "Zen": "https://www.youtube.com/watch?v=UF5H3EfvXTk"}
        st.video(v_links[v_choice])
    
    st.markdown("---")
    # Using the form to group the input and button
    with st.form("diary_form", clear_on_submit=True):
        diary_entry = st.text_area("What is on your mind today?")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_entry:
                with st.spinner("Listening..."):
                    try:
                        resp = super_brain.generate_content(f"Respond to: {diary_entry}").text
                        st.success(resp)
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_entry, "ai": resp})
                    except Exception as e:
                        if "429" in str(e):
                            st.error("The Guide is at capacity for today. Please try again tomorrow.")
                        else:
                            st.error("The Guide is resting. Please try again shortly.")
            elif not super_brain:
                st.warning("Guide setup is incomplete. Check API Key.")

    for entry in reversed(st.session_state.private_journal):
        st.write(f"🕒 {entry['time']} | {entry['diary']}")
        st.info(entry['ai'])

# --- PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("## The Marketplace")
    def display_product(label, img_file, desc):
        st.markdown(f"#### {label}")
        if os.path.exists(img_file): 
            st.image(img_file, use_container_width=True)
        st.write(desc)
        wa_url = "https://wa.me/919876543210?text=" + urllib.parse.quote(f"Interest: {label}")
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:12px; padding:12px; background-color:#25D366; color:white; border:none; font-weight:bold; cursor:pointer;">💬 WhatsApp</button></a>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: display_product("Natural Stones", "stones.jpg", "Grounding tools.")
    with c2: display_product("Crafted Beads", "beads.jpg", "Tactile focus.")
    with c3: display_product("Geometric Yantras", "yantras.jpg", "Visual focal points.")

# --- PAGE: VISION ---
elif st.session_state.current_page == "Vision":
    st.markdown("## Our Vision")
    st.write("Sukoon exists to provide peace in a loud world.")
    st.markdown('<a href="https://wa.me/919876543210" target="_blank"><button style="border-radius:10px; padding:12px; background-color:#25D366; color:white; border:none; font-weight:bold; cursor:pointer;">Message Founder</button></a>', unsafe_allow_html=True)

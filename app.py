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
css_template = """
<style>
    html, body, .stApp { background-color: V_BG !important; color: V_TXT !important; }
    h1, h2, h3, h4, label, p, li { color: V_TXT !important; font-weight: 200 !important; }
    textarea { background-color: V_IN !important; color: V_TXT !important; border: 1px solid #444 !important; }
    button[kind="secondaryFormSubmit"], .stButton>button { background-color: V_BTN !important; color: V_TXT !important; border: 1px solid #444 !important; border-radius: 10px !important; }
    hr { border-top: 1px solid V_TXT !important; opacity: 0.3; }
    div[data-testid="stColumn"] { transition: all 0.4s ease; padding: 15px; border-radius: 20px; border: 1px solid rgba(128,128,128,0.1); margin-bottom: 10px; }
    div[data-testid="stColumn"]:hover { transform: translateY(-8px); box-shadow: 0px 15px 30px V_HOV; border: 1px solid V_BLUE; }
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], svg { display: none !important; }
</style>
"""
clean_css = css_template.replace("V_BG", bg).replace("V_TXT", txt).replace("V_IN", input_bg).replace("V_BTN", btn_bg).replace("V_HOV", card_hover).replace("V_BLUE", soft_blue)
st.markdown(clean_css, unsafe_allow_html=True)
st.markdown("---")

# --- PAGE: JOURNAL ---
if st.session_state.current_page == "Journal":
    st.markdown("<div style='text-align: center; padding: 20px;'><h3>Welcome to your sanctuary.</h3></div>", unsafe_allow_html=True)
    audio_type = st.radio("Ambient Sounds", ["Silent", "Library", "YouTube"], horizontal=True)
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
    with st.form("diary_form", clear_on_submit=True):
        diary_entry = st.text_area("What is on your mind today?")
        if st.form_submit_button("Consult Guide"):
            if super_brain and diary_entry:
                with st.spinner("Listening..."):
                    try:
                        resp = super_brain.generate_content("Respond to: " + diary_entry).text
                        st.success(resp)
                        st.session_state.private_journal.append({"time": datetime.now().strftime("%H:%M"), "diary": diary_entry, "ai": resp})
                    except:
                        st.error("The Guide is at capacity for today.")
    for entry in reversed(st.session_state.private_journal):
        st.write("🕒 " + entry['time'] + " | " + entry['diary'])
        st.info(entry['ai'])

# --- PAGE: MARKETPLACE ---
elif st.session_state.current_page == "Marketplace":
    st.markdown("<h2 style='text-align: center;'>The Marketplace</h2>", unsafe_allow_html=True)
    def display_product(label, desc):
        st.markdown("#### " + label)
        st.write(desc)
        wa_url = "https://wa.me/919876543210?text=" + urllib.parse.quote("Interest: " + label)
        btn_style = "width:100%; border-radius:10px; padding:10px; border:none; font-weight:bold; cursor:pointer;"
        btn_html = f'<a href="{wa_url}" target="_blank">'
        btn_html += f'<button style="{btn_style} background-color:{soft_blue}; color:#0A0E0B;">'
        btn_html += '💬 WhatsApp</button></a>'
        st.markdown(btn_html, unsafe_allow_html=True)

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1: display_product("Natural Stones", "Tactile grounding tools.")
    with r1c2: display_product("Sacred Buddha", "A focal point for stillness.")
    with r1c3: display_product("Artic Art", "Minimalist visual tranquility.")
    
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1: display_product("Vaastu Objects", "Harmonizing your space.")
    with r2c2: display_product("Crafted Beads", "Focus through touch.")
    with r2c3: display_product("Insight Journals", "Pathways to inner clarity.")

# --- PAGE: VISION ---
elif st.session_state.current_page == "Vision":
    st.markdown("<h2 style='text-align: center;'>Our Vision</h2>", unsafe_allow_html=True)
    st.write("### Silence in a Loud World")
    st.write("Sukoon was born from a simple realization: the world is getting louder, but our internal spaces are getting smaller. We believe that technology should be a gateway to tranquility, not a source of distraction.")
    st.write("---")
    st.write("### The Journey")
    st.write("Sukoon is more than an app; it is a commitment to mental clarity. We are constantly evolving, integrating affective computing to better understand human emotion and provide support when it is needed most.")
    st.markdown("<br>", unsafe_allow_html=True)
    wa_support = "https://wa.me/919876543210?text=" + urllib.parse.quote("Hi, I'd like to support the Sukoon vision.")
    v_btn = f'<div style="text-align: center;"><a href="{wa_support}" target="_blank">'
    v_btn += f'<button style="padding:10px 25px; border-radius:10px; border:none; font-weight:bold; cursor:pointer; font-size:16px; background-color:{soft_blue}; color:#0A0E0B;">'
    v_btn += '💬 Connect with Founder</button></a></div>'
    st.markdown(v_btn, unsafe_allow_html=True)

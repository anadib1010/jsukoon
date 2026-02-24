import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# ==========================================
# WAKE UP THE SUPER BRAIN
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-2.5-flash')

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "emergency_lock" not in st.session_state:
    st.session_state.emergency_lock = False

def save_journal(user_text, ai_response, hidden_mood):
    now = datetime.now()
    today = now.strftime("%H:%M")
    entry = {"time": today, "diary": user_text, "ai_advice": ai_response, "mood": hidden_mood}
    st.session_state.private_journal.append(entry)

# ==========================================
# THE SIDEBAR
# ==========================================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["My Private Journal 📖", "The Marketplace 🛍️"])
st.sidebar.markdown("---")
st.sidebar.title("🎨 Atmosphere")
theme = st.sidebar.selectbox("Choose your vibe:", ["Peaceful 🌿", "Midnight Calm 🌙", "Psychedelic 🌀"])

# Theme CSS
if theme == "Peaceful 🌿":
    css = """<style>.stApp { background-color: #F9FDF9; color: #2E4032; } h1, h2, h3 { color: #4A7055 !important; font-family: 'Helvetica Neue', sans-serif; } textarea { background-color: #FFFFFF !important; color: #2E4032 !important; border: 1px solid #4A7055 !important; } .stButton>button { background-color: #4A7055 !important; color: white !important; }</style>"""
elif theme == "Midnight Calm 🌙":
    css = """<style>.stApp { background-color: #121212; color: #E0E0E0; } h1, h2, h3 { color: #AEC6CF !important; font-family: 'Georgia', serif; } textarea { background-color: #1E1E1E !important; color: #AEC6CF !important; border: 1px solid #AEC6CF !important; } .stButton>button { background-color: #AEC6CF !important; color: #121212 !important; }</style>"""
else:
    css = """<style>.stApp { background-image: linear-gradient(120deg, #ff00cc, #3333ff, #00ffcc); background-size: 400% 400%; color: white; } h1, h2, h3 { color: #FFFFFF !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-family: 'Courier New', monospace; } textarea { background-color: rgba(15, 10, 60, 0.8) !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; } .stButton>button { background-color: #0A0520 !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; }</style>"""

st.markdown(css, unsafe_allow_html=True)

# ==========================================
# ROOM 1: THE JOURNAL
# ==========================================
if page == "My Private Journal 📖":
    st.title("🌿 Sukoon: Your Peaceful Space")
    
    if st.session_state.emergency_lock:
        st.error("🚨 **CRISIS ALERT: PLEASE GET HELP IMMEDIATELY** 🚨")
        st.markdown("*Emergency: 112 | Vandrevala Foundation: 9999 666 555*")
    else:
        st.write("Welcome. Your thoughts here are completely private.")

        with st.expander("🎵 Play Peaceful Sounds"):
            audio_source = st.radio("Choose format:", ["App Audio Library (Data Saver)", "YouTube Video Streams"])
            
            if audio_source == "App Audio Library (Data Saver)":
                local_choice = st.selectbox("Choose an audio track:", ["Forest 🌿", "Waves 🌊", "Birds 🌲", "Wind 🍃", "Flute 🎶"])
                
                # Dictionary to map names to files
                audio_files = {
                    "Forest 🌿": "forest.mp3",
                    "Waves 🌊": "waves.mp3",
                    "Birds 🌲": "birds.mp3",
                    "Wind 🍃": "wind.mp3",
                    "Flute 🎶": "flute.mp3"
                }
                
                target_file = audio_files[local_choice]
                
                # SAFETY CHECK: Only play if file exists
                if os.path.exists(target_file):
                    st.audio(target_file)
                else:
                    st.warning(f"⚠️ Audio file '{target_file}' not found in vault. Please upload it to GitHub.")
                
            elif audio_source == "YouTube Video Streams":
                stream_choice = st.selectbox("Choose a stream:", ["Forest Rain", "Ocean Sunset", "Soothing Flute"])
                if stream_choice == "Forest Rain": st.video("https://www.youtube.com/watch?v=BIcl7DrBcjg")
                elif stream_choice == "Ocean Sunset": st.video("https://www.youtube.com/watch?v=unvd_fjiiAQ")
                elif stream_choice == "Soothing Flute": st.video("https://www.youtube.com/watch?v=UF5H3EfvXTk")

        with st.form("diary_form"):
            diary_entry = st.text_area("Dear Diary...")
            submitted = st.form_submit_button("Share my thoughts")
            
            if submitted:
                if diary_entry:
                    trigger_phrases = ["suicide", "kill myself", "harm myself", "want to die"]
                    if any(phrase in diary_entry.lower() for phrase in trigger_phrases):
                        st.session_state.emergency_lock = True
                        st.rerun()
                    else:
                        with st.spinner("Thinking..."):
                            prompt = f"Mindfulness guide: '{diary_entry}'. Format: Mood: [Word] Message: [2 sentences]"
                            response = super_brain.generate_content(prompt)
                            st.success(response.text)
                            save_journal(diary_entry, response.text, "Detected")

        st.write("---")
        for entry in reversed(st.session_state.private_journal):
            st.write(f"🕒 {entry['time']} | **You:** {entry['diary']}")

# ==========================================
# ROOM 2: THE MARKETPLACE
# ==========================================
elif page == "The Marketplace 🛍️":
    st.title("The Marketplace")
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("## 🪨\n#### Natural Stones")
        st.button("View Stones", key="s")
    with c2:
        st.markdown("## 📿\n#### Crafted Beads")
        st.button("View Beads", key="b")
    with c3:
        st.markdown("## 💠\n#### Geometric Yantras")
        st.button("View Yantras", key="y")
    
    st.write("---")
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("## 🏺\n#### Joyful Sculptures")
        st.button("View Sculptures", key="sc")
    with c5:
        st.markdown("## 📐\n#### Spatial Decor")
        st.button("View Decor", key="v")
    with c6:
        st.markdown("## 🖼️\n#### Heritage Art")
        st.button("View Art", key="a")

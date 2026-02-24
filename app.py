import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse
from google.api_core import exceptions

# ==========================================
# WAKE UP THE SUPER BRAIN
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-1.5-flash') # Slightly more stable for free tier

if "private_journal" not in st.session_state:
    st.session_state.private_journal = []
if "emergency_lock" not in st.session_state:
    st.session_state.emergency_lock = False

def get_daily_quote():
    try:
        prompt = "Create a unique, 1-sentence mindfulness quote."
        response = super_brain.generate_content(prompt)
        return response.text
    except:
        return "Peace begins with a single, conscious breath."

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

MY_NUMBER = "919876543210" # Your number

st.sidebar.markdown("---")
st.sidebar.title("🎨 Atmosphere")
theme = st.sidebar.selectbox("Choose your vibe:", ["Peaceful 🌿", "Midnight Calm 🌙", "Psychedelic 🌀"])

if theme == "Peaceful 🌿":
    css = """<style>.stApp { background-color: #F9FDF9; color: #2E4032; } h1, h2, h3 { color: #4A7055 !important; } .stButton>button { background-color: #4A7055 !important; color: white !important; }</style>"""
elif theme == "Midnight Calm 🌙":
    css = """<style>.stApp { background-color: #121212; color: #E0E0E0; } h1, h2, h3 { color: #AEC6CF !important; } .stButton>button { background-color: #AEC6CF !important; color: #121212 !important; }</style>"""
else:
    css = """<style>.stApp { background-image: linear-gradient(120deg, #ff00cc, #3333ff, #00ffcc); background-size: 400% 400%; color: white; } h1, h2, h3 { color: #FFFFFF !important; } .stButton>button { background-color: #0A0520 !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; }</style>"""

st.markdown(css, unsafe_allow_html=True)

st.sidebar.markdown("---")
feedback_msg = urllib.parse.quote("Hi! I have some feedback or a question about the Sukoon app.")
st.sidebar.markdown(f'''<a href="https://wa.me/{MY_NUMBER}?text={feedback_msg}" target="_blank"><button style="width:100%; border-radius:8px; padding:8px; background-color:#25D366; color:white; border:none; cursor:pointer; font-weight:bold;">Send Feedback / Support</button></a>''', unsafe_allow_html=True)
st.sidebar.caption("⚖️ **LEGAL & MEDICAL DISCLAIMER:**")
st.sidebar.caption("*Sukoon is designed solely for personal mindfulness exploration. It is NOT a medical tool.*")

# ==========================================
# ROOM 1: THE JOURNAL
# ==========================================
if page == "My Private Journal 📖":
    st.title("🌿 Sukoon")
    
    if st.session_state.emergency_lock:
        st.error("🚨 **CRISIS ALERT** 🚨")
        st.markdown("*Emergency: 112 | Vandrevala Foundation: 9999 666 555*")
    else:
        st.markdown(f"### *Today's Reflection:*")
        st.info(f"“{get_daily_quote()}”")
        
        with st.expander("🎵 Play Peaceful Sounds"):
            audio_source = st.radio("Choose format:", ["App Audio Library (Data Saver)", "YouTube Video Streams"])
            if audio_source == "App Audio Library (Data Saver)":
                local_choice = st.selectbox("Choose an audio track:", ["Forest 🌿", "Waves 🌊", "Birds 🌲", "Wind 🍃", "Flute 🎶"])
                audio_files = {"Forest 🌿": "forest.mp3", "Waves 🌊": "waves.mp3", "Birds 🌲": "birds.mp3", "Wind 🍃": "wind.mp3", "Flute 🎶": "flute.mp3"}
                target_file = audio_files[local_choice]
                if os.path.exists(target_file): st.audio(target_file)
                else: st.warning(f"⚠️ Audio file missing.")
            elif audio_source == "YouTube Video Streams":
                stream_choice = st.selectbox("Choose a stream:", ["Forest Rain", "Ocean Sunset", "Soothing Flute"])
                if stream_choice == "Forest Rain": st.video("https://www.youtube.com/watch?v=BIcl7DrBcjg")
                elif stream_choice == "Ocean Sunset": st.video("https://www.youtube.com/watch?v=unvd_fjiiAQ")
                elif stream_choice == "Soothing Flute": st.video("https://www.youtube.com/watch?v=UF5H3EfvXTk")

        with st.form("diary_form"):
            diary_entry = st.text_area("What is on your mind today?")
            submitted = st.form_submit_button("Share my thoughts")
            if submitted and diary_entry:
                if any(p in diary_entry.lower() for p in ["suicide", "kill myself", "harm myself", "want to die"]):
                    st.session_state.emergency_lock = True
                    st.rerun()
                else:
                    with st.spinner("Your guide is listening..."):
                        try:
                            prompt = f"""
                            You are the 'Sukoon Mindfulness Guide'. User: '{diary_entry}'
                            1. If HAPPY: Celebrate! 
                            2. If SAD: Be soft, ask to share more.
                            3. If OFFICE/MANAGER STRESS: Give 3 professional tips to handle a difficult boss and validate feelings.
                            4. End with a breathing exercise (4-7-8 or Box Breathing).
                            """
                            response = super_brain.generate_content(prompt)
                            st.success(response.text)
                            save_journal(diary_entry, response.text, "Processed")
                        except exceptions.ResourceExhausted:
                            st.warning("🏮 The Guide is currently meditating (Rate Limit Reached). Please wait 60 seconds and try again.")
                        except Exception as e:
                            st.error("The Guide is having a moment of silence. Please try again shortly.")

        st.write("---")
        for entry in reversed(st.session_state.private_journal):
            st.write(f"🕒 {entry['time']} | **You:** {entry['diary']}")

# ==========================================
# ROOM 2: THE MARKETPLACE
# ==========================================
elif page == "The Marketplace 🛍️":
    st.title("The Marketplace")
    def display_product(label, img_file, desc):
        st.markdown(f"#### {label}")
        if os.path.exists(img_file): st.image(img_file, use_container_width=True)
        else: st.warning(f"📸 Image missing.")
        st.write(desc)
        wa_url = f"https://wa.me/{MY_NUMBER}?text=" + urllib.parse.quote(f"Interest: {label}")
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:10px; padding:10px; background-color:#25D366; color:white; border:none; font-weight:bold;">💬 Buy via WhatsApp</button></a>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: display_product("Natural Stones", "stones.jpg", "Grounding stones.")
    with c2: display_product("Crafted Beads", "beads.jpg", "Breathing beads.")
    with c3: display_product("Geometric Yantras", "yantras.jpg", "Focal points.")
    st.write("---")
    c4, c5, c6 = st.columns(3)
    with c4: display_product("Joyful Sculptures", "buddha.jpg", "Contentment figures.")
    with c5: display_product("Spatial Decor", "vaastu.jpg", "Balance pieces.")
    with c6: display_product("Heritage Art", "art.jpg", "Serene art.")

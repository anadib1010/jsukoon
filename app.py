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

# Set up the Sandbox AND the Emergency Lock
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
# THE SIDEBAR (Navigation, Theme & Legal)
# ==========================================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["My Private Journal 📖", "The Marketplace 🛍️"])

st.sidebar.markdown("---")

st.sidebar.title("🎨 Atmosphere")
theme = st.sidebar.selectbox("Choose your vibe:", ["Peaceful 🌿", "Midnight Calm 🌙", "Psychedelic 🌀"])

if theme == "Peaceful 🌿":
    css = """<style>.stApp { background-color: #F9FDF9; color: #2E4032; } h1, h2, h3 { color: #4A7055 !important; font-family: 'Helvetica Neue', sans-serif; } textarea { background-color: #FFFFFF !important; color: #2E4032 !important; border: 1px solid #4A7055 !important; } div[data-baseweb="base-input"] { background-color: transparent !important; } .stButton>button, .stFormSubmitButton>button { background-color: #4A7055 !important; color: white !important; border-radius: 10px; border: none; }</style>"""
elif theme == "Midnight Calm 🌙":
    css = """<style>.stApp { background-color: #121212; color: #E0E0E0; } h1, h2, h3 { color: #AEC6CF !important; font-family: 'Georgia', serif; } textarea { background-color: #1E1E1E !important; color: #AEC6CF !important; border: 1px solid #AEC6CF !important; } div[data-baseweb="base-input"] { background-color: transparent !important; } .stButton>button, .stFormSubmitButton>button { background-color: #AEC6CF !important; color: #121212 !important; border-radius: 20px; font-weight: bold; border: none; }</style>"""
else: # Psychedelic 🌀
    css = """<style>.stApp { background-image: linear-gradient(120deg, #ff00cc, #3333ff, #00ffcc); background-size: 400% 400%; color: white; } h1, h2, h3 { color: #FFFFFF !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-family: 'Courier New', monospace; } textarea { background-color: rgba(15, 10, 60, 0.8) !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; } div[data-baseweb="base-input"] { background-color: transparent !important; } .stButton>button, .stFormSubmitButton>button { background-color: #0A0520 !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; font-weight: bold; box-shadow: 0 0 10px #00ffcc;}</style>"""

st.markdown(css, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("⚖️ **LEGAL & MEDICAL DISCLAIMER:**")
st.sidebar.caption("*Sukoon is designed solely for personal mindfulness, journaling, and aesthetic exploration. It is NOT a medical or psychological application. The AI guidance and tools provided are not a substitute for professional medical advice, psychiatric diagnosis, or therapy. Always seek the advice of a qualified health provider with any questions regarding mental health or medical conditions.*")

# ==========================================
# ROOM 1: THE JOURNAL
# ==========================================
if page == "My Private Journal 📖":
    st.title("🌿 Sukoon: Your Peaceful Space")
    
    if st.session_state.emergency_lock:
        st.error("🚨 **CRISIS ALERT: PLEASE GET HELP IMMEDIATELY** 🚨")
        st.write("Your safety is the absolute priority right now. We have detected phrases indicating you may be in immediate danger.")
        st.write("Sukoon is an AI, not a human, and cannot provide the support you need right now. Please reach out to a professional who can help.")
        st.markdown("""
        ### 📞 Immediate Resources:
        * **Emergency Services:** 112
        * **Kiran Mental Health Helpline:** 1800-599-0019
        * **Vandrevala Foundation:** 9999 666 555
        * **AASRA Helpline:** +91-9820466726
        """)
        st.info("To ensure your safety, the AI journal has been temporarily locked. Please call one of the numbers above or go to the nearest hospital.")
    
    else:
        st.write("Welcome. Your thoughts here are completely private and will vanish when you close the page.")

        # ---------------------------------------------------------
        # THE DUAL AUDIO ENGINE
        # ---------------------------------------------------------
        with st.expander("🎵 Play Peaceful Sounds"):
            st.write("Select a background soundscape to play while you journal:")
            
            audio_source = st.radio("Choose format:", ["App Audio Library (Data Saver)", "YouTube Video Streams"])
            
            if audio_source == "App Audio Library (Data Saver)":
                local_choice = st.selectbox("Choose an audio track:", [
                    "Founder's A Cappella 🎤", 
                    "Peaceful Rain 🌧️", 
                    "Ocean Waves 🌊", 
                    "Forest Birds 🌲", 
                    "Soft Wind 🍃", 
                    "Zen Flute 🎶"
                ])
                
                # Check your exact file names here!
                if local_choice == "Founder's A Cappella 🎤":
                    st.audio("mysong.mp3") 
                elif local_choice == "Peaceful Rain 🌧️":
                    st.audio("rain.mp3")
                elif local_choice == "Ocean Waves 🌊":
                    st.audio("ocean.mp3")
                elif local_choice == "Forest Birds 🌲":
                    st.audio("birds.mp3")
                elif local_choice == "Soft Wind 🍃":
                    st.audio("wind.mp3")
                elif local_choice == "Zen Flute 🎶":
                    st.audio("flute.mp3")
                
                st.caption("*(Audio-only tracks use significantly less mobile data.)*")
                
            elif audio_source == "YouTube Video Streams":
                stream_choice = st.selectbox("Choose a video stream:", ["Forest Rain 🌧️", "Ocean Sunset 🌊", "Soothing Flute 🎶"])
                if stream_choice == "Forest Rain 🌧️":
                    st.video("https://www.youtube.com/watch?v=BIcl7DrBcjg")
                elif stream_choice == "Ocean Sunset 🌊":
                    st.video("https://www.youtube.com/watch?v=unvd_fjiiAQ")
                elif stream_choice == "Soothing Flute 🎶":
                    st.video("https://www.youtube.com/watch?v=UF5H3EfvXTk")

        with st.form("diary_form"):
            diary_entry = st.text_area("Dear Diary...")
            submitted = st.form_submit_button("Share my thoughts")
            st.caption("⚠️ *Disclaimer: Sukoon is an AI companion for mindfulness. It is not a medical, psychological, or psychiatric tool. If you are in distress, please seek professional help immediately.*")
            
            if submitted:
                if diary_entry == "":
                    st.warning("Please write something first!")
                else:
                    trigger_phrases = [
                        "suicide", "kill myself", "end my life", "want to die", 
                        "hurt myself", "harm myself", "cut myself", 
                        "kill someone", "hurt someone", "harm someone", "don't want to live"
                    ]
                    
                    user_text_lower = diary_entry.lower()
                    is_crisis = any(phrase in user_text_lower for phrase in trigger_phrases)

                    if is_crisis:
                        st.session_state.emergency_lock = True
                        st.rerun()
                    else:
                        with st.spinner("Your AI guide is thinking..."):
                            prompt = f"""You are a highly empathetic mindfulness guide. Read this diary entry and silently detect the user's underlying emotional state. Diary Entry: '{diary_entry}' You must respond STRICTLY in this exact format:
                            Mood: [Write exactly ONE word describing their emotion]
                            Message: [Write two short, comforting sentences]"""
                            
                            response = super_brain.generate_content(prompt)
                            ai_output = response.text
                            
                            try:
                                parts = ai_output.split("Message:")
                                detected_mood = parts[0].replace("Mood:", "").strip()
                                comforting_message = parts[1].strip()
                            except:
                                detected_mood = "Unknown"
                                comforting_message = ai_output
                            
                            st.success("Your guide has replied:")
                            st.write(comforting_message)
                            st.caption(f"*(Silent detection: The AI sensed you are feeling {detected_mood})*")
                            save_journal(diary_entry, comforting_message, detected_mood)

        st.write("---")
        st.subheader("📖 Today's Private Thoughts")
        if len(st.session_state.private_journal) == 0:
            st.write("Your sand garden is empty. Write your first entry above!")
        else:
            for entry in reversed(st.session_state.private_journal):
                st.write("🕒", entry["time"])
                st.write(f"**Detected Mood:** {entry.get('mood', 'Unknown')}") 
                st.write("**You:**", entry["diary"])
                st.write("**AI Guide:**", entry["ai_advice"])
                st.write("-")

# ==========================================
# ROOM 2: THE MARKETPLACE
# ==========================================
elif page == "The Marketplace 🛍️":
    st.title("The Marketplace")
    st.write("Curated physical items to ground your space and support your mindfulness practice.")
    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("## 🪨")
        st.markdown("#### Natural Stones")
        st.write("Unpolished, naturally sourced stones. Perfect for providing a cool, grounding physical touchstone during moments of high stress.")
        st.button("View Stones", key="btn_stones")

    with col2:
        st.markdown("## 📿")
        st.markdown("#### Crafted Beads")
        st.write("Tactile wooden and seed beads. A purely mechanical tool to help you keep rhythm during breathing exercises or meditation.")
        st.button("View Beads", key="btn_beads")

    with col3:
        st.markdown("## 💠")
        st.markdown("#### Geometric Yantras")
        st.write("Precision-crafted metalwork featuring complex symmetry. Designed to provide a focal point for the eyes when practicing concentration.")
        st.button("View Yantras", key="btn_yantras")

    st.write("---")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("## 🏺")
        st.markdown("#### Joyful Sculptures")
        st.write("Traditional artistic figures representing contentment and abundance. Perfect as a cheerful, grounding desk ornament for your workspace.")
        st.button("View Sculptures", key="btn_buddha")

    with col5:
        st.markdown("## 📐")
        st.markdown("#### Spatial Decor")
        st.write("Architectural decor pieces designed to inspire a sense of balance and spatial awareness in your living environment.")
        st.button("View Decor", key="btn_vaastu")

    with col6:
        st.markdown("## 🖼️")
        st.markdown("#### Heritage Art")
        st.write("Intricately crafted photo frames and classical statues inspired by historical iconography, offering a serene, artistic focal point.")
        st.button("View Art", key="btn_deities")

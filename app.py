import streamlit as st
from datetime import datetime
import os
import google.generativeai as genai

# ==========================================
# THE THEME ENGINE 
# ==========================================
st.sidebar.title("🎨 Atmosphere")
theme = st.sidebar.selectbox("Choose your vibe:", ["Peaceful 🌿", "Midnight Calm 🌙", "Psychedelic 🌀"])

if theme == "Peaceful 🌿":
    css = """
    <style>
    .stApp { background-color: #F9FDF9; color: #2E4032; }
    h1, h2, h3 { color: #4A7055 !important; font-family: 'Helvetica Neue', sans-serif; }
    textarea { background-color: #FFFFFF !important; color: #2E4032 !important; border: 1px solid #4A7055 !important; }
    div[data-baseweb="base-input"] { background-color: transparent !important; }
    .stButton>button, .stFormSubmitButton>button { background-color: #4A7055 !important; color: white !important; border-radius: 10px; border: none; }
    </style>
    """
elif theme == "Midnight Calm 🌙":
    css = """
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2, h3 { color: #AEC6CF !important; font-family: 'Georgia', serif; }
    textarea { background-color: #1E1E1E !important; color: #AEC6CF !important; border: 1px solid #AEC6CF !important; }
    div[data-baseweb="base-input"] { background-color: transparent !important; }
    .stButton>button, .stFormSubmitButton>button { background-color: #AEC6CF !important; color: #121212 !important; border-radius: 20px; font-weight: bold; border: none; }
    </style>
    """
else: # Psychedelic 🌀
    css = """
    <style>
    .stApp { background-image: linear-gradient(120deg, #ff00cc, #3333ff, #00ffcc); background-size: 400% 400%; color: white; }
    h1, h2, h3 { color: #FFFFFF !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-family: 'Courier New', monospace; }
    textarea { background-color: rgba(15, 10, 60, 0.8) !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; }
    div[data-baseweb="base-input"] { background-color: transparent !important; }
    .stButton>button, .stFormSubmitButton>button { background-color: #0A0520 !important; color: #00ffcc !important; border: 2px solid #00ffcc !important; font-weight: bold; box-shadow: 0 0 10px #00ffcc;}
    </style>
    """

st.markdown(css, unsafe_allow_html=True)

# ==========================================
# WAKE UP THE SUPER BRAIN
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# THE PRIVATE SANDBOX (Session State Memory)
# ==========================================
# Check if this user has a temporary journal yet. If not, make one!
if "private_journal" not in st.session_state:
    st.session_state.private_journal = []

def save_journal(user_text, ai_response, hidden_mood):
    now = datetime.now()
    today = now.strftime("%H:%M") # Just showing time since it's a daily sandbox
    entry = {"time": today, "diary": user_text, "ai_advice": ai_response, "mood": hidden_mood}
    
    # Save it directly into the user's temporary browser memory
    st.session_state.private_journal.append(entry)

# ==========================================
# THE FACE
# ==========================================
st.title("🌿 Sukoon: Your Peaceful Space")
st.write("Welcome. Your thoughts here are completely private and will vanish when you close the page.")

with st.form("diary_form"):
    diary_entry = st.text_area("Dear Diary...")
    submitted = st.form_submit_button("Share my thoughts")
    
    if submitted:
        if diary_entry == "":
            st.warning("Please write something first!")
        else:
            with st.spinner("Your AI guide is thinking..."):
                prompt = f"""
                You are a highly empathetic mindfulness guide. 
                Read this diary entry and silently detect the user's underlying emotional state.
                Diary Entry: '{diary_entry}'
                You must respond STRICTLY in this exact format:
                Mood: [Write exactly ONE word describing their emotion]
                Message: [Write two short, comforting sentences]
                """
                
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
                
                # Save to the private sandbox!
                save_journal(diary_entry, comforting_message, detected_mood)

# ==========================================
# THE MANAGER
# ==========================================
st.write("---")
st.subheader("📖 Today's Private Thoughts")

# Read backwards from the sandbox memory
if len(st.session_state.private_journal) == 0:
    st.write("Your sand garden is empty. Write your first entry above!")
else:
    for entry in reversed(st.session_state.private_journal):
        st.write("🕒", entry["time"])
        st.write(f"**Detected Mood:** {entry.get('mood', 'Unknown')}") 
        st.write("**You:**", entry["diary"])
        st.write("**AI Guide:**", entry["ai_advice"])
        st.write("-")

import streamlit as st
import json
from datetime import datetime
import os
import google.generativeai as genai

# ==========================================
# THE THEME ENGINE (CSS Injection)
# ==========================================
st.sidebar.title("🎨 Atmosphere")
theme = st.sidebar.selectbox("Choose your vibe:", ["Peaceful 🌿", "Glamorous ✨", "Psychedelic 🌀"])

if theme == "Peaceful 🌿":
    css = """
    <style>
    .stApp { background-color: #F9FDF9; color: #2E4032; }
    h1, h2, h3 { color: #4A7055; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #4A7055; color: white; border-radius: 10px; border: none; }
    </style>
    """
elif theme == "Glamorous ✨":
    css = """
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 20px; font-weight: bold; border: none; }
    </style>
    """
else: # Psychedelic 🌀
    css = """
    <style>
    .stApp { background-image: linear-gradient(120deg, #ff00cc, #3333ff, #00ffcc); background-size: 400% 400%; color: white; }
    h1, h2, h3 { color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00ffcc; border: 2px solid #00ffcc; font-weight: bold; box-shadow: 0 0 10px #00ffcc;}
    </style>
    """

# Apply the paint to the walls!
st.markdown(css, unsafe_allow_html=True)


# ==========================================
# WAKE UP THE SUPER BRAIN
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-2.5-flash')

def save_journal(user_text, ai_response, hidden_mood):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M")
    entry = {"date": today, "diary": user_text, "ai_advice": ai_response, "mood": hidden_mood}
    try:
        with open("super_journal.json", "r") as f:
            history = json.load(f)
    except:
        history = []
    history.append(entry)
    with open("super_journal.json", "w") as f:
        json.dump(history, f)


# ==========================================
# THE FACE
# ==========================================
st.title("🌿 Sukoon: Your Peaceful Space")
st.write("Welcome. Write your thoughts below, and your AI guide will respond.")

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
                save_journal(diary_entry, comforting_message, detected_mood)


# ==========================================
# THE MANAGER
# ==========================================
st.write("---")
st.subheader("📖 My AI Journal History")

try:
    with open("super_journal.json", "r") as f:
        history = json.load(f)
        
    for entry in reversed(history):
        st.write("🕒", entry["date"])
        st.write(f"**Detected Mood:** {entry.get('mood', 'Unknown')}") 
        st.write("**You:**", entry["diary"])
        st.write("**AI Guide:**", entry["ai_advice"])
        st.write("-")
except:
    st.write("Your journal is empty. Write your first entry above!")

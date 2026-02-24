%%writefile app.py
import streamlit as st
import json
from datetime import datetime
import os
import google.generativeai as genai

# 1. Grab the key from the backpack
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
super_brain = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# THE KITCHEN (Now saves the hidden mood!)
# ==========================================
def save_journal(user_text, ai_response, hidden_mood):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M")
    
    # We pack the hidden mood into the memory box!
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
                
                # -----------------------------------------
                # THE SECRET PROMPT (Affective Computing)
                # -----------------------------------------
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
                
                # -----------------------------------------
                # THE PYTHON SPLIT TRICK
                # -----------------------------------------
                # The AI will give us a string like "Mood: Sad \n Message: It is okay."
                # We use .split() to chop it into pieces so we can separate the mood from the message!
                
                try:
                    # Chop the text in half at the word "Message:"
                    parts = ai_output.split("Message:")
                    
                    # Clean up the Mood part (remove the word "Mood:" and any extra spaces)
                    detected_mood = parts[0].replace("Mood:", "").strip()
                    
                    # Clean up the Message part
                    comforting_message = parts[1].strip()
                    
                except:
                    # Just in case the AI messes up the formatting!
                    detected_mood = "Unknown"
                    comforting_message = ai_output
                
                # Show ONLY the comforting message to the user!
                st.success("Your guide has replied:")
                st.write(comforting_message)
                
                # Show the silently detected mood as a tiny, subtle caption
                st.caption(f"*(Silent detection: The AI sensed you are feeling {detected_mood})*")
                
                # Send everything to the Kitchen
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
        
        # Now we show the detected mood in the history!
        st.write(f"**Detected Mood:** {entry.get('mood', 'Unknown')}") 
        st.write("**You:**", entry["diary"])
        st.write("**AI Guide:**", entry["ai_advice"])
        st.write("-")
except:
    st.write("Your journal is empty. Write your first entry above!")

import streamlit as st
import json
from datetime import datetime
import os
import google.generativeai as genai

# 1. Look in the invisible backpack for the API key!
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Wake up the Super Brain
super_brain = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# THE KITCHEN (Saves both your words and the AI's words!)
# ==========================================
def save_journal(user_text, ai_response):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M")
    entry = {"date": today, "diary": user_text, "ai_advice": ai_response}
    
    try:
        with open("super_journal.json", "r") as f:
            history = json.load(f)
    except:
        history = []
        
    history.append(entry)
    
    with open("super_journal.json", "w") as f:
        json.dump(history, f)

# ==========================================
# THE FACE (The Website)
# ==========================================
st.title("🌿 My AI Mindfulness Companion")
st.write("Welcome. Write your thoughts below, and your AI guide will respond.")

with st.form("diary_form"):
    diary_entry = st.text_area("Dear Diary...")
    submitted = st.form_submit_button("Share my thoughts")
    
    if submitted:
        if diary_entry == "":
            st.warning("Please write something first!")
        else:
            # Show a spinning wheel while the AI thinks!
            with st.spinner("Your AI guide is thinking..."):
                
                # We give the AI secret instructions on how to act!
                prompt = f"You are a kind, mindful therapist. The user says: '{diary_entry}'. Write 2 short, comforting sentences to help them."
                
                # Make the phone call!
                response = super_brain.generate_content(prompt)
                ai_words = response.text
                
                # Print the AI's response to the screen
                st.success("The AI says:")
                st.write(ai_words)
                
                # Tell the Kitchen to save everything!
                save_journal(diary_entry, ai_words)

# ==========================================
# THE MANAGER (Reads the memory)
# ==========================================
st.write("---")
st.subheader("📖 My AI Journal History")

try:
    with open("super_journal.json", "r") as f:
        history = json.load(f)
        
    for entry in reversed(history):
        st.write("🕒", entry["date"])
        st.write("**You:**", entry["diary"])
        st.write("**AI Guide:**", entry["ai_advice"])
        st.write("-")
except:
    st.write("Your journal is empty. Write your first entry above!")

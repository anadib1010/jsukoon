import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import os
import google.generativeai as genai
import urllib.parse

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
soft_blue = "#5B96B2" 
GA_ID = "G-29F4EM37KE"

# --- 2. CONFIG & PWA META TAGS ---
st.set_page_config(page_title="Sukoon", layout="centered", initial_sidebar_state="collapsed")

st.markdown(f"""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
    """, unsafe_allow_html=True)

if "core_journal" not in st.session_state: st.session_state.core_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "energy_history" not in st.session_state: st.session_state.energy_history = []
if "active_audio" not in st.session_state: st.session_state.active_audio = None
if "active_focus" not in st.session_state: st.session_state.active_focus = "Release"

# --- 3. GOOGLE ANALYTICS ---
components.html(f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}', {{ 'anonymize_ip': true }});
    </script>
    """, height=0)

# --- 4. THE BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None
if api_key:
    genai.configure(api_key=api_key)
    # RESTORED: The flagship 2.5-flash model tied to your Jio 20-use quota
    model = genai.GenerativeModel("gemini-2.5-flash")

# --- 5. DESIGN CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #121212 !important; color: #E0E0E0 !important; }}
    .block-container {{ max-width: 600px !important; margin: auto; padding-top: 4.5rem !important; text-align: center !important; }}
    
    @keyframes pulse426 {{
        0%   {{ transform: scale(1); opacity: 0.3; border-width: 2px; }}
        33%  {{ transform: scale(1.8); opacity: 1; border-width: 4px; }}
        50%  {{ transform: scale(1.8); opacity: 1; border-width: 4px; }}
        100% {{ transform: scale(1); opacity: 0.3; border-width: 2px; }}
    }}
    
    .breathing-circle {{
        width: 60px; height: 60px; border: 3px solid {soft_blue}; border-radius: 50%;
        margin: 25px auto; animation: pulse426 12s infinite ease-in-out !important;
        box-shadow: 0 0 25px rgba(91, 150, 178, 0.5);
    }}

    .main-title {{ text-align: center; letter-spacing: 12px; font-weight: 200; font-size: 2.5rem; color: #FFFFFF; text-transform: uppercase; }}
    .section-header {{ font-size: 13px; letter-spacing: 4px; text-transform: uppercase; margin: 30px 0 15px 0; color: {soft_blue}; border-bottom: 1px solid #333; padding-bottom: 8px; }}
    
    .stButton>button {{ 
        background: linear-gradient(180deg, rgba(50,50,50,1) 0%, rgba(20,20,20,1) 100%) !important; 
        color: #E0E0E0 !important; border: 1px solid #444 !important; border-radius: 4px !important; 
        min-height: 48px !important; width: 100% !important; font-size: 11px !important;
    }}
    
    .market-slab {{ background: rgba(255,255,255,0.05); border: 1px solid #444; border-radius: 12px; padding: 25px; margin-bottom: 20px; text-align: center; }}
    .bundle-title {{ font-size: 22px; letter-spacing: 2px; color: #FFF; margin-bottom: 10px; }}
    .price-tag {{ font-size: 20px; color: {soft_blue}; font-weight: 600; margin-bottom: 15px; }}
    
    .disclaimer-box {{ text-align: left; font-size: 12px; opacity: 0.7; line-height: 1.8; background: #1A1A1A; padding: 20px; border-radius: 8px; border-left: 3px solid {soft_blue}; }}
    .faq-q {{ font-weight: bold; color: {soft_blue}; margin-top: 15px; text-align: left; }}
    .faq-a {{ font-size: 13px; opacity: 0.8; margin-bottom: 10px; text-align: left; border-bottom: 1px solid #222; padding-bottom: 10px; }}
    
    textarea {{ background: #1A1A1A !important; color: #E0E0E0 !important; border: 1px solid #333 !important; text-align: center !important; font-size: 15px !important; }}
    .journal-entry {{ background: #1A1A1A; border-left: 3px solid {soft_blue}; padding: 18px; margin-bottom: 5px; border-radius: 6px; color: #FFFFFF; text-align: left; font-size: 15px; line-height: 1.6; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. HEADER ---
st.markdown("<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown("<div class='breathing-circle'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:10px; opacity:0.5; letter-spacing:3px;'>INHALE 4 • HOLD 2 • EXHALE 6</div>", unsafe_allow_html=True)

nav_row = st.columns(4)
nav_list = [("Journal", "Journal"), ("Focus", "Focus"), ("Market", "Market"), ("Info", "Info")]
for i, (lab, tar) in enumerate(nav_list):
    with nav_row[i]:
        if st.button(lab, key=f"nav_{lab}"): st.session_state.current_page = tar; st.rerun()

# --- 7. PAGES ---

if st.session_state.current_page == "Journal":
    st.markdown("<div class='section-header'>AMBIENCE</div>", unsafe_allow_html=True)
    aud_cols = st.columns(5)
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    for i, name in enumerate(sounds.keys()):
        with aud_cols[i]:
            if st.button(name, key=f"aud_{name}"): st.session_state.active_audio = sounds[name]
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    components.html("""
        <div style="background:#1A1A1A; border: 1px solid #333; border-radius: 8px; position:relative; width:100%; height:120px; overflow:hidden; cursor:crosshair;" id="zen-box">
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:#5B96B2; font-family:sans-serif; font-size:11px; letter-spacing:2px; opacity:0.4; pointer-events:none; text-align:center;">
                TOUCH THE SURFACE<br>TO GROUND YOURSELF
            </div>
            <canvas id="zenCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0;"></canvas>
        </div>
        <script>
            const canvas = document.getElementById('zenCanvas');
            const ctx = canvas.getContext('2d');
            let ripples = [];
            function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
            window.addEventListener('resize', resize); resize();
            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < ripples.length; i++) {
                    let r = ripples[i];
                    ctx.beginPath(); ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
                    ctx.strokeStyle = `rgba(91, 150, 178, ${r.alpha})`; ctx.lineWidth = 2; ctx.stroke();
                    r.radius += 0.8; r.alpha -= 0.01;
                }
                ripples = ripples.filter(r => r.alpha > 0); requestAnimationFrame(draw);
            }
            document.getElementById('zen-box').addEventListener('pointerdown', (e) => {
                const rect = canvas.getBoundingClientRect();
                ripples.push({ x: e.clientX - rect.left, y: e.clientY - rect.top, radius: 5, alpha: 0.8 });
            });
            draw();
        </script>
    """, height=135)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    voice_input = st.audio_input("Record your thoughts")
    text_msg = st.text_area("Or type your reflection...", height=150)
    
    c_short, c_deep = st.columns(2)
    with c_short:
        btn_short = st.button("GUIDE (SHORT)", use_container_width=True)
    with c_deep:
        btn_deep = st.button("GUIDE (DEEP)", use_container_width=True)
    
    if btn_short or btn_deep:
        if model:
            with st.spinner("Channeling Wisdom..."):
                length_instruction = "Keep the response short: maximum 2 paragraphs." if btn_short else "Provide a detailed, deep, and highly comforting long-form response. Take your time to thoroughly explain and explore their feelings."
                
                context = f"""You are the Sukoon Mentor. 
                1. Detect the language the user is speaking or typing. You MUST respond in that exact same language.
                2. STRICT LANGUAGE RULE: If the user speaks or writes in pure English, you MUST respond in pure English. If the user speaks or writes in 'Hinglish' (Hindi words using the English alphabet), you MUST respond entirely in Hinglish. Do not mix them up.
                3. {length_instruction} Use simple, easy-to-understand words.
                4. End with a brief 'Inhale 4 - Hold 2 - Exhale 6' reminder, translated perfectly into their language/Hinglish.
                5. If the user provides an audio recording, start with 'You said: [their transcribed words]' in their exact language, then give your advice."""
                
                try:
                    if voice_input:
                        audio_part = {"mime_type": "audio/wav", "data": voice_input.getvalue()}
                        prompt_parts = [context, audio_part, "Listen to my voice note, transcribe it exactly, then respond."]
                    elif text_msg:
                        prompt_parts = [context, text_msg]
                    else:
                        prompt_parts = [context, "I am seeking silence."]
                        
                    resp = model.generate_content(prompt_parts)
                    unique_id = str(datetime.now().timestamp()).replace('.', '')
                    
                    st.session_state.core_journal.append({
                        "time": datetime.now().strftime("%H:%M"), 
                        "ai": resp.text,
                        "id": unique_id
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Technical Error: {str(e)}")
        else:
            st.warning("The Mentor is resting. Please try again in an hour.")

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    for entry in reversed(st.session_state.core_journal):
        safe_speech_text = urllib.parse.quote(entry['ai'])
        html_button = f"""
        <style>
            .listen-btn {{
                background: linear-gradient(180deg, rgba(50,50,50,1) 0%, rgba(20,20,20,1) 100%);
                color: #E0E0E0; border: 1px solid #444; border-radius: 4px; padding: 12px;
                font-size: 11px; font-family: sans-serif; cursor: pointer; width: 100%; text-transform: uppercase;
                margin-bottom: 5px;
            }}
            .listen-btn:active {{ background: #333; }}
        </style>
        <button class="listen-btn" onclick="playVoice()">LISTEN TO MENTOR ({entry['time']})</button>
        <script>
            function playVoice() {{
                window.speechSynthesis.cancel();
                var decodedText = decodeURIComponent("{safe_speech_text}");
                var m = new SpeechSynthesisUtterance(decodedText);
                m.rate = 0.85;
                m.lang = 'hi-IN'; 
                
                function setVoiceAndSpeak() {{
                    var voices = window.speechSynthesis.getVoices();
                    var localVoice = voices.find(v => v.lang.includes('hi-IN') || v.lang.includes('en-IN') || v.name.includes('India') || v.name.includes('Hindi'));
                    
                    if (localVoice) {{
                        m.voice = localVoice;
                    }}
                    window.speechSynthesis.speak(m);
                }}

                if (window.speechSynthesis.getVoices().length === 0) {{
                    window.speechSynthesis.onvoiceschanged = setVoiceAndSpeak;
                }} else {{
                    setVoiceAndSpeak();
                }}
            }}
        </script>
        """
        components.html(html_button, height=50)

        formatted_text = entry['ai'].replace('\n', '<br>')
        st.markdown(f"<div class='journal-entry'><b>{entry['time']}</b><br><br>{formatted_text}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>ENERGY STATE</div>", unsafe_allow_html=True)
    m_cols = st.columns(5)
    for i, m in enumerate(["Quiet", "Heavier", "Neutral", "Steady", "Vibrant"]):
        with m_cols[i]:
            if st.button(m, key=f"m_{m}"): st.session_state.energy_history.append(m); st.rerun()

elif st.session_state.current_page == "Focus":
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        if st.button("The Release"): st.session_state.active_focus = "Release"; st.rerun()
    with g_col2:
        if st.button("The Bloom"): st.session_state.active_focus = "Bloom"; st.rerun()

    if st.session_state.active_focus == "Release":
        st.markdown("<div class='section-header'>THE RELEASE</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px;'>Tap the rising thoughts to release them.</p>", unsafe_allow_html=True)
        
        game_html = """
        <div style="background:#1A1A1A; border: 1px solid #333; border-radius: 8px; position:relative; width:100%; height:450px; overflow:hidden;">
            <div id="scoreDisplay" style="position:absolute; top:15px; width:100%; text-align:center; color:#5B96B2; font-family:sans-serif; font-size:12px; letter-spacing:3px; z-index:10; pointer-events:none;">
                THOUGHTS RELEASED: <span id="scoreVal">0</span>
            </div>
            <canvas id="gameCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
        </div>
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            let bubbles = []; let score = 0;
            
            function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
            window.addEventListener('resize', resize); resize();

            function createBubble() {
                bubbles.push({
                    x: Math.random() * (canvas.width - 40) + 20, y: canvas.height + 20,
                    radius: Math.random() * 15 + 15, speed: Math.random() * 0.8 + 0.4,
                    alpha: 0.6, popping: false
                });
            }
            setInterval(createBubble, 1200);

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = bubbles.length - 1; i >= 0; i--) {
                    let b = bubbles[i];
                    ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
                    
                    if (b.popping) {
                        b.radius += 2; b.alpha -= 0.05;
                        ctx.strokeStyle = `rgba(91, 150, 178, ${b.alpha})`; ctx.lineWidth = 2; ctx.stroke();
                        if (b.alpha <= 0) bubbles.splice(i, 1);
                    } else {
                        b.y -= b.speed;
                        ctx.fillStyle = `rgba(91, 150, 178, ${b.alpha})`; ctx.fill();
                        ctx.shadowBlur = 15; ctx.shadowColor = "rgba(91, 150, 178, 0.5)";
                        if (b.y < -50) bubbles.splice(i, 1);
                    }
                }
                requestAnimationFrame(draw);
            }

            canvas.addEventListener('pointerdown', (e) => {
                const rect = canvas.getBoundingClientRect();
                const clickX = e.clientX - rect.left; const clickY = e.clientY - rect.top;
                for (let i = 0; i < bubbles.length; i++) {
                    let b = bubbles[i];
                    if (!b.popping && Math.hypot(clickX - b.x, clickY - b.y) < b.radius + 15) {
                        b.popping = true; score++; document.getElementById('scoreVal').innerText = score; break;
                    }
                }
            });
            draw();
        </script>
        """
        components.html(game_html, height=470)

    elif st.session_state.active_focus == "Bloom":
        st.markdown("<div class='section-header'>THE BLOOM</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 13px; opacity: 0.8; margin-bottom: 20px;'>Tap the center slowly to grow your light.</p>", unsafe_allow_html=True)
        
        bloom_html = """
        <div style="background:#1A1A1A; border: 1px solid #333; border-radius: 8px; position:relative; width:100%; height:450px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
            <canvas id="bloomCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
            <div id="bloomMessage" style="position:absolute; z-index:10; color:#FFFFFF; font-family:sans-serif; font-size:14px; letter-spacing:3px; text-align:center; opacity:0; transition: opacity 1.5s ease-in-out; pointer-events:none; background:rgba(0,0,0,0.5); padding:10px 20px; border-radius:4px; border:1px solid #5B96B2;">
            </div>
        </div>
        <script>
            const c = document.getElementById('bloomCanvas');
            const ctx = c.getContext('2d');
            const msg = document.getElementById('bloomMessage');
            let taps = 0;
            const maxTaps = 6;
            const affirmations = ["BEAUTIFUL FOCUS", "YOU ARE GROWING", "A MOMENT OF PEACE", "PERFECT HARMONY", "YOU ARE ENOUGH"];

            function resize() { c.width = c.offsetWidth; c.height = c.offsetHeight; draw(); }
            window.addEventListener('resize', resize);
            
            function draw() {
                ctx.clearRect(0, 0, c.width, c.height);
                const cx = c.width / 2;
                const cy = c.height / 2;
                
                if (taps === 0) {
                    ctx.fillStyle = "#5B96B2"; ctx.globalAlpha = 0.5; ctx.font = "12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "2px";
                    ctx.fillText("TAP TO BLOOM", cx, cy);
                    return;
                }
                
                for (let i = 1; i <= taps; i++) {
                    ctx.beginPath();
                    ctx.arc(cx, cy, i * 25, 0, Math.PI * 2);
                    ctx.strokeStyle = "#5B96B2";
                    ctx.lineWidth = 1.5;
                    ctx.globalAlpha = 0.2 + (i * 0.1);
                    ctx.stroke();
                    
                    for (let j = 0; j < 8; j++) {
                        let angle = (j * Math.PI / 4) + (i * 0.2);
                        let px = cx + Math.cos(angle) * (i * 25);
                        let py = cy + Math.sin(angle) * (i * 25);
                        ctx.beginPath();
                        ctx.arc(px, py, 4 + i, 0, Math.PI * 2);
                        ctx.fillStyle = "#5B96B2";
                        ctx.shadowBlur = 15;
                        ctx.shadowColor = "#5B96B2";
                        ctx.fill();
                    }
                }
            }
            
            c.addEventListener('pointerdown', () => {
                if (taps < maxTaps) {
                    taps++;
                    draw();
                    if (taps === maxTaps) {
                        msg.innerText = affirmations[Math.floor(Math.random() * affirmations.length)];
                        msg.style.opacity = 1;
                        setTimeout(() => {
                            msg.style.opacity = 0;
                            setTimeout(() => { taps = 0; draw(); }, 1500);
                        }, 3500);
                    }
                }
            });
            resize();
        </script>
        """
        components.html(bloom_html, height=470)

elif st.session_state.current_page == "Market":
    st.markdown("<div class='section-header'>RITUAL BUNDLES</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab'>
        <div class='bundle-title'>Starter Ritual</div>
        <div class='bundle-desc'>Selection of Grounding Stones, Buddha Sculpture, and Hand-crafted Beads.</div>
        <div class='price-tag'>₹2,499</div>
        <a href='https://wa.me/{MY_PHONE}?text=I am interested in the Starter Ritual' style='text-decoration:none;'><div style='background:{soft_blue}; color:white; padding:12px; border-radius:5px; font-weight:bold;'>ORDER VIA WHATSAPP</div></a>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab'>
        <div class='bundle-title'>Master Sanctuary</div>
        <div class='bundle-desc'>Full 5-Item Set including Art pieces and premium ritual objects.</div>
        <div class='price-tag'>₹4,999</div>
        <a href='https://wa.me/{MY_PHONE}?text=I am interested in the Master Sanctuary' style='text-decoration:none;'><div style='background:{soft_blue}; color:white; padding:12px; border-radius:5px; font-weight:bold;'>ORDER VIA WHATSAPP</div></a>
    </div>""", unsafe_allow_html=True)

elif st.session_state.current_page == "Info":
    st.markdown("<div class='section-header'>INSTALL SUKOON</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab' style='text-align:left; font-size:13px;'>
        1. Open this link in <b>Safari (iPhone)</b> or <b>Chrome (Android)</b>.<br><br>
        2. Tap the <b>Share</b> or <b>Menu (⋮)</b> icon.<br><br>
        3. Select <b>'Add to Home Screen'</b>.<br><br>
        4. Open Sukoon from your home screen for a <b>Full-Screen experience</b>.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>FREQUENTLY ASKED</div>", unsafe_allow_html=True)
    faqs = [
        ("Is my journal data stored?", "No. Your reflections stay in your current session. We do not store personal journal history on our servers."),
        ("What is the 4-2-6 Rhythm?", "It is a breathing pattern designed to reduce stress and clear the mind."),
        ("Is this therapy?", "No. Sukoon is a lifestyle companion for mindfulness and well-being."),
        ("Are the objects religious?", "No. They are tactile grounding tools intended for sensory focus.")
    ]
    for q, a in faqs:
        st.markdown(f"<div class='faq-q'>{q}</div><div class='faq-a'>{a}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>LEGAL & ETHICAL DISCLAIMER</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='disclaimer-box'>
        <b>1. SECULAR PRACTICE:</b> The term 'Ritual' refers to secular mindfulness practices for wellness. <br><br>
        <b>2. NO SUPERNATURAL CLAIMS:</b> Sukoon does not make spiritual claims regarding physical objects. They are strictly tactile tools for focus. <br><br>
        <b>3. NOT MEDICAL ADVICE:</b> This app is for lifestyle purposes only. Not intended to diagnose or treat medical conditions. <br><br>
        <b>4. DATA PRIVACY:</b> Your journal entries and voice recordings are session-based and are not permanently stored on our servers. <br><br>
        <b>5. COMMERCE & TAXES:</b> Physical bundle sales are initiated via WhatsApp and are subject to standard shipping timelines and applicable state taxes (including GST).
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:10px; opacity:0.3;'>Sukoon Sanctuary v102.0 | Lean Founder Build</div>", unsafe_allow_html=True)

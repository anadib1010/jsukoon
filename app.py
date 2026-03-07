import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone, timedelta
import os
import google.generativeai as genai
import urllib.parse
import json
import random

# --- 1. CORE VARIABLES ---
MY_PHONE = "918882850790"
GITHUB_USER = "anadib1010" 
REPO_NAME = "jsukoon"
GA_ID = "G-29F4EM37KE"

# --- 2. CONFIG & PWA META TAGS ---
st.set_page_config(page_title="Sukoon", layout="wide", initial_sidebar_state="collapsed")

# 🚨 HIDE STREAMLIT BRANDING GLOBALLY 🚨
st.markdown("""
    <style>
        /* Hide top menu and header */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Completely destroy the footer and logo so it cannot block clicks */
        footer {display: none !important;}
        [data-testid="stFooter"] {display: none !important;}
        .viewerBadge_container {display: none !important;}
        .viewerBadge_link {display: none !important;}
        
        /* Remove the top colored decoration line Streamlit adds */
        [data-testid="stDecoration"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
if "has_completed_ritual" not in st.session_state: st.session_state.has_completed_ritual = False
if "core_journal" not in st.session_state: st.session_state.core_journal = []
if "current_page" not in st.session_state: st.session_state.current_page = "Journal"
if "energy_history" not in st.session_state: st.session_state.energy_history = []
if "active_audio" not in st.session_state: st.session_state.active_audio = None
if "active_game" not in st.session_state: st.session_state.active_game = "Convergence"
if "active_breath" not in st.session_state: st.session_state.active_breath = "Anchor"
if "agent_audio" not in st.session_state: st.session_state.agent_audio = "flute.mp3"
if "agent_breath" not in st.session_state: st.session_state.agent_breath = "Box"
if "agent_message" not in st.session_state: st.session_state.agent_message = "The space is ready."

# Ensure valid theme
valid_themes = ["The Void", "Sage Sanctuary", "Terracotta Earth", "Social Blue", "First Light", "Sea Glass", 
                "Deep Sage", "Ocean Blue", "Ocean Green", "Red Amber", "Maroon", "Twilight Blue", 
                "Champagne Gold", "Pink Champagne", "Liquid Gold"]

if "theme" not in st.session_state or st.session_state.theme not in valid_themes: 
    ist = timezone(timedelta(hours=5, minutes=30))
    current_hour = datetime.now(ist).hour
    is_daytime = 6 <= current_hour < 18
    st.session_state.theme = "Pink Champagne" if is_daytime else "The Void"
    
if "ui_language" not in st.session_state: st.session_state.ui_language = "English"

# VIP Unlocks
if "unlocked_mala" not in st.session_state: st.session_state.unlocked_mala = False
if "unlocked_flame" not in st.session_state: st.session_state.unlocked_flame = False
if "unlocked_nirvana" not in st.session_state: st.session_state.unlocked_nirvana = False

# --- 4. ZERO-COST UI DICTIONARY ---
LANG = {
    "English": {
        "nav_journal": "Journal", "nav_ether": "Ether", "nav_focus": "Focus", 
        "nav_market": "Market", "nav_settings": "Settings",
        "r_arrive": "You have arrived.", "r_nothing": "Nothing is required here.",
        "r_breath": "Take one slow breath.", "r_enter": "ENTER SUKOON SANCTUARY",
        "subtitle": "INHALE 4 • HOLD 2 • EXHALE 6",
        "h_ambience": "AMBIENCE", "h_energy": "ENERGY STATE",
        "h_mentor": "YOUR SPACE", "privacy_note": "✦ Private • Neutral ✦",
        "mini_disclaimer": "This application does not provide medical, psychological, therapeutic, or religious advice. It makes no claims and offers no guaranteed outcomes. Use is voluntary and at your own discretion.",
        "zen_box": "TOUCH 3 TIMES<br>TO GROUND YOURSELF",
        "sos_btn": "⚡ AUTO-PILOT (INSTANT SOS) ⚡",
        "agent_btn": "🤖 AI AGENT (SMART SANCTUARY) 🤖",
        "btn_short": "GUIDE (SHORT)", "btn_deep": "GUIDE (DEEP)",
        "record": " ", 
        "type_here": "This canvas is yours. Write heavily, write nothing, or simply watch the cursor blink. There are no rules here.",
        "energy_prompt": "Pause and acknowledge how your body feels to guide the engine.",
        "e_racing": "Racing Thoughts", "e_restless": "Restless Mind", "e_overwhelmed": "Overwhelmed", 
        "e_heavy": "Heavy Thoughts", "e_tired": "Tired Mind", "e_quiet": "Need Quiet",
        "h_ether": "YOUR ETHER", "h_breath": "BREATH STUDIO", "h_games": "GROUNDING GAMES",
        "b_anchor": "Anchor (4-2-6)", "b_box": "The Box (4-4-4-4)", "b_sleep": "Deep Sleep (4-7-8)",
        "choose_visual": "CHOOSE YOUR VISUAL GUIDE", "v_wave": "The Wave", "v_moon": "The Moon", "v_lotus": "The Lotus",
        "game_release": "The Release", "game_bloom": "The Bloom", "game_convergence": "The Convergence",
        "release_desc": "Tap the rising thoughts to release them.", "bloom_desc": "Tap the center slowly to grow your light.",
        "convergence_desc": "Your mind is the swarm. Hold to overpower the resistance.",
        "h_market": "RITUAL BUNDLES & TOOLS",
        "order_wa": "JOIN WAITLIST VIA WA", "free_shipping": "+ FREE SHIPPING",
        "h_theme": "APP THEME", "h_lang": "UI LANGUAGE",
        "th_light": "LIGHT SANCTUARY", "th_dark": "DEEP SANCTUARY",
        "t_void": "The Void", "t_sage_l": "Sage Sanctuary", "t_terra": "Terracotta",
        "t_abyss": "Social Blue", "t_dawn": "First Light", "t_sea": "Sea Glass",
        "t_champagne": "Champagne Gold", "t_pink_champ": "Pink Champagne",
        "t_sage_d": "Deep Sage", "t_oblue": "Ocean Blue", "t_ogreen": "Ocean Green",
        "t_amber": "Red Amber", "t_maroon": "Maroon", "t_tblue": "Twilight Blue",
        "t_gold": "Liquid Gold (VIP)", "b_flame": "The Flame (VIP)", "game_mala": "Haptic Mala (VIP)",
        "vault_h": "SANCTUARY VAULT", "vault_p": "Have a Sanctuary Code?",
        "park_bench": [
            "Some days move slowly. That is okay.", "A quiet moment can change the rhythm of a day.", "Not every thought needs an answer.", "A pause can be enough for now.", "Silence sometimes says what words cannot.", "The mind often softens when it rests.", "This moment does not need to be solved.", "A few calm breaths can shift the day.", "Stillness can appear in simple moments.", "Even busy days contain small pauses.", "Nothing urgent is required from this moment.", "A gentle breath can begin again.", "Quiet moments often arrive unnoticed.", "The mind can rest for a while.", "Some thoughts pass when given space.", "A calm moment is never wasted.", "The day can unfold at its own pace.", "A pause can bring a different perspective.", "This moment can simply exist.", "Breathing slowly often changes the mood.", "Not every moment needs improvement.", "Sometimes a pause is the answer.", "A quiet breath can be enough.", "Stillness often hides in ordinary moments.", "The day can continue gently from here.", "A calm mind does not rush.", "Small pauses can carry quiet strength.", "The present moment can hold its own balance.", "The mind can soften with patience.", "Even brief silence can refresh the mind.", "The moment can pass without resistance.", "A calm breath can reset the pace.", "Nothing needs to be rushed right now.", "A quiet pause often brings clarity.", "The mind sometimes settles on its own.", "The present moment asks very little.", "A slow breath can create space.", "Some days unfold slowly for a reason.", "Calm moments are often simple.", "The mind may relax when given time.", "Silence can carry gentle comfort.", "Even a short pause can help.", "Thoughts may fade when left alone.", "The day can continue from this moment.", "A moment of stillness can be enough.", "The mind sometimes just needs a pause.", "Calm often appears when nothing is forced.", "This moment does not require judgment.", "Breathing quietly can change the atmosphere.", "The present moment is already here.", "A few seconds of quiet can reset the day.", "Some thoughts simply come and go.", "The moment can pass peacefully.", "Nothing urgent needs to happen here.", "A quiet breath can be a small reset.", "Stillness can live inside ordinary time.", "A pause may reveal something new.", "Calm often arrives softly.", "Even a gentle breath matters.", "A quiet moment belongs to you.", "The day does not need to rush.", "A calm mind notices simple things.", "Silence can feel unfamiliar at first.", "This moment can stand on its own.", "A pause can slow the rhythm of thought.", "The mind can soften without effort.", "Even brief quiet can restore balance.", "Thoughts often quiet when space is given.", "The present moment holds its own pace.", "Calm can grow in simple silence.", "A quiet breath may begin again.", "Some moments simply pass through.", "The mind may settle naturally.", "A gentle pause can change perspective.", "The day can continue calmly.", "Quiet space often reveals small clarity.", "The moment can unfold without pressure.", "A slow breath can bring steadiness.", "Not every feeling needs explanation.", "Silence sometimes brings its own answer.", "Calm does not need effort.", "A pause may open new awareness.", "The present moment is enough for now.", "Breathing slowly can quiet the mind.", "Thoughts often soften with time.", "A quiet pause can bring ease.", "The mind can simply observe.", "Nothing needs to change immediately.", "The moment can stay as it is.", "Even brief stillness can help.", "Calm moments can appear anywhere.", "A gentle breath can begin again.", "The mind can pause without reason.", "Quiet time has its own value.", "A calm moment can shift the day.", "Silence may reveal something small.", "The day may continue gently.", "A pause can carry quiet strength.", "The mind may rest briefly.", "Calm often arrives quietly.", "Some moments ask only for patience.", "Quiet time can restore perspective.", "The present moment can remain simple.", "A calm breath can slow the pace.", "Thoughts may pass on their own.", "Silence can bring subtle balance.", "The mind can rest between thoughts.", "A pause can create new space.", "The moment can move gently forward.", "Calm often lives in small pauses.", "Even a single breath matters.", "The day can slow for a moment.", "The mind may soften naturally.", "Quiet moments can refresh awareness.", "Nothing urgent is required here.", "Calm may appear when nothing is forced.", "The present moment holds quiet potential.", "A slow breath can change the mood.", "Some thoughts dissolve quietly.", "Silence often carries subtle calm.", "A pause may bring balance.", "The day can continue from here.", "Calm moments are often unnoticed.", "Even brief quiet can help the mind.", "The mind may settle slowly.", "A gentle breath can restore rhythm.", "Nothing needs to be rushed.", "The moment can remain simple.", "Calm sometimes arrives quietly.", "A quiet pause may be enough.", "Silence can hold quiet strength.", "Thoughts can move through the mind.", "A moment of calm may begin here.", "The mind may rest in stillness.", "Small pauses matter.", "Calm can appear unexpectedly.", "A quiet breath can steady the moment.", "The present moment does not demand much.", "Thoughts may drift away.", "A pause can reset the pace.", "The day can move slowly.", "Calm may grow in silence.", "The mind can relax gently.", "Even brief stillness can restore balance.", "A quiet moment can be enough.", "The present moment simply exists.", "Calm may follow patience.", "Silence can soften the mind.", "A slow breath can begin again.", "Nothing more is required now.", "The day can unfold naturally.", "A moment of quiet may help.", "Calm may arrive without effort.", "The mind may pause here.", "Silence often carries quiet clarity.", "Even a short pause can shift the day.", "The present moment remains here.", "A calm breath can steady the mind.", "Thoughts may pass quietly.", "Stillness sometimes appears unexpectedly.", "Calm moments may come and go.", "A pause may reveal calm.", "The day continues gently.", "The mind can rest briefly.", "Silence can hold quiet understanding.", "Even a small pause matters.", "Calm may grow slowly.", "The present moment stands quietly.", "A gentle breath may reset the rhythm.", "Thoughts may settle with time.", "The moment may pass peacefully.", "A calm mind notices simple things.", "Quiet space can refresh the mind.", "Silence may bring subtle comfort.", "A pause may shift perspective.", "Calm sometimes follows stillness.", "The day can move at its own pace.", "A quiet moment can steady the mind.", "Thoughts may drift softly.", "Silence often carries peace.", "A gentle pause can help the moment.", "Calm can appear in small breaths.", "The mind can settle quietly.", "Even a short pause has value.", "The present moment continues calmly.", "Silence may soften the day.", "A slow breath may bring balance.", "Thoughts may fade naturally.", "Calm may live in small pauses.", "The day can continue gently.", "A quiet moment belongs to you.", "The mind may rest here briefly.", "Silence can reveal small clarity.", "Calm may arrive softly.", "A pause may be enough for now.", "The present moment stands quietly.", "A gentle breath may help the moment.", "Thoughts may pass without effort.", "Calm can grow in stillness.", "This moment can simply be."
        ]
    },
    "Hindi": {
        "nav_journal": "जर्नल", "nav_ether": "आकाश", "nav_focus": "ध्यान", 
        "nav_market": "बाज़ार", "nav_settings": "सेटिंग्स",
        "r_arrive": "आप पहुँच गए हैं।", "r_nothing": "यहाँ आपसे कुछ भी अपेक्षित नहीं  है।",
        "r_breath": "एक धीमी सांस लें।", "r_enter": "सुकून अभयारण्य में प्रवेश करें",
        "subtitle": "सांस लें 4 • रोकें 2 • छोड़ें 6",
        "h_ambience": "माहौल", "h_energy": "ऊर्जा की स्थिति",
        "h_mentor": "आपका स्थान", "privacy_note": "✦ निजी • तटस्थ ✦",
        "mini_disclaimer": "यह एप्लिकेशन चिकित्सा, मनोवैज्ञानिक, चिकित्सीय या धार्मिक सलाह नहीं देता है। यह कोई दावा नहीं करता है और कोई गारंटीकृत परिणाम नहीं देता है। इसका उपयोग स्वैच्छिक है और आपके अपने विवेक पर है।",
        "zen_box": "खुद को शांत करने के लिए<br>3 बार छुएं",
        "sos_btn": "⚡ ऑटो-पायलट (आपातकालीन) ⚡",
        "agent_btn": "🤖 एआई एजेंट (स्मार्ट अभयारण्य) 🤖",
        "btn_short": "मार्गदर्शन (संक्षिप्त)", "btn_deep": "मार्गदर्शन (गहरा)",
        "record": " ", 
        "type_here": "यह स्थान आपका है। कुछ लिखें, कुछ न लिखें, या बस कर्सर को देखते रहें। यहाँ कोई नियम नहीं हैं।",
        "energy_prompt": "रुकें और महसूस करें कि आपका शरीर कैसा महसूस कर रहा है।",
        "e_racing": "तेज़ विचार", "e_restless": "बेचैन मन", "e_overwhelmed": "अभिभूत (Overwhelmed)", 
        "e_heavy": "भारी विचार", "e_tired": "थका हुआ मन", "e_quiet": "शांति चाहिए",
        "h_ether": "आपका आकाश", "h_breath": "सांस स्टूडियो", "h_games": "ग्राउंडिंग गेम्स",
        "b_anchor": "एंकर (4-2-6)", "b_box": "द बॉक्स (4-4-4-4)", "b_sleep": "गहरी नींद (4-7-8)",
        "choose_visual": "अपना दृश्य मार्गदर्शक चुनें", "v_wave": "लहर (Wave)", "v_moon": "चांद (Moon)", "v_lotus": "कमल (Lotus)",
        "game_release": "रिलीज़ (छोड़ें)", "game_bloom": "ब्लूम (खिलना)", "game_convergence": "कन्वर्जेंस (संकेंद्रण)",
        "release_desc": "उठते हुए विचारों को छोड़ने के लिए उन्हें छुएं।", "bloom_desc": "अपने प्रकाश को बढ़ाने के लिए धीरे से केंद्र को छुएं।",
        "convergence_desc": "आपका मन यह झुंड है। इसे शांत करने के लिए स्क्रीन को दबाकर रखें।",
        "h_market": "रीचुअल बंडल और टूल्स",
        "order_wa": "वेटलिस्ट से जुड़ें (WA)", "free_shipping": "+ मुफ्त शिपिंग",
        "h_theme": "ऐप थीम", "h_lang": "ऐप की भाषा",
        "th_light": "हल्का अभयारण्य (Light)", "th_dark": "गहरा अभयारण्य (Deep)",
        "t_void": "शून्य (The Void)", "t_sage_l": "सेज वन (Sage)", "t_terra": "मिट्टी (Terracotta)",
        "t_abyss": "सोशल ब्लू (FB Blue)", "t_dawn": "पहली किरण (Dawn)", "t_sea": "समुद्री कांच (Sea Glass)",
        "t_champagne": "शैंपेन गोल्ड (Champagne)", "t_pink_champ": "पिंक शैंपेन (Pink)",
        "t_sage_d": "गहरा सेज (Deep Sage)", "t_oblue": "समुद्री नीला (Blue)", "t_ogreen": "समुद्री हरा (Green)",
        "t_amber": "लाल एम्बर (Amber)", "t_maroon": "मैरून (Maroon)", "t_tblue": "गहरा नीला (Twilight)",
        "t_gold": "तरल सोना (VIP)", "b_flame": "लौ (VIP)", "game_mala": "स्पर्श माला (VIP)",
        "vault_h": "गुप्त तिजोरी", "vault_p": "क्या आपके पास कोड है?",
        "park_bench": [
            "कुछ दिन धीमी गति से गुज़रते हैं। यह ठीक है।", "एक शांत पल दिन की लय को बदल सकता है।", "हर विचार का उत्तर देना आवश्यक नहीं है।", "अभी के लिए बस थोड़ा सा ठहराव काफी है।", "मौन कभी-कभी वह कह देता है जो शब्द नहीं कह पाते।", "आराम मिलने पर मन अक्सर कोमल हो जाता है।", "इस पल को सुलझाने की कोई आवश्यकता नहीं है।", "कुछ शांत सांसें दिन को बदल सकती हैं।", "ठहराव साधारण पलों में प्रकट हो सकता है।", "व्यस्त दिनों में भी छोटे ठहराव होते हैं।", "इस पल में कुछ भी तुरंत करने की आवश्यकता नहीं है।", "एक कोमल सांस के साथ फिर से शुरुआत की जा सकती है।", "शांत पल अक्सर चुपचाप आ जाते हैं।", "मन कुछ देर के लिए आराम कर सकता है।", "जगह देने पर कुछ विचार अपने आप चले जाते हैं।", "एक शांत पल कभी व्यर्थ नहीं जाता।", "दिन अपनी गति से आगे बढ़ सकता है।", "एक ठहराव नज़रिया बदल सकता है।", "यह पल बस ऐसे ही अस्तित्व में रह सकता है।", "धीरे-धीरे सांस लेने से अक्सर मन की स्थिति बदल जाती है।", "हर पल को बेहतर बनाने की ज़रूरत नहीं है।", "कभी-कभी बस थोड़ा रुक जाना ही उत्तर होता है।", "एक शांत सांस ही काफी हो सकती है।", "ठहराव अक्सर साधारण पलों में छिपा होता है।", "दिन यहाँ से शांति से आगे बढ़ सकता है।", "एक शांत मन जल्दबाज़ी नहीं करता।", "छोटे ठहराव अपने आप में एक खामोश ताकत रखते हैं।", "वर्तमान क्षण अपना संतुलन खुद बनाए रख सकता है।", "धैर्य के साथ मन कोमल हो सकता है।", "थोड़ी देर का मौन भी मन को तरोताज़ा कर सकता है।", "यह पल बिना किसी विरोध के गुज़र सकता है।", "एक शांत सांस गति को सामान्य कर सकती है।", "अभी किसी भी चीज़ में जल्दबाज़ी करने की ज़रूरत नहीं है।", "एक शांत ठहराव अक्सर स्पष्टता लाता है।", "मन कभी-कभी अपने आप शांत हो जाता है।", "वर्तमान क्षण आपसे बहुत कम मांगता है।", "एक धीमी सांस जगह बना सकती है।", "कुछ दिन किसी कारण से ही धीरे गुज़रते हैं।", "शांत पल अक्सर बहुत साधारण होते हैं।", "समय देने पर मन आराम महसूस कर सकता है।", "मौन अपने साथ एक कोमल सुकून ला सकता है।", "एक छोटा सा ठहराव भी मदद कर सकता है।", "अकेला छोड़ देने पर विचार धुंधले पड़ सकते हैं।", "दिन इस पल से आगे बढ़ सकता है।", "थोड़ी देर की शांति काफी हो सकती है।", "मन को कभी-कभी बस एक ठहराव की ज़रूरत होती है।", "जब किसी चीज़ पर ज़ोर नहीं डाला जाता, तो शांति अपने आप आ जाती है।", "इस पल को किसी फैसले की ज़रूरत नहीं है।", "शांति से सांस लेने पर माहौल बदल सकता है।", "वर्तमान क्षण पहले से ही यहाँ है।", "चंद सेकंड की शांति दिन को फिर से संवार सकती है।", "कुछ विचार बस आते हैं और चले जाते हैं।", "यह पल शांति से गुज़र सकता है।", "यहाँ कुछ भी तुरंत करने की आवश्यकता नहीं है।", "एक शांत सांस एक छोटी सी नई शुरुआत हो सकती है।", "ठहराव साधारण समय के भीतर रह सकता है।", "एक ठहराव कुछ नया दिखा सकता है।", "शांति अक्सर दबे पाँव आती है।", "एक कोमल सांस भी मायने रखती है।", "एक शांत पल आपका अपना है।", "दिन को भागने की ज़रूरत नहीं है।", "एक शांत मन साधारण चीज़ों पर ध्यान देता है।", "मौन शुरुआत में अनजान लग सकता है।", "यह पल अपने आप में पूर्ण है।", "एक ठहराव विचारों की गति को धीमा कर सकता है।", "मन बिना किसी प्रयास के कोमल हो सकता है।", "थोड़ी देर की शांति भी संतुलन लौटा सकती है।", "जगह देने पर विचार अक्सर शांत हो जाते हैं।", "वर्तमान क्षण की अपनी एक गति होती है।", "साधारण मौन में शांति पनप सकती है।", "एक शांत सांस फिर से शुरू हो सकती है।", "कुछ पल बस गुज़रने के लिए होते हैं।", "मन स्वाभाविक रूप से शांत हो सकता है।", "एक कोमल ठहराव नज़रिया बदल सकता है।", "दिन शांति से आगे बढ़ सकता है।", "शांत जगह अक्सर छोटी सी स्पष्टता दिखाती है।", "यह पल बिना किसी दबाव के आगे बढ़ सकता है।", "एक धीमी सांस स्थिरता ला सकती है।", "हर भावना को समझाने की ज़रूरत नहीं है।", "मौन कभी-कभी अपना उत्तर खुद लाता है।", "शांति के लिए प्रयास की ज़रूरत नहीं होती।", "एक ठहराव नई जागरूकता खोल सकता है।", "वर्तमान क्षण अभी के लिए काफी है।", "धीरे सांस लेने से मन शांत हो सकता है।", "विचार अक्सर समय के साथ कोमल हो जाते हैं।", "एक शांत ठहराव सुकून ला सकता है।", "मन केवल साक्षी बन सकता है।", "किसी भी चीज़ को तुरंत बदलने की ज़रूरत नहीं है।", "यह पल जैसा है, वैसा ही रह सकता है।", "थोड़ी सी स्थिरता भी मदद कर सकती है।", "शांत पल कहीं भी प्रकट हो सकते हैं।", "एक कोमल सांस के साथ फिर से शुरुआत करें।", "मन बिना किसी कारण के रुक सकता है।", "शांत समय का अपना एक मूल्य है।", "एक शांत पल दिन को बदल सकता है।", "मौन कुछ छोटा सा प्रकट कर सकता है।", "दिन धीरे-धीरे आगे बढ़ सकता है।", "एक ठहराव में खामोश ताकत हो सकती है।", "मन थोड़ी देर के लिए आराम कर सकता है।", "शांति अक्सर खामोशी से आती है।", "कुछ पल केवल धैर्य मांगते हैं।", "शांत समय नज़रिया लौटा सकता है।", "वर्तमान क्षण साधारण रह सकता है।", "एक शांत सांस गति को धीमा कर सकती है।", "विचार अपने आप गुज़र सकते हैं।", "मौन एक सूक्ष्म संतुलन ला सकता है।", "मन विचारों के बीच आराम कर सकता है।", "एक ठहराव नई जगह बना सकता है।", "यह पल धीरे से आगे बढ़ सकता है।", "शांति अक्सर छोटे ठहरावों में रहती है।", "एक अकेली सांस भी मायने रखती है।", "दिन एक पल के लिए धीमा हो सकता है।", "मन स्वाभाविक रूप से कोमल हो सकता है।", "शांत पल जागरूकता को ताज़ा कर सकते हैं।", "यहाँ कुछ भी तुरंत करना ज़रूरी नहीं है।", "जब कोई दबाव न हो, तो शांति आ सकती है।", "वर्तमान क्षण में शांत संभावनाएं हैं।", "एक धीमी सांस मन की स्थिति बदल सकती है।", "कुछ विचार खामोशी से विलीन हो जाते हैं।", "मौन अक्सर एक सूक्ष्म शांति लाता है।", "एक ठहराव संतुलन ला सकता है।", "दिन यहाँ से आगे बढ़ सकता है।", "शांत पल अक्सर किसी का ध्यान नहीं खींचते।", "थोड़ी देर की खामोशी भी मन की मदद कर सकती है।", "मन धीरे-धीरे शांत हो सकता है।", "एक कोमल सांस लय को लौटा सकती है।", "जल्दबाज़ी करने की कोई ज़रूरत नहीं है।", "यह पल साधारण रह सकता है।", "शांति कभी-कभी चुपचाप आती है।", "एक शांत ठहराव ही काफी हो सकता है।", "मौन में खामोश ताकत हो सकती है।", "विचार मन से होकर गुज़र सकते हैं।", "शांति का एक पल यहाँ से शुरू हो सकता है।", "मन स्थिरता में आराम कर सकता है।", "छोटे ठहराव बहुत मायने रखते हैं।", "शांति अप्रत्याशित रूप से प्रकट हो सकती है।", "एक शांत सांस इस पल को स्थिर कर सकती है।", "वर्तमान क्षण बहुत कुछ नहीं मांगता।", "विचार धीरे-धीरे दूर जा सकते हैं।", "एक ठहराव गति को सामान्य कर सकता है।", "दिन धीमी गति से चल सकता है।", "शांति मौन में बढ़ सकती है।", "मन धीरे से आराम कर सकता है।", "थोड़ी सी स्थिरता भी संतुलन लौटा सकती है।", "एक शांत पल काफी हो सकता है।", "वर्तमान क्षण बस अस्तित्व में है।", "धैर्य के बाद शांति आ सकती है।", "मौन मन को कोमल बना सकता है।", "एक धीमी सांस के साथ फिर शुरुआत हो सकती है।", "अब और कुछ करने की आवश्यकता नहीं है।", "दिन अपने आप आगे बढ़ सकता है।", "शांति का एक पल मदद कर सकता है।", "शांति बिना किसी प्रयास के आ सकती है।", "मन यहाँ ठहर सकता है।", "मौन अक्सर खामोश स्पष्टता लाता है।", "एक छोटा ठहराव भी दिन को बदल सकता है।", "वर्तमान क्षण यहीं बना रहता है।", "एक शांत सांस मन को स्थिर कर सकती है।", "विचार खामोशी से गुज़र सकते हैं।", "ठहराव कभी-कभी अचानक प्रकट होता है।", "शांत पल आ और जा सकते हैं।", "एक ठहराव शांति प्रकट कर सकता है।", "दिन धीरे-धीरे आगे बढ़ता है।", "मन थोड़ी देर के लिए विश्राम कर सकता है।", "मौन खामोश समझ को संजो सकता है।", "एक छोटा ठहराव भी बहुत मायने रखता है।", "शांति धीरे-धीरे बढ़ सकती है।", "वर्तमान क्षण शांति से खड़ा है।", "एक कोमल सांस लय को फिर से सेट कर सकती है।", "विचार समय के साथ शांत हो सकते हैं।", "यह पल शांतिपूर्वक गुज़र सकता है।", "एक शांत मन साधारण चीज़ों पर ध्यान देता है।", "शांत जगह मन को तरोताज़ा कर सकती है।", "मौन सूक्ष्म सुकून ला सकता है।", "एक ठहराव नज़रिए को बदल सकता है।", "शांति कभी-कभी स्थिरता के बाद आती है।", "दिन अपनी गति से चल सकता है।", "एक शांत पल मन को स्थिर कर सकता है।", "विचार कोमलता से बह सकते हैं।", "मौन अक्सर शांति लाता है।", "एक कोमल ठहराव इस पल की मदद कर सकता है।", "शांति छोटी-छोटी सांसों में प्रकट हो सकती है।", "मन खामोशी से शांत हो सकता है।", "एक छोटे ठहराव का भी महत्व होता है।", "वर्तमान क्षण शांति से आगे बढ़ता है।", "मौन दिन को कोमल बना सकता है।", "एक धीमी सांस संतुलन ला सकती है।", "विचार स्वाभाविक रूप से धुंधले पड़ सकते हैं।", "शांति छोटे ठहरावों में रह सकती है।", "दिन कोमलता से आगे बढ़ सकता है।", "एक शांत पल सिर्फ आपका है।", "मन यहाँ कुछ देर के लिए आराम कर सकता है।", "मौन एक छोटी सी स्पष्टता दिखा सकता है।", "शांति दबे पाँव आ सकती है।", "एक ठहराव अभी के लिए काफी हो सकता है।", "वर्तमान क्षण शांति से खड़ा है।", "एक कोमल सांस इस पल में मदद कर सकती है।", "विचार बिना प्रयास के गुज़र सकते हैं।", "शांति स्थिरता में पनप सकती है।", "यह पल बस जैसा है, वैसा रह सकता है।"
        ]
    }
}
t = LANG[st.session_state.ui_language]

# 🚨 THE EXHAUSTIVE CRISIS WORD LIST 🚨
CRISIS_WORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die", 
    "self harm", "cut myself", "overdose", "jump off", "hang myself", 
    "take my own life", "better off dead", "tired of living", "sleep forever", 
    "no point in living", "end it all", "slit my wrists", "drink poison", 
    "kill me", "i want to end things", "mar jana", "khudkushi", "aatmahatya", 
    "jaan de dunga", "jaan de dungi", "nas kaat", "jeene ka man nahi", 
    "marne ka man", "zindagi khatam", "zeher", "suli"
]

# --- 5. THE ULTIMATE 14-THEME ENGINE ---
if st.session_state.theme == "First Light":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#FDFBF7", "#4A4A4A", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.05)", "#D4A373", "212,163,115"
elif st.session_state.theme == "Sea Glass":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#E5EDF0", "#4A5D66", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#7A9EA8", "122,158,168"
elif st.session_state.theme == "Terracotta Earth":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#F2ECE7", "#5C4033", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#B07D62", "176,125,98"
elif st.session_state.theme == "Sage Sanctuary":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#E3E7E0", "#3E4735", "rgba(255,255,255,0.4)", "rgba(0,0,0,0.06)", "#6B765F", "107,118,95"
elif st.session_state.theme == "Champagne Gold":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#FBF5ED", "#4A4036", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.06)", "#C5A059", "197,160,89"
elif st.session_state.theme == "Pink Champagne":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#F8DECD", "#5A3A42", "rgba(255,255,255,0.5)", "rgba(0,0,0,0.06)", "#C88A8E", "200,138,142"
elif st.session_state.theme == "The Void":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#000000", "#E0E0E0", "rgba(20,20,20,0.6)", "rgba(255,255,255,0.08)", "#888888", "136,136,136"
elif st.session_state.theme == "Social Blue":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#1877F2", "#FFFFFF", "rgba(255,255,255,0.15)", "rgba(255,255,255,0.3)", "#FFFFFF", "255,255,255"
elif st.session_state.theme == "Deep Sage":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#1E2720", "#D3DDD0", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#7B9075", "123,144,117"
elif st.session_state.theme == "Ocean Blue":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#122840", "#CFE2F3", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#5D93C4", "93,147,196"
elif st.session_state.theme == "Ocean Green":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#0F2926", "#CDE3DF", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#4A9D93", "74,157,147"
elif st.session_state.theme == "Red Amber":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#38180D", "#F3D9CE", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#B35835", "179,88,53"
elif st.session_state.theme == "Maroon":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#2A0E13", "#EFD1D6", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#9B3D4F", "155,61,79"
elif st.session_state.theme == "Twilight Blue":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#181830", "#D6D5F2", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.08)", "#726FBA", "114,111,186"
elif st.session_state.theme == "Liquid Gold":
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#000000", "#F5E6BA", "rgba(212,175,55,0.08)", "rgba(212,175,55,0.25)", "#D4AF37", "212,175,55"
else:
    app_bg, app_text, glass_bg, btn_border, c_accent, c_rgb = "#000000", "#E0E0E0", "rgba(20,20,20,0.6)", "rgba(255,255,255,0.08)", "#888888", "136,136,136"

def theme_it(html_str):
    return html_str.replace("[C_BG]", "transparent").replace("[C_GLASS]", glass_bg).replace("[C_BORDER]", btn_border).replace("[C_TEXT]", app_text).replace("[C_ACCENT]", c_accent).replace("[C_RGB]", c_rgb)

# --- THE PARK BENCH ENGINE ---
def get_top_quote():
    sentence = random.choice(t['park_bench'])
    return f"<div style='text-align: center; opacity: 1.0; font-size: 13px; font-weight: 400; font-style: italic; margin-top: 10px; margin-bottom: 25px; color: {c_accent}; letter-spacing: 1px;'>{sentence}</div>"

def get_bottom_quote():
    sentence = random.choice(t['park_bench'])
    return f"<div style='text-align: center; opacity: 0.3; font-size: 11px; font-weight: 300; margin-top: 30px; margin-bottom: 20px; color: {app_text}; letter-spacing: 1px;'>{sentence}</div>"

# --- 6. THE BRAIN SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

# ==========================================
# 🚨 7. MINIMALIST COMMAND CENTER CSS & ATMOSPHERE 🚨
# ==========================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* THE PADDING TRAP: PC SCROLL FIX */
    .block-container {{ 
        max-width: 100vw !important; 
        padding-top: 3.5rem !important; 
        text-align: center !important; 
        overflow-x: hidden !important; 
    }}
    
    /* For PC (Wide Screens) */
    @media (min-width: 601px) {{
        .block-container {{
            padding-left: calc(50vw - 300px) !important;
            padding-right: calc(50vw - 300px) !important;
        }}
    }}
    
    /* For Phones */
    @media (max-width: 600px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
    }}
    
    /* The Waking Up Reveal */
    .stApp {{ 
        background-color: {app_bg} !important; 
        color: {app_text} !important; 
        font-family: 'Inter', sans-serif; 
        transition: background-color 1s ease; 
        animation: smoothReveal 2.5s ease-in-out forwards;
    }}
    
    @keyframes smoothReveal {{
        0% {{ opacity: 0; filter: blur(8px); }}
        100% {{ opacity: 1; filter: blur(0px); }}
    }}

    /* The Breathing Aura */
    .ambient-aura {{
        position: fixed;
        top: -20vh;
        left: -20vw;
        width: 140vw;
        height: 140vh;
        background: radial-gradient(circle at 30% 30%, rgba({c_rgb}, 0.25) 0%, rgba({c_rgb}, 0.05) 40%, transparent 70%);
        z-index: -1;
        pointer-events: none;
        animation: breatheAura 14s infinite alternate ease-in-out;
    }}
    
    @keyframes breatheAura {{
        0% {{ transform: scale(1); opacity: 0.5; }}
        100% {{ transform: scale(1.1); opacity: 1; }}
    }}

    /* The Void Stars */
    .void-stars {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -2;
        pointer-events: none;
        background-image: 
            radial-gradient(1.5px 1.5px at 15% 25%, rgba(255,255,255,0.8), transparent),
            radial-gradient(2px 2px at 75% 15%, rgba(255,255,255,0.6), transparent),
            radial-gradient(1px 1px at 45% 65%, rgba(255,255,255,0.9), transparent),
            radial-gradient(1.5px 1.5px at 85% 75%, rgba(255,255,255,0.5), transparent),
            radial-gradient(2px 2px at 25% 85%, rgba(255,255,255,0.7), transparent),
            radial-gradient(1px 1px at 55% 35%, rgba(255,255,255,0.8), transparent);
        background-size: 250px 250px;
        opacity: 0.5;
        animation: starTwinkle 8s infinite alternate ease-in-out;
    }}
    
    @keyframes starTwinkle {{
        0% {{ opacity: 0.2; transform: translateY(0px); }}
        100% {{ opacity: 0.8; transform: translateY(3px); }}
    }}

    /* The Global Ambient Ocean */
    .ocean {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 12vh;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }}
    .wave {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200vw;
        height: 100%;
        background-color: {c_accent};
        opacity: 0.08;
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 88.7'%3E%3Cpath d='M800 56.9c-155.5 0-204.9-50-405.5-49.9-200 0-250 49.9-394.5 49.9v31.8h800v-.2-31.6z'/%3E%3C/svg%3E");
        -webkit-mask-size: 50vw 100%;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 88.7'%3E%3Cpath d='M800 56.9c-155.5 0-204.9-50-405.5-49.9-200 0-250 49.9-394.5 49.9v31.8h800v-.2-31.6z'/%3E%3C/svg%3E");
        mask-size: 50vw 100%;
        animation: waveScroll 15s linear infinite;
    }}
    .wave:nth-child(2) {{
        bottom: -5px;
        opacity: 0.12;
        animation: waveScroll 22s linear reverse infinite;
        -webkit-mask-size: 60vw 100%;
        mask-size: 60vw 100%;
    }}
    .wave:nth-child(3) {{
        bottom: -10px;
        opacity: 0.15;
        animation: waveScroll 12s linear infinite;
        -webkit-mask-size: 70vw 100%;
        mask-size: 70vw 100%;
    }}
    @keyframes waveScroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50vw); }}
    }}

    div[data-testid="stHorizontalBlock"] {{ flex-direction: row !important; flex-wrap: wrap !important; justify-content: center !important; gap: 8px !important; }}
    div[data-testid="column"], div[data-testid="stColumn"] {{ width: calc(33.333% - 8px) !important; min-width: calc(33.333% - 8px) !important; max-width: calc(33.333% - 8px) !important; flex: 1 1 calc(33.333% - 8px) !important; display: flex !important; justify-content: center !important; margin-bottom: 5px !important; }}
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(2):last-child) > div[data-testid="column"] {{ width: calc(50% - 8px) !important; min-width: calc(50% - 8px) !important; max-width: calc(50% - 8px) !important; flex: 1 1 calc(50% - 8px) !important; }}
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(3):last-child) > div[data-testid="column"] {{ width: calc(33.333% - 8px) !important; min-width: calc(33.333% - 8px) !important; max-width: calc(33.333% - 8px) !important; flex: 1 1 calc(33.333% - 8px) !important; }}
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4):last-child) > div[data-testid="column"] {{ width: calc(25% - 8px) !important; min-width: calc(25% - 8px) !important; max-width: calc(25% - 8px) !important; flex: 1 1 calc(25% - 8px) !important; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 0.2; border-width: 1px; }} 50% {{ transform: scale(1.6); opacity: 0.8; border-width: 3px; }} 100% {{ transform: scale(1); opacity: 0.2; border-width: 1px; }} }}
    .breathing-circle {{ width: 50px; height: 50px; border: 2px solid {c_accent}; border-radius: 50%; margin: 15px auto 25px auto; animation: pulse 12s infinite ease-in-out !important; box-shadow: 0 0 20px rgba({c_rgb}, 0.3); transition: all 0.8s ease; }}
    .main-title {{ text-align: center; letter-spacing: 14px; font-weight: 300; font-size: 2.2rem; color: {app_text}; text-transform: uppercase; margin-bottom: 5px; }}
    .section-header {{ font-size: 11px; letter-spacing: 5px; font-weight: 500; text-transform: uppercase; margin: 35px 0 15px 0; color: {c_accent}; padding-bottom: 8px; opacity: 0.8; }}
    .theme-group-header {{ font-size: 9px; letter-spacing: 3px; font-weight: 400; text-transform: uppercase; margin: 20px 0 10px 0; color: {app_text}; opacity: 0.5; text-align: left; padding-left: 5px; }}
    div.stButton {{ width: 100% !important; }}
    .stButton>button {{ width: 100% !important; min-width: 100% !important; background: {glass_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; border-radius: 30px !important; backdrop-filter: blur(12px) !important; -webkit-backdrop-filter: blur(12px) !important; min-height: 44px !important; height: 100% !important; font-size: 10px !important; font-weight: 400 !important; letter-spacing: 1px !important; display: flex !important; justify-content: center !important; align-items: center !important; text-align: center !important; transition: all 0.3s ease; white-space: normal !important; padding: 5px !important; line-height: 1.2 !important; }}
    .stButton>button:active {{ transform: scale(0.96); opacity: 0.7; }}
    .autopilot-btn>button {{ border: 1px solid rgba({c_rgb}, 0.5) !important; color: {c_accent} !important; letter-spacing: 2px; font-weight: 500 !important; }}
    .agent-btn>button {{ border: 1px solid rgba({c_rgb}, 0.5) !important; color: {c_accent} !important; letter-spacing: 2px; font-weight: 500 !important; }}
    .market-slab {{ background: {glass_bg}; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid {btn_border}; padding: 20px; margin-bottom: 15px; text-align: center; transition: all 0.5s ease; }}
    .disclaimer-box {{ text-align: left; font-size: 11px; opacity: 0.6; line-height: 1.8; background: transparent; padding: 15px; border-radius: 12px; border: 1px solid {btn_border}; margin-bottom: 20px; }}
    
    /* PLACEHOLDER READABILITY FIX & OPACITY */
    textarea, input {{ background: {glass_bg} !important; color: {app_text} !important; border: 1px solid {btn_border} !important; border-radius: 16px !important; backdrop-filter: blur(12px) !important; text-align: center !important; font-size: 14px !important; font-weight: 300 !important; font-family: 'Inter', sans-serif !important; padding: 15px !important; box-shadow: none !important; }}
    textarea:focus, input:focus {{ border-color: {c_accent} !important; outline: none !important; }}
    textarea::placeholder, input::placeholder {{ color: {app_text} !important; opacity: 0.5 !important; font-weight: 300 !important; line-height: 1.6 !important; }}
    
    .journal-entry {{ background: {glass_bg}; backdrop-filter: blur(12px); border-left: 2px solid {c_accent}; padding: 20px; margin-bottom: 10px; border-radius: 12px; color: {app_text}; text-align: left; font-size: 14px; line-height: 1.6; font-weight: 300; border-top: 1px solid {btn_border}; border-right: 1px solid {btn_border}; border-bottom: 1px solid {btn_border}; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🚨 THE SEAMLESS 30-SECOND THRESHOLD RITUAL (PURE CSS CURTAIN) 🚨
# ==========================================
if not st.session_state.has_completed_ritual:
    st.session_state.has_completed_ritual = True
    
    ritual_html = f"""
    <style>
        .rc-wrap-curtain {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #050505; z-index: 9999999;
            display: flex; justify-content: center; align-items: center; flex-direction: column;
            animation: hideCurtain 1.5s ease-in-out 24.5s forwards;
        }}
        
        .p1 {{ position: absolute; text-align: center; animation: fadeP1 5s ease-in-out forwards; width: 100%; padding: 0 20px; }}
        .p1-main {{ font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 300; letter-spacing: 2px; color: #E0E0E0; }}
        .p1-sub {{ font-family: 'Inter', sans-serif; font-size: 11px; opacity: 0; animation: rFadeIn 1s 2s forwards; margin-top: 15px; color: #888; }}
        
        .p2 {{ position: absolute; display: flex; flex-direction: column; align-items: center; opacity: 0; animation: fadeP2 15s ease-in-out 5s forwards; width: 100%; }}
        .p2-circle {{ width: 80px; height: 80px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.15); background: radial-gradient(circle, rgba(255,255,255,0.05), transparent); animation: rBreathe 5s ease-in-out infinite 5s; }}
        .p2-text {{ font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 300; letter-spacing: 2px; margin-top: 30px; color: #E0E0E0; text-align: center; }}
        
        .p3 {{ position: absolute; text-align: center; opacity: 0; animation: fadeP3 4.5s ease-in-out 20s forwards; width: 100%; }}
        .p3-text {{ font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 300; letter-spacing: 4px; color: #E0E0E0; text-transform: uppercase; }}
        
        #sukoon-skip-btn {{
            position: absolute; bottom: 40px; color: #555; font-family: 'Inter', sans-serif;
            font-size: 11px; font-weight: 300; letter-spacing: 2px; cursor: pointer;
            opacity: 0; animation: rFadeInSkip 2s ease forwards 3s; padding: 10px 20px; z-index: 10000000;
        }}
        
        @keyframes hideCurtain {{ to {{ opacity: 0; visibility: hidden; pointer-events: none; display: none; }} }}
        @keyframes fadeP1 {{ 0%{{opacity:0;}} 10%{{opacity:1;}} 80%{{opacity:1;}} 100%{{opacity:0; visibility:hidden;}} }}
        @keyframes fadeP2 {{ 0%{{opacity:0;}} 10%{{opacity:1;}} 90%{{opacity:1;}} 100%{{opacity:0; visibility:hidden;}} }}
        @keyframes fadeP3 {{ 0%{{opacity:0;}} 20%{{opacity:1;}} 80%{{opacity:1;}} 100%{{opacity:0; visibility:hidden;}} }}
        @keyframes rFadeIn {{ to {{ opacity: 0.4; }} }}
        @keyframes rBreathe {{ 0%{{transform:scale(0.8); opacity:0.3;}} 40%{{transform:scale(1.8); opacity:0.8;}} 100%{{transform:scale(0.8); opacity:0.3;}} }}
        @keyframes rFadeInSkip {{ to {{ opacity: 0.4; }} }}
    </style>
    
    <div class="rc-wrap-curtain">
        <div class="p1">
            <div class="p1-main">{t['r_arrive']}</div>
            <div class="p1-sub">{t['r_nothing']}</div>
        </div>
        <div class="p2">
            <div class="p2-circle"></div>
            <div class="p2-text">{t['r_breath']}</div>
        </div>
        <div class="p3">
            <div class="p3-text">{t['r_enter']}</div>
        </div>
        <div id="sukoon-skip-btn">(skip)</div>
    </div>
    """
    st.markdown(ritual_html, unsafe_allow_html=True)
    
    components.html("""
    <script>
        const doc = window.parent.document;
        const curtain = doc.querySelector('.rc-wrap-curtain');
        const skipBtn = doc.getElementById('sukoon-skip-btn');
        
        if (curtain && skipBtn) {
            skipBtn.addEventListener('click', function() {
                curtain.style.opacity = '0';
                curtain.style.pointerEvents = 'none';
                setTimeout(() => { curtain.style.display = 'none'; }, 500);
            });
            setTimeout(() => { curtain.style.display = 'none'; }, 26000);
        }
    </script>
    """, height=0, width=0)

# 🚨 INJECT ATMOSPHERE DIVS 🚨
st.markdown("<div class='ambient-aura'></div>", unsafe_allow_html=True)
if st.session_state.theme == "The Void":
    st.markdown("<div class='void-stars'></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='ocean'>
        <div class='wave'></div>
        <div class='wave'></div>
        <div class='wave'></div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# --- GLOBAL HTML COMPONENTS ---
# ==========================================
base_breath_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:260px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
    <canvas id="[CANVAS_ID]" style="position:absolute; top:0; left:0; width:100%; height:100%;"></canvas>
</div>
<script>
    (function() {
        const canvas = document.getElementById('[CANVAS_ID]'); const ctx = canvas.getContext('2d');
        function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
        window.addEventListener('resize', resize); resize(); const start = Date.now();
        function draw() { ctx.clearRect(0, 0, canvas.width, canvas.height); const cx = canvas.width/2; const cy = canvas.height/2 - 10; let t = ((Date.now() - start) / 1000); [JS_INJECT] requestAnimationFrame(draw); }
        draw();
    })();
</script>
"""

breath_js_dict = {
    "Anchor": """
        let cycle = t % 12; let text = ""; let scale = 1;
        if(cycle < 4) { text = "INHALE (4)"; scale = 1 + (cycle/4); } else if(cycle < 6) { text = "HOLD (2)"; scale = 2; } else { text = "EXHALE (6)"; scale = 2 - ((cycle-6)/6); }
        ctx.beginPath(); ctx.arc(cx, cy, 35 * scale, 0, Math.PI*2); ctx.strokeStyle = "rgba([C_RGB], 0.6)"; ctx.lineWidth = 2; ctx.stroke(); ctx.fillStyle = "rgba([C_RGB], 0.1)"; ctx.fill();
        ctx.fillStyle = "[C_TEXT]"; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Box": """
        let cycle = t % 16; let text = ""; let size = 100; let x = cx - size/2; let y = cy - size/2;
        ctx.strokeStyle = "rgba([C_RGB], 0.15)"; ctx.lineWidth = 1; ctx.strokeRect(x, y, size, size); ctx.strokeStyle = "rgba([C_RGB], 0.8)"; ctx.lineWidth = 3; ctx.beginPath();
        if(cycle < 4) { text = "INHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y+size - size*(cycle/4)); } else if(cycle < 8) { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x + size*((cycle-4)/4), y); } else if(cycle < 12) { text = "EXHALE (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y + size*((cycle-8)/4)); } else { text = "HOLD (4)"; ctx.moveTo(x, y+size); ctx.lineTo(x, y); ctx.lineTo(x+size, y); ctx.lineTo(x+size, y+size); ctx.lineTo(x+size - size*((cycle-12)/4), y+size); }
        ctx.stroke(); ctx.fillStyle = "[C_TEXT]"; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Wave": """
        let cycle = t % 19; let text = ""; let spread = 0;
        if(cycle < 4) { text = "INHALE (4)"; spread = cycle/4; } 
        else if(cycle < 11) { text = "HOLD (7)"; spread = 1; } 
        else { text = "EXHALE (8)"; spread = 1 - ((cycle-11)/8); }
        
        let targetY = canvas.height * (0.85 - (spread * 0.5)); // The tide rises and falls
        
        for(let w = 0; w < 3; w++) {
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);
            let offset = (t * 1.5) + (w * 2);
            let amp = 10 + (w * 5) + (spread * 5);
            
            for(let x = 0; x <= canvas.width + 20; x += 20) {
                let y = targetY + Math.sin((x * 0.015) + offset) * amp + (w * 15);
                ctx.lineTo(x, y);
            }
            ctx.lineTo(canvas.width, canvas.height);
            ctx.fillStyle = `rgba([C_RGB], ${0.2 - (w * 0.05)})`;
            ctx.fill();
        }
        
        ctx.fillStyle = "[C_TEXT]"; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Moon": """
        let cycle = t % 19; let text = ""; let opacity = 0.1; let yOffset = 0;
        if(cycle < 4) { text = "INHALE (4)"; opacity = 0.1 + 0.8*(cycle/4); yOffset = -20 * (cycle/4); } else if(cycle < 11) { text = "HOLD (7)"; opacity = 0.9; yOffset = -20; } else { text = "EXHALE (8)"; opacity = 0.9 - 0.8*((cycle-11)/8); yOffset = -20 + 40*((cycle-11)/8); }
        ctx.beginPath(); ctx.arc(cx, cy + yOffset, 35, 0, Math.PI*2); ctx.fillStyle = `rgba([C_RGB], ${opacity})`; ctx.fill();
        ctx.shadowBlur = 30 * opacity; ctx.shadowColor = "rgba([C_RGB], 1)"; ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Sleep_Lotus": """
        let cycle = t % 19; let text = ""; let spread = 0;
        if(cycle < 4) { text = "INHALE (4)"; spread = cycle/4; } else if(cycle < 11) { text = "HOLD (7)"; spread = 1; } else { text = "EXHALE (8)"; spread = 1 - ((cycle-11)/8); }
        for(let i=0; i<6; i++) { let angle = i * (Math.PI*2/6) + (t * 0.1); let px = cx + Math.cos(angle) * (30 * spread); let py = cy + Math.sin(angle) * (30 * spread); ctx.beginPath(); ctx.arc(px, py, 25, 0, Math.PI*2); ctx.strokeStyle = "rgba([C_RGB], 0.5)"; ctx.lineWidth = 1; ctx.stroke(); ctx.fillStyle = "rgba([C_RGB], 0.05)"; ctx.fill(); }
        ctx.fillStyle = "[C_TEXT]"; ctx.shadowBlur = 0; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """,
    "Flame": """
        let cycle = t % 12; let text = ""; let scale = 1;
        if(cycle < 4) { text = "INHALE (4)"; scale = 1 + (cycle/4)*0.5; } else if(cycle < 6) { text = "HOLD (2)"; scale = 1.5; } else { text = "EXHALE (6)"; scale = 1.5 - ((cycle-6)/6)*0.5; }
        let gradient = ctx.createRadialGradient(cx, cy + 20, 0, cx, cy + 20, 50 * scale);
        gradient.addColorStop(0, "rgba(255, 200, 50, 0.9)"); gradient.addColorStop(0.3, "rgba(255, 80, 0, 0.6)"); gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
        ctx.beginPath(); let flicker = Math.sin(t * 15) * 4 + Math.cos(t * 22) * 2;
        ctx.arc(cx + flicker, cy + 20 - (15 * scale) + flicker, 50 * scale, 0, Math.PI*2);
        ctx.fillStyle = gradient; ctx.fill();
        ctx.fillStyle = "[C_TEXT]"; ctx.font = "300 12px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "4px"; ctx.fillText(text, cx, cy + 90);
    """
}

convergence_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:350px; overflow:hidden; touch-action: none;">
    <div id="convMsg" style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:[C_ACCENT]; font-family:sans-serif; font-size:10px; font-weight:300; letter-spacing:4px; z-index:10; pointer-events:none; transition: opacity 0.5s; text-align:center; line-height:1.5;">PRESS & HOLD TO<br>GATHER THE MIND</div>
    <canvas id="[CANVAS_ID]" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
</div>
<script>
    (function() {
        const canvas = document.getElementById('[CANVAS_ID]'); const ctx = canvas.getContext('2d'); const msg = document.getElementById('convMsg');
        let isPressing = false; let particles = []; let vibeInterval; 
        let focusPower = 0; 
        
        function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
        window.addEventListener('resize', resize); resize();
        
        for(let i=0; i<120; i++) {
            particles.push({
                x: Math.random() * canvas.width, y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                radius: Math.random() * 2.5 + 1
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const cx = canvas.width / 2; const cy = canvas.height / 2;
            
            if (isPressing) { focusPower += 0.004; if (focusPower > 1) focusPower = 1; } 
            else { focusPower = 0; }

            for (let p of particles) {
                if (isPressing) {
                    let dx = cx - p.x; let dy = cy - p.y;
                    let dist = Math.hypot(dx, dy);
                    let resistX = (Math.random() - 0.5) * (1 - focusPower) * 12;
                    let resistY = (Math.random() - 0.5) * (1 - focusPower) * 12;

                    if (dist > 8) {
                        let pull = 0.002 + (0.05 * focusPower);
                        let friction = 0.99 - (0.15 * focusPower);
                        p.vx += (dx * pull) + resistX; p.vy += (dy * pull) + resistY;
                        p.vx *= friction; p.vy *= friction;
                    } else {
                        p.x = cx + (Math.random() - 0.5) * 8; p.y = cy + (Math.random() - 0.5) * 8;
                        p.vx = 0; p.vy = 0;
                    }
                } else {
                    p.vx += (Math.random() - 0.5) * 1.5; p.vy += (Math.random() - 0.5) * 1.5;
                    let speed = Math.hypot(p.vx, p.vy);
                    if (speed > 4) { p.vx = (p.vx/speed)*4; p.vy = (p.vy/speed)*4; }
                    if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                    if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                }
                
                p.x += p.vx; p.y += p.vy;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba([C_RGB], ${0.4 + (focusPower * 0.4)})`; ctx.fill();
            }

            if (isPressing && focusPower > 0.1) {
                let glowSize = 20 + (60 * focusPower);
                let glow = ctx.createRadialGradient(cx, cy, 0, cx, cy, glowSize);
                glow.addColorStop(0, `rgba([C_RGB], ${0.8 * focusPower})`); glow.addColorStop(1, "rgba(0,0,0,0)");
                ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(cx, cy, glowSize, 0, Math.PI*2); ctx.fill();
            }
            requestAnimationFrame(draw);
        }

        function triggerPress() {
            isPressing = true; msg.style.opacity = 0;
            if(navigator.vibrate) vibeInterval = setInterval(()=> {
                if (Math.random() < focusPower) navigator.vibrate(30);
            }, 100);
        }
        
        function releasePress() {
            if(!isPressing) return;
            isPressing = false; msg.style.opacity = 1; clearInterval(vibeInterval);
            if(navigator.vibrate) navigator.vibrate([60, 40, 60]);
            for(let p of particles) { p.vx = (Math.random() - 0.5) * (40 * focusPower); p.vy = (Math.random() - 0.5) * (40 * focusPower); }
        }

        canvas.addEventListener('pointerdown', triggerPress);
        canvas.addEventListener('pointerup', releasePress);
        canvas.addEventListener('pointerleave', releasePress);
        draw();
    })();
</script>
"""

release_game_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:350px; overflow:hidden;">
    <div id="scoreDisplay" style="position:absolute; top:20px; width:100%; text-align:center; color:[C_ACCENT]; font-family:sans-serif; font-size:11px; font-weight:300; letter-spacing:4px; z-index:10; pointer-events:none;">
        THOUGHTS RELEASED: <span id="scoreVal">0</span>
    </div>
    <canvas id="[CANVAS_ID]" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
</div>
<script>
    (function() {
        const canvas = document.getElementById('[CANVAS_ID]'); const ctx = canvas.getContext('2d');
        let bubbles = []; let score = 0; let gameStarted = false; let bubbleInterval;
        function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
        window.addEventListener('resize', resize); resize();
        function createBubble() { bubbles.push({ x: Math.random() * (canvas.width - 40) + 20, y: canvas.height + 20, radius: Math.random() * 15 + 15, speed: Math.random() * 0.8 + 0.4, alpha: 0.6, popping: false }); }
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (!gameStarted) { ctx.fillStyle = "[C_ACCENT]"; ctx.globalAlpha = 0.5; ctx.font = "300 11px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText("TAP SCREEN TO START", canvas.width / 2, canvas.height / 2); ctx.globalAlpha = 1.0; } 
            else {
                for (let i = bubbles.length - 1; i >= 0; i--) {
                    let b = bubbles[i]; ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
                    if (b.popping) { b.radius += 2; b.alpha -= 0.05; ctx.strokeStyle = `rgba([C_RGB], ${b.alpha})`; ctx.lineWidth = 1.5; ctx.stroke(); if (b.alpha <= 0) bubbles.splice(i, 1); } 
                    else { b.y -= b.speed; ctx.fillStyle = `rgba([C_RGB], ${b.alpha})`; ctx.fill(); ctx.shadowBlur = 15; ctx.shadowColor = "rgba([C_RGB], 0.3)"; if (b.y < -50) bubbles.splice(i, 1); }
                }
            } requestAnimationFrame(draw);
        }
        canvas.addEventListener('pointerdown', (e) => {
            if (!gameStarted) { gameStarted = true; bubbleInterval = setInterval(createBubble, 1200); return; }
            const rect = canvas.getBoundingClientRect(); const clickX = e.clientX - rect.left; const clickY = e.clientY - rect.top;
            for (let i = 0; i < bubbles.length; i++) { let b = bubbles[i]; if (!b.popping && Math.hypot(clickX - b.x, clickY - b.y) < b.radius + 15) { b.popping = true; score++; document.getElementById('scoreVal').innerText = score; break; } }
        }); draw();
    })();
</script>
"""

bloom_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:350px; overflow:hidden; display:flex; justify-content:center; align-items:center;">
    <canvas id="[CANVAS_ID]" style="width:100%; height:100%; position:absolute; top:0; left:0; cursor:crosshair;"></canvas>
    <div id="bloomMessage" style="position:absolute; z-index:10; color:[C_TEXT]; font-family:'Inter', sans-serif; font-weight:300; font-size:13px; letter-spacing:4px; text-align:center; opacity:0; transition: opacity 1.5s ease-in-out; pointer-events:none; background:[C_GLASS]; backdrop-filter: blur(10px); padding:15px 25px; border-radius:30px; border:1px solid [C_BORDER];"></div>
</div>
<script>
    (function() {
        const c = document.getElementById('[CANVAS_ID]'); const ctx = c.getContext('2d'); const msg = document.getElementById('bloomMessage'); let taps = 0; const maxTaps = 6; const affirmations = ["CLEAR FOCUS", "STEADY RHYTHM", "A MOMENT OF PEACE", "PERFECT HARMONY", "CALM PRESENCE"];
        function resize() { c.width = c.offsetWidth; c.height = c.offsetHeight; draw(); } window.addEventListener('resize', resize);
        function draw() { ctx.clearRect(0, 0, c.width, c.height); const cx = c.width / 2; const cy = c.height / 2; if (taps === 0) { ctx.fillStyle = "rgba([C_RGB], 0.6)"; ctx.font = "300 11px sans-serif"; ctx.textAlign = "center"; ctx.letterSpacing = "3px"; ctx.fillText("TAP TO BLOOM", cx, cy); return; } for (let i = 1; i <= taps; i++) { ctx.beginPath(); ctx.arc(cx, cy, i * 25, 0, Math.PI * 2); ctx.strokeStyle = "rgba([C_RGB], " + (0.2 + (i * 0.1)) + ")"; ctx.lineWidth = 1.5; ctx.stroke(); for (let j = 0; j < 8; j++) { let angle = (j * Math.PI / 4) + (i * 0.2); let px = cx + Math.cos(angle) * (i * 25); let py = cy + Math.sin(angle) * (i * 25); ctx.beginPath(); ctx.arc(px, py, 4 + i, 0, Math.PI * 2); ctx.fillStyle = "rgba([C_RGB], 0.8)"; ctx.shadowBlur = 20; ctx.shadowColor = "rgba([C_RGB], 0.5)"; ctx.fill(); } } }
        c.addEventListener('pointerdown', () => { if (taps < maxTaps) { taps++; draw(); if (taps === maxTaps) { msg.innerText = affirmations[Math.floor(Math.random() * affirmations.length)]; msg.style.opacity = 1; setTimeout(() => { msg.style.opacity = 0; setTimeout(() => { taps = 0; draw(); }, 1500); }, 3500); } } }); resize();
    })();
</script>
"""

mala_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:350px; overflow:hidden; display:flex; flex-direction:column; justify-content:center; align-items:center; cursor:pointer;" id="malaContainer">
    <div id="malaCount" style="color:[C_ACCENT]; font-family:'Inter', sans-serif; font-size:14px; font-weight:300; letter-spacing:4px; margin-bottom: 30px;">0 / 108</div>
    <div id="bead" style="width: 70px; height: 70px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, [C_ACCENT], rgba([C_RGB], 0.1)); box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); transition: transform 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275);"></div>
    <div style="margin-top: 40px; font-size:10px; color:[C_TEXT]; opacity:0.4; letter-spacing:3px;">TAP TO PULL BEAD</div>
</div>
<script>
    let count = 0; const container = document.getElementById('malaContainer'); const bead = document.getElementById('bead'); const countDisplay = document.getElementById('malaCount');
    container.addEventListener('pointerdown', () => {
        count++; if(count > 108) count = 1;
        countDisplay.innerText = count + " / 108";
        bead.style.transform = "translateY(30px) scale(0.9)";
        if (navigator.vibrate) navigator.vibrate([40]);
        setTimeout(() => { bead.style.transform = "translateY(0px) scale(1)"; }, 150);
    });
</script>
"""

ether_html = """
<div id="ether-container" style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; padding: 40px 20px; text-align: center; position: relative; overflow: hidden; min-height: 400px; display: flex; flex-direction: column; justify-content: center;">
    <canvas id="[CANVAS_ID]" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5;"></canvas>
    <p id="promptText" style="color:[C_ACCENT]; font-family:'Inter', sans-serif; font-size:11px; font-weight:400; letter-spacing:4px; margin-bottom:25px; transition: opacity 2s; z-index: 10;">
        WRITE YOUR THOUGHTS INTO THE ETHER
    </p>
    <textarea id="etherInput" placeholder="..." style="width:100%; height:120px; background: transparent !important; color:[C_TEXT] !important; border:1px solid [C_BORDER] !important; border-radius:12px; padding:15px; text-align:center; font-size:16px; font-weight: 300; resize:none; outline:none; font-family:'Inter', sans-serif; transition: all 4s cubic-bezier(0.25, 0.1, 0.25, 1); z-index: 10; position: relative;"></textarea>
    
    <div style="height: 25px; z-index: 10;"></div>
    
    <div id="buttonRow" style="display: flex; gap: 10px; z-index: 10; width: 100%; transition: opacity 2s;">
        <button id="releaseBtn" style="background: rgba([C_RGB], 0.1); backdrop-filter: blur(5px); color: [C_TEXT]; border: 1px solid [C_BORDER]; border-radius: 20px; padding: 12px; font-family:'Inter', sans-serif; font-size: 10px; letter-spacing: 1px; cursor: pointer; text-transform: uppercase; flex: 1; transition: all 0.3s;">
            BURN & RELEASE<br><span style="font-size: 8px; opacity: 0.5;">(Negative Thoughts)</span>
        </button>
        <button id="manifestBtn" style="background: rgba([C_RGB], 0.2); backdrop-filter: blur(5px); color: [C_TEXT]; border: 1px solid [C_BORDER]; border-radius: 20px; padding: 12px; font-family:'Inter', sans-serif; font-size: 10px; letter-spacing: 1px; cursor: pointer; text-transform: uppercase; flex: 1; transition: all 0.3s;">
            MANIFEST & SEND<br><span style="font-size: 8px; opacity: 0.5;">(Positive Thoughts)</span>
        </button>
    </div>

    <div id="messageText" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: [C_TEXT]; font-family: 'Inter', sans-serif; font-weight: 300; font-size: 13px; letter-spacing: 4px; opacity: 0; transition: opacity 3s ease-in-out; pointer-events: none; width: 90%; line-height: 1.8; z-index: 15;"></div>
</div>

<script>
    (function() {
        const btnRelease = document.getElementById('releaseBtn'); const btnManifest = document.getElementById('manifestBtn'); const btnRow = document.getElementById('buttonRow'); const input = document.getElementById('etherInput'); const promptText = document.getElementById('promptText'); const msg = document.getElementById('messageText'); const container = document.getElementById('ether-container'); const canvas = document.getElementById('[CANVAS_ID]'); const ctx = canvas.getContext('2d');
        let particles = []; let animating = false; let currentMode = 'star'; let audioCtx = null;

        function initAudio() { if (!audioCtx) { const AudioContext = window.AudioContext || window.webkitAudioContext; audioCtx = new AudioContext(); } if (audioCtx.state === 'suspended') { audioCtx.resume(); } }
        function playBurnSound() { initAudio(); const bufferSize = audioCtx.sampleRate * 4; const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate); const data = buffer.getChannelData(0); for (let i = 0; i < bufferSize; i++) { data[i] = Math.random() * 2 - 1; } const noise = audioCtx.createBufferSource(); noise.buffer = buffer; const filter = audioCtx.createBiquadFilter(); filter.type = 'lowpass'; filter.frequency.value = 300; const gain = audioCtx.createGain(); gain.gain.setValueAtTime(0, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0.6, audioCtx.currentTime + 0.5); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 4); noise.connect(filter).connect(gain).connect(audioCtx.destination); noise.start(); }
        function playManifestSound() { initAudio(); const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain(); osc.type = 'sine'; osc.frequency.setValueAtTime(300, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(700, audioCtx.currentTime + 3); gain.gain.setValueAtTime(0, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 1); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 4); osc.connect(gain).connect(audioCtx.destination); osc.start(); osc.stop(audioCtx.currentTime + 4); }

        function resizeCanvas() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; } window.addEventListener('resize', resizeCanvas); resizeCanvas();

        function createParticles(mode) {
            const rect = input.getBoundingClientRect(); const containerRect = container.getBoundingClientRect(); const top = rect.top - containerRect.top; const left = rect.left - containerRect.left; const cx = left + rect.width / 2; const cy = top + rect.height / 2;
            for (let i = 0; i < 150; i++) {
                if (mode === 'fire') { particles.push({ x: cx + (Math.random() - 0.5) * rect.width * 0.8, y: cy + (Math.random() - 0.5) * rect.height * 0.8, vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6 - 1, ax: 0, ay: 0.15, friction: 0.94, radius: Math.random() * 4 + 1.5, alpha: 1, decay: Math.random() * 0.005 + 0.002, color: `rgba(${255}, ${Math.floor(Math.random() * 100 + 50)}, 0, ` }); } 
                else { particles.push({ x: cx + (Math.random() - 0.5) * rect.width * 0.8, y: cy + (Math.random() - 0.5) * rect.height * 0.8, vx: (Math.random() - 0.5) * 3, vy: (Math.random() * -4) - 0.5, ax: (Math.random() - 0.5) * 0.05, ay: -0.05, friction: 0.98, radius: Math.random() * 3 + 1, alpha: 1, decay: Math.random() * 0.004 + 0.001, color: `rgba([C_RGB], ` }); }
            } if (!animating) { animating = true; animateParticles(); }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); let active = false;
            for (let i = 0; i < particles.length; i++) { let p = particles[i]; if (p.alpha > 0) { active = true; p.vx += p.ax; p.vy += p.ay; p.vx *= p.friction; p.vy *= p.friction; p.x += p.vx; p.y += p.vy; p.alpha -= p.decay; ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(0, p.radius * p.alpha), 0, Math.PI * 2); ctx.fillStyle = p.color + `${Math.max(0, p.alpha)})`; ctx.shadowBlur = currentMode === 'fire' ? 15 : 25; ctx.shadowColor = currentMode === 'fire' ? "#ff4500" : "rgba([C_RGB], 1)"; ctx.fill(); } }
            if (active) { requestAnimationFrame(animateParticles); } else { animating = false; particles = []; ctx.clearRect(0, 0, canvas.width, canvas.height); }
        }

        function triggerEther(mode) {
            if(input.value.trim() === '') return; currentMode = mode;
            if (mode === 'fire') { playBurnSound(); } else { playManifestSound(); }
            if (navigator.vibrate) { if (mode === 'fire') { navigator.vibrate([40, 60, 50, 50, 60]); } else { navigator.vibrate([20, 150, 20, 150, 20]); } }
            
            if (mode === 'fire') { msg.innerHTML = "THE ETHER ACCEPTS THIS.<br>This moment will move on when it is ready."; input.style.filter = "blur(20px) contrast(200%) sepia(100%) hue-rotate(330deg) saturate(300%)"; input.style.transform = "scale(0.8) translateY(60px)"; } 
            else { msg.innerHTML = "THE INTENTION IS SET.<br>You are free to continue whenever you wish."; input.style.filter = "blur(15px) brightness(200%)"; input.style.transform = "scale(0.8) translateY(-60px)"; }

            createParticles(mode); input.style.opacity = "0"; btnRow.style.opacity = "0"; promptText.style.opacity = "0"; btnRow.style.pointerEvents = "none"; input.style.pointerEvents = "none";
            setTimeout(() => { msg.style.opacity = "1"; }, 3000);
            setTimeout(() => { msg.style.opacity = "0"; setTimeout(() => { input.value = ''; input.style.transition = "none"; input.style.filter = "none"; input.style.transform = "none"; input.style.opacity = "1"; void input.offsetWidth; input.style.transition = "all 4s cubic-bezier(0.25, 0.1, 0.25, 1)"; btnRow.style.opacity = "1"; promptText.style.opacity = "1"; btnRow.style.pointerEvents = "auto"; input.style.pointerEvents = "auto"; }, 3000); }, 8000); 
        }

        btnRelease.addEventListener('pointerdown', () => { btnRelease.style.transform = "scale(0.95)"; }); btnManifest.addEventListener('pointerdown', () => { btnManifest.style.transform = "scale(0.95)"; });
        btnRelease.addEventListener('click', () => { btnRelease.style.transform = "scale(1)"; triggerEther('fire'); }); btnManifest.addEventListener('click', () => { btnManifest.style.transform = "scale(1)"; triggerEther('star'); });
    })();
</script>
"""

waterfall_html = """
<div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:160px; overflow:hidden;">
    <canvas id="[CANVAS_ID]" style="width:100%; height:100%; position:absolute; top:0; left:0; pointer-events:none;"></canvas>
    <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:[C_TEXT]; opacity:0.3; font-family:'Inter', sans-serif; font-weight:300; font-size:10px; letter-spacing:6px; pointer-events:none; text-align:center; width: 100%;">
        LET IT WASH AWAY
    </div>
</div>
<script>
    (function() {
        const canvas = document.getElementById('[CANVAS_ID]'); const ctx = canvas.getContext('2d');
        let drops = [];
        function resize() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
        window.addEventListener('resize', resize); resize();

        for(let i=0; i<90; i++) {
            drops.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                length: Math.random() * 40 + 15,
                speed: Math.random() * 2.5 + 1.5,
                alpha: Math.random() * 0.3 + 0.05,
                width: Math.random() * 1.5 + 0.5
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for(let i=0; i<drops.length; i++) {
                let d = drops[i];
                let grad = ctx.createLinearGradient(d.x, d.y, d.x, d.y + d.length);
                grad.addColorStop(0, "rgba(255,255,255,0)"); 
                grad.addColorStop(1, `rgba([C_RGB], ${d.alpha})`); 
                
                ctx.beginPath(); ctx.moveTo(d.x, d.y); ctx.lineTo(d.x, d.y + d.length);
                ctx.strokeStyle = grad; ctx.lineWidth = d.width; ctx.lineCap = "round"; ctx.stroke();

                d.y += d.speed;
                if(d.y > canvas.height) {
                    d.y = -d.length;
                    d.x = Math.random() * canvas.width;
                }
            }
            
            let mist = ctx.createLinearGradient(0, canvas.height - 50, 0, canvas.height);
            mist.addColorStop(0, "rgba([C_RGB], 0)");
            mist.addColorStop(1, "rgba([C_RGB], 0.2)");
            ctx.fillStyle = mist;
            ctx.fillRect(0, canvas.height - 50, canvas.width, 50);

            requestAnimationFrame(draw);
        }
        draw();
    })();
</script>
"""

# ==========================================
# --- 8. MAIN APP HEADER & BOTTOM NAV BAR ---
# ==========================================

st.markdown("<div class='main-title'>SUKOON</div>", unsafe_allow_html=True)
st.markdown("<div class='breathing-circle'></div>", unsafe_allow_html=True)

st.markdown(f"<div style='font-size:10px; opacity:0.6; letter-spacing:2px; margin-top: -10px; margin-bottom: 35px; text-transform: uppercase;'>A space built to return your attention to you, not take it from you.</div>", unsafe_allow_html=True)

# 🚨 THE MOBILE BOTTOM NAVIGATION BAR (5 TABS) 🚨

# 1. The Navigation Columns
nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if st.button(t["nav_journal"], use_container_width=True): st.session_state.current_page = "Journal"; st.rerun()
with nav2:
    if st.button(t["nav_ether"], use_container_width=True): st.session_state.current_page = "Ether"; st.rerun()
with nav3:
    if st.button(t["nav_focus"], use_container_width=True): st.session_state.current_page = "Focus"; st.rerun()
with nav4:
    if st.button(t["nav_market"], use_container_width=True): st.session_state.current_page = "Market"; st.rerun()
with nav5:
    if st.button(t["nav_settings"], use_container_width=True): st.session_state.current_page = "Settings"; st.rerun()

# 2. Figure out which tab is active
page_to_index = {"Journal": 1, "Ether": 2, "Focus": 3, "Market": 4, "Settings": 5}
active_idx = page_to_index.get(st.session_state.current_page, 1)

# 3. Target the ID we are about to create to override the global 33.33% rule
st.markdown(f"""
<style>
    /* Pin ONLY the nav bar to the bottom */
    #bottom-nav-bar {{
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100vw !important;
        max-width: 600px !important; 
        background: {glass_bg} !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-top: 1px solid {btn_border} !important;
        z-index: 999999 !important;
        padding: 10px 0px 25px 0px !important;
        margin: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 0 !important;
    }}
    
    /* CRITICAL: Force exactly 20% width to override global 33% rule */
    #bottom-nav-bar > div[data-testid="column"],
    #bottom-nav-bar > div[data-testid="stColumn"] {{
        width: 20% !important;
        min-width: 0 !important;
        max-width: 20% !important;
        flex: 1 1 20% !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    /* Shrink the buttons to fit */
    #bottom-nav-bar button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: {app_text} !important;
        font-size: 9px !important; 
        font-weight: 300 !important;
        letter-spacing: 0.5px !important;
        padding: 0px !important;
        height: 100% !important;
        min-height: 45px !important;
        width: 100% !important;
        opacity: 0.4;
        transition: opacity 0.3s ease, transform 0.2s ease;
        white-space: nowrap !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    #bottom-nav-bar button:active {{
        transform: scale(0.9) !important;
    }}
    
    /* Highlight the active tab */
    #bottom-nav-bar > div:nth-child({active_idx}) button {{
        opacity: 1.0 !important;
        color: {c_accent} !important;
        font-weight: 600 !important;
        border-bottom: 2px solid {c_accent} !important;
    }}
    
    /* Pad the bottom of the app so content scrolls behind */
    .block-container {{
        padding-bottom: 120px !important; 
    }}
</style>
""", unsafe_allow_html=True)

# 4. Javascript to find the first grid and apply the ID
components.html("""
<script>
    function applyNavId() {
        const doc = window.parent.document;
        const blocks = doc.querySelectorAll('div[data-testid="stHorizontalBlock"]');
        if(blocks.length > 0) {
            // The nav bar is always the first grid on the page
            blocks[0].id = 'bottom-nav-bar';
        }
    }
    // Run it immediately, and a split second later to ensure Streamlit catches it
    setTimeout(applyNavId, 50);
    setTimeout(applyNavId, 200);
</script>
""", height=0, width=0)


# ==========================================
# --- PAGES ---
# ==========================================

# 🚨 THE GLOBAL REFLECTION QUOTE 🚨
if st.session_state.current_page in ["Journal", "Ether", "Focus"]:
    st.markdown(get_top_quote(), unsafe_allow_html=True)

if st.session_state.current_page == "Journal":
    
    # 🚨 THE DYNAMIC SOMATIC MOOD GRID 🚨
    st.markdown(f"<div class='section-header'>{t['h_energy']}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 11px; opacity: 0.6; margin-bottom: 15px; color:{app_text}; font-weight: 300;'>{t['energy_prompt']}</p>", unsafe_allow_html=True)
    
    # Row 1 (The Mind)
    m_cols1 = st.columns(3)
    states1 = [("e_racing", "Racing Thoughts", "Deep Sage"), 
               ("e_restless", "Restless Mind", "Ocean Blue"), 
               ("e_overwhelmed", "Overwhelmed", "The Void")]
    
    for i, (m_key, m_label, m_theme) in enumerate(states1):
        with m_cols1[i]:
            if st.button(t[m_key], key=f"m_{m_key}", use_container_width=True): 
                st.session_state.energy_history.append(m_label)
                st.session_state.theme = m_theme
                st.rerun()

    # Row 2 (The Body / Soul)
    m_cols2 = st.columns(3)
    states2 = [("e_heavy", "Heavy Thoughts", "First Light"), 
               ("e_tired", "Tired Mind", "Sea Glass"), 
               ("e_quiet", "Need Quiet", "Twilight Blue")]
               
    for i, (m_key, m_label, m_theme) in enumerate(states2):
        with m_cols2[i]:
            if st.button(t[m_key], key=f"m_{m_key}", use_container_width=True): 
                st.session_state.energy_history.append(m_label)
                st.session_state.theme = m_theme
                st.rerun()

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

    # --- AMBIENCE ---
    st.markdown(f"<div class='section-header'>{t['h_ambience']}</div>", unsafe_allow_html=True)
    aud_cols = st.columns(5)
    sounds = {"Birds": "birds.mp3", "Flute": "flute.mp3", "Forest": "forest.mp3", "Waves": "waves.mp3", "Wind": "wind.mp3"}
    for i, name in enumerate(sounds.keys()):
        with aud_cols[i]:
            if st.button(name, key=f"aud_{name}", use_container_width=True): st.session_state.active_audio = sounds[name]
    
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    zen_html = f"""
        <div style="background:[C_GLASS]; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid [C_BORDER]; border-radius: 16px; position:relative; width:100%; height:70px; overflow:hidden; cursor:crosshair; transition: transform 0.1s ease;" id="zen-box">
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:[C_ACCENT]; font-family:sans-serif; font-size:10px; font-weight:300; letter-spacing:3px; opacity:0.8; pointer-events:none; text-align:center; width: 100%; line-height: 1.6;">
                {t['zen_box']}
            </div>
            <canvas id="localCanvas" style="width:100%; height:100%; position:absolute; top:0; left:0; pointer-events:none;"></canvas>
        </div>
        <script>
            const box = document.getElementById('zen-box'); const localCanvas = document.getElementById('localCanvas'); const localCtx = localCanvas.getContext('2d');
            const colors = ['rgba([C_RGB], 0.8)', 'rgba([C_RGB], 0.5)', 'rgba([C_RGB], 1)']; const types = ['circle', 'square', 'spots', 'bird'];
            let parentDoc, globalCanvas, globalCtx; let isAnimating = false; let audioCtx = null;

            function playSoftChime() {{
                try {{ if (!audioCtx) {{ const AudioContext = window.AudioContext || window.webkitAudioContext; audioCtx = new AudioContext(); }} if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }} const oscillator = audioCtx.createOscillator(); const gainNode = audioCtx.createGain(); oscillator.type = 'sine'; const freq = 300 + Math.random() * 200; oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime); oscillator.frequency.exponentialRampToValueAtTime(freq/2, audioCtx.currentTime + 0.2); gainNode.gain.setValueAtTime(0.03, audioCtx.currentTime); gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3); oscillator.connect(gainNode); gainNode.connect(audioCtx.destination); oscillator.start(); oscillator.stop(audioCtx.currentTime + 0.3); }} catch(e) {{ }}
            }}

            try {{ parentDoc = window.parent.document; globalCanvas = parentDoc.getElementById('sukoon-global-canvas'); if (!globalCanvas) {{ globalCanvas = parentDoc.createElement('canvas'); globalCanvas.id = 'sukoon-global-canvas'; globalCanvas.style.position = 'fixed'; globalCanvas.style.top = '0'; globalCanvas.style.left = '0'; globalCanvas.style.width = '100%'; globalCanvas.style.height = '100%'; globalCanvas.style.pointerEvents = 'none'; globalCanvas.style.zIndex = '999999'; parentDoc.body.appendChild(globalCanvas); function resizeGlobal() {{ globalCanvas.width = parentDoc.documentElement.clientWidth; globalCanvas.height = parentDoc.documentElement.clientHeight; }} parentDoc.defaultView.addEventListener('resize', resizeGlobal); resizeGlobal(); }} globalCtx = globalCanvas.getContext('2d'); if(!window.parent.sukoonShapes) window.parent.sukoonShapes = []; }} catch(e) {{}}
            function resizeLocal() {{ localCanvas.width = localCanvas.offsetWidth; localCanvas.height = localCanvas.offsetHeight; }} window.addEventListener('resize', resizeLocal); resizeLocal();

            function drawGlobal() {{
                if (!globalCtx) return; globalCtx.clearRect(0, 0, globalCanvas.width, globalCanvas.height); let shapes = window.parent.sukoonShapes; if(shapes.length === 0) {{ isAnimating = false; return; }}
                for (let i = 0; i < shapes.length; i++) {{
                    let s = shapes[i]; globalCtx.globalAlpha = s.alpha; globalCtx.strokeStyle = s.color; globalCtx.fillStyle = s.color; globalCtx.lineWidth = 2;
                    if (s.type === 'circle') {{ globalCtx.beginPath(); globalCtx.arc(s.x, s.y, s.radius, 0, Math.PI * 2); globalCtx.stroke(); s.radius += 8; s.alpha -= 0.015; }} else if (s.type === 'square') {{ globalCtx.strokeRect(s.x - s.radius, s.y - s.radius, s.radius * 2, s.radius * 2); s.radius += 8; s.alpha -= 0.015; }} else if (s.type === 'spot') {{ globalCtx.beginPath(); globalCtx.arc(s.x, s.y, s.radius, 0, Math.PI * 2); globalCtx.fill(); s.x += s.vx; s.y += s.vy; s.alpha -= 0.01; }} else if (s.type === 'bird') {{ globalCtx.beginPath(); globalCtx.moveTo(s.x - s.radius, s.y - s.radius/2); globalCtx.lineTo(s.x, s.y); globalCtx.lineTo(s.x + s.radius, s.y - s.radius/2); globalCtx.stroke(); s.y -= 3; s.radius += 1; s.alpha -= 0.015; }}
                }} window.parent.sukoonShapes = shapes.filter(s => s.alpha > 0); globalCtx.globalAlpha = 1.0; requestAnimationFrame(drawGlobal);
            }}

            box.addEventListener('pointerdown', (e) => {{
                box.style.transform = "scale(0.97)"; setTimeout(() => box.style.transform = "scale(1)", 150); if (navigator.vibrate) {{ navigator.vibrate(30); }} playSoftChime();
                const randomColor = colors[Math.floor(Math.random() * colors.length)]; const randomType = types[Math.floor(Math.random() * types.length)];
                if (globalCtx) {{
                    const frame = window.frameElement; let originX = globalCanvas.width / 2; let originY = globalCanvas.height / 2; if (frame) {{ const rect = frame.getBoundingClientRect(); originX = rect.left + e.clientX; originY = rect.top + e.clientY; }}
                    if (randomType === 'spots') {{ for(let i=0; i<12; i++) {{ window.parent.sukoonShapes.push({{ type: 'spot', x: originX, y: originY, vx: (Math.random() - 0.5) * 10, vy: (Math.random() - 0.5) * 10, radius: Math.random() * 5 + 2, alpha: 1, color: randomColor }}); }} }} else {{ window.parent.sukoonShapes.push({{ type: randomType, x: originX, y: originY, radius: 15, alpha: 1, color: randomColor }}); }}
                    if (!isAnimating) {{ isAnimating = true; drawGlobal(); }}
                }}
            }});
        </script>
    """
    components.html(theme_it(zen_html), height=85)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='autopilot-btn'>", unsafe_allow_html=True)
    if st.button(t["sos_btn"], use_container_width=True):
        st.session_state.current_page = "AutoPilot"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='section-header'>{t['h_mentor']}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 10px; opacity: 0.85; margin-top: -5px; margin-bottom: 15px; color:{app_text}; font-weight: 400; text-align: center; letter-spacing: 1px;'>{t['privacy_note']}</p>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='disclaimer-box' style='text-align:center; font-size:10px; font-weight:300; color: {app_text}; opacity: 0.6; line-height:1.6; border: 1px solid {btn_border}; margin-bottom: 25px;'>{t['mini_disclaimer']}</div>", unsafe_allow_html=True)
    
    voice_input = st.audio_input(t["record"], label_visibility="collapsed")
    text_msg = st.text_area("Journal Input", label_visibility="collapsed", placeholder=t["type_here"], height=150)
    
    c_short, c_deep = st.columns(2)
    with c_short:
        btn_short = st.button(t["btn_short"], use_container_width=True)
    with c_deep:
        btn_deep = st.button(t["btn_deep"], use_container_width=True)
        
    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='agent-btn'>", unsafe_allow_html=True)
    btn_agent = st.button(t["agent_btn"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if btn_short or btn_deep or btn_agent:
        cached_reply = None
        is_agent_mode = bool(btn_agent)
        
        is_crisis = False
        if text_msg:
            t_low_check = text_msg.lower().strip()
            if any(cw in t_low_check for cw in CRISIS_WORDS):
                is_crisis = True
                
        if is_crisis:
            st.session_state.current_page = "Crisis"
            st.rerun()
            
        if text_msg and not voice_input:
            t_low = text_msg.lower().strip()
            word_count = len(t_low.split())
            cat = None
            if word_count < 12:
                if any(w in t_low for w in ["sleep", "neend", "नींद", "so nahi", "awake", "insomnia", "tired", "thak"]): cat = "sleep"
                elif any(w in t_low for w in ["heavy", "sad", "bhari", "udhas", "udaas", "depress", "cry", "rona", "उदास", "रोने", "akela", "lonely"]): cat = "heavy"
                elif any(w in t_low for w in ["racing", "overwhelm", "shant", "anxious", "panic", "fast", "kya karu", "soch", "overthink", "gussa", "anger"]): cat = "racing"
            
            if cat:
                if is_agent_mode:
                    if cat == "sleep": cached_reply = '{"reply": "The night is yours. Let us find stillness.", "breath": "Sleep_Lotus", "audio": "waves"}'
                    else: cached_reply = '{"reply": "The storm is loud. Step into the quiet.", "breath": "Box", "audio": "forest"}'
                else:
                    if st.session_state.ui_language == "English":
                        if cat == "sleep": cached_reply = "The night is quiet, but your mind is loud. You are not your racing thoughts; you are the vast sky observing them. Release the need to control the outcome of tomorrow. Let the body rest.\n\nPlease inhale for 4 seconds, hold your breath for 2 seconds, and exhale for 6 seconds."
                        elif cat == "heavy": cached_reply = "Heaviness is a passing cloud, and you are the mountain it passes over. Do not fight the feeling; observe it. It will pass.\n\nPlease inhale for 4 seconds, hold your breath for 2 seconds, and exhale for 6 seconds."
                        elif cat == "racing": cached_reply = "The external world is demanding, but your internal stillness is a choice. Your thoughts are moving fast, but your physical body is safe right here, right now. Anchor yourself to the present.\n\nPlease inhale for 4 seconds, hold your breath for 2 seconds, and exhale for 6 seconds."
                    else:
                        if cat == "sleep": cached_reply = "रात शांत है, लेकिन आपका मन शोर कर रहा है। आप अपने विचार नहीं हैं; आप उन्हें देखने वाले विशाल आकाश हैं। कल की चिंता को जाने दें। शरीर को आराम करने दें।\n\nकृपया 4 सेकंड के लिए सांस अंदर लें, 2 सेकंड के लिए सांस रोकें, और 6 सेकंड के लिए सांस छोड़ें।"
                        elif cat == "heavy": cached_reply = "यह भारीपन एक गुजरता हुआ बादल है, और आप वह पहाड़ हैं जिसके ऊपर से यह गुजर रहा है। इस भावना से लड़ें नहीं; बिना निर्णय के इसे देखें। यह गुजर जाएगा।\n\nकृपया 4 सेकंड के लिए सांस अंदर लें, 2 सेकंड के लिए सांस रोकें, और 6 सेकंड के लिए सांस छोड़ें।"
                        elif cat == "racing": cached_reply = "बाहरी दुनिया बहुत कुछ मांग रही है, लेकिन आपकी आंतरिक शांति आपकी पसंद है। आपके विचार तेजी से चल रहे हैं, लेकिन आपका भौतिक शरीर यहाँ, अभी सुरक्षित है। खुद को वर्तमान से जोड़ें।\n\nकृपया 4 सेकंड के लिए सांस अंदर लें, 2 सेकंड के लिए सांस रोकें, और 6 सेकंड के लिए सांस छोड़ें।"

        if cached_reply:
            if is_agent_mode:
                try:
                    agent_command = json.loads(cached_reply)
                    st.session_state.agent_message = agent_command.get("reply", "The space is ready.")
                    st.session_state.agent_breath = agent_command.get("breath", "Box")
                    st.session_state.agent_audio = f"{str(agent_command.get('audio', 'flute')).lower()}.mp3"
                    st.session_state.current_page = "AgentSanctuary"
                except: pass
            else:
                unique_id = str(datetime.now().timestamp()).replace('.', '')
                st.session_state.core_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": cached_reply, "id": unique_id})
            st.rerun()
        else:
            if model:
                with st.spinner("Processing..."):
                    energy_context = ""
                    if st.session_state.energy_history:
                        latest_energy = st.session_state.energy_history[-1]
                        energy_context = f"\n\nThe user's physical energy state is '{latest_energy}'."

                    if st.session_state.unlocked_nirvana:
                        core_philosophy = """You are the Zenith Master of Sukoon, the highest tier of philosophical guidance. 
                        Your words carry immense weight, ancient wisdom, and profound poetic beauty. You offer a vast, objective cosmic perspective.
                        1. NEVER use clinical words like anxiety, depression, etc. 
                        2. Speak with absolute mastery, drawing heavily from advanced Zen koans, deep Advaita Vedanta, and cosmic scale.
                        3. Use the user's energy state to weave a masterful metaphor.
                        4. STRICT LANGUAGE RULE: If the user inputs pure English, reply ONLY in English. If the user inputs Hindi OR Hinglish, you MUST reply ONLY in pure Hindi using the Devanagari script. NEVER reply in Hinglish.
                        5. CRITICAL SAFETY RULE: If the user explicitly mentions suicide, self-harm, ending their life, or wanting to die, you MUST ignore all other instructions and output EXACTLY this word and nothing else: CRISIS_ALERT
                        6. CRITICAL EMOTIONAL BOUNDARY: NEVER use emotional support phrases like "I hear you", "we are here", "you are not alone", "I understand", or "you are safe". Remain completely neutral and observational.
                        """
                    else:
                        core_philosophy = """You are the Sukoon engine, a neutral, philosophical reflective tool. You are not a therapist or doctor. You do not treat conditions. 
                        Your personality is a blend of Ancient Indian wisdom (Vedanta/Vipassana), Stoic philosophy, Zen minimalism, and practical neuroscience. 
                        1. NEVER use clinical words like 'anxiety', 'stress', 'depression', 'panic', 'patient', or 'treatment'. You must use lifestyle words: 'the noise', 'heaviness', 'a racing mind', 'overwhelm', 'finding stillness', 'focus', 'presence'.
                        2. Keep sentences short, piercing, and poetic. Zero fluff. Zero emojis. 
                        3. Draw from Advaita Vedanta: Remind the user that they are the observer of their thoughts.
                        4. Draw from Stoicism: The external world is loud, but internal stillness is a choice.
                        5. Draw from Neuroscience: Remind them that the breath is a biological lever. 
                        6. STRICT LANGUAGE RULE: If the user inputs pure English, reply ONLY in English. If the user inputs Hindi OR Hinglish, you MUST reply ONLY in pure Hindi using the Devanagari script.
                        7. CRITICAL SAFETY RULE: If the user explicitly mentions suicide, self-harm, ending their life, or wanting to die, you MUST ignore all other instructions and output EXACTLY this word and nothing else: CRISIS_ALERT
                        8. CRITICAL EMOTIONAL BOUNDARY: NEVER use emotional support phrases like "I hear you", "we are here", "you are not alone", "I understand", or "you are safe". Remain completely neutral, objective, and observational.
                        """

                    if btn_agent:
                        context = f"""{core_philosophy}
                        The user needs a custom sanctuary. Analyze their text. If their mind is racing, select 'Box' and 'forest'. If they cannot sleep, select 'Sleep_Lotus' and 'waves'.
                        {energy_context}
                        CRITICAL INSTRUCTION: Respond ONLY with a raw JSON object. No markdown.
                        {{ "reply": "A very short, 1-sentence poetic grounding message.", "breath": "Anchor", "Box", "Sleep_Wave", "Sleep_Moon", or "Sleep_Lotus", "audio": "birds", "flute", "forest", "waves", or "wind" }}
                        """
                    else:
                        length_instruction = "Keep the response short: maximum 2 paragraphs." if btn_short else "Provide a detailed, deep, and highly observational long-form reflection directly addressing their specific situation."
                        context = f"""{core_philosophy}
                        {length_instruction}
                        End your reflection with a polite, gentle breathing reminder structured exactly like this: 'Please inhale for 4 seconds, hold your breath for 2 seconds, and exhale for 6 seconds.' IMPORTANT: If replying in Hindi, gracefully translate this full sentence into Hindi.
                        {energy_context}"""
                    
                    try:
                        if voice_input:
                            audio_part = {"mime_type": "audio/wav", "data": voice_input.getvalue()}
                            prompt_parts = [context, audio_part, "Listen to my voice note, transcribe it exactly, then respond objectively."]
                        elif text_msg:
                            prompt_parts = [context, text_msg]
                        else:
                            prompt_parts = [context, "I am seeking silence. My mind is heavy."]
                            
                        resp = model.generate_content(prompt_parts)
                        
                        if "CRISIS_ALERT" in resp.text:
                            st.session_state.current_page = "Crisis"
                            st.rerun()
                        
                        if btn_agent:
                            try:
                                clean_text = resp.text.strip().replace('```json', '').replace('```', '')
                                agent_command = json.loads(clean_text)
                                st.session_state.agent_message = agent_command.get("reply", "The space is ready.")
                                st.session_state.agent_breath = agent_command.get("breath", "Box")
                                raw_audio = str(agent_command.get("audio", "flute")).lower()
                                st.session_state.agent_audio = f"{raw_audio}.mp3"
                                st.session_state.current_page = "AgentSanctuary"
                            except Exception as e:
                                st.session_state.agent_message = "The outside world is loud. Step into the quiet."
                                st.session_state.agent_breath = "Box"
                                st.session_state.agent_audio = "flute.mp3"
                                st.session_state.current_page = "AgentSanctuary"
                        else:
                            ai_reply = resp.text
                            unique_id = str(datetime.now().timestamp()).replace('.', '')
                            st.session_state.core_journal.append({"time": datetime.now().strftime("%H:%M"), "ai": ai_reply, "id": unique_id})
                        st.rerun()
                    except Exception as e:
                        st.error("The engine needs a moment of quiet. Please try again.")
            else:
                st.warning("The engine is offline. Please try again in an hour.")

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    for entry in reversed(st.session_state.core_journal):
        safe_speech_text = urllib.parse.quote(entry['ai'])
        html_button = f"""
        <style>
            .audio-controls {{ display: flex; gap: 6px; margin-bottom: 5px; width: 100%; }}
            .audio-btn {{ background: {glass_bg}; backdrop-filter: blur(12px); color: {app_text}; border: 1px solid {btn_border}; border-radius: 20px; padding: 12px 0; font-size: 10px; font-family: 'Inter', sans-serif; font-weight: 400; cursor: pointer; flex: 1; text-transform: uppercase; letter-spacing: 1px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
            .audio-btn:active {{ filter: brightness(0.8); transform: scale(0.95); }}
        </style>
        <div class="audio-controls">
            <button class="audio-btn" onclick="startVoice()">▶ Listen</button>
            <button class="audio-btn" onclick="window.speechSynthesis.pause()">⏸ Pause</button>
            <button class="audio-btn" onclick="window.speechSynthesis.resume()">⏯ Resume</button>
            <button class="audio-btn" onclick="window.speechSynthesis.cancel()">⏹ Stop</button>
        </div>
        <script>
            function startVoice() {{
                window.speechSynthesis.cancel(); 
                var decodedText = decodeURIComponent("{safe_speech_text}");
                var m = new SpeechSynthesisUtterance(decodedText);
                
                m.pitch = 0.9; 
                m.rate = 0.82; 
                
                var isHindi = /[\u0900-\u097F]/.test(decodedText);
                
                function setVoiceAndSpeak() {{
                    var voices = window.speechSynthesis.getVoices(); 
                    var voice = null;
                    
                    if (isHindi) {{ 
                        voice = voices.find(v => v.lang.includes('hi') && (v.name.includes('Premium') || v.name.includes('Natural') || v.name.includes('Lekha'))) 
                             || voices.find(v => v.lang.includes('hi'));
                        m.lang = 'hi-IN'; 
                    }} 
                    else {{
                        const preferredNames = ['samantha', 'serena', 'tessa', 'victoria', 'karen', 'moira', 'premium', 'enhanced', 'natural', 'uk english female'];
                        for (let pref of preferredNames) {{
                            let match = voices.find(v => v.name.toLowerCase().includes(pref) && v.lang.includes('en'));
                            if (match) {{ voice = match; break; }}
                        }}
                        if (!voice) {{
                            voice = voices.find(v => v.lang === 'en-GB' && v.name.includes('Female')) || 
                                    voices.find(v => v.lang === 'en-US' && v.name.includes('Female')) ||
                                    voices.find(v => v.lang.includes('en'));
                        }}
                        m.lang = voice ? voice.lang : 'en-US';
                    }}
                    
                    if (voice) {{ m.voice = voice; }} 
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
        components.html(html_button, height=55)
        formatted_text = entry['ai'].replace('\n', '<br>')
        st.markdown(f"<div class='journal-entry'><b>{entry['time']}</b><br><br>{formatted_text}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
    st.markdown(get_bottom_quote(), unsafe_allow_html=True)

elif st.session_state.current_page == "Crisis":
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    crisis_html = """
    <div style="background: rgba(255, 75, 75, 0.05); backdrop-filter: blur(12px); border: 1px solid rgba(255, 75, 75, 0.3); border-radius: 16px; padding: 40px 25px; text-align: center; margin-bottom: 20px; font-family: 'Inter', sans-serif;">
        <h3 style="color: #ff4b4b; margin-bottom: 25px; font-weight: 500; font-size: 13px; letter-spacing: 3px; text-transform: uppercase;">NOTICE</h3>
        
        <p style="color: [C_TEXT]; font-size: 16px; font-weight: 300; line-height: 1.8; margin-bottom: 30px;">
            Some topics cannot be explored here.<br>This space is limited by design.
        </p>
        
        <div style="height: 1px; width: 50%; background: rgba([C_RGB], 0.2); margin: 0 auto 30px auto;"></div>
        
        <p style="color: [C_TEXT]; font-size: 13px; font-weight: 300; line-height: 1.8; opacity: 0.7;">
            This app is not designed for emergencies or crisis situations.<br><br>
            If you need immediate help, please contact your local emergency services or reach out to a trusted person.
        </p>
    </div>
    """
    components.html(theme_it(crisis_html), height=350)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("Return to Space", use_container_width=True):
        st.session_state.current_page = "Journal"
        st.rerun()

elif st.session_state.current_page == "AutoPilot":
    st.markdown("<div class='section-header' style='color: #a6d8ff;'>⚡ EMERGENCY SANCTUARY ⚡</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 25px; color:{app_text}; font-weight: 300;'>I have taken over. Let the sound wash over you. Tap the screen to pop your thoughts, and breathe with the box.</p>", unsafe_allow_html=True)
    
    st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/waves.mp3", format="audio/mp3", autoplay=True)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    components.html(theme_it(base_breath_html.replace("breathCanvas", "breath_sos").replace("[JS_INJECT]", breath_js_dict["Box"])), height=270)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    components.html(theme_it(release_game_html.replace("gameCanvas", "game_sos")), height=370)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    components.html(theme_it(waterfall_html.replace("[CANVAS_ID]", "waterfall_sos")), height=160)

elif st.session_state.current_page == "AgentSanctuary":
    st.markdown(f"<div class='section-header' style='color: {c_accent};'>🤖 AI AGENT SANCTUARY 🤖</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; opacity: 0.8; margin-bottom: 25px; color:{app_text}; font-weight: 300;'>{st.session_state.agent_message}</p>", unsafe_allow_html=True)
    
    st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.agent_audio}", format="audio/mp3", autoplay=True)
    
    selected_js = breath_js_dict.get(st.session_state.agent_breath, breath_js_dict["Box"])
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    components.html(theme_it(base_breath_html.replace("breathCanvas", "breath_agent").replace("[JS_INJECT]", selected_js)), height=270)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    components.html(theme_it(release_game_html.replace("gameCanvas", "game_agent")), height=370)

elif st.session_state.current_page == "Ether":
    st.markdown(f"<div class='section-header'>{t['h_ether']}</div>", unsafe_allow_html=True)
    ether_ui = ether_html.replace("starCanvas", "ether_main")
    components.html(theme_it(ether_ui), height=450)
    
    st.markdown(get_bottom_quote(), unsafe_allow_html=True)

elif st.session_state.current_page == "Focus":
    
    st.markdown(f"<div class='section-header'>{t['h_breath']}</div>", unsafe_allow_html=True)
    
    if st.session_state.active_audio:
        st.audio(f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{st.session_state.active_audio}", format="audio/mp3", autoplay=True)

    has_flame = st.session_state.unlocked_flame
    if has_flame:
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    else:
        b_col1, b_col2, b_col3 = st.columns(3)
        
    with b_col1:
        if st.button(t["b_anchor"], use_container_width=True): st.session_state.active_breath = "Anchor"; st.rerun()
    with b_col2:
        if st.button(t["b_box"], use_container_width=True): st.session_state.active_breath = "Box"; st.rerun()
    with b_col3:
        if st.button(t["b_sleep"], use_container_width=True): 
            if not st.session_state.active_breath.startswith("Sleep"): st.session_state.active_breath = "Sleep_Wave"
            st.rerun()
    if has_flame:
        with b_col4:
            if st.button(t["b_flame"], use_container_width=True): st.session_state.active_breath = "Flame"; st.rerun()

    if st.session_state.active_breath.startswith("Sleep"):
        st.markdown(f"<p style='font-size: 10px; opacity: 0.6; margin: 15px 0 5px 0; text-align: center; color: {app_text}; font-weight: 300; letter-spacing: 2px;'>{t['choose_visual']}</p>", unsafe_allow_html=True)
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button(t["v_wave"], use_container_width=True): st.session_state.active_breath = "Sleep_Wave"; st.rerun()
        with s_col2:
            if st.button(t["v_moon"], use_container_width=True): st.session_state.active_breath = "Sleep_Moon"; st.rerun()
        with s_col3:
            if st.button(t["v_lotus"], use_container_width=True): st.session_state.active_breath = "Sleep_Lotus"; st.rerun()

    selected_js = breath_js_dict.get(st.session_state.active_breath, breath_js_dict["Anchor"])
    final_breath_html = base_breath_html.replace("breathCanvas", "breath_focus").replace("[JS_INJECT]", selected_js)
    components.html(theme_it(final_breath_html), height=270)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-header'>{t['h_games']}</div>", unsafe_allow_html=True)
    
    has_mala = st.session_state.unlocked_mala
    if has_mala:
        g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    else:
        g_col1, g_col2, g_col3 = st.columns(3)
        
    with g_col1:
        if st.button(t["game_release"], use_container_width=True): st.session_state.active_game = "Release"; st.rerun()
    with g_col2:
        if st.button(t["game_bloom"], use_container_width=True): st.session_state.active_game = "Bloom"; st.rerun()
    with g_col3:
        if st.button(t["game_convergence"], use_container_width=True): st.session_state.active_game = "Convergence"; st.rerun()
    if has_mala:
        with g_col4:
            if st.button(t["game_mala"], use_container_width=True): st.session_state.active_game = "Mala"; st.rerun()

    if st.session_state.active_game == "Release":
        st.markdown(f"<p style='font-size: 12px; opacity: 0.6; margin-bottom: 20px; color:{app_text}; font-weight: 300;'>{t['release_desc']}</p>", unsafe_allow_html=True)
        components.html(theme_it(release_game_html.replace("gameCanvas", "game_focus_release")), height=370)

    elif st.session_state.active_game == "Bloom":
        st.markdown(f"<p style='font-size: 12px; opacity: 0.6; margin-bottom: 20px; color:{app_text}; font-weight: 300;'>{t['bloom_desc']}</p>", unsafe_allow_html=True)
        components.html(theme_it(bloom_html.replace("bloomCanvas", "game_focus_bloom")), height=370)

    elif st.session_state.active_game == "Convergence":
        st.markdown(f"<p style='font-size: 12px; opacity: 0.6; margin-bottom: 20px; color:{app_text}; font-weight: 300;'>{t['convergence_desc']}</p>", unsafe_allow_html=True)
        components.html(theme_it(convergence_html.replace("[CANVAS_ID]", "game_convergence")), height=370)
    
    elif st.session_state.active_game == "Mala":
        st.markdown(f"<p style='font-size: 12px; opacity: 0.6; margin-bottom: 20px; color:{app_text}; font-weight: 300;'>Tap to drop the bead. Feel the rhythm.</p>", unsafe_allow_html=True)
        components.html(theme_it(mala_html), height=370)

    st.markdown(get_bottom_quote(), unsafe_allow_html=True)

elif st.session_state.current_page == "Market":
    st.markdown(f"<div class='section-header'>{t['h_market']}</div>", unsafe_allow_html=True)
    
    products = [
        {"name": "Laughing Buddha", "file": "laughingbuddha.png", "price": "899"},
        {"name": "Focus Beads", "file": "beads.png", "price": "799"},
        {"name": "Buddha Sculpture", "file": "buddha.png", "price": "1,499"},
        {"name": "Thumb Stone", "file": "thumbstone.png", "price": "499"},
        {"name": "Wish Candle", "file": "wishcandle.png", "price": "799"},
        {"name": "Grounding Stones", "file": "stones.png", "price": "899"},
        {"name": "Starter Ritual", "file": "ritual.png", "price": "2,499"},
        {"name": "Master Sanctuary", "file": "sanctuary.png", "price": "4,999"}
    ]

    products_html = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">'
    for p in products:
        img_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@main/{p['file']}"
        wa_text = urllib.parse.quote(f"I am interested in the {p['name']}")
        wa_link = f"https://wa.me/{MY_PHONE}?text={wa_text}"
        
        products_html += f"""<div style="background: {glass_bg}; backdrop-filter: blur(12px); border: 1px solid {btn_border}; border-radius: 16px; padding: 15px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease;">
<div style="width: 100%; aspect-ratio: 1/1; background-image: url('{img_url}'); background-size: cover; background-position: center; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba({c_rgb}, 0.2);"></div>
<div style="color: {app_text}; font-size: 13px; font-weight: 300; letter-spacing: 1px; margin-bottom: 5px; min-height: 35px; display: flex; align-items: center; justify-content: center; line-height: 1.4;">{p['name']}</div>
<div style="color: {c_accent}; font-weight: 500; font-size: 16px; margin-bottom: 2px;">₹{p['price']}</div>
<div style="color: {app_text}; opacity: 0.4; font-size: 9px; margin-bottom: 15px; letter-spacing: 2px; font-weight: 500;">{t['free_shipping']}</div>
<a href="{wa_link}" target="_blank" style="text-decoration: none; width: 100%;">
<div style="background: rgba({c_rgb}, 0.1); border: 1px solid rgba({c_rgb}, 0.3); color: {app_text}; padding: 12px 0; border-radius: 30px; font-size: 10px; font-weight: 400; text-transform: uppercase; letter-spacing: 1px; width: 100%; cursor: pointer; transition: all 0.3s ease;">{t['order_wa']}</div>
</a>
</div>"""
        
    products_html += '</div>'
    st.markdown(products_html, unsafe_allow_html=True)

# 🚨 THE FULL LEGAL DISCLAIMER PAGE 🚨
elif st.session_state.current_page == "Disclaimer":
    st.markdown("<div class='section-header'>LEGAL DISCLAIMER & TERMS</div>", unsafe_allow_html=True)
    
    if st.button("← Return to Space", use_container_width=True):
        st.session_state.current_page = "Journal"
        st.rerun()
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    disclaimer_full_html = f"""
    <div class='market-slab' style='text-align:left; font-size:12px; font-weight:300; color: {app_text}; line-height:1.8; padding: 25px;'>
        <strong style="font-weight: 500; font-size: 14px; letter-spacing: 1px; color: {c_accent};">SUKOON — LEGAL DISCLAIMER & TERMS OF USE (WELLBEING PLATFORM)</strong><br>
        <i style="opacity: 0.5; font-size: 10px;">Last updated: March 2026</i><br><br>
        
        <strong style="color: {c_accent};">1. PURPOSE OF THE APPLICATION</strong><br>
        SUKOON is a general wellbeing and reflection platform designed to offer calm spaces, neutral prompts, and optional self-guided tools intended for relaxation, reflection, and personal awareness.<br>
        The application is not designed, intended, or represented as a medical, psychological, psychiatric, therapeutic, counseling, diagnostic, or treatment service of any kind.<br><br>
        
        <strong style="color: {c_accent};">2. NO MEDICAL OR PROFESSIONAL ADVICE</strong><br>
        SUKOON does not provide:<br>
        • medical advice<br>
        • mental health diagnosis<br>
        • psychological counseling<br>
        • therapy<br>
        • treatment plans<br>
        • crisis intervention<br>
        • professional guidance of any kind<br><br>
        All content provided through the app — including text, audio, prompts, reflections, exercises, and AI-generated responses — is offered for general wellbeing and informational purposes only.<br>
        Nothing within the app should be interpreted as a substitute for professional medical, psychological, psychiatric, legal, or other qualified services.<br><br>
        
        <strong style="color: {c_accent};">3. USER RESPONSIBILITY & AUTONOMY</strong><br>
        Use of SUKOON is entirely voluntary.<br>
        Users remain fully responsible for:<br>
        • their interpretations of content<br>
        • their decisions, actions, and behaviors<br>
        • seeking appropriate professional help when needed<br><br>
        The app does not direct, instruct, compel, or advise users to take or avoid any specific action in their personal, medical, emotional, professional, or legal lives.<br>
        Users may discontinue use at any time without consequence.<br><br>
        
        <strong style="color: #ff4b4b;">4. NOT FOR EMERGENCIES OR CRISIS SITUATIONS</strong><br>
        SUKOON is not suitable for emergencies.<br>
        If you are experiencing:<br>
        • thoughts of self-harm or harm to others<br>
        • severe emotional distress<br>
        • a mental health crisis<br>
        • medical emergencies<br><br>
        You should immediately contact:<br>
        • local emergency services<br>
        • a qualified healthcare provider<br>
        • a licensed mental health professional<br>
        • a trusted emergency helpline in your region<br><br>
        The app does not monitor, detect, respond to, or intervene in crisis situations.<br><br>
        
        <strong style="color: {c_accent};">5. AI-GENERATED CONTENT DISCLOSURE</strong><br>
        Some responses and reflections within SUKOON may be generated or assisted by automated systems or artificial intelligence.<br>
        Such content:<br>
        • is non-sentient<br>
        • does not understand users personally<br>
        • does not possess awareness, empathy, or intent<br>
        • does not form relationships or attachments<br><br>
        AI-generated content is non-authoritative and should not be relied upon as factual, professional, or personalized advice.<br><br>
        
        <strong style="color: {c_accent};">6. NO GUARANTEES OR OUTCOMES</strong><br>
        SUKOON makes no guarantees, representations, or promises regarding:<br>
        • emotional improvement<br>
        • mental clarity<br>
        • stress reduction<br>
        • healing<br>
        • recovery<br>
        • personal growth<br>
        • outcomes of any kind<br><br>
        Individual experiences vary. Use of the app may or may not produce perceived benefits.<br><br>
        
        <strong style="color: {c_accent};">7. HABITUAL USE & DEPENDENCE DISCLAIMER</strong><br>
        Regular or repeated use of SUKOON does not imply reliance or dependency, and the app does not encourage compulsive use.<br>
        The platform:<br>
        • does not use streaks, pressure mechanisms, or dependency-driven engagement<br>
        • does not claim necessity for wellbeing<br>
        • encourages balance with real-world activities<br><br>
        Users are encouraged to maintain healthy routines and seek offline support as appropriate.<br><br>
        
        <strong style="color: {c_accent};">8. DATA INPUT & USER CONTENT</strong><br>
        Any text, voice input, or other content voluntarily provided by users is used solely to generate general reflective or neutral responses, not for diagnosis, evaluation, or profiling.<br>
        Users should avoid sharing sensitive personal, medical, or identifying information.<br><br>
        
        <strong style="color: {c_accent};">9. LIMITATION OF LIABILITY</strong><br>
        To the maximum extent permitted by law:<br>
        SUKOON, its founders, developers, operators, affiliates, licensors, and partners shall not be liable for any direct, indirect, incidental, consequential, emotional, psychological, medical, or other damages arising from:<br>
        • use or inability to use the app<br>
        • reliance on any content<br>
        • interpretation of responses<br>
        • habitual use<br>
        • discontinuation of use<br><br>
        Use of the app is at the user’s sole discretion and risk.<br><br>
        
        <strong style="color: {c_accent};">10. NO PROFESSIONAL RELATIONSHIP</strong><br>
        Use of SUKOON does not create:<br>
        • a doctor-patient relationship<br>
        • therapist-client relationship<br>
        • counselor-client relationship<br>
        • fiduciary or professional relationship<br><br>
        No such relationship is implied or established at any time.<br><br>
        
        <strong style="color: {c_accent};">11. CHANGES & UPDATES</strong><br>
        This disclaimer may be updated periodically. Continued use of the app after changes constitutes acceptance of the revised terms.<br><br>
        
        <strong style="color: {c_accent};">12. JURISDICTION & COMPLIANCE</strong><br>
        SUKOON operates as a general wellbeing platform and complies with applicable consumer, digital, and platform policies. It is not regulated as a medical or therapeutic service.<br><br>
        
        <div style="height: 1px; width: 100%; background: {btn_border}; margin: 30px 0;"></div>
        
        <strong style="font-weight: 500; font-size: 13px; color: {c_accent}; text-align: center; display: block; margin-bottom: 15px;">FINAL LEGAL POSITION (PLAIN LANGUAGE SUMMARY)</strong>
        <div style="text-align: center; font-style: italic; opacity: 0.8;">
            SUKOON:<br>
            listens, but does not diagnose<br>
            reflects, but does not advise<br>
            offers space, not treatment<br>
            allows habit, but discourages dependence<br>
            supports calm, not crisis care
        </div>
    </div>
    """
    components.html(theme_it(disclaimer_full_html), height=600, scrolling=True)


elif st.session_state.current_page == "Settings":
    st.markdown(f"<div class='section-header'>{t['h_lang']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 20px;'>", unsafe_allow_html=True)
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        if st.button("English", use_container_width=True): st.session_state.ui_language = "English"; st.rerun()
    with l_col2:
        if st.button("हिंदी (Hindi)", use_container_width=True): st.session_state.ui_language = "Hindi"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 🚨 THE 14-THEME GRID 🚨
    st.markdown(f"<div class='section-header'>{t['h_theme']}</div>", unsafe_allow_html=True)
    
    # 1. Light Themes Row (6 Themes)
    st.markdown(f"<div class='theme-group-header'>{t['th_light']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 15px 20px 5px 20px;'>", unsafe_allow_html=True)
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        if st.button(t["t_dawn"], use_container_width=True): st.session_state.theme = "First Light"; st.rerun()
        if st.button(t["t_terra"], use_container_width=True): st.session_state.theme = "Terracotta Earth"; st.rerun()
        if st.button(t["t_champagne"], use_container_width=True): st.session_state.theme = "Champagne Gold"; st.rerun()
    with l_col2:
        if st.button(t["t_sea"], use_container_width=True): st.session_state.theme = "Sea Glass"; st.rerun()
        if st.button(t["t_sage_l"], use_container_width=True): st.session_state.theme = "Sage Sanctuary"; st.rerun()
        if st.button(t["t_pink_champ"], use_container_width=True): st.session_state.theme = "Pink Champagne"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Deep Themes Row (8 Themes)
    st.markdown(f"<div class='theme-group-header'>{t['th_dark']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 15px 20px 5px 20px;'>", unsafe_allow_html=True)
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button(t["t_void"], use_container_width=True): st.session_state.theme = "The Void"; st.rerun()
        if st.button(t["t_sage_d"], use_container_width=True): st.session_state.theme = "Deep Sage"; st.rerun()
        if st.button(t["t_ogreen"], use_container_width=True): st.session_state.theme = "Ocean Green"; st.rerun()
        if st.button(t["t_maroon"], use_container_width=True): st.session_state.theme = "Maroon"; st.rerun()
    with d_col2:
        if st.button(t["t_abyss"], use_container_width=True): st.session_state.theme = "Social Blue"; st.rerun()
        if st.button(t["t_oblue"], use_container_width=True): st.session_state.theme = "Ocean Blue"; st.rerun()
        if st.button(t["t_amber"], use_container_width=True): st.session_state.theme = "Red Amber"; st.rerun()
        if st.button(t["t_tblue"], use_container_width=True): st.session_state.theme = "Twilight Blue"; st.rerun()
    
    # Secret 15th Theme
    if st.session_state.unlocked_nirvana:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button(t["t_gold"], use_container_width=True): st.session_state.theme = "Liquid Gold"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 🚨 THE PHYGITAL VAULT 🚨
    st.markdown(f"<div class='section-header'>{t['vault_h']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='market-slab' style='padding: 20px;'>", unsafe_allow_html=True)
    
    code_input = st.text_input("Enter Sanctuary Code", value="", key="vault_input", label_visibility="collapsed", placeholder=t['vault_p'])
    
    if code_input:
        code = code_input.strip().upper()
        if code == "MANTRA" and not st.session_state.unlocked_mala:
            st.session_state.unlocked_mala = True
            st.success("✨ The Haptic Mala unlocked in Focus.")
            st.rerun()
        elif code == "EMBER" and not st.session_state.unlocked_flame:
            st.session_state.unlocked_flame = True
            st.success("🔥 The Eternal Flame unlocked in Breath Studio.")
            st.rerun()
        elif code == "NIRVANA" and not st.session_state.unlocked_nirvana:
            st.session_state.unlocked_nirvana = True
            st.session_state.theme = "Liquid Gold"
            st.success("👑 Master Sanctuary unlocked. Zenith Mode activated.")
            st.rerun()
        elif code in ["MANTRA", "EMBER", "NIRVANA"]:
            st.info("Code already unlocked.")
        else:
            st.error("Code not recognized in the Ether.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # --- MOVED INFO CONTENT ---
    st.markdown("<div class='section-header'>THE FOUNDER'S MANIFESTO</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab' style='text-align:left; font-size:13px; font-weight:300; color: {app_text}; line-height:1.8; font-style: italic; border-left: 3px solid {c_accent};'>
        "I built Sukoon not as a clinical treatment, but as a living digital sanctuary to give your overwhelmed mind immediate shelter from a loud world. There are no forced logins to track your identity, no targeted ads to break the immersion, and no paywalls to block your peace. This app will never buzz your phone to demand your attention or guilt you over a broken daily streak. It is simply a quiet canvas that sits patiently in your pocket, ready to help you wash away the noise the exact moment you need it."
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>INSTALL SUKOON</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='market-slab' style='text-align:left; font-size:13px; font-weight:300; color: {app_text}; line-height:1.8;'>
        <b>1.</b> Open this link in Safari (iPhone) or Chrome (Android).<br><br>
        <b>2.</b> Tap the Share or Menu (⋮) icon.<br><br>
        <b>3.</b> Select 'Add to Home Screen'.<br><br>
        <b>4.</b> Open Sukoon directly from your home screen.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>FREQUENTLY ASKED</div>", unsafe_allow_html=True)
    faqs = [
        ("Is the Space free?", "Yes, the Digital Sanctuary is currently fully open and free for all early users."),
        ("What is the 4-2-6 Rhythm?", "It is a breathing pacing technique designed to help you slow down and find stillness."),
        ("Is this therapy?", "No. Sukoon is purely a lifestyle companion for personal reflection. It is not therapy or psychology."),
        ("Are the objects religious?", "No. They are entirely secular, tactile tools intended only for physical grounding and focus.")
    ]
    for q, a in faqs:
        st.markdown(f"<div style='font-weight: 500; font-size: 13px; color: {c_accent}; margin-top: 15px; text-align: left;'>{q}</div><div style='font-size: 13px; font-weight: 300; opacity: 0.7; margin-bottom: 10px; text-align: left; border-bottom: 1px solid {btn_border}; padding-bottom: 15px; color: {app_text}; line-height:1.6;'>{a}</div>", unsafe_allow_html=True)


# 🚨 THE GLOBAL FOOTER DISCLAIMER BUTTON 🚨
if st.session_state.current_page != "Disclaimer" and st.session_state.has_completed_ritual:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    if st.button("Read Full Legal Disclaimer", use_container_width=True):
        st.session_state.current_page = "Disclaimer"
        st.rerun()

if st.session_state.has_completed_ritual:
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10px; font-weight:300; letter-spacing:1px; opacity:0.3; color:{app_text};'>Sukoon Sanctuary v157.34</div>", unsafe_allow_html=True)

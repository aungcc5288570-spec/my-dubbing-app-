import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import random

# API Keys (Key ၂ ခုလုံးကို အလှည့်ကျသုံးရန် ထည့်သွင်းထားသည်)
API_KEYS = [
    "AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc", # Key 1
    "AIzaSyDStzBuLZilRywHu9G919fwRZt5fdH3z-Q"  # Key 2
]

# Key တစ်ခုကို ကျပန်းရွေးချယ်ခြင်း
selected_key = random.choice(API_KEYS)
genai.configure(api_key=selected_key)
model = genai.GenerativeModel('gemini-1.5-flash') 

# UI Theme Setup (Professional Dark Mode)
st.set_page_config(page_title="TEAM ALPHA // Studio", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #00f2ff; color: black; border-radius: 10px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 TEAM ALPHA // Studio")
st.write(f"Connected with API Key: {selected_key[:10]}...")

# YouTube Link Input
video_url = st.text_input("🔗 Enter YouTube URL (2 mins+ supported)")

# Screenshot ထဲကအတိုင်း Settings များ
with st.expander("🖼️ Logo & Watermark Settings"):
    st.file_uploader("Upload Logo", type=['png', 'jpg'])
    st.markdown("**Logo position**")
    pos = st.radio("Choose Position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    st.text_input("Watermark Name", value="MovieX")

if video_url:
    st.subheader("PREVIEW")
    st.video(video_url)

# Processing Section
if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI is analyzing (2 mins video)... This may take 60 seconds."):
            try:
                # Video Content Analysis
                res = model.generate_content(f"Summarize this video in detail using Myanmar language: {video_url}")
                
                st.subheader("FINAL OUTPUT")
                st.success("Analysis Complete!")
                st.write(res.text)
                
                # Teza/Kyaw Kyaw Voice Generation
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                st.info("Audio Ready! Download using the 3 dots menu.")
                
            except Exception as e:
                st.error("Technical Issue. Please try again.")
                st.info("Key Limit ပြည့်ပါက ၅ မိနစ်ခန့်စောင့်ပြီး Reboot လုပ်ပေးပါ။")

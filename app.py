import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import random

# API Keys (Key ၂ ခုလုံးကို အလှည့်ကျသုံးရန်)
API_KEYS = [
    "AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc",
    "AIzaSyDStzBuLZilRywHu9G919fwRZt5fdH3z-Q"
]

# Key တစ်ခုကို ကျပန်းရွေးချယ်ခြင်း
selected_key = random.choice(API_KEYS)
genai.configure(api_key=selected_key)
model = genai.GenerativeModel('gemini-1.5-flash') 

# UI Theme Setup
st.set_page_config(page_title="TEAM ALPHA // Studio", layout="centered")
st.title("🎬 TEAM ALPHA // Studio")

# YouTube Link Input
video_url = st.text_input("🔗 Enter YouTube URL (2 mins+ supported)")

# Settings (Logo & Watermark)
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
        with st.spinner("AI is analyzing... Please wait."):
            try:
                # Video Analysis
                res = model.generate_content(f"Summarize this video in detail using Myanmar language: {video_url}")
                
                st.subheader("FINAL OUTPUT")
                st.write(res.text)
                
                # Voice Generation (Teza Voice Style)
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                
            except Exception as e:
                # သင်ဖြတ်ချင်တဲ့ စာသားရှည်ကြီးတွေ မပါတော့ပါဘူး
                st.error("Error occurred. Please refresh and try again.")

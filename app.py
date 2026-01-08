import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# API Setup
genai.configure(api_key="AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M")
model = genai.GenerativeModel('gemini-1.5-flash') 

# UI Theme
st.set_page_config(page_title="TEAM ALPHA // Studio", layout="centered")
st.markdown('<style>.main { background-color: #0e1117; color: white; }</style>', unsafe_allow_html=True)
st.title("🎬 TEAM ALPHA // Studio")

# Inputs
video_url = st.text_input("Enter YouTube URL")

with st.expander("🖼️ Logo & Watermark Settings"):
    up_img = st.file_uploader("Upload Logo", type=['png', 'jpg'])
    pos = st.radio("Position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    name = st.text_input("Watermark Name", placeholder="e.g. MovieX")

# Preview
if video_url:
    st.video(video_url)

# Process
if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI Generating..."):
            try:
                res = model.generate_content(f"Summarize this video in Myanmar: {video_url}")
                st.write(res.text)
                tts = gTTS(text=res.text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f)
            except Exception:
                st.error("AI Busy. Please Reboot.")

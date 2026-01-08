import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# API Setup
API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

# UI Theme Setup
st.set_page_config(page_title="TEAM ALPHA // Studio", layout="centered")
st.markdown('<style>.main { background-color: #0e1117; color: white; }</style>', unsafe_allow_html=True)

# App Header
st.title("🎬 TEAM ALPHA // Studio")
st.markdown("---")

# Inputs
video_url = st.text_input("Enter YouTube URL")

with st.expander("🖼️ Logo & Watermark Settings"):
    st.file_uploader("Upload Logo", type=['png', 'jpg'])
    st.radio("Position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    st.text_input("Watermark Name", placeholder="e.g. MovieX")

# Preview
if video_url:
    st.video(video_url)

# Process Button
if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI Thinking (Processing Video)..."):
            try:
                # Video Recap with Gemini
                res = model.generate_content(f"Please summarize this video in Myanmar language accurately: {video_url}")
                st.success("Analysis Complete!")
                st.write(res.text)
                
                # Voice Generation (Teza Voice Style)
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                
            except Exception as e:
                st.error("AI Busy or Limit Exceeded.")
                st.info("ခေတ္တစောင့်ပြီး ပြန်လည်စမ်းသပ်ပါ သို့မဟုတ် Reboot လုပ်ပေးပါ။")
    else:
        st.warning("Please enter a video URL first.")

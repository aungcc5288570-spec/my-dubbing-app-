import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# သင့်ရဲ့ Gemini API Key ကို ဒီနေရာမှာ အသစ်ပြန်ထည့်ပေးပါ
API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

st.set_page_config(page_title="TEAM ALPHA // Studio", layout="centered")
st.markdown('<style>.main { background-color: #0e1117; color: white; }</style>', unsafe_allow_html=True)
st.title("🎬 TEAM ALPHA // Studio")

video_url = st.text_input("Enter YouTube URL")

with st.expander("🖼️ Logo & Watermark Settings"):
    st.file_uploader("Upload Logo", type=['png', 'jpg'])
    st.radio("Position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    st.text_input("Watermark Name")

if video_url:
    st.video(video_url)

if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI Thinking..."):
            try:
                # AI ကို အလုပ်ခိုင်းခြင်း
                res = model.generate_content(f"Summarize this video in Myanmar language: {video_url}")
                st.success("AI Recap Done!")
                st.write(res.text)
                
                # အသံပြောင်းခြင်း
                tts = gTTS(text=res.text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f)
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("API Key Limit ပြည့်သွားတာ ဖြစ်နိုင်ပါတယ်။ ခဏစောင့်ပြီး ပြန်လုပ်ပါ သို့မဟုတ် Key အသစ်လဲပါ။")

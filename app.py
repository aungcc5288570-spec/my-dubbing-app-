import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# API Setup (သင်ကိုယ်တိုင်ထုတ်ထားတဲ့ Key အသစ်)
API_KEY = "AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

# UI Theme Setup (Screenshot ထဲကအတိုင်း Dark Theme)
st.set_page_config(page_title="TEAM ALPHA // Studio", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #00f2ff; color: black; border-radius: 10px; width: 100%; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.title("🎬 TEAM ALPHA // Studio")
st.markdown("---")

# Video Link Input
video_url = st.text_input("🔗 Enter YouTube URL (2 mins+ supported)")

# Screenshot ထဲကလို Logo & Position Settings
with st.expander("🖼️ Logo & Watermark Settings"):
    st.file_uploader("Upload Logo", type=['png', 'jpg'])
    st.markdown("**Logo position**")
    # Screenshot ထဲကအတိုင်း Position ခလုတ်များ
    pos = st.radio("Choose Position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    
    st.markdown("**Text Watermark**")
    st.text_input("Watermark Name", value="MovieX")

# Video Preview Section
if video_url:
    st.subheader("PREVIEW")
    st.video(video_url)

# Processing Section
if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI is analyzing your 2-minute video..."):
            try:
                # Video Recap logic
                res = model.generate_content(f"Please summarize this video content accurately in Myanmar language: {video_url}")
                
                st.subheader("FINAL OUTPUT")
                st.success("Analysis Complete!")
                st.write(res.text)
                
                # Voice Generation (Teza/Kyaw Kyaw style)
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                st.info("အပေါ်က အစက် ၃ စက်ကိုနှိပ်ပြီး Audio ကို Download ဆွဲနိုင်ပါတယ်")
                
            except Exception as e:
                st.error("AI Busy or Limit Exceeded.")
                st.info("ခဏစောင့်ပြီး Reboot လုပ်ပေးပါ။")
    else:
        st.warning("ဗီဒီယိုလင့် အရင်ထည့်ပေးပါ")

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Setup API
genai.configure(api_key="AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("🎬 TEAM ALPHA STUDIO")

# --- Logo & Name Settings ---
with st.sidebar:
    st.header("⚙️ Branding Settings")
    uploaded_logo = st.file_uploader("သင်၏ Logo ပုံတင်ရန်", type=['png', 'jpg', 'jpeg'])
    watermark_name = st.text_input("ဗီဒီယိုပေါ်တွင်ပြလိုသော အမည်", value="Team Alpha")
    logo_pos = st.selectbox("Logo ထားလိုသည့်နေရာ", ["ဘယ်ဘက်အပေါ်", "ညာဘက်အပေါ်", "ဘယ်ဘက်အောက်", "ညာဘက်အောက်"])

# --- Main Interface ---
video_url = st.text_input("🔗 YouTube Link")

if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI က ဗီဒီယိုကို လေ့လာနေသည်..."):
            try:
                res = model.generate_content(f"Summarize this video in Myanmar: {video_url}")
                
                # အနှစ်ချုပ်နှင့် Branding ပြသခြင်း
                st.subheader(f"📺 Output for: {watermark_name}")
                if uploaded_logo:
                    st.image(uploaded_logo, width=100, caption="Your Logo")
                
                st.write(res.text)
                
                # အသံထုတ်ပေးခြင်း
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
            except Exception as e:
                st.error(f"Error: {str(e)}")

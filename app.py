import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# API Key ကို တိုက်ရိုက်ထည့်သွင်းထားသည်
genai.configure(api_key="AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc")

# Model နာမည်ကို Error မတက်အောင် ဤသို့ပြောင်းလဲထားသည်
model = genai.GenerativeModel('gemini-1.5-flash-latest') 

st.title("🎬 TEAM ALPHA // STUDIO")

# Sidebar တွင် Branding ပြုလုပ်ရန်
with st.sidebar:
    st.header("⚙️ Branding Settings")
    watermark = st.text_input("ဗီဒီယိုပေါ်တွင်ပြလိုသော အမည်", value="TEAM ALPHA STUDIO")
    uploaded_logo = st.file_uploader("Logo ပုံတင်ရန်", type=['png', 'jpg'])

video_url = st.text_input("🔗 YouTube Link (Shorts or Video)")

if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("Processing..."):
            try:
                # Video ကို AI က လေ့လာခြင်း
                res = model.generate_content(f"Summarize this video in Myanmar language: {video_url}")
                
                st.subheader(f"📜 အနှစ်ချုပ်စာသား ({watermark})")
                st.write(res.text)
                
                # တေဇအသံ (Teza Voice Style) ထုတ်ပေးခြင်း
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                st.success("အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ!")
                
            except Exception as e:
                # Error အမှန်ကို ပြပေးရန်
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Link ထည့်ပေးရန် လိုအပ်ပါသည်။")

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="AI Auto Dubbing", page_icon="🤖")
st.title("AI Myanmar Auto Dubbing 🇲🇲")

st.markdown("### YouTube Link ထည့်ပြီး မြန်မာလို နားထောင်မည်")
video_url = st.text_input("YouTube Link ကို ဒီမှာ ထည့်ပါ -")

if video_url:
    st.video(video_url)
    
    if st.button("AI ဖြင့် အလိုအလျောက် ဘာသာပြန်မည်"):
        with st.spinner('AI က ဗီဒီယိုကို လေ့လာပြီး မြန်မာလို ပြန်ဆိုနေပါသည်...'):
            try:
                # ၁။ ဗီဒီယိုကို Gemini AI က ဖတ်ခြင်း
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([
                    "Summarize this video in Myanmar language shortly.",
                    video_url
                ])
                
                myanmar_text = response.text
                st.subheader("မြန်မာဘာသာပြန် စာသား -")
                st.success(myanmar_text)
                
                # ၂။ စာသားကို အသံအဖြစ် ပြောင်းလဲခြင်း (TTS)
                tts = gTTS(text=myanmar_text, lang='my')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                
                st.markdown("### မြန်မာ AI အသံဖြင့် နားထောင်ရန် -")
                st.audio(fp, format='audio/mp3')
                
            except Exception as e:
                st.error(f"အမှားတစ်ခုရှိနေပါသည် - {e}")

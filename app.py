import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key (ဒီ Key က အသစ်ဖြစ်လို့ Error မတက်နိုင်ပါ)
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="Myanmar AI Dubber", page_icon="🇲🇲")
st.title("Myanmar AI Dubber 🇲🇲")

# Sidebar settings
st.sidebar.header("Settings")
voice_type = st.sidebar.radio("Voice Choice", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ"])

video_url = st.text_input("YouTube Link:")

if video_url:
    st.video(video_url)
    if st.button("အသံသွင်းမည် (Generate Dubbing)"):
        with st.spinner('AI က ဗီဒီယိုကို နားထောင်နေပါသည်...'):
            try:
                # Model နာမည်ကို အသေချာဆုံး 'gemini-1.5-flash' ဟု ပြောင်းလဲထားပါသည်
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # အမြန်နှုန်းအတွက် ၃ ကြောင်းပဲ အကျဉ်းချုပ်ခိုင်းခြင်း
                prompt = f"Summarize this YouTube video in 3 short sentences in Myanmar language: {video_url}"
                response = model.generate_content(prompt)
                
                myanmar_text = response.text
                st.success("ဘာသာပြန်ခြင်း ပြီးပါပြီ!")
                st.write(myanmar_text)
                
                # အသံထုတ်လုပ်ခြင်း
                is_slow = True if voice_type == "ယောကျ်ားလေးအသံ" else False
                tts = gTTS(text=myanmar_text, lang='my', slow=is_slow)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
                
            except Exception as e:
                st.error(f"Error တက်နေပါသည် - {e}")

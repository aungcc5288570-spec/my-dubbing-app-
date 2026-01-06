import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="Myanmar AI Dubber", page_icon="🇲🇲")
st.title("Myanmar AI Dubber 🇲🇲")

# Sidebar settings
st.sidebar.header("Settings")
voice_type = st.sidebar.radio("အသံရွေးချယ်ရန်", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ"])

video_url = st.text_input("YouTube Link:")

if video_url:
    st.video(video_url)
    if st.button("အသံသွင်းမည် (Generate Dubbing)"):
        with st.spinner('AI က ဗီဒီယိုကို လေ့လာနေပါသည်...'):
            try:
                # 404 Error မတက်စေရန် gemini-1.5-flash-latest ကို တိုက်ရိုက်ခေါ်သုံးပါသည်
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # အမြန်ဆုံး အကျဉ်းချုပ်ခိုင်းခြင်း
                prompt = f"Summarize this YouTube video content in 3 short sentences in Myanmar language. URL: {video_url}"
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
                # အကယ်၍ Error ထပ်တက်ပါက အရန် Model ဖြင့် ထပ်မံကြိုးစားခြင်း
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.error(f"Error အသေးစိတ်: {e}")

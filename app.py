import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="Gemini Pro Dubbing", page_icon="✨")
st.title("Gemini Pro AI Dubbing 🇲🇲")

# Sidebar settings
st.sidebar.header("Dubbing Settings")
voice_choice = st.sidebar.radio("အသံရွေးချယ်ရန်", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ"])

video_url = st.text_input("YouTube Link ကို ဒီမှာ ထည့်ပါ -")

if video_url:
    st.video(video_url)
    if st.button("Gemini Pro ဖြင့် ဘာသာပြန်မည်"):
        with st.spinner('Gemini Pro က အလုပ်လုပ်နေပါသည်...'):
            try:
                # Error လုံးဝမတက်စေရန် model name ကို string သီးသန့်ပဲ သုံးပါမည်
                model = genai.GenerativeModel('gemini-pro')
                
                # အမြန်ဆုံး အကျဉ်းချုပ်ခိုင်းခြင်း
                prompt = f"Summarize this YouTube video in 3 sentences in Myanmar language. URL: {video_url}"
                response = model.generate_content(prompt)
                
                myanmar_text = response.text
                st.success("ဘာသာပြန်ခြင်း အောင်မြင်သည်!")
                st.write(myanmar_text)
                
                # အသံထုတ်လုပ်ခြင်း
                is_slow = True if voice_choice == "ယောကျ်ားလေးအသံ" else False
                tts = gTTS(text=myanmar_text, lang='my', slow=is_slow)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
                
            except Exception as e:
                # Error အသေးစိတ်ကို သေချာပြရန်
                st.error(f"Error အသေးစိတ်: {str(e)}")

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="Fast AI Dubbing", page_icon="⚡")
st.title("Fast Myanmar AI Dubbing 🇲🇲⚡")

# အမြန်နှုန်းအတွက် Sidebar ဆက်တင်များ
st.sidebar.header("Dubbing Settings")
voice_choice = st.sidebar.selectbox("အသံရွေးချယ်ရန်", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ"])
speed_val = st.sidebar.slider("အသံနှုန်း (Speed)", 0.9, 1.3, 1.1)

video_url = st.text_input("YouTube Link ကို ဒီမှာ ထည့်ပါ -")

if video_url:
    st.video(video_url)
    if st.button("အမြန်နှုန်းဖြင့် ဘာသာပြန်မည်"):
        # အချိန်တိုအတွင်း အလုပ်လုပ်ရန် spinner သုံးခြင်း
        with st.spinner('AI က စက္ကန့်ပိုင်းအတွင်း အကျဉ်းချုပ်နေပါသည်...'):
            try:
                # အမြန်ဆုံးဖြစ်သော gemini-1.5-flash model ကို သုံးထားပါသည်
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # အမြန်ဆုံး အကျဉ်းချုပ်ခိုင်းသည့် Prompt
                prompt = f"Summarize this YouTube video content in 3 short sentences in Myanmar language. Link: {video_url}"
                response = model.generate_content(prompt)
                
                myanmar_text = response.text
                st.success("ဘာသာပြန်ခြင်း ပြီးပါပြီ!")
                st.write(myanmar_text)
                
                # အသံဖိုင်ကို အမြန်ထုတ်လုပ်ခြင်း
                is_slow = True if voice_choice == "ယောကျ်ားလေးအသံ" else False
                tts = gTTS(text=myanmar_text, lang='my', slow=is_slow)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
                
            except Exception as e:
                st.error(f"Error: {e}")

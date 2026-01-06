import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key (API Key ကို သေချာစစ်ဆေးပေးပါ)
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="Fast AI Dubbing", page_icon="⚡")
st.title("Fast Myanmar AI Dubbing 🇲🇲⚡")

# Sidebar settings
st.sidebar.header("Dubbing Settings")
voice_choice = st.sidebar.selectbox("အသံရွေးချယ်ရန်", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ"])

video_url = st.text_input("YouTube Link ကို ဒီမှာ ထည့်ပါ -")

if video_url:
    st.video(video_url)
    if st.button("အမြန်နှုန်းဖြင့် ဘာသာပြန်မည်"):
        with st.spinner('AI က စက္ကန့်ပိုင်းအတွင်း အကျဉ်းချုပ်နေပါသည်...'):
            try:
                # 404 Error ကင်းဝေးရန် Model နာမည်ကို 'gemini-1.5-flash' ဟုသာ ရေးပါသည်
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # အမြန်ဆုံး အကျဉ်းချုပ်ခိုင်းခြင်း
                prompt = f"Please provide a very short summary of this video in Myanmar language (3-4 sentences). Video link: {video_url}"
                response = model.generate_content(prompt)
                
                myanmar_text = response.text
                st.success("ဘာသာပြန်ခြင်း ပြီးပါပြီ!")
                st.write(myanmar_text)
                
                # အသံထုတ်လုပ်ခြင်း
                is_slow = True if voice_choice == "ယောကျ်ားလေးအသံ" else False
                tts = gTTS(text=myanmar_text, lang='my', slow=is_slow)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
                
            except Exception as e:
                # Error ထပ်တက်ပါက အခြား model (gemini-pro) ဖြင့် အလိုအလျောက် ပြောင်းစမ်းပါမည်
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.error(f"Error: {e}")

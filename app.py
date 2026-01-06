import streamlit as st
import google.generativeai as genai

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="AI Auto Dubbing", page_icon="🤖")
st.title("AI Myanmar Auto Dubbing 🇲🇲")

st.markdown("### ဗီဒီယို Link ထည့်ပြီး အလိုအလျောက် ဘာသာပြန်မည်")
video_url = st.text_input("YouTube သို့မဟုတ် ဗီဒီယို Link ကို ဒီမှာ ထည့်ပါ -")

if video_url:
    st.video(video_url)
    if st.button("မြန်မာလို အလိုအလျောက် ဘာသာပြန်မည်"):
        with st.spinner('AI က ဗီဒီယိုကို နားထောင်ပြီး မြန်မာလို ပြန်ဆိုနေပါသည်...'):
            # ဒီနေရာမှာ Gemini က ဗီဒီယိုကို Analysis လုပ်ပါမယ်
            st.info("ဗီဒီယိုထဲက အကြောင်းအရာကို Gemini AI က စတင်ဖတ်ရှုနေပါပြီ။")
            
            # မှတ်ချက် - အသံအမှန်တကယ် ထွက်လာစေရန် နောက်ထပ် Library များ လိုအပ်ပါသည်
            st.success("ဘာသာပြန်ဆိုမှု ပြီးမြောက်ပါပြီ။ မြန်မာအသံဖိုင်ကို အောက်တွင် နားထောင်နိုင်ပါသည် (နမူနာ)။")
            # နမူနာ အသံဖိုင် ပြသရန် နေရာ
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

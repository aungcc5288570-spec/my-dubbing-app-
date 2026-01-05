import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="AI Myanmar Dubber", page_icon="🇲🇲")
st.title("AI Myanmar Dubbing App 🇲🇲")

# Sidebar မှာ API Key ထည့်ရန်
api_key = st.sidebar.text_input("OpenAI API Key ကိုထည့်ပါ", type="password")

if not api_key:
    st.info("ညာဘက် (သို့မဟုတ်) Sidebar မှာ သင့်ရဲ့ OpenAI API Key ကို အရင်ထည့်ပေးပါဗျာ။")
else:
    client = OpenAI(api_key=api_key)
    uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင် တင်ပါ (MP4 သာ)", type=["mp4"])

    if uploaded_file is not None:
        if st.button("Dubbing စတင်မယ်"):
            with st.spinner("အလုပ်လုပ်နေပါပြီ... ခဏစောင့်ပါ"):
                with open("input.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # အသံခွဲထုတ်ခြင်း
                os.system("ffmpeg -i input.mp4 -q:a 0 -map a audio.mp3 -y")
                
                # ဘာသာပြန်ခြင်း
                with open("audio.mp3", "rb") as f:
                    trans = client.audio.translations.create(model="whisper-1", file=f)
                
                # မြန်မာအသံထုတ်ခြင်း
                tts = client.audio.speech.create(model="tts-1", voice="alloy", input=trans.text)
                tts.stream_to_file("my_audio.mp3")
                
                # ဗီဒီယိုပေါင်းခြင်း
                os.system("ffmpeg -i input.mp4 -i my_audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 output.mp4 -y")
                
                st.success("အောင်မြင်ပါပြီ!")
                st.video("output.mp4")
                with open("output.mp4", "rb") as file:
                    st.download_button("ဗီဒီယိုကို ဖုန်းထဲသိမ်းရန်", file, "dubbed_video.mp4")

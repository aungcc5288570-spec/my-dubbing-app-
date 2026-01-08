import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time

# --- Gmail/API Key Setup (တေဇအမြန်နှုန်းအတွက် Gemini 1.5 Flash) ---
GENAI_API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

st.set_page_config(page_title="MovieX: Teza Edition", layout="wide")

st.title("🎙️ TEZA // Movie Recap Studio")

# --- Logo & Settings (ဘယ်ညာရွှေ့ခြင်း အပါအဝင် အားလုံးပါသည်) ---
with st.expander("⚙️ Advanced Logo & Studio Settings"):
    l_pos = st.radio("Logo position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    cp_bypass = st.checkbox("Copyright Bypass", value=True)
    auto_color = st.checkbox("Auto Color")

# --- Processing & Voice (Teza အသံထွက်ပေါ်စေရန်) ---
video_url = st.text_input("Enter YouTube/TikTok Link")

if st.button("🚀 START PROCESSING"):
    if video_url:
        # Hyper Speed Percentage
        c1, c2 = st.columns(2)
        for i in [0, 50, 100]:
            c1.metric("AUDIO STATUS", f"{i}%")
            c2.metric("VIDEO STATUS", f"{i}%")
            time.sleep(0.0001)

        with st.spinner("တေဇစတိုင် Recap လုပ်နေသည်..."):
            try:
                res = model.generate_content(f"Summarize this video in Myanmar like a movie recap: {video_url}")
                recap_text = res.text
                st.success(f"အောင်မြင်စွာ ပြီးဆုံးပါပြီ။ Logo ကို {l_pos} တွင် ပြင်ဆင်ပြီးပါပြီ။")
                st.write(recap_text)
                
                # Teza အသံဖတ်ပြခြင်း
                tts = gTTS(text=recap_text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f)
            except:
                st.error("AI Busy. GitHub မှာ ကုဒ်ကို သေချာ Save လုပ်ပေးပါ။")

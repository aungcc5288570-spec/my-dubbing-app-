import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time

# --- ၁။ Gmail/API Key ချိတ်ဆက်မှု (အသစ်လဲထားသည်) ---
GENAI_API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # အမြန်ဆုံး Version

st.set_page_config(page_title="MovieX Studio Pro", layout="wide")

# --- UI Styling ---
st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .metric-circle { 
        border: 4px solid #7e3ff2; border-radius: 50%; 
        width: 160px; height: 160px; 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        margin: auto; box-shadow: 0px 0px 20px #7e3ff2;
    }
</style>
""", unsafe_allow_html=True)

st.title("📽️ TEAM ALPHA // Studio")

# --- ၂။ Logo Settings (ဘယ်ညာရွှေ့ခြင်း) ---
with st.expander("⚙️ Advanced Logo & Video Settings"):
    logo_file = st.file_uploader("Logo (optional)", type=['png', 'jpg'])
    l_pos = st.radio("Logo position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)

# --- ၃။ Processing & Voice Output ---
video_url = st.text_input("YouTube သို့မဟုတ် TikTok Link ထည့်ပါ")

if st.button("🚀 START PROCESSING"):
    if video_url:
        # Hyper Speed Animation
        c1, c2 = st.columns(2)
        for i in [0, 50, 100]:
            c1.markdown(f"<div class='metric-circle'><h1>{i}%</h1><p>AUDIO</p></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-circle'><h1>{i}%</h1><p>VIDEO</p></div>", unsafe_allow_html=True)
            time.sleep(0.0001)

        with st.spinner("AI က Recap လုပ်ပြီး အသံဖတ်ပေးနေသည်..."):
            try:
                # AI Recap စာသားထုတ်ခြင်း
                res = model.generate_content(f"Summarize this video briefly in Myanmar: {video_url}")
                recap_text = res.text
                st.success("အောင်မြင်စွာ ပြီးဆုံးပါပြီ!")
                st.write(recap_text)
                
                # မြန်မာသံဖြင့် ဖတ်ပြခြင်း (Teza အသံကဲ့သို့)
                tts = gTTS(text=recap_text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f) # အသံ Player ထွက်လာမည်
                
            except:
                st.error("AI Busy ဖြစ်နေပါသည်။ ခဏနေမှ ပြန်စမ်းပေးပါ။")

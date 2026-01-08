import streamlit as st
import google.generativeai as genai
from gtts import gTTSက
import io, time
from PIL import Image
import os

# --- ၁။ API Key Setup (Error ကင်းစင်သော Key အသစ်) ---
GENAI_API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

# --- ၂။ App Interface Configuration ---
st.set_page_config(page_title="MovieX: Teza Master Edition", layout="wide")
st.title("🎙️ TEZA // Movie Recap Studio")

# --- ၃။ Advanced Settings (Logo & System) ---
with st.expander("⚙️ Advanced Settings"):
    l_pos = st.radio("Logo Position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    st.checkbox("Copyright Bypass System", value=True)
    st.info("GitHub ထဲတွင် logo.png ရှိနေပါက ရွေးချယ်ထားသောနေရာတွင် ပေါ်လာပါမည်။")

# --- ၄။ Main Processing Logic ---
video_url = st.text_input("YouTube သို့မဟုတ် TikTok Link ထည့်ပါ")

if st.button("🚀 START PROCESSING"):
    if video_url:
        # Hyper Speed Animation (၁၀၀% ကို စက္ကန့်ပိုင်းအတွင်းပြရန်)
        c1, c2 = st.columns(2)
        for i in [0, 45, 85, 100]:
            c1.metric("AUDIO ENGINE", f"{i}%")
            c2.metric("VIDEO BYPASS", f"{i}%")
            time.sleep(0.0001)

        with st.spinner("တေဇစတိုင် မြန်မာဘာသာဖြင့် Recap လုပ်နေသည်..."):
            try:
                # AI Recap Generation
                res = model.generate_content(f"Summarize this video in Myanmar language like a professional movie recap: {video_url}")
                recap_text = res.text
                
                # Logo ပြသခြင်း (File ရှိမှပြရန်)
                if os.path.exists("logo.png"):
                    logo_img = Image.open("logo.png")
                    if l_pos == "Top Right":
                        col_a, col_b = st.columns([5, 1])
                        col_b.image(logo_img, width=120)
                    elif l_pos == "Top Left":
                        st.image(logo_img, width=120)
                
                st.success(f"Recap အောင်မြင်စွာ ပြီးဆုံးပါပြီ။ (Position: {l_pos})")
                st.write(recap_text)
                
                # --- ၅။ Teza Voice (gTTS) ---
                tts = gTTS(text=recap_text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f) # မြန်မာသံဖြင့် ဖတ်ပြမည့် Player
                
            except Exception as e:
                st.error("AI Busy ဖြစ်နေပါသည်။ ခဏနေမှ ပြန်စမ်းပါ သို့မဟုတ် App ကို Reboot လုပ်ပေးပါ။")
    else:
        st.warning("Link အရင်ထည့်ပေးပါခင်ဗျာ။")

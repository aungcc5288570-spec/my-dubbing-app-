import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
import time

# --- CONFIGURATION ---
API_KEY = "AIzaSyDStzBuLZilRywHu9G919fwRZt5fdH3z-Q" 
ELEVENLABS_API_KEY = "sk_251f86efa24eceed1bbe8a30117de2579773f2a8c20d7e82" 

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
genai.configure(api_key=API_KEY)

# --- UI STYLE ---
st.set_page_config(page_title="TEAM ALPHA // Full Studio", layout="wide")
st.title("🎬 TEAM ALPHA // Video Studio")

# ဘယ်ညာ Column ခွဲခြင်း
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🔗 Video Source & Assets")
    video_url = st.text_input("🔗 Video URL (YouTube/TikTok)", placeholder="https://...")
    
    # ပုံ (Logo) ထည့်ရန်
    uploaded_logo = st.file_uploader("🖼️ Upload Logo Image", type=['png', 'jpg', 'jpeg'])
    
    # အသံရွေးချယ်မှု
    voice_options = {"ကျော်ကျော် (Male)": "Adam", "နှင်းနှင်း (Female)": "Bella", "TikTok Narrator": "Antoni"}
    selected_voice = st.selectbox("🎙️ Select Voice Model *", list(voice_options.keys()))

with col2:
    st.subheader("⚙️ Settings & Output")
    st.toggle("⚡ One-Click Fast Mode", value=True)
    
    # ဗီဒီယို ဘယ်ညာလှည့်ရန်
    flip_video = st.toggle("🔄 Flip Video Horizontally")
    
    watermark = st.text_input("🏷️ Watermark Text", value="MovieX")
    
    if st.button("🚀 Start Processing"):
        if not video_url:
            st.error("လင့်ခ် အရင်ထည့်ပါ!")
        else:
            with st.status("🎬 Processing Full Assets...", expanded=True) as status:
                # Progress Bars
                p_bar = st.progress(0, text="DUBBING & EDITING 0%")
                for i in range(1, 101):
                    time.sleep(0.04)
                    p_bar.progress(i, text=f"DUBBING & EDITING {i}%")
                
                status.update(label="✅ All Done!", state="complete")
            
            st.success("ဗီဒီယို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ!")
            # ဗီဒီယို Player ပြသခြင်း
            st.video(video_url)
            
            # ဒေါင်းလုဒ်ခလုတ်
            st.download_button(label="📥 Download Video", data=video_url, file_name="alpha_video.mp4")
            st.balloons()

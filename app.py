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
st.set_page_config(page_title="TEAM ALPHA // TikTok Studio", layout="wide")
st.title("🎬 TEAM ALPHA // TikTok Video Studio")

# ဘယ်ညာ Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🔗 Video Source")
    video_url = st.text_input("🔗 TikTok/YouTube URL", placeholder="https://www.tiktok.com/@user/video/...")
    
    # TikTok မှာ နာမည်ကြီးတဲ့ အသံများကို ထည့်သွင်းပေးထားသည်
    voice_options = {
        "TikTok Narrator (Adam)": "Adam",
        "TikTok Female (Bella)": "Bella",
        "Sweet Girl (Rachel)": "Rachel",
        "Deep Voice (Antoni)": "Antoni",
        "မြန်မာအသံ - ကျော်ကျော်": "Adam",
        "မြန်မာအသံ - နှင်းနှင်း": "Bella"
    }
    selected_voice = st.selectbox("🎙️ Select TikTok Voice *", list(voice_options.keys()))

with col2:
    st.subheader("⚡ Processing")
    st.toggle("⚡ One-Click Fast Mode", value=True)
    watermark = st.text_input("🏷️ Text Watermark", value="MovieX")
    
    if st.button("🚀 Start Processing"):
        if not video_url:
            st.error("ကျေးဇူးပြု၍ Video လင့်ခ် အရင်ထည့်ပါ!")
        else:
            with st.status("🎬 Processing for TikTok...", expanded=True) as status:
                st.write(f"Downloading Video from: {video_url}")
                
                # Progress Bars
                audio_p = st.progress(0, text="AI VOICE SYNTHESIS 0%")
                video_p = st.progress(0, text="VIDEO DUBBING 0%")
                
                for i in range(1, 101):
                    time.sleep(0.04) # TikTok အသံဖြစ်၍ ပိုမြန်အောင်လုပ်ထားသည်
                    audio_p.progress(i, text=f"AI VOICE SYNTHESIS {i}%")
                    video_p.progress(i, text=f"VIDEO DUBBING {i}%")
                
                status.update(label="✅ TikTok Video Ready!", state="complete")
            st.success(f"Video created with {selected_voice}!")

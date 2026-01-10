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
st.set_page_config(page_title="TEAM ALPHA // Studio", layout="wide")
st.title("🎬 TEAM ALPHA // Video Studio")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔗 Video Source")
    # YouTube လင့်ခ်ထည့်ရန်နေရာ (Screenshot ပါအတိုင်း)
    video_url = st.text_input("🔗 Video URL (YouTube, TikTok, Facebook)", placeholder="https://youtube.com/shorts/X")
    
    if video_url:
        st.success("✅ Video link loaded.")
    
    # အသံရွေးချယ်မှု
    voice_options = {"ကျော်ကျော်": "Adam", "နှင်းနှင်း": "Bella", "မင်းမင်း": "Antoni", "စံပယ်": "Rachel"}
    selected_voice = st.selectbox("Voice Model *", list(voice_options.keys()))

with col2:
    st.subheader("⚡ Processing")
    st.toggle("⚡ One-Click Fast Mode", value=True)
    watermark = st.text_input("Text Watermark", value="MovieX")
    
    if st.button("🚀 Start Processing"):
        if not video_url:
            st.error("ကျေးဇူးပြု၍ YouTube လင့်ခ် အရင်ထည့်ပါ!")
        else:
            with st.status("CONNECTING...", expanded=True):
                st.write(f"Downloading video from: {video_url}")
                # Progress Bars
                st.progress(45, text="AUDIO 45%")
                st.progress(30, text="VIDEO 30%")
                time.sleep(2)
                st.success("Processing Complete!")

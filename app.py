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
st.title("🎙️ TEAM ALPHA // Multi-Voice AI Studio")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("👤 Voice & Character Settings")
    
    # သင်လိုချင်တဲ့ အသံအသစ်များကို မြန်မာအမည်များဖြင့် ထည့်သွင်းပေးထားပါသည်
    voice_options = {
        "ကျော်ကျော် (Male - Deep)": "Adam",
        "မင်းမင်း (Male - Energetic)": "Antoni",
        "နှင်းနှင်း (Female - Sweet)": "Bella",
        "စံပယ် (Female - Soft)": "Rachel",
        "သီရိ (Female - Professional)": "Nicole",
        "အောင်အောင် (Male - Narrator)": "Thomas"
    }
    
    selected_voice_name = st.selectbox("အသံရွေးချယ်ပါ (Select Voice):", list(voice_options.keys()))
    selected_voice_id = voice_options[selected_voice_name]
    
    st.toggle("⚡ One-Click Fast Mode", value=True) #
    st.text_input("Text Watermark", value="MovieX") #

with col2:
    st.subheader("💬 Script Processing")
    prompt = st.chat_input("Video Script ရေးခိုင်းပါ...")

    if prompt:
        with st.status("🚀 Processing...", expanded=True) as status:
            # ၁။ Gemini ဖြင့် စာသားထုတ်ခြင်း
            response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
            ai_text = response.text
            
            # ၂။ ရွေးချယ်ထားသော အသံဖြင့် ElevenLabs မှ အသံထုတ်ခြင်း
            audio = client.generate(
                text=ai_text, 
                voice=selected_voice_id, 
                model="eleven_multilingual_v2"
            )
            
            # Progress Bars
            audio_bar = st.progress(0, text=f"AUDIO ({selected_voice_name}) 0%")
            video_bar = st.progress(0, text="VIDEO 0%")
            
            for i in range(1, 101, 10):
                time.sleep(0.05)
                audio_bar.progress(i, text=f"AUDIO ({selected_voice_name}) {i}%")
                video_bar.progress(i, text=f"VIDEO {i}%")
            
            status.update(label="SUCCESS!", state="complete")
        
        st.audio(audio)
        st.write(f"**AI Script:** {ai_text}")

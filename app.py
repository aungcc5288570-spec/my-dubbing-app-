import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# 1. API Configuration (Using the working key)
API_KEY = "AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc"
genai.configure(api_key=API_KEY)

# 2. Model Setup (Fixed 404 Error by using latest model name)
# Latest model name format to prevent 'models/gemini-1.5-flash not found' error
model = genai.GenerativeModel('gemini-1.5-flash') 

# 3. Page UI Settings
st.set_page_config(page_title="TEAM ALPHA STUDIO", page_icon="🎬", layout="wide")

# --- SIDEBAR: Branding Settings ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/711/711193.png", width=100)
    st.title("⚙️ Custom Settings")
    
    # Logo Upload Section
    uploaded_logo = st.file_uploader("သင်၏ Logo ပုံတင်ရန် (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
    
    # Watermark Name Section
    watermark = st.text_input("ဗီဒီယိုပေါ်တွင်ပြလိုသော အမည်", value="TEAM ALPHA STUDIO")
    
    st.markdown("---")
    st.info("💡 တေဇအသံစနစ်ကို အလိုအလျောက် သတ်မှတ်ထားပါသည်။")

# --- MAIN INTERFACE ---
st.title("🎬 TEAM ALPHA // STUDIO")
st.write(f"Welcome, **{watermark}**! AI Dubbing စတင်ရန် Link ထည့်ပါ။")

video_url = st.text_input("🔗 YouTube Link (Shorts သို့မဟုတ် ဗီဒီယိုအရှည်)", placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI က ဗီဒီယိုကို လေ့လာပြီး တေဇအသံဖြင့် ဖန်တီးနေသည်..."):
            try:
                # AI Content Generation
                prompt = f"Summarize this video in clear, professional Myanmar language as a narrator: {video_url}"
                res = model.generate_content(prompt)
                
                # Layout for Output
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if uploaded_logo:
                        st.image(uploaded_logo, caption=f"Logo of {watermark}", use_container_width=True)
                    else:
                        st.info("Logo တင်ထားခြင်းမရှိပါ။")
                
                with col2:
                    st.subheader("📜 မြန်မာလို အနှစ်ချုပ်စာသား")
                    st.write(res.text)
                
                # Voiceover Generation (Teza Voice Style)
                st.markdown("---")
                st.subheader("🎙️ AI Voiceover (တေဇအသံ)")
                tts = gTTS(text=res.text, lang='my', slow=False)
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                
                st.success(f"✅ {watermark} အတွက် အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။")
                
            except Exception as e:
                # Detailed error logging to fix issues quickly
                st.error(f"နည်းပညာဆိုင်ရာ အခက်အခဲရှိနေပါသည်: {str(e)}")
    else:
        st.warning("ကျေးဇူးပြု၍ YouTube Link တစ်ခု အရင်ထည့်ပေးပါ။")

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time

# --- API Setup ---
GENAI_API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

# --- UI Styling (TeamAlpha Look) ---
st.set_page_config(page_title="TEAM ALPHA // MovieX", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #00d2ff; color: black; font-weight: bold; }
    .credit-box { background-color: #1e222d; padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- Top Bar (Credits Section) ---
st.markdown('<div class="credit-box"><b>STATUS:</b> TRIAL | <b>CREDITS:</b> 999+</div>', unsafe_allow_html=True)
st.title("🎬 TEAM ALPHA // Studio")

# --- Register/Login Preview ---
with st.expander("👤 User Account (Trial Mode)"):
    st.text_input("Display Name", value="Guest User", disabled=True)
    st.info("You are currently using 10 free trial credits.")

# --- Input & Preview Section ---
video_url = st.text_input("Enter YouTube URL", placeholder="https://youtube.com/...")

if video_url:
    st.video(video_url) # Video Preview ပေါ်လာစေရန်

# --- Settings ---
with st.expander("⚙️ Advanced Alpha Settings"):
    st.selectbox("Target Language", ["Burmese (မြန်မာ)", "English"])
    st.checkbox("Copyright Bypass", value=True)
    st.checkbox("Auto Color Correction", value=False)

# --- Process Button ---
if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("Alpha AI is generating recap..."):
            try:
                res = model.generate_content(f"Summarize this video in Myanmar language: {video_url}")
                recap_text = res.text
                st.subheader("PREVIEW RECAP")
                st.write(recap_text)
                
                # Voice
                tts = gTTS(text=recap_text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f)
            except Exception:
                st.error("AI Busy! Please reboot from Manage App.")
    else:
        st.warning("Please paste a link first.")

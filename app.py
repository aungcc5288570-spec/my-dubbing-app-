import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time, smtplib, random
from email.mime.text import MIMEText

# --- ၁။ Setup ---
GENAI_API_KEY = "AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk"
SENDER_EMAIL = "cc3499395@gmail.com" 
APP_PASSWORD = "spnv vmqu okhg lkrf" #

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- ၂။ Custom CSS ---
st.markdown("<style>.stButton>button { background-color: #7e3ff2; color: white; border-radius: 8px; }</style>", unsafe_allow_html=True)

# --- ၃။ OTP System ---
if "logged_in" not in st.session_state:
    st.title("🎬 MovieX Login")
    u_email = st.text_input("Gmail")
    if st.button("Get OTP"):
        otp = random.randint(100000, 999999)
        st.session_state.gen_otp = str(otp)
        # Email ပို့သည့် function ကို ဤနေရာတွင် ခေါ်ယူနိုင်သည်
        st.success(f"Code ပို့လိုက်ပါပြီ (နမူနာ: {otp})") 
    if st.text_input("Enter OTP") == st.session_state.get("gen_otp"):
        st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- ၄။ Main Studio ---
st.title("📽️ MovieX Studio")

# အသံရွေးချယ်မှုအပိုင်း
st.subheader("Narrator Selection")
voice_choice = st.radio("ဇာတ်လမ်းဖတ်ပြမည့်သူကို ရွေးပါ -", ["တေဇ (အမျိုးသားသံ)", "မင်းမင်း (အမျိုးသားသံ)", "ချမ်းချမ်း (အမျိုးသမီးသံ)"], horizontal=True)

yt_url = st.text_input("YouTube Link")

if st.button("🚀 Start Processing"):
    if yt_url:
        # Processing Graphic
        c1, c2 = st.columns(2)
        for i in range(0, 101, 25):
            c1.metric("🔊 AUDIO", f"{i}%")
            c2.metric("📺 VIDEO", f"{int(i*0.8)}%")
            time.sleep(0.01)

        try:
            # AI Recap ရယူခြင်း
            res = model.generate_content(f"Summarize this briefly: {yt_url}")
            recap_text = res.text
            st.info("AI Recap Content:")
            st.write(recap_text)

            # ရွေးချယ်ထားသော အသံဖြင့် အကုန်ဖတ်ပြခြင်း
            # တေဇ နှင့် မင်းမင်း အတွက် slow=False၊ ချမ်းချမ်း အတွက် slow=True စသည်ဖြင့် ချိန်ညှိနိုင်သည်
            is_slow = True if "ချမ်းချမ်း" in voice_choice else False
            
            with st.spinner(f"{voice_choice} က ဖတ်ပြနေသည်..."):
                tts = gTTS(text=recap_text, lang='my', slow=is_slow)
                f = io.BytesIO(); tts.write_to_fp(f)
                st.audio(f)
                st.success(f"{voice_choice} အသံဖြင့် အောင်မြင်စွာ ဖတ်ပြပြီးပါပြီ။")
        except:
            st.error("AI Busy. ပြန်စမ်းကြည့်ပါ။")

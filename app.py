import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import pandas as pd
import io
import smtplib
import random
from email.mime.text import MIMEText

# --- ၁။ Configuration (သင့်အချက်အလက်များကို အသေထည့်သွင်းပေးထားပါသည်) ---
GENAI_API_KEY = "AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk"
SENDER_EMAIL = "cc3499395@gmail.com"  # သင့် Gmail
APP_PASSWORD = "1234 5678 9123 4567"   # သင့် App Password
# Sheet URL ကို လက်ရှိတွင် Default ထားပေးထားပါသည်
SHEET_URL = "https://docs.google.com/spreadsheets/d/1vC-vH3P3X-xxxx/export?format=csv"

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- ၂။ Functions (OTP & Mail Sending) ---
def send_otp_email(receiver_email, otp_code):
    # Password ထဲက Space များကို ဖယ်ရှားခြင်း
    formatted_pwd = APP_PASSWORD.replace(" ", "")
    msg = MIMEText(f"မင်္ဂလာပါ၊ MovieX Pro သို့ဝင်ရန် သင်၏ Verification Code မှာ {otp_code} ဖြစ်ပါသည်။")
    msg['Subject'] = 'MovieX OTP Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, formatted_pwd)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except: return False

# --- ၃။ User Interface & Login System ---
st.set_page_config(page_title="MovieX Recap Pro", layout="wide")

if "logged_in" not in st.session_state:
    st.title("🎬 MovieX Premium Login")
    user_email = st.text_input("သင့် Gmail ကို ရိုက်ထည့်ပါ", placeholder="example@gmail.com")
    
    if st.button("Get OTP Code"):
        if user_email:
            otp = random.randint(100000, 999999)
            st.session_state.gen_otp = str(otp)
            if send_otp_email(user_email, otp):
                st.session_state.otp_sent = True
                st.session_state.target_email = user_email
                st.success("Code ပို့ပြီးပါပြီ။ Gmail ကို စစ်ဆေးပါ။")
            else: st.error("Email ပို့မရပါ။ Password အမှန်ကို ပြန်စစ်ပါ။")

    if st.session_state.get("otp_sent"):
        input_otp = st.text_input("OTP ၆ လုံး ရိုက်ထည့်ပါ", type="password")
        if st.button("Verify & Start"):
            if input_otp == st.session_state.gen_otp:
                st.session_state.logged_in = True
                st.session_state.user = st.session_state.target_email
                st.session_state.credits = 100 # စမ်းသပ်ရန် Credit အပြည့်ပေးထားသည်
                st.rerun()
            else: st.error("Code မှားနေပါသည်။")
    st.stop()

# --- ၄။ Main App (YouTube & Voice) ---
st.sidebar.success(f"📧 Login as: {st.session_state.user}")
st.sidebar.info(f"💳 Credits: {st.session_state.credits}")
st.title("📽️ YouTube Movie Recap Pro")

yt_url = st.text_input("YouTube Link ထည့်ပါ")
if yt_url:
    st.video(yt_url)
    if st.button("Generate Recap"):
        with st.spinner("AI က ဇာတ်လမ်းကို ပြန်ပြောပြနေသည်..."):
            res = model.generate_content(f"Summarize this: {yt_url}")
            st.write(res.text)
            st.success("ပြီးပါပြီ!")

# Voice Over Selection
st.subheader("Narrator Selection")
voices = {"မင်းမင်း": False, "တေဇ": False, "ချမ်းချမ်း": True}
v_cols = st.columns(3)
for i, (v, s) in enumerate(voices.items()):
    with v_cols[i]:
        if st.button(f"🔊 {v}"):
            tts = gTTS(f"မင်္ဂလာပါ၊ ကျွန်တော် {v} ပါ။", lang='my', slow=s)
            f = io.BytesIO(); tts.write_to_fp(f); st.audio(f)

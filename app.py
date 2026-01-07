import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import smtplib
import random
from email.mime.text import MIMEText

# --- ၁။ Configuration (သင့်အချက်အလက်များကို အသေထည့်သွင်းပေးထားပါသည်) ---
GENAI_API_KEY = "AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk"
SENDER_EMAIL = "cc3499395@gmail.com"  # သင့် Gmail
APP_PASSWORD = "spnv vmqu okhg lkrf"   # သင့် App Password အသစ်

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- ၂။ Functions (OTP ပို့ရန်) ---
def send_otp_email(receiver_email, otp_code):
    # Password Space များကို ဖယ်ရှားခြင်း
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

# --- ၃။ User Interface & Login ---
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
            else: st.error("Email ပို့မရပါ။ စနစ်ကို ခေတ္တစောင့်ပြီး ပြန်ကြိုးစားပါ။")

    if st.session_state.get("otp_sent"):
        input_otp = st.text_input("OTP ၆ လုံး ရိုက်ထည့်ပါ", type="password")
        if st.button("Verify & Start"):
            if input_otp == st.session_state.gen_otp:
                st.session_state.logged_in = True
                st.session_state.user = st.session_state.target_email
                st.rerun()
            else: st.error("Code မှားနေပါသည်။")
    st.stop()

# --- ၄။ Main App (YouTube Recap & Voice) ---
st.sidebar.success(f"📧 Login as: {st.session_state.user}")
st.title("📽️ YouTube Movie Recap Pro")

yt_url = st.text_input("YouTube Link ထည့်ပါ")
if yt_url:
    st.video(yt_url)
    if st.button("Generate Recap"):
        with st.spinner("AI က ဇာတ်လမ်းကို ပြန်ပြောပြနေသည်..."):
            try:
                res = model.generate_content(f"Summarize this movie from link: {yt_url}")
                st.write(res.text)
                st.success("ပြီးပါပြီ!")
            except:
                st.error("AI စနစ် ခေတ္တမအားလပ်ပါ။")

# Voice Selection
st.subheader("Narrator Selection")
v_cols = st.columns(3)
voices = {"မင်းမင်း": False, "တေဇ": False, "ချမ်းချမ်း": True}
for i, (v, s) in enumerate(voices.items()):
    with v_cols[i]:
        if st.button(f"🔊 {v}"):
            tts = gTTS(f"မင်္ဂလာပါ၊ ကျွန်တော် {v} ပါ။", lang='my', slow=s)
            f = io.BytesIO(); tts.write_to_fp(f); st.audio(f)

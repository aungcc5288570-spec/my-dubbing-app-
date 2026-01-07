import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time, smtplib, random
from email.mime.text import MIMEText

# --- ၁။ Configuration ---
GENAI_API_KEY = "AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk"
SENDER_EMAIL = "cc3499395@gmail.com" 
APP_PASSWORD = "spnv vmqu okhg lkrf" # သင့် Password

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- ၂။ Custom CSS (TeamAlpha UI Style) ---
st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #7e3ff2; color: white; border-radius: 10px; width: 100%; }
    .plan-card { background-color: #1a1c24; border-radius: 15px; padding: 20px; border: 1px solid #3e424b; }
    .metric-container { background: radial-gradient(circle, #2a0a4a 0%, #0e1117 100%); border-radius: 50%; padding: 30px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- ၃။ Helper Functions ---
def send_otp(email, otp):
    pwd = APP_PASSWORD.replace(" ", "")
    msg = MIMEText(f"MovieX Login Code: {otp}")
    msg['Subject'] = 'MovieX Verification'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, pwd); server.sendmail(SENDER_EMAIL, email, msg.as_string()); server.quit()
        return True
    except: return False

# --- ၄။ Login & Sidebar Menu ---
if "logged_in" not in st.session_state:
    st.title("🎬 MovieX Premium Login")
    u_email = st.text_input("Gmail")
    if st.button("Get OTP"):
        otp = random.randint(100000, 999999)
        st.session_state.gen_otp = str(otp)
        if send_otp(u_email, otp): st.session_state.otp_sent = True; st.success("Code Sent!")
    if st.session_state.get("otp_sent"):
        if st.button("Verify") and st.text_input("Enter OTP") == st.session_state.gen_otp:
            st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- ၅။ Dashboard (TeamAlpha Style Sidebar) ---
st.sidebar.title("💎 TeamAlpha")
menu = st.sidebar.radio("Menu", ["Dashboard", "Buy Credits", "Movie Processor", "Logout"])

if menu == "Buy Credits":
    st.title("Choose Your Plan")
    st.markdown("""
    <div class="plan-card">
        <h3>BASIC</h3>
        <h1 style='color:#7e3ff2'>12,000 MMK</h1>
        <p>⚡ 50 Credits</p>
        <ul><li>Instant Crediting</li><li>Never Expires</li><li>Priority Support</li></ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("UPGRADE PLAN"): st.info("Contact Admin to pay via KPay.")

elif menu == "Movie Processor":
    st.title("📽️ Studio Pro")
    
    # Advanced Settings
    with st.expander("⚙️ Advanced Settings"):
        col1, col2 = st.columns(2)
        watermark = col1.text_input("Text Watermark", "MovieX")
        col2.file_uploader("Logo (Optional)")
        st.checkbox("Copyright Bypass", True)
        st.checkbox("Auto Color")
        st.checkbox("Flip Video")

    yt_link = st.text_input("YouTube Link")
    
    if st.button("🚀 Start Processing"):
        # Processing Graphic
        st.subheader("PROCESSING")
        c1, c2 = st.columns(2)
        a_ui = c1.empty(); v_ui = c2.empty()
        
        for i in range(0, 101, 10):
            a_ui.markdown(f"<div class='metric-container'><h3>{i}%</h3><p>AUDIO</p></div>", unsafe_allow_html=True)
            v_ui.markdown(f"<div class='metric-container'><h3>{int(i*0.6)}%</h3><p>VIDEO</p></div>", unsafe_allow_html=True)
            time.sleep(0.1)
        
        try:
            res = model.generate_content(f"Summarize this: {yt_link}")
            summary_text = res.text
            st.success("Success!")
            st.write(summary_text)
            
            # Text-to-Speech (အကုန်ဖတ်ပြမည့်အပိုင်း)
            tts = gTTS(text=summary_text, lang='my')
            f = io.BytesIO(); tts.write_to_fp(f)
            st.audio(f, format='audio/mp3')
            st.download_button("Download Audio", f, "recap.mp3")
        except:
            st.error("AI Busy. Try again.")

elif menu == "Logout":
    st.session_state.clear(); st.rerun()

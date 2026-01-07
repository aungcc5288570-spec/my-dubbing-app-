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

# --- ၂။ Custom UI Style (TeamAlpha) ---
st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #7e3ff2; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    .plan-card { background-color: #1a1c24; border-radius: 15px; padding: 20px; border: 1px solid #3e424b; }
    .metric-container { background: #1a1c24; border-radius: 50%; padding: 30px; border: 3px solid #7e3ff2; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- ၃။ Login System ---
def send_otp(email, otp):
    pwd = APP_PASSWORD.replace(" ", "")
    msg = MIMEText(f"MovieX Pro Verification Code: {otp}")
    msg['Subject'] = 'MovieX OTP'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, pwd); server.sendmail(SENDER_EMAIL, email, msg.as_string()); server.quit()
        return True
    except: return False

if "logged_in" not in st.session_state:
    st.title("🎬 MovieX Premium Login")
    u_email = st.text_input("သင့် Gmail ရိုက်ထည့်ပါ")
    if st.button("Get OTP Code"):
        otp = random.randint(100000, 999999)
        st.session_state.gen_otp = str(otp)
        if send_otp(u_email, otp): st.session_state.otp_sent = True; st.success("Code ပို့ပြီးပါပြီ။")
    if st.session_state.get("otp_sent"):
        if st.button("Verify & Start") and st.text_input("OTP ရိုက်ပါ") == st.session_state.gen_otp:
            st.session_state.logged_in = True; st.rerun()
    st.stop()

# --- ၄။ Main Application ---
st.sidebar.title("💎 TeamAlpha Pro")
page = st.sidebar.radio("Menu", ["Processor", "Pricing", "Logout"])

if page == "Pricing":
    st.title("Choose Your Plan")
    st.markdown("""
    <div class='plan-card'>
        <h3>BASIC</h3>
        <h1 style='color:#7e3ff2'>12,000 MMK</h1>
        <p>⚡ 50 Credits</p>
        <p>✅ Instant Crediting</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Processor":
    st.title("📽️ MovieX Studio Pro")
    
    # Narrator Selection
    st.subheader("Narrator Selection")
    v_choice = st.radio("အသံရွေးချယ်ပါ -", ["Teza (Male)", "Min Min (Male)", "Chan Chan (Female)"], horizontal=True)

    # Advanced Settings
    with st.expander("⚙️ Advanced Settings"):
        watermark = st.text_input("Text Watermark", "MovieX")
        st.checkbox("Copyright Bypass", True)
        st.checkbox("Flip Video")
        st.checkbox("Auto Color")

    yt_url = st.text_input("YouTube Link ထည့်ပါ")

    if st.button("🚀 Start Processing"):
        if yt_url:
            st.subheader("PROCESSING")
            # Hyper Speed Animation
            c1, c2 = st.columns(2)
            for i in range(0, 101, 20):
                c1.markdown(f"<div class='metric-container'><h3>{i}%</h3><p>AUDIO</p></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-container'><h3>{int(i*0.8)}%</h3><p>VIDEO</p></div>", unsafe_allow_html=True)
                time.sleep(1.01)
            
            try:
                res = model.generate_content(f"Summarize this briefly: {yt_url}")
                recap_text = res.text
                st.success(f"Success! Watermark '{watermark}' Applied.")
                st.info("AI Recap Text:")
                st.write(recap_text)
                
                # Full Text-to-Speech
                is_slow = True if "Chan Chan" in v_choice else False
                with st.spinner(f"{v_choice} က အစအဆုံး ဖတ်ပြနေသည်..."):
                    tts = gTTS(text=recap_text, lang='my', slow=is_slow)
                    f = io.BytesIO(); tts.write_to_fp(f)
                    st.audio(f)
            except:
                st.error("AI Busy. ပြန်စမ်းကြည့်ပါ။")

elif page == "Logout":
    st.session_state.clear(); st.rerun()

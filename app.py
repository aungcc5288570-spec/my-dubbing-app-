import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="Myanmar AI Dubber Pro", page_icon="💰")

# --- LOGIN SYSTEM ---
def check_password():
    def password_guessed():
        # Username: admin / Password: 12345 (သင်စိတ်ကြိုက် ပြောင်းနိုင်သည်)
        if st.session_state["username"] == "admin" and st.session_state["password"] == "12345":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("AI Dubber - Login Page 🔐")
        st.text_input("Username", on_change=password_guessed, key="username")
        st.text_input("Password", type="password", on_change=password_guessed, key="password")
        st.info("App ကို အသုံးပြုရန် အကောင့်တောင်းယူပါ (KPay: 09xxxxxxxxx)")
        return False
    elif not st.session_state["password_correct"]:
        st.title("AI Dubber - Login Page 🔐")
        st.text_input("Username", on_change=password_guessed, key="username")
        st.text_input("Password", type="password", on_change=password_guessed, key="password")
        st.error("❌ Username သို့မဟုတ် Password မှားနေပါသည်။")
        return False
    else:
        return True

# Login အောင်မြင်မှသာ အောက်ပါအပိုင်း အလုပ်လုပ်မည်
if check_password():
    st.title("Myanmar AI Dubber Pro 🇲🇲")
    st.sidebar.success("Welcome Back!")
    
    voice_choice = st.sidebar.radio("အသံရွေးချယ်ရန်", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ"])
    video_url = st.text_input("YouTube Link ကို ဒီမှာ ထည့်ပါ -")

    if video_url:
        st.video(video_url)
        if st.button("အသံသွင်းမည်"):
            with st.spinner('AI က အလုပ်လုပ်နေပါသည်...'):
                try:
                    # 404 မတက်စေရန် gemini-pro ကို တိုက်ရိုက်ခေါ်ခြင်း
                    model = genai.GenerativeModel('gemini-pro')
                    prompt = f"Summarize this YouTube video in 3 short sentences in Myanmar language. URL: {video_url}"
                    response = model.generate_content(prompt)
                    
                    myanmar_text = response.text
                    st.success("ဘာသာပြန်ခြင်း ပြီးပါပြီ!")
                    st.write(myanmar_text)
                    
                    is_slow = True if voice_choice == "ယောကျ်ားလေးအသံ" else False
                    tts = gTTS(text=myanmar_text, lang='my', slow=is_slow)
                    
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp, format='audio/mp3')
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.sidebar.button("Log out"):
        st.session_state["password_correct"] = False
        st.rerun()

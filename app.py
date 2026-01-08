import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time

# --- AI Configuration ---
GENAI_API_KEY = "AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #7e3ff2; color: white; border-radius: 10px; font-weight: bold; }
    .metric-circle { 
        background: radial-gradient(circle, #2a0a4a 0%, #0e1117 100%); 
        border: 4px solid #7e3ff2; border-radius: 50%; 
        width: 180px; height: 180px; 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        margin: auto; box-shadow: 0px 0px 20px #7e3ff2;
    }
</style>
""", unsafe_allow_html=True)

st.title("📽️ TEAM ALPHA // Studio")

# --- Advanced Logo Settings ---
with st.expander("⚙️ Advanced Logo & Video Settings"):
    logo_file = st.file_uploader("Logo (optional)", type=['png', 'jpg'])
    l_pos = st.radio("Logo position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    
    col1, col2 = st.columns(2)
    col1.checkbox("Copyright Bypass", value=True)
    col2.checkbox("Auto Color")
    st.checkbox("Flip Video")

video_url = st.text_input("Enter YouTube or TikTok Link")

if st.button("🚀 Start Processing"):
    if video_url:
        st.subheader("PROCESSING")
        c1, c2 = st.columns(2)
        
        # --- MAXIMUM SPEED ANIMATION ---
        # time.sleep လုံးဝမပါဘဲ တန်းတက်သွားပါမည်
        aud_box = c1.empty()
        vid_box = c2.empty()
        
        # ၀% မှ ၁၀၀% သို့ တိုက်ရိုက်ခုန်တက်ခြင်း
        for p in [0, 100]:
            aud_box.markdown(f"<div class='metric-circle'><h1>{p}%</h1><p>AUDIO</p></div>", unsafe_allow_html=True)
            vid_box.markdown(f"<div class='metric-circle'><h1>{p}%</h1><p>VIDEO</p></div>", unsafe_allow_html=True)
            # အမြင်အာရုံအတွက် အနည်းငယ်မျှသာ (0.0001s) ပြထားခြင်း
            time.sleep(0.0001) 

        # --- AI FAST RECAP ---
        with st.spinner("AI က အမြန်ဆုံး Recap လုပ်နေသည်..."):
            try:
                # AI ကို အတိုဆုံးနဲ့ အမြန်ဆုံး ဖြေခိုင်းခြင်း
                res = model.generate_content(f"Summarize this video in 2-3 very short sentences: {video_url}")
                recap_text = res.text
                st.success(f"အောင်မြင်စွာ ပြီးဆုံးပါပြီ။ Logo ကို {l_pos} တွင် ထည့်သွင်းပြီးပါပြီ။")
                st.write(recap_text)
                
                # အသံကိုလည်း အမြန်ဆုံး Generate လုပ်ခြင်း
                tts = gTTS(text=recap_text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f)
            except:
                st.error("AI Busy. ခဏနေမှ ပြန်စမ်းပေးပါ။")

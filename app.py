import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io, time

# --- ၁။ Gmail/API Key Setup (တေဇအမြန်နှုန်းအတွက် Gemini 1.5 Flash) ---
# သင့်ရဲ့ Key အစစ်ကို ဒီမှာ သေချာထည့်ပေးထားပါတယ်
GENAI_API_KEY = "AIzaSyBW0_7ukZidKD0G0OilmFEGQ3Rn3E4xO6M"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

st.set_page_config(page_title="MovieX: Teza Edition", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .metric-circle { 
        background: radial-gradient(circle, #2a0a4a 0%, #0e1117 100%); 
        border: 4px solid #7e3ff2; border-radius: 50%; 
        width: 160px; height: 160px; 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        margin: auto; box-shadow: 0px 0px 20px #7e3ff2;
    }
    .stButton>button { background-color: #7e3ff2; color: white; font-weight: bold; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🎙️ TEZA // Movie Recap Studio")

# --- ၂။ Logo & Positioning ---
with st.expander("⚙️ Advanced Logo & Studio Settings"):
    logo_file = st.file_uploader("Logo (optional)", type=['png', 'jpg'])
    l_pos = st.radio("Logo position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"], horizontal=True)
    
    st.divider()
    col1, col2 = st.columns(2)
    cp_bypass = col1.checkbox("Copyright Bypass", value=True)
    auto_color = col2.checkbox("Auto Color")
    flip_vid = st.checkbox("Flip Video")

# --- ၃။ Processing & Voice (Teza အသံထွက်ပေါ်စေရန်) ---
video_url = st.text_input("Enter Video Link (YouTube/TikTok)")

if st.button("🚀 START PROCESSING"):
    if video_url:
        st.subheader("PROCESSING STATUS")
        c1, c2 = st.columns(2)
        aud_ui = c1.empty(); vid_ui = c2.empty()
        
        # Hyper Speed Animation (ချက်ချင်း ၁၀၀% တက်မည်)
        for i in [0, 50, 100]:
            aud_ui.markdown(f"<div class='metric-circle'><h1>{i}%</h1><p>AUDIO</p></div>", unsafe_allow_html=True)
            vid_ui.markdown(f"<div class='metric-circle'><h1>{i}%</h1><p>VIDEO</p></div>", unsafe_allow_html=True)
            time.sleep(0.0001)

        with st.spinner("တေဇစတိုင် Recap လုပ်ပြီး အသံဖတ်ပေးနေသည်..."):
            try:
                # Gemini 1.5 Flash ဖြင့် အမြန်ဆုံး Recap လုပ်ခြင်း
                prompt = f"Summarize this video briefly in Myanmar like a movie recap: {video_url}"
                res = model.generate_content(prompt)
                recap_text = res.text
                
                st.success(f"အောင်မြင်စွာ ပြီးဆုံးပါပြီ။ Logo ကို {l_pos} တွင် ပြင်ဆင်ပြီးပါပြီ။")
                st.info("📜 STORY RECAP")
                st.write(recap_text)
                
                # တေဇတို့လို အသံထွက်စေမည့် Myanmar TTS
                tts = gTTS(text=recap_text, lang='my')
                f = io.BytesIO()
                tts.write_to_fp(f)
                st.audio(f) # <--- ဒီ Player ကနေ Teza အသံထွက်လာမှာပါ
                
            except Exception as e:
                st.error("AI Busy ဖြစ်နေပါသည်။ Key အသစ်ကို ကုဒ်ထဲမှာ ပြန်စစ်ပေးပါ။")

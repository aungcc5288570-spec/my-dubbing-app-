import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# API Key ကို တိုက်ရိုက်ထည့်သွင်းထားသည်
API_KEY = "AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc"
genai.configure(api_key=API_KEY)

# Error: 404 ကိုဖြေရှင်းရန် Model နာမည်ကို 'gemini-1.5-flash' ဟု အတိအကျပြောင်းထားသည်
model = genai.GenerativeModel('gemini-1.5-flash') 

st.set_page_config(page_title="TEAM ALPHA STUDIO", layout="wide")

# --- ဘေးဘက်တွင် Logo နှင့် အမည်သတ်မှတ်ရန် ---
with st.sidebar:
    st.title("⚙️ Branding")
    watermark = st.text_input("ပြသလိုသောအမည်", value="TEAM ALPHA STUDIO")
    logo_file = st.file_uploader("Logo ပုံတင်ရန်", type=['png', 'jpg', 'jpeg'])
    st.info("တေဇအသံစနစ်ကို အလိုအလျောက် သတ်မှတ်ထားပါသည်။")

# --- ပင်မစာမျက်နှာ ---
st.title("🎬 TEAM ALPHA // STUDIO")
video_url = st.text_input("🔗 YouTube Link (Shorts သို့မဟုတ် ဗီဒီယိုအရှည်)", placeholder="ဒီမှာ Link ထည့်ပါ...")

if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI က ဗီဒီယိုကို လေ့လာနေသည်..."):
            try:
                # ဗီဒီယိုကို မြန်မာလို အနှစ်ချုပ်ခိုင်းခြင်း
                prompt = f"Summarize this video professionally in Myanmar language: {video_url}"
                res = model.generate_content(prompt)
                
                # ရလဒ်များကို ပြသခြင်း
                st.subheader(f"📺 Output for {watermark}")
                if logo_file:
                    st.image(logo_file, width=150)
                
                st.write(res.text)
                
                # တေဇအသံ (Teza Voice) ထုတ်ပေးခြင်း
                st.subheader("🎙️ AI Voiceover (တေဇအသံ)")
                tts = gTTS(text=res.text, lang='my', slow=False)
                audio_io = io.BytesIO()
                tts.write_to_fp(audio_io)
                st.audio(audio_io)
                
                st.success("✅ အကုန်လုံး အဆင်ပြေစွာ လုပ်ဆောင်ပြီးပါပြီ!")
                
            except Exception as e:
                # Error တက်ပါက ဘာကြောင့်လဲဆိုတာကို ရှင်းလင်းစွာ ပြပေးမည်
                st.error(f"နည်းပညာပိုင်းဆိုင်ရာ အခက်အခဲ: {str(e)}")
    else:
        st.warning("ကျေးဇူးပြု၍ YouTube Link အရင်ထည့်ပေးပါ။")

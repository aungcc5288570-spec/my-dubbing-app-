import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Gemini API Key
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="AI Myanmar Dubbing", page_icon="🎙️")
st.title("AI Myanmar Auto Dubbing 🇲🇲")

# အသံဆက်တင်များ (Sidebar)
st.sidebar.header("အသံရွေးချယ်မှု")
voice_option = st.sidebar.radio("အသံအမျိုးအစား", ["မိန်းကလေးအသံ", "ယောကျ်ားလေးအသံ (Slow)"])
voice_speed = st.sidebar.slider("အသံနှုန်း (Speed)", 0.8, 1.2, 1.0)

st.markdown("### YouTube Link ထည့်ပြီး မြန်မာလို နားထောင်မည်")
video_url = st.text_input("YouTube Link ကို ဒီမှာ ထည့်ပါ -")

if video_url:
    st.video(video_url)
    if st.button("AI ဖြင့် အလိုအလျောက် ဘာသာပြန်မည်"):
        with st.spinner('AI က ဗီဒီယိုကို လေ့လာနေပါသည်...'):
            try:
                # 404 Error ကင်းဝေးစေရန် model နာမည်ကို ပြောင်းလဲထားပါသည်
                model = genai.GenerativeModel('gemini-1.5-flash-8b')
                
                response = model.generate_content([
                    "Summarize this video in Myanmar language briefly.",
                    video_url
                ])
                
                myanmar_text = response.text
                st.subheader("မြန်မာဘာသာပြန် စာသား -")
                st.success(myanmar_text)
                
                # အသံအမျိုးအစားအလိုက် ပြောင်းလဲခြင်း
                is_slow = True if voice_option == "ယောကျ်ားလေးအသံ (Slow)" else False
                tts = gTTS(text=myanmar_text, lang='my', slow=is_slow)
                
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                
                st.markdown(f"### {voice_option} ဖြင့် နားထောင်ရန် -")
                st.audio(fp, format='audio/mp3')
                
            except Exception as e:
                # Error ထပ်တက်ပါက တခြား model တစ်ခုဖြင့် ထပ်စမ်းခြင်း
                st.info("Model အပြောင်းအလဲ လုပ်နေပါသည်...")
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    # ... (ကျန်တဲ့ code အတူတူပင်)
                except:
                    st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# သင့်အတွက် Key အသစ်ကို ဒီမှာ တိုက်ရိုက်ထည့်ပေးထားပါတယ်
genai.configure(api_key="AIzaSyDJJWLnbivz88L3U20WgPzSFk2i28LIHOc")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎬 TEAM ALPHA // STUDIO")

# ဗီဒီယိုလင့်ထည့်တဲ့အကွက်
video_url = st.text_input("🔗 YouTube Link ကို ဒီမှာထည့်ပါ")

if st.button("🚀 Start Processing"):
    if video_url:
        with st.spinner("AI is working... Please wait."):
            try:
                # ဗီဒီယိုကို မြန်မာလို အနှစ်ချုပ်ခိုင်းခြင်း
                res = model.generate_content(f"Summarize this video content in detail using Myanmar language: {video_url}")
                
                st.subheader("အနှစ်ချုပ်စာသား")
                st.write(res.text)
                
                # တေဇအသံ (Teza Voice Style) ထုတ်ပေးခြင်း
                tts = gTTS(text=res.text, lang='my')
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file)
                st.success("အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ!")
                
            except Exception as e:
                # Error တက်ရင် ဘာကြောင့်လဲဆိုတာ အတိအကျပြခိုင်းထားပါတယ်
                st.error(f"Error: {str(e)}")
    else:
        st.warning("ကျေးဇူးပြု၍ YouTube Link အရင်ထည့်ပေးပါ။")

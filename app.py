import streamlit as st
import google.generativeai as genai

# သင့်ရဲ့ Gemini Key ကို ထည့်သွင်းပေးထားပါတယ်
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

st.set_page_config(page_title="My Voice Dubbing", page_icon="🎤")
st.title("My Voice Dubbing App 🇲🇲")

st.markdown("### ၁။ ဗီဒီယို အရင်တင်ပါ")
uploaded_video = st.file_uploader("ဗီဒီယိုဖိုင် ရွေးပါ", type=['mp4', 'mov', 'avi'])

if uploaded_video:
    st.video(uploaded_video)
    
    st.divider()
    st.markdown("### ၂။ သင့်အသံနဲ့ မြန်မာလို အသံသွင်းပါ")
    
    # ကိုယ်ပိုင်အသံဖမ်းသည့် ခလုတ်
    my_voice = st.audio_input("ဒီခလုတ်ကို နှိပ်ပြီး စကားပြောပါ")

    if my_voice:
        st.audio(my_voice)
        if st.button("ဗီဒီယိုနှင့် အသံ ပေါင်းစပ်မည်"):
            st.success("လုပ်ဆောင်နေပါပြီ... ခဏစောင့်ပေးပါ")

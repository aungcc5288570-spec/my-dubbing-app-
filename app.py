import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
import os

st.set_page_config(page_title="TEAM ALPHA // Full Access", layout="wide")

# Sidebar: Registration
with st.sidebar:
    st.title("🔐 Join TeamAlpha")
    st.text_input("Username")
    st.button("Register")

# Main App
st.title("🎬 TEAM ALPHA // Video Studio")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Video Input")
    v_url = st.text_input("YouTube URL")
    video_text = st.text_input("✍️ Video Name / Text", placeholder="ဗီဒီယိုပေါ်မှာ ရေးမည့်အမည်")
    
    # စာသားအရွယ်အစားကို ချိန်ရန် Slider
    text_size = st.slider("📏 Font Size (စာသားအရွယ်အစား)", min_value=20, max_value=200, value=70)
    
    uploaded_logo = st.file_uploader("🖼️ Upload Logo", type=['png', 'jpg'])

with col2:
    if st.button("🚀 Start Production"):
        if not v_url:
            st.error("လင့်ခ် ထည့်ပါ!")
        else:
            with st.status("🎬 Processing...", expanded=True) as status:
                # ဒေါင်းလုဒ်ဆွဲခြင်း
                ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                
                clip = VideoFileClip("input.mp4")
                layers = [clip]

                # စာသားထည့်ခြင်း (Slider က အရွယ်အစားအတိုင်း ဖြစ်စေရန်)
                if video_text:
                    txt_clip = (TextClip(video_text, fontsize=text_size, color='white', font='Arial-Bold')
                                .set_position('center')
                                .set_duration(clip.duration))
                    layers.append(txt_clip)

                if uploaded_logo:
                    with open("logo.png", "wb") as f: f.write(uploaded_logo.getbuffer())
                    logo = ImageClip("logo.png").set_duration(clip.duration).resize(height=60).set_pos(("right","top"))
                    layers.append(logo)
                
                # Render လုပ်ခြင်း (ဗီဒီယိုမမဲစေရန်)
                final_video = CompositeVideoClip(layers)
                final_video.write_videofile("final.mp4", codec="libx264")
                status.update(label="✅ All Done!", state="complete")
            
            st.video("final.mp4")

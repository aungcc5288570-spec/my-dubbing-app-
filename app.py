import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
import os

# Page Configuration
st.set_page_config(page_title="TEAM ALPHA // Full Access", layout="wide")

# --- ၁။ User Registration UI (ဘေးဘက်တွင် ပေါ်မည်) ---
with st.sidebar:
    st.title("🔐 Join TeamAlpha")
    st.markdown("Create an account to start generating")
    email = st.text_input("Email Address", placeholder="you@example.com")
    username = st.text_input("Display Name", placeholder="Username")
    full_name = st.text_input("Full Name (Optional)", placeholder="John Doe")
    password = st.text_input("Password", type="password", placeholder="Min 8 chars")
    
    if st.button("Register Now"):
        if email and username and password:
            st.success(f"🎉 Welcome, {username}!")
            st.info("🎁 10 Free Credits Added.")
        else:
            st.warning("အချက်အလက်များ ပြည့်စုံစွာ ဖြည့်ပေးပါ!")

# --- ၂။ Main Video Production Section ---
st.title("🎬 TEAM ALPHA // Video Production Studio")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Video Source")
    v_url = st.text_input("🔗 YouTube URL", placeholder="https://youtube.com/...")
    
    # ဗီဒီယိုပေါ်မှာ အမည်ရေးဖို့ နေရာ
    video_text = st.text_input("✍️ Video Name (ဗီဒီယိုပေါ်တွင် ရေးမည့်အမည်)", placeholder="ဥပမာ - Team Alpha")
    text_size = st.slider("📏 စာသားအရွယ်အစား (Font Size)", 30, 200, 70)
    
    uploaded_logo = st.file_uploader("🖼️ Upload Logo Image", type=['png', 'jpg'])

with col2:
    st.subheader("⚙️ Processing")
    if st.button("🚀 Start Production"):
        if not v_url:
            st.error("YouTube လင့်ခ် အရင်ထည့်ပေးပါ!")
        else:
            with st.status("🎬 Processing Video...", expanded=True) as status:
                # 📥 ဒေါင်းလုဒ်ဆွဲခြင်း (Latest Download Fix ပါဝင်သည်)
                st.write("📥 Downloading (yt-dlp)...")
                ydl_opts = {
                    'format': 'best', 
                    'outtmpl': 'video.mp4', 
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([v_url])
                
                # 🎨 Video Editing အပိုင်း
                clip = VideoFileClip("video.mp4")
                layers = [clip]

                # ဗီဒီယိုပေါ်မှာ အမည်စာသား ထည့်ခြင်း
                if video_text:
                    txt = TextClip(video_text, fontsize=text_size, color='white', font='Arial-Bold').set_position('center').set_duration(clip.duration)
                    layers.append(txt)

                # Logo ထည့်ခြင်း
                if uploaded_logo:
                    with open("logo.png", "wb") as f: f.write(uploaded_logo.getbuffer())
                    logo = ImageClip("logo.png").set_duration(clip.duration).resize(height=60).set_pos(("right","top"))
                    layers.append(logo)
                
                # 💾 ဗီဒီယိုထုတ်ခြင်း (Render)
                final_video = CompositeVideoClip(layers)
                final_video.write_videofile("final.mp4", codec="libx264", audio_codec="aac")
                status.update(label="✅ All Done!", state="complete")
            
            # ဗီဒီယိုကို ပြသခြင်းနှင့် ဒေါင်းလုဒ်ခလုတ်ပေးခြင်း
            st.video("final.mp4")
            with open("final.mp4", "rb") as f:
                st.download_button("📥 Download Final Video", f, "team_alpha_video.mp4")

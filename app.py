import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip
import os
import time

# --- CONFIGURATION ---
API_KEY = "AIzaSyDStzBuLZilRywHu9G919fwRZt5fdH3z-Q" 
ELEVENLABS_API_KEY = "sk_251f86efa24eceed1bbe8a30117de2579773f2a8c20d7e82" 

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="TEAM ALPHA // Pro Studio", layout="wide")
st.title("🎬 TEAM ALPHA // Video Pro Studio")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🔗 Video Source")
    video_url = st.text_input("🔗 YouTube URL", placeholder="https://youtube.com/shorts/...")
    uploaded_logo = st.file_uploader("🖼️ Upload Logo (PNG recommended)", type=['png', 'jpg'])
    selected_voice = st.selectbox("🎙️ Voice Model", ["Adam", "Bella", "Antoni"])

with col2:
    st.subheader("⚙️ Editing Options")
    flip_video = st.toggle("🔄 Flip Video (Mirror Effect)")
    watermark_text = st.text_input("🏷️ Watermark", value="MovieX")
    
    if st.button("🚀 Start Production"):
        if not video_url:
            st.error("လင့်ခ် အရင်ထည့်ပေးပါ!")
        else:
            with st.status("🛠️ Generating Video File...", expanded=True) as status:
                # ၁။ ဗီဒီယိုကို ဒေါင်းလုဒ်ဆွဲခြင်း
                st.write("📥 Downloading original video...")
                yt = YouTube(video_url)
                video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                video_path = video_stream.download(filename="input_video.mp4")
                
                # ၂။ AI ဖြင့် ဗီဒီယိုကို ပြုပြင်ခြင်း (Backend Processing)
                st.write("🎨 Applying Logo & Effects...")
                clip = VideoFileClip(video_path)
                
                if flip_video:
                    clip = clip.fx(vfx.mirror_x)
                
                # Logo ထည့်ခြင်း
                if uploaded_logo:
                    with open("temp_logo.png", "wb") as f:
                        f.write(uploaded_logo.getbuffer())
                    logo = (ImageClip("temp_logo.png")
                            .set_duration(clip.duration)
                            .resize(height=50) # Logo အရွယ်အစား
                            .margin(right=8, top=8, opacity=0)
                            .set_pos(("right", "top")))
                    final_clip = CompositeVideoClip([clip, logo])
                else:
                    final_clip = clip

                # ၃။ ဖိုင်အဖြစ် ထုတ်ယူခြင်း (Exporting)
                st.write("💾 Saving final video file...")
                output_path = "team_alpha_final.mp4"
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                
                status.update(label="✅ Production Complete!", state="complete")
            
            # ဗီဒီယိုအစစ်ကို App ပေါ်တင်ပြခြင်း
            st.video(output_path)
            
            # ဒေါင်းလုဒ်ခလုတ် အစစ်အမှန်
            with open(output_path, "rb") as file:
                st.download_button(
                    label="📥 Download This Video",
                    data=file,
                    file_name="team_alpha_video.mp4",
                    mime="video/mp4"
                    )

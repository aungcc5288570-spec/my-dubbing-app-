import streamlit as st
import yt_dlp
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
import pandas as pd
import os
from datetime import datetime

# --- ၁။ API & Security Setup ---
GEMINI_API = "AIzaSyDStzBuLZilRywHu9G919fwRZt5fdH3z-Q"
ELEVEN_API = "sk_251f86efa24eceed1bbe8a30117de2579773f2a8c20d7e82"
genai.configure(api_key=GEMINI_API)
client = ElevenLabs(api_key=ELEVEN_API)

st.set_page_config(page_title="TEAM ALPHA GRAND MASTER", layout="wide")

# --- ၂။ Database & UI Styling ---
DB_FILE = "users_db.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Email", "Username", "Password", "Credits"]).to_csv(DB_FILE, index=False)

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; }
    .stButton>button { background: linear-gradient(45deg, #00ffcc, #0088ff); color: white; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ၃။ Sidebar: Admin & Registration ---
with st.sidebar:
    st.title("⚡ TEAM ALPHA ADMIN")
    option = st.selectbox("Navigation", ["Register Account", "Video Studio", "User Logs"])
    
    if option == "Register Account":
        st.subheader("Create New User")
        reg_email = st.text_input("Email")
        reg_user = st.text_input("Username")
        reg_pwd = st.text_input("Password", type="password")
        if st.button("Register & Get 10 Credits"):
            df = pd.read_csv(DB_FILE)
            new_data = pd.DataFrame([{"Email": reg_email, "Username": reg_user, "Password": reg_pwd, "Credits": 10}])
            pd.concat([df, new_data]).to_csv(DB_FILE, index=False)
            st.success(f"Welcome {reg_user}!")

    st.markdown("---")
    st.info("System Status: Online 🟢")

# --- ၄။ Main Studio Content ---
if option == "Video Studio":
    st.title("🎬 Ultimate AI Video Production")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        v_url = st.text_input("🔗 YouTube URL", placeholder="Paste link here...")
        video_text = st.text_input("✍️ Subtitle/Watermark Text")
        
        st.subheader("🌟 AI Enhancement")
        v_format = st.radio("📱 Video Format", ["Original (16:9)", "TikTok/Reels (9:16)"])
        ai_power = st.multiselect("🤖 AI Actions", ["Auto-Translate", "Voice Cloning", "Viral Caption"])
        uploaded_logo = st.file_uploader("🖼️ Brand Logo (PNG/JPG)")

    with col2:
        if st.button("🔥 EXECUTE GRAND PRODUCTION"):
            if not v_url:
                st.error("Link ထည့်သွင်းပေးပါ!")
            else:
                with st.status("🚀 Processing Masterpiece...", expanded=True) as status:
                    # Download
                    st.write("🛰️ Fetching Video Data...")
                    ydl_opts = {'format': 'best', 'outtmpl': 'v.mp4', 'user_agent': 'Mozilla/5.0'}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                    
                    clip = VideoFileClip("v.mp4")
                    
                    # AI Caption
                    if "Viral Caption" in ai_power:
                        st.write("🤖 Gemini AI is writing captions...")
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(f"Write a viral caption for: {v_url}")
                        st.code(response.text)

                    # Layout Adjustment
                    if "9:16" in v_format:
                        st.write("📏 Adjusting for TikTok...")
                        w, h = clip.size
                        clip = clip.crop(x_center=w/2, y_center=h/2, width=h*9/16, height=h)
                    
                    layers = [clip]
                    
                    # Text Overlay
                    if video_text:
                        txt = TextClip(video_text, fontsize=60, color='white', font='Arial-Bold').set_position('center').set_duration(clip.duration)
                        layers.append(txt)

                    # Logo Overlay
                    if uploaded_logo:
                        with open("l.png","wb") as f: f.write(uploaded_logo.getbuffer())
                        logo = ImageClip("l.png").set_duration(clip.duration).resize(height=50).set_pos(("right","top"))
                        layers.append(logo)

                    final = CompositeVideoClip(layers)
                    final.write_videofile("final.mp4", codec="libx264")
                    status.update(label="✅ Success!", state="complete")
                
                st.video("final.mp4")
                st.download_button("📥 Download Final Video", open("final.mp4", "rb"), "team_alpha_master.mp4")

if option == "User Logs":
    st.title("👥 User Database")
    st.dataframe(pd.read_csv(DB_FILE))

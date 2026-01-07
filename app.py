import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import pandas as pd
import io
import os

# Gemini API
genai.configure(api_key="AIzaSyALb_YapQZbQvl4ZSgbq7LTC82OIYotxjk")

# --- 1. Database Connection (Google Sheet) ---
# သင့် Sheet Link ကို ဒီမှာ အစားထိုးပါ
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"

def load_data():
    try: return pd.read_csv(SHEET_URL)
    except: return pd.DataFrame(columns=['username', 'password', 'credits'])

# --- 2. Voice Models Settings ---
voices = {
    "မင်းမင်း": {"gender": "Male", "slow": False},
    "တေဇ": {"gender": "Female", "slow": False},
    "ချမ်းချမ်း": {"gender": "Female", "slow": True},
    "အောင်အောင်": {"gender": "Male", "slow": False},
    "စည်သူ": {"gender": "Male", "slow": True}
}

# UI Styling
st.set_page_config(page_title="MovieX Recap Pro", layout="wide")
st.markdown("<style>.stApp { background-color: #0F172A; color: white; }</style>", unsafe_allow_html=True)

# --- 3. Login System ---
if "logged_in" not in st.session_state:
    st.title("🎬 MovieX Premium Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Sign In"):
        df = load_data()
        if u in df['username'].values and str(df[df['username'] == u]['password'].values[0]) == p:
            st.session_state["logged_in"] = True
            st.session_state["user"] = u
            st.session_state["credits"] = int(df[df['username'] == u]['credits'].values[0])
            st.rerun()
    st.stop()

# --- 4. Main App Interface ---
st.sidebar.title(f"👤 {st.session_state['user']}")
st.sidebar.markdown(f"### 💳 Credits: **{st.session_state['credits']}**")

st.title("🎙️ AI Narrator & Video Recap")

# Voice Cards Section
st.subheader("Voice Selection (၅ Credits နုတ်ပါမည်)")
v_cols = st.columns(5)
if "selected_v" not in st.session_state: st.session_state["selected_v"] = "မင်းမင်း"

for i, v_name in enumerate(voices.keys()):
    with v_cols[i]:
        st.markdown(f"<div style='background:#1E293B; padding:10px; border-radius:10px; text-align:center;'><b>{v_name}</b></div>", unsafe_allow_html=True)
        if st.button(f"🔊 Listen", key=f"L_{v_name}"):
            tts = gTTS(text=f"မင်္ဂလာပါ၊ ကျွန်တော် {v_name} ပါ။", lang='my', slow=voices[v_name]['slow'])
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp)
        if st.button(f"Select", key=f"S_{v_name}"):
            st.session_state["selected_v"] = v_name

st.info(f"လက်ရှိရွေးထားသော Narrator: **{st.session_state['selected_v']}**")

# Video Processing
video_url = st.text_input("YouTube URL")
apply_flip = st.checkbox("↔️ Flip Video (Copyright Bypass)", value=True)

if st.button("🚀 START PROCESSING"):
    if st.session_state["credits"] >= 5:
        with st.spinner("AI က ဗီဒီယိုကို လေ့လာပြီး အသံသွင်းနေပါသည်..."):
            # Logic: Gemini Recap -> gTTS Voice -> Update Credit
            st.session_state["credits"] -= 5
            st.success("✅ အောင်မြင်ပါသည်။ ၅ Credits နုတ်ယူလိုက်ပါပြီ။")
            # အသံဖိုင်နှင့် Video Output ကို ဒီနေရာတွင် ပြပေးပါမည်
    else:
        st.error("❌ Credit မလုံလောက်ပါ။ ကျေးဇူးပြု၍ ဖြည့်သွင်းပါ။")

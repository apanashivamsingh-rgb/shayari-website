import streamlit as st
import json
import os
from datetime import datetime
from streamlit_lottie import st_lottie
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import base64
from PIL import Image
from io import BytesIO

# --- 🌹 SETTINGS (Yahan details check karein) ---
# --- SETTINGS (Secrets for Security) ---
DB_FILE = "shayari_db.json"

# Ye lines Streamlit Cloud ki 'tijori' se password uthayengi
try:
    SENDER_EMAIL = st.secrets["GMAIL_USER"]
    SENDER_PASSWORD = st.secrets["GMAIL_PASSWORD"]
except:
    # Agar aap abhi local chala rahe hain to ye error nahi dega
    SENDER_EMAIL = "apnashivamsingh@gmail.com" 
    SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"

# Photo ka path (GitHub par upload karne ke baad ye likhna)
PHOTO_PATH = "Atul_Ki_Photo.jpeg"

# --- 📁 DATABASE & UTILS (Data hamesha ke liye save) ---
def load_data():
    if not os.path.exists(DB_FILE):
        return {"shayaris": [], "subscribers": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

def get_base64_image(image_path):
    """Local photo ko browser-friendly format mein badalne ke liye"""
    try:
        img = Image.open(image_path)
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"
    except Exception as e:
        return "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 📩 REAL EMAIL LOGIC (Nayi shayari aate hi mail jayega) ---
def send_email_notification(subject, body, subscribers):
    if not subscribers: return
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        for recipient in subscribers:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.quit()
    except Exception as e:
        st.sidebar.error(f"Mail Error: {e}")

data = load_data()

# --- 🎨 PAGE CONFIG & ROMANTIC THEME ---
st.set_page_config(page_title="Shauk Se Shayar", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Serif+Devanagari:wght@400;700&display=swap');
    
    /* Pure website ka Dark Romantic Vibe */
    .stApp { background: linear-gradient(to bottom, #1a0505, #000000); color: #f5e6e6; }
    
    /* Sidebar Glassmorphism effect */
    section[data-testid="stSidebar"] { 
        background: rgba(44, 8, 8, 0.6) !important; 
        backdrop-filter: blur(15px); 
        border-right: 1px solid rgba(255, 77, 77, 0.3); 
    }
    
    /* Heading Styles */
    .hindi-title { 
        font-family: 'Noto Serif Devanagari', serif; 
        font-size: 75px; color: #ff4d4d; 
        text-align: center; 
        text-shadow: 0px 0px 15px #ff0000; 
        margin-bottom: -10px; 
    }
    
    .romantic-font { 
        font-family: 'Dancing Script', cursive; 
        font-size: 26px; color: #d4af37; 
        text-align: center; 
        margin-bottom: 40px; 
    }

    /* Shayari Card Styling */
    .shayari-card { 
        background: rgba(255, 255, 255, 0.03); 
        padding: 40px; border-radius: 25px; 
        border-left: 5px solid #ff4d4d; 
        backdrop-filter: blur(8px); 
        margin-bottom: 35px; 
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5); 
    }

    /* Floating Photo Animation */
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    .romantic-profile-photo { 
        width: 280px; height: 280px; 
        border-radius: 50%; 
        object-fit: cover; 
        border: 3px solid #ff4d4d; 
        box-shadow: 0px 0px 30px rgba(255, 77, 77, 0.7); 
        animation: float 5s ease-in-out infinite; 
        display: block; margin: auto; 
    }
    
    .sidebar-quote { 
        font-family: 'Dancing Script', cursive; 
        color: #d4af37; font-size: 18px; 
        text-align: center; padding: 10px; 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        border-radius: 10px; background: rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🍷 SIDEBAR NAVIGATION (Cool & Dynamic) ---
with st.sidebar:
    lottie_romance = load_lottieurl("https://lottie.host/e2d0981b-5683-4903-999d-16f316238b97/D7S3P0pGfK.json")
    if lottie_romance: st_lottie(lottie_romance, height=180)
    
    st.markdown("<h2 style='text-align:center; color:#ff4d4d; font-family:Dancing Script;'>Mehfil-e-Khaas</h2>", unsafe_allow_html=True)
    
    quotes = ["Poetry is the mathematics of feelings.", "Ishq, Intezaar aur IIT...", "Where logic ends, Shayari begins."]
    st.markdown(f'<p class="sidebar-quote">"{random.choice(quotes)}"</p>', unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Chaliye...", ["📜 Home (शायरी फ़ीड)", "👨‍🎓 The Shayar (Profile)", "🔐 Kavi's Desk (Admin)"])
    st.divider()
    st.caption("© 2026 Shauk Se Shayar | IIT Delhi Alumnus")

# --- 🏠 PAGE 1: HOME (Subke dekhne ke liye) ---
if page == "📜 Home (शायरी फ़ीड)":
    st.markdown('<h1 class="hindi-title">शौक़ से शायर</h1>', unsafe_allow_html=True)
    st.markdown('<p class="romantic-font">Written with numbers, felt with heart...</p>', unsafe_allow_html=True)
    st.divider()
    
    if not data["shayaris"]:
        st.info("Abhi mehfil khali hai... Kavi sahab kuch naya soch rahe hain.")
    else:
        col_l, col_m, col_r = st.columns([1, 4, 1])
        with col_m:
            for item in reversed(data["shayaris"]):
                st.markdown(f"""
                    <div class="shayari-card">
                        <small style="color:#ff4d4d; font-weight:bold;">📅 {item['date']}</small>
                        <h2 style="color:#d4af37; font-family:Dancing Script; font-size:32px;">{item['title']}</h2>
                        <p style="font-size:22px; line-height:1.8; font-family:Noto Serif Devanagari; white-space:pre-wrap;">{item['content']}</p>
                    </div>
                """, unsafe_allow_html=True)

# --- 👨‍🎓 PAGE 2: PROFILE (Unique & Advanced) ---
elif page == "👨‍🎓 The Shayar (Profile)":
    st.markdown("<h1 style='text-align:center; color:#ff4d4d; text-shadow: 0px 0px 10px #ff0000;'>The Mathematician's Soul</h1>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1.2, 1.5], gap="large")
    with col_a:
        # Base64 Fix: Photo bina error ke dikhegi
        image_base64 = get_base64_image(PHOTO_PATH)
        st.markdown(f'<img src="{image_base64}" class="romantic-profile-photo"><p style="text-align:center; margin-top:20px; font-family:Dancing Script; color:#d4af37; font-size:24px;">~ Kavi Sahab</p>', unsafe_allow_html=True)
        st.divider()
        st.markdown("<p style='color:#ff4d4d; font-weight:bold;'>The Balance of Life:</p>", unsafe_allow_html=True)
        st.write("Complex Analysis & Logic"); st.progress(95)
        st.write("Urdu Ghazals & Poetry"); st.progress(100)
    
    with col_b:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border: 1px solid rgba(212, 175, 55, 0.2);">
            <h3 style="color:#d4af37; font-family:Dancing Script;">From Equations to Emotions</h3>
            <p>Doston, IIT Delhi (M.Sc. Maths) ke campus mein equations solve karte-karte kab shayari shuru hui, pata hi nahi chala. Logic defines my degree, but Shayari defines my soul.</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.subheader("📬 Khabar Pane Ke Liye (Newsletter)")
        sub_email = st.text_input("Enter Email to join the circle:")
        if st.button("Subscribe Now"):
            if sub_email and "@" in sub_email:
                if sub_email not in data["subscribers"]:
                    data["subscribers"].append(sub_email); save_data(data)
                    st.success("Dosti pakki! Subscribed successfully.")
                else: st.warning("Aap pehle se hi hamare dost hain!")

# --- 🔐 PAGE 3: ADMIN (Nayi shayari yahan se dalo) ---
elif page == "🔐 Kavi's Desk (Admin)":
    st.title("🔐 Post New Content")
    pw = st.text_input("Secret Code dalo", type="password")
    
    if pw == "iitd_love": # <--- Password check
        with st.form("admin_form"):
            t = st.text_input("Title of the Piece")
            c = st.text_area("Write in Hindi/English...", height=300)
            if st.form_submit_button("Post & Email Everyone 🚀"):
                if t and c:
                    new_post = {"title": t, "content": c, "date": datetime.now().strftime("%d %B, %Y")}
                    data["shayaris"].append(new_post); save_data(data)
                    
                    # ACTUAL NOTIFICATION
                    email_msg = f"Nayi Shayari: {t}\n\n{c}\n\nPadhne ke liye visit karein: Shauk Se Shayar"
                    send_email_notification(f"Naya Kalam: {t}", email_msg, data["subscribers"])
                    
                    st.balloons(); st.success(f"Published! {len(data['subscribers'])} log ko email chala gaya.")
                else: st.error("Please fill both Title and Content!")
    elif pw: st.error("Galat Code! Sirf Kavi sahab ko ijazat hai.")

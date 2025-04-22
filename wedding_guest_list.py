import streamlit as st
import pandas as pd
import os

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Afifah ❤️ Syafiq Wedding List", layout="centered")

# ---- STYLE & MUSIC ----
st.markdown("""
    <style>
    body {
        background-color: #fff0f5;
    }
    .main {
        background: linear-gradient(to right, #fff0f5, #fce4ec);
        padding: 20px;
        border-radius: 15px;
    }
    h1, h2, h4 {
        color: #d63384;
        font-family: 'Georgia', serif;
        text-align: center;
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    </style>
    <div class='main'>
        <h1>🕌 Wedding Guest List</h1>
        <h2>Afifah ❤️ Syafiq</h2>
        <h4>27 December 2025</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <audio autoplay loop>
      <source src="https://www.bensound.com/bensound-music/bensound-love.mp3" type="audio/mp3">
      Your browser does not support the audio element.
    </audio>
""", unsafe_allow_html=True)

# ---- FILE PATH ----
file_path = "guest_list.csv"

# ---- STATE & AREA OPTIONS ----
state_area = {
    "Johor": ["Johor Bahru", "Batu Pahat", "Muar", "Kluang", "Segamat"],
    "Kedah": ["Alor Setar", "Sungai Petani", "Kulim", "Langkawi", "Baling"],
    "Kelantan": ["Kota Bharu", "Pasir Mas", "Tanah Merah", "Tumpat", "Machang"],
    "Melaka": ["Melaka Tengah", "Alor Gajah", "Jasin"],
    "Negeri Sembilan": ["Seremban", "Port Dickson", "Tampin"],
    "Pahang": ["Kuantan", "Temerloh", "Bentong", "Raub", "Jerantut"],
    "Penang": ["George Town", "Seberang Perai", "Bukit Mertajam"],
    "Perak": ["Ipoh", "Taiping", "Teluk Intan", "Lumut", "Sitiawan"],
    "Perlis": ["Kangar", "Arau", "Padang Besar"],
    "Sabah": ["Kota Kinabalu", "Sandakan", "Tawau", "Lahad Datu", "Keningau"],
    "Sarawak": ["Kuching", "Miri", "Sibu", "Bintulu", "Bau"],
    "Selangor": ["Shah Alam", "Petaling Jaya", "Klang", "Kajang", "Ampang"],
    "Terengganu": ["Kuala Terengganu", "Dungun", "Kemaman", "Besut", "Marang"],
    "W.P. Kuala Lumpur": ["Cheras", "Setapak", "Sentul", "Bukit Bintang"],
    "W.P. Labuan": ["Labuan Town", "Victoria"],
    "W.P. Putrajaya": ["Presint 1", "Presint 2", "Presint 3", "Presint 4"],
    "Other": []
}

# ---- USER TYPE ----
user_type = st.sidebar.selectbox("Login as", ["Family Member", "Admin (Me)"])

# ---- GUEST FORM ----
st.markdown("## ✍️ Add Guest")
name = st.text_input("Guest Name")
state = st.selectbox("State", list(state_area.keys()))

# --- Dynamic Area Input ---
if state == "Other":
    area = st.text_input("Enter your area")
else:
    area = st.selectbox("Area", state_area[state])

if st.button("Add Guest"):
    if name and area:
        new_row = pd.DataFrame([[name, state, area]], columns=["Name", "State", "Area"])
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
        df.to_csv(file_path, index=False)
        st.success(f"Guest '{name}' from {area}, {state} added successfully!")
    else:
        st.warning("Please fill in all fields.")

# ---- ADMIN VIEW ----
if user_type == "Admin (Me)":
    st.markdown("## 👀 View & Manage Guest List (Admin)")
    password = st.text_input("Enter Admin Password", type="password")

    if password == "familysahaja777":
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            # Display table with delete option
            for i in range(len(df)):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                col1.write(df.iloc[i]["Name"])
                col2.write(df.iloc[i]["State"])
                col3.write(df.iloc[i]["Area"])
                delete = col4.button("🗑️ Delete", key=f"del_{i}")
                if delete:
                    df = df.drop(i).reset_index(drop=True)
                    df.to_csv(file_path, index=False)
                    st.success("Guest deleted successfully!")
                    st.experimental_rerun()

            # Download CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Guest List", csv, "guest_list.csv", "text/csv")
        else:
            st.info("No guest data found.")
    elif password:
        st.error("Incorrect password.")

# ---- FOOTER ----
st.markdown("---")
st.markdown("<center><small>System Created by Aarif</small></center>", unsafe_allow_html=True)

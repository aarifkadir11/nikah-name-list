import streamlit as st
import pandas as pd
import os

# ----- PAGE CONFIG -----
st.set_page_config(page_title="Afifah ❤️ Syafiq Wedding List", layout="centered")

# ----- WEDDING STYLE -----
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
        <h1>💒 Wedding Guest List</h1>
        <h2>Afifah ❤️ Syafiq</h2>
        <h4>27 December 2025</h4>
    </div>
""", unsafe_allow_html=True)

# ----- MUSIC PLAYER -----
st.markdown("""
    <audio autoplay loop>
      <source src="https://www.bensound.com/bensound-music/bensound-love.mp3" type="audio/mp3">
      Your browser does not support the audio element.
    </audio>
""", unsafe_allow_html=True)

# ----- FILE SETUP -----
file_path = "guest_list.csv"

# ----- USER TYPE -----
user_type = st.sidebar.selectbox("Login as", ["Family Member", "Admin (Me)"])

# ----- GUEST FORM -----
st.markdown("## ✍️ Add Guest")
with st.form("form"):
    name = st.text_input("Guest Name")
    state = st.selectbox("State", [
        "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak",
        "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu", "W.P. Kuala Lumpur"
    ])
    submit = st.form_submit_button("Add Guest")

    if submit and name:
        new = pd.DataFrame([[name, state]], columns=["Name", "State"])
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, new], ignore_index=True)
        else:
            df = new
        df.to_csv(file_path, index=False)
        st.success(f"Guest '{name}' added!")

# ----- ADMIN VIEW -----
if user_type == "Admin (Me)":
    st.markdown("## 👀 View Guest List (Admin Only)")
    password = st.text_input("Admin Password", type="password")

    if password == "mypassword123":
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            st.dataframe(df.sort_values("State"))
            st.download_button("📥 Download List", df.to_csv(index=False), "guest_list.csv")
        else:
            st.info("No guests added yet.")
    elif password:
        st.error("Wrong password.")

# ----- FOOTER -----
st.markdown("---")
st.markdown("<center><small>System Create by Aarif</small></center>", unsafe_allow_html=True)

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

# ---- GUEST LIST FILE ----
file_path = "guest_list.csv"

# ---- STATE & AREA OPTIONS ----
state_area = {
    "Johor": ["Johor Bahru", "Batu Pahat", "Muar", "Segamat"],
    "Selangor": ["Shah Alam", "Petaling Jaya", "Klang"],
    "Pahang": ["Kuantan", "Temerloh", "Bentong"],
    "Kedah": ["Alor Setar", "Sungai Petani", "Kulim"],
    "Other": ["Other Area"]
}

# ---- USER TYPE ----
user_type = st.sidebar.selectbox("Login as", ["Family Member", "Admin (Me)"])

# ---- GUEST FORM ----
st.markdown("## ✍️ Add Guest")
with st.form("form"):
    name = st.text_input("Guest Name")
    state = st.selectbox("State", list(state_area.keys()))
    area = st.selectbox("Area", state_area[state])
    submit = st.form_submit_button("Add Guest")

    if submit and name:
        new_row = pd.DataFrame([[name, state, area]], columns=["Name", "State", "Area"])
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
        df.to_csv(file_path, index=False)
        st.success(f"Guest '{name}' added successfully!")

# ---- ADMIN VIEW ----
if user_type == "Admin (Me)":
    st.markdown("## 👀 View & Manage Guest List (Admin)")
    password = st.text_input("Enter Admin Password", type="password")

    if password == "familysahaja777":
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            # Display table with delete option
            for i in range(len(df)):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
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
st.markdown("<center><small>System Create by Aarif</small></center>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import os

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Afifah ❤️ Syafiq Wedding List", layout="centered", page_icon="🕌")

# ---- STYLE & MUSIC ----
st.markdown("""
<style>
  body { background-color: #fff0f5; }
  .main { background: linear-gradient(to right, #fff0f5, #fce4ec); padding:20px; border-radius:15px; }
  h1,h2,h4 { color:#d63384; font-family:Georgia, serif; text-align:center; animation:fadeIn 2s; }
  @keyframes fadeIn { from {opacity:0;} to {opacity:1;} }
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
</audio>
""", unsafe_allow_html=True)

# ---- DATA FILE ----
file_path = "guest_list.csv"

# ---- STATE & AREA DICT ----
state_area = {
  "Johor": ["Johor Bahru","Batu Pahat","Muar","Kluang","Segamat","Kota Tinggi","Kulai","Tangkak","Mersing","Pontian"],
  "Kedah": ["Alor Setar","Sungai Petani","Kulim","Langkawi","Baling"],
  "Kelantan": ["Kota Bharu","Pasir Mas","Tanah Merah","Tumpat","Machang"],
  "Melaka": ["Melaka Tengah","Alor Gajah","Jasin"],
  "Negeri Sembilan": ["Seremban","Port Dickson","Tampin","Jelebu","Rembau"],
  "Pahang": ["Kuantan","Temerloh","Bentong","Raub","Jerantut"],
  "Penang": ["George Town","Seberang Perai","Bukit Mertajam"],
  "Perak": ["Ipoh","Taiping","Teluk Intan","Lumut","Sitiawan"],
  "Perlis": ["Kangar","Arau","Padang Besar"],
  "Sabah": ["Kota Kinabalu","Sandakan","Tawau","Lahad Datu","Keningau"],
  "Sarawak": ["Kuching","Miri","Sibu","Bintulu","Bau"],
  "Selangor": ["Shah Alam","Petaling Jaya","Klang","Kajang","Ampang"],
  "Terengganu": ["Kuala Terengganu","Dungun","Kemaman","Besut","Marang"],
  "W.P. Kuala Lumpur": ["Cheras","Setapak","Sentul","Bukit Bintang"],
  "W.P. Labuan": ["Labuan Town","Victoria"],
  "W.P. Putrajaya": ["Presint 1","Presint 2","Presint 3","Presint 4"],
  "Other": []
}

# ---- ROLE SELECTION ----
role = st.sidebar.selectbox("Login as", ["Family Member","Admin (Me)"])

# ---- ADD GUEST ----
st.markdown("## ✍️ Add Guest")
name = st.text_input("Guest Name")
state = st.selectbox("State", list(state_area.keys()))
area = st.text_input("Area") if state=="Other" else st.selectbox("Area", state_area[state])
if st.button("Add Guest"):
    if name and area:
        df_new = pd.DataFrame([[name, state, area]], columns=["Name","State","Area"])
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, df_new], ignore_index=True)
        else:
            df = df_new
        df.to_csv(file_path, index=False)
        st.success(f"Added {name} ({area}, {state})")
    else:
        st.warning("Fill all fields.")

# ---- ADMIN VIEW ----
if role=="Admin (Me)":
    st.markdown("## 👀 Manage Guest List")
    pwd = st.text_input("Admin Password", type="password")
    if pwd=="familysahaja777":
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Search + Filter
            name_filter = st.text_input("🔍 Search by Name")
            state_filter = st.selectbox("📌 Filter by State", ["All"]+list(state_area.keys()))
            df_filtered = df
            if name_filter:
                df_filtered = df_filtered[df_filtered["Name"].str.contains(name_filter, case=False)]
            if state_filter!="All":
                df_filtered = df_filtered[df_filtered["State"]==state_filter]
            st.markdown(f"**Total: {len(df_filtered)}**")
            for i,row in df_filtered.iterrows():
                c1,c2,c3,c4 = st.columns([3,2,2,1])
                c1.write(row["Name"]); c2.write(row["State"]); c3.write(row["Area"])
                if c4.button("🗑️", key=f"del{i}"):
                    idx = df.index[df["Name"]==row["Name"]][0]
                    df = df.drop(idx).reset_index(drop=True)
                    df.to_csv(file_path, index=False)
                    st.experimental_rerun()
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download CSV", csv, "guest_list.csv", "text/csv")
        else:
            st.info("No data yet.")
    elif pwd:
        st.error("Wrong password.")

# ---- FOOTER ----
st.markdown("---")
st.markdown("<div style='text-align:center; color:gray; font-size:13px;'>System Created by Aarif • Powered by Streamlit</div>", unsafe_allow_html=True)

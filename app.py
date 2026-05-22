import streamlit as st
import pandas as pd
import altair as alt
from team.team_page import show_team_page
from datetime import datetime, timedelta
from functions.week_helpers import show_weekly_view
from functions.productivity_helpers import show_productivity_view
import html

from utils.data_manager import DataManager
from utils.login_manager import LoginManager
from pages.home_page import show_home_page

st.set_page_config(page_title="Lernapp", page_icon=":material/home:")

# Optional: Globales CSS
st.markdown("""
<style>
html, body, .stApp {
    height: 100%;
    background: linear-gradient(135deg, #dbeafe, #fce7f3);
    background-attachment: fixed;
}
.stAppViewContainer, .main, .block-container {
    background: transparent !important;
}
.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ------------------------- LOGIN --------------------------
# ---------------------------------------------------------
data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="lernapp"
)
login_manager = LoginManager(data_manager)
login_manager.login_register()
st.session_state["username"]

# ---------------------------------------------------------
# --------------------- NAVIGATION -------------------------
# ---------------------------------------------------------
# Initialisiere die Seite beim ersten Laden
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h1 style='color:#7c3aed;'>kipi✦</h1>", unsafe_allow_html=True)
    if st.button("🏠 Home"):
        st.session_state.page = "Home"
    if st.button("📅 Woche"):
        st.session_state.page = "Woche"
    if st.button("✅ Aufgaben"):
        st.session_state.page = "Aufgaben"
    if st.button("📚 Prüfungen"):
        st.session_state.page = "Prüfungen"
    if st.button("⭐ Punkte"):
        st.session_state.page = "Punkte"
    if st.button("👥 Team"):
        st.session_state.page = "Team"
    st.markdown(
        "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;margin-top:32px;'>"
        "<span style='font-size:24px;'>🔥</span>"
        "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
        "</div>", unsafe_allow_html=True
    )
    st.button("Logout", use_container_width=True)

# ---------------------------------------------------------
# --------------------- SEITENLOGIK ------------------------
# ---------------------------------------------------------
if st.session_state.page == "Home":
    show_home_page()
elif st.session_state.page == "Woche":
    show_weekly_view(data_manager)
elif st.session_state.page == "Aufgaben":
    st.write("Hier kommt deine Aufgaben-Ansicht.")
elif st.session_state.page == "Prüfungen":
    st.write("Hier kommt deine Prüfungs-Ansicht.")
elif st.session_state.page == "Punkte":
    show_productivity_view()
elif st.session_state.page == "Team":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    show_team_page()
    st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st

# Pages
from pages.home_page import show_home_page
from pages.weekly_page import show_weekly_page
from pages.tasks_page import show_tasks_page
from team.team_page import show_team_page
from pages.exams_page import show_exams_page
from pages.point_system_page import show_point_system_page
from pages.profile_page import show_profile_page

from utils.data_manager import DataManager

import html

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

from pages.home_page import show_home_page, show_profile_sidebar_button, show_sidebar_nav

# ---------------------------------------------------------
# 4.1 Login‑System und Zugriffskontrolle
# ---------------------------------------------------------

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="lernapp")
login_manager = LoginManager(data_manager)
login_manager.login_register()
show_profile_sidebar_button()
if "username" not in st.session_state or st.session_state.username is None:
    st.stop()

show_sidebar_nav()

# Standardseite setzen
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------------------------------------
# 4.2 Benutzeroberfläche und visuelles Design (CSS)
# ---------------------------------------------------------

st.set_page_config(page_title="lernapp", page_icon=":material/home:")
st.markdown("""
<style>

html, body, .stApp {
    height: 100%;
    background: linear-gradient(135deg, #dbeafe, #fce7f3);
    background-attachment: fixed;}

/* Entfernt ALLE weißen Balken */
.stAppViewContainer, .main, .block-container {
    background: transparent !important;}

/* Cards wirken wie schwebende Elemente */
.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 30px;}

/* Eingabefelder */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
    border: 1px solid #d0d0d0;
    padding: 10px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(6px);}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #9333ea);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: bold;
    border: none;
    transition: 0.2s;}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #4338ca, #7e22ce);}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Erweiterte CSS‑Gestaltung (Buttons, Themes, Layout)
# ---------------------------------------------------------

st.markdown(f"""
<style>


</style>
""", unsafe_allow_html=True)
# Neue Farben für die violetten Buttons
BUTTON_PRIMARY = "#14b8a6"      # Türkis
BUTTON_HOVER = "#0f766e"        # Dunkler beim Hover
BUTTON_TEXT = "#ffffff"

st.markdown(f"""
<style>

/* Sidebar Buttons links */
.stButton > button {{
    background-color: {BUTTON_PRIMARY};
    color: {BUTTON_TEXT};
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.3s;
}}

/* Hover Effekt */
.stButton > button:hover {{
    background-color: {BUTTON_HOVER};
    color: white;
}}

/* Obere Theme Buttons */
.theme-btn {{
    background-color: {BUTTON_PRIMARY};
    color: white;
    border-radius: 14px;
    padding: 12px 24px;
    font-weight: bold;
    border: none;
}}

.theme-btn:hover {{
    background-color: {BUTTON_HOVER};
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

    .main {
        padding-top: 20px;
    }
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
        border: 1px solid #d0d0d0;
        padding: 8px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }

    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Seitenrouting und App‑Struktur
# ---------------------------------------------------------

# Session State initialisieren
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "theme" not in st.session_state:
    st.session_state.theme = "default"


if st.session_state.page == "Home":
    show_home_page()
elif st.session_state.page == "Woche":
    from pages.weekly_page import show_weekly_page
    show_weekly_page()
elif st.session_state.page == "Aufgaben":
    show_tasks_page()
elif st.session_state.page == "Prüfungen":
    show_exams_page()
elif st.session_state.page == "Team":
    show_team_page()
elif st.session_state.page == "Punkte":
    show_point_system_page()
elif st.session_state.page == "Profil":
    show_profile_page()




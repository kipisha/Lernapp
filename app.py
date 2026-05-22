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
st.markdown("""
<style>

html, body, .stApp {
    height: 100%;
    background: linear-gradient(135deg, #dbeafe, #fce7f3);
    background-attachment: fixed;
}

/* Entfernt ALLE weißen Balken */
.stAppViewContainer, .main, .block-container {
    background: transparent !important;
}

/* Cards wirken wie schwebende Elemente */
.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

/* Eingabefelder */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
    border: 1px solid #d0d0d0;
    padding: 10px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(6px);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #9333ea);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: bold;
    border: none;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #4338ca, #7e22ce);
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ------------------------- CSS ----------------------------
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
# ------------------------- LOGIN --------------------------
# ---------------------------------------------------------

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="lernapp"
)
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Session State initialisieren
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "theme" not in st.session_state:
    st.session_state.theme = "default"

# immer Sidebar anzeigen
def show_sidebar_nav():
    colors = get_theme_colors()

    sidebar_bg = colors["card"]
    primary = colors["primary"]
    text = colors["text"]

    st.markdown(
        f"""
        <style>
        /* Sidebar Hintergrund */
        [data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            padding: 20px;
        }}

        /* Sidebar Titel */
        .sidebar-title {{
            font-size: 32px;
            font-weight: 800;
            color: {primary};
            margin-bottom: 20px;
        }}

        /* Navigation Buttons */
        .sidebar-btn > button {{
            width: 100%;
            background: {primary};
            color: white;
            border-radius: 12px;
            padding: 10px 18px;
            font-weight: 600;
            border: none;
            margin-bottom: 10px;
            transition: 0.2s ease;
        }}

        .sidebar-btn > button:hover {{
            background: {colors["secondary"]};
            transform: scale(1.03);
        }}

        /* Streak Box */
        .streak-box {{
            background: rgba(255,255,255,0.5);
            padding: 14px;
            border-radius: 12px;
            margin-top: 20px;
            display: flex;
            gap: 12px;
            align-items: center;
        }}

        .streak-box span {{
            font-size: 28px;
        }}

        .streak-text {{
            font-size: 14px;
            color: {text};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("<div class='sidebar-title'>kipi✦</div>", unsafe_allow_html=True)

        nav_items = [
            ("🏠 Home", "Home"),
            ("📅 Woche", "Woche"),
            ("✅ Aufgaben", "Aufgaben"),
            ("📚 Prüfungen", "Prüfungen"),
            ("📈 Produktivität", "Produktivität"),
            ("⭐ Punkte", "Punkte"),
            ("📝 Notizen", "Notizen"),
            ("🎯 Ziele", "Ziele"),
            ("👥 Team", "Team"),
        ]

        for label, page in nav_items:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()

        st.markdown(
            f"""
            <div class="streak-box">
                <span>🔥</span>
                <div>
                    <b>{st.session_state.get("streak", 7)} Tage Streak</b><br>
                    <span class="streak-text">Weiter so!</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            st.session_state.username = None
            st.rerun()


        # Streak Box
        st.markdown(
            f"""
            <div style='background:{colors['card']}; padding:12px; border-radius:12px;
                 display:flex; align-items:center; gap:10px;'>
                <span style='font-size:26px;'>🔥</span>
                <div>
                    <b>{st.session_state.get("streak", 7)} Tage Streak</b><br>
                    <span style='font-size:12px; color:#666;'>Weiter so!</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Logout
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            st.session_state.username = None
            st.rerun()



if st.session_state.page == "Home":
    show_home_page()
elif st.session_state.page == "Woche":
    from pages.weekly_page import show_weekly_page
    show_weekly_page()



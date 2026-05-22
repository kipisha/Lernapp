import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Pages
from pages.home_page import show_home_page
from pages.weekly_page import show_weekly_page
from team.team_page import show_team_page

# Helpers
from functions.week_helpers import show_weekly_view
from functions.productivity_helpers import show_productivity_view

# Utils
from utils.data_manager import DataManager
from utils.login_manager import LoginManager


# ---------------------------------------------------------
# ------------------------- PAGE CONFIG --------------------
# ---------------------------------------------------------
st.set_page_config(page_title="Lernapp", page_icon=":material/home:")


# ---------------------------------------------------------
# ------------------------- THEME SYSTEM -------------------
# ---------------------------------------------------------

if "theme" not in st.session_state:
    st.session_state["theme"] = "Cozy"

THEMES = {
    "Cozy": {
        "primary": "#E26DBF",
        "secondary": "#eb73e9",
        "background": "#ffe6f6",
        "card": "#fffadc",
        "text": "#000000",
        "button": "#ec4899"
    },
    "Focus": {
        "primary": "#337b1d",
        "secondary": "#8abe93",
        "background": "#d4f0cc",
        "card": "#e8f5e9",
        "text": "#000000",
        "button": "#22c55e"
    },
    "Energy": {
        "primary": "#fca311",
        "secondary": "#38bdf8",
        "background": "#fef9c3",
        "card": "#fffbea",
        "text": "#22223b",
        "button": "#facc15"
    },
    "Minimal": {
        "primary": "#000000",
        "secondary": "#1f2937",
        "background": "#fff9ec",
        "card": "#f5f5f5",
        "text": "#222",
        "button": "#4b5563"
    }
}

def get_theme_colors():
    return THEMES.get(st.session_state.theme, THEMES["Cozy"])

def apply_theme():
    c = get_theme_colors()

    st.markdown(f"""
        <style>
        .stApp {{
            background: {c['background']} !important;
            color: {c['text']};
        }}

        .card {{
            background: {c['card']};
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 24px;
        }}

        .stProgress > div > div > div > div {{
            background-image: linear-gradient(90deg, {c['primary']} 0%, {c['secondary']} 100%);
        }}

        .stButton > button {{
            background-color: {c['button']} !important;
            color: white !important;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
            transition: 0.2s;
        }}

        .stButton > button:hover {{
            filter: brightness(0.9);
            transform: scale(1.02);
        }}
        </style>
    """, unsafe_allow_html=True)

apply_theme()


# ---------------------------------------------------------
# ------------------------- LOGIN --------------------------
# ---------------------------------------------------------

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="lernapp"
)

login_manager = LoginManager(data_manager)
login_manager.login_register()


# ---------------------------------------------------------
# ------------------------- SIDEBAR NAV --------------------
# ---------------------------------------------------------

def show_sidebar_nav():
    colors = get_theme_colors()

    with st.sidebar:
        # Logo
        st.markdown(
            f"<h1 style='color:{colors['primary']}; margin-bottom: 10px;'>kipi✦</h1>",
            unsafe_allow_html=True
        )

        # Navigation
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

        st.markdown("---")

        # Streak Box
        streak = data_manager.load("streak.json") or 0
        st.markdown(
            f"""
            <div style='background:{colors['card']}; padding:12px; border-radius:12px;
                 display:flex; align-items:center; gap:10px;'>
                <span style='font-size:26px;'>🔥</span>
                <div>
                    <b>{streak} Tage Streak</b><br>
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


# Sidebar anzeigen
show_sidebar_nav()


# ---------------------------------------------------------
# ------------------------- PAGE ROUTING -------------------
# ---------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    show_home_page()

elif st.session_state.page == "Woche":
    show_weekly_page()

elif st.session_state.page == "Team":
    show_team_page()



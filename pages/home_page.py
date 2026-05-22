import streamlit as st
from datetime import datetime, timedelta
from pages.themes_page import get_theme_colors, apply_theme, show_theme_switcher

def show_home_page():
    # --- THEME INITIALIZATION ---
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#7c3aed;'>smartplan</h1>", unsafe_allow_html=True)
        
        # Navigation Buttons
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
        if st.button("📅 Woche", use_container_width=True):
            st.session_state.page = "Woche"
            st.rerun()
        if st.button("✅ Aufgaben", use_container_width=True):
            st.session_state.page = "Aufgaben"
            st.rerun()
        if st.button("📚 Prüfungen", use_container_width=True):
            st.session_state.page = "Prüfungen"
            st.rerun()
        if st.button("⭐ Punkte", use_container_width=True):
            st.session_state.page = "Punkte"
            st.rerun()
        if st.button("👥 Team", use_container_width=True):
            st.session_state.page = "Team"
            st.rerun()
        
        st.markdown("---")
        st.markdown(
            "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;'>"
            "<span style='font-size:24px;'>🔥</span>"
            "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
            "</div>", unsafe_allow_html=True
        )
        if st.button("Logout", use_container_width=True):
            st.session_state.username = None
            st.rerun()

    # --- APPLY THEME ---
    apply_theme()
    colors = get_theme_colors()

    # --- THEME SWITCHER ---
    show_theme_switcher()

    # --- HEADER ---
    st.markdown(
        f"""
        <div style='margin-bottom: 16px;'>
            <span style='color:{colors['primary']};font-size:14px;font-weight:bold;'>HOME / STARTSEITE</span>
            <h2 style='margin:0;color:{colors['text']};'>Hey Lara! 👋</h2>
            <span style='color:#b0aeb8;'>Schön, dass du da bist. Bereit für einen produktiven Tag?</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- PROGRESS & OVERVIEW ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### Tagesfortschritt")
        st.progress(0.7)
        st.markdown(f"<span style='color:{colors['primary']};font-size:32px;font-weight:bold;'>70%</span>", unsafe_allow_html=True)
        st.caption("Super gemacht! Weiter so! 💪")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### Deine Übersicht")
        st.markdown(
            """
            <div style='display:flex;gap:24px;justify-content:center;'>
                <div style='text-align:center;'><div style='font-size:24px;'>📅</div><b>3</b><br><span style='font-size:12px;'>Aufgaben</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>📚</div><b>1</b><br><span style='font-size:12px;'>Prüfung</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>⭐</div><b>5</b><br><span style='font-size:12px;'>Stufe</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>🏆</div><b>120</b><br><span style='font-size:12px;'>Punkte</span></div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### Motivation für dich")
        st.info("„Disziplin heute, Stolz morgen.,,")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TASKS & EXAMS ---
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Aufgabe")
        st.success("Mathe Hausaufgaben\n\nBis morgen, 15:00")
        st.button("Jetzt starten")
        st.markdown("</div>", unsafe_allow_html=True)
    with col5:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Prüfung")
        st.warning("Deutsch Prüfung\n\nFreitag, 17. Mai\n\nIn 3 Tagen")
        st.button("Prüfung ansehen")
        st.markdown("</div>", unsafe_allow_html=True)
    with col6:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Motivation für dich")
        st.markdown("🏁", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- WEEK OVERVIEW ---
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### Deine Woche auf einen Blick")
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    today = datetime.now()
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**{days[i]}**")
            st.markdown(f"{(today + timedelta(days=i)).day}")
            st.progress([0.7, 0.3, 0.5, 0.8, 0.6, 0.2, 0.1][i])
    st.markdown(f"<div style='text-align:right;'><a href='#' style='color:{colors['primary']};text-decoration:underline;'>Zur Wochenübersicht</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
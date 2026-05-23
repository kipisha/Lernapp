import streamlit as st
from datetime import datetime, timedelta
from pages.themes_page import get_theme_colors, apply_theme, show_theme_switcher

def show_sidebar_nav():
    """Rendert ausschließlich die Sidebar-Navigation auf der linken Seite"""
    colors = get_theme_colors()
    
    # --- DYNAMIC SIDEBAR NAVIGATION STYLING ---
    st.markdown("""
<style>
.motivation-box {
    background: white;
    border-radius: 12px;
    width: 110px;        /* feste Breite */
    height: 110px;       /* feste Höhe */
    padding: 10px;
    margin: 0 auto;      /* zentriert */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    text-align: center;
}

.motivation-icon {
    font-size: 20px;
    margin-bottom: 4px;
}

.motivation-text {
    font-size: 10px;
    font-weight: 600;
    color: #444;
    line-height: 1.2;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Entfernt gelben Hintergrund hinter Emojis */
span, div {
    background: none !important;
}
</style>
""", unsafe_allow_html=True)



    # --- SIDEBAR NAVIGATION ---
with st.sidebar:
        st.markdown("<h1 style='color:#7c3aed;'>smartplan ✦</h1>", unsafe_allow_html=True)
        
        nav_items = [
            ("🏠 Home", "Home"),
            ("📅 Woche", "Woche"),
            ("✅ Aufgaben", "Aufgaben"),
            ("📚 Prüfungen", "Prüfungen"),
            ("⭐ Punkte", "Punkte"),
            ("👥 Team", "Team"),
        ]
        
        for label, page in nav_items:
            if st.button(label, use_container_width=True):
                st.session_state.page = page
                st.rerun()
        
        st.markdown("---")
        st.markdown(
            "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;'>"
            "<span style='font-size:24px;'>🔥</span>"
            "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
            "</div>",
            unsafe_allow_html=True
        )

        if st.button("Logout", use_container_width=True):
            st.session_state.username = None
            st.rerun()

import random
from datetime import date
st.markdown("""
<style>
.motivation-box {
    background: white;
    border-radius: 12px;
    padding: 12px;
    width: 100%;
    aspect-ratio: 1 / 1;
    max-width: 130px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    text-align: center;
}

.motivation-icon {
    font-size: 22px;
    margin-bottom: 6px;
}

.motivation-text {
    font-size: 11px;
    font-weight: 600;
    color: #444;
    line-height: 1.3;
}
</style>
""", unsafe_allow_html=True)



MOTIVATION_LIST = [
    "Disziplin heute, Stolz morgen.",
    "Auch kleine Schritte bringen dich ans Ziel.",
    "Du bist stärker als deine Ausreden.",
    "Jeder Tag ist eine neue Chance.",
    "Erfolg beginnt im Kopf.",
    "Mach es für dein zukünftiges Ich.",
    "Wenn du aufgibst, wird es nie passieren.",
    "Heute ist ein guter Tag, um anzufangen.",
    "Du wächst an deinen Herausforderungen.",
    "Konstanz schlägt Talent."
]

def get_daily_motivation():
    today = date.today().toordinal()
    random.seed(today)
    return random.choice(MOTIVATION_LIST)

def show_home_page():
    """Rendert den Hauptinhalt der Startseite im Zentrum"""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    colors = get_theme_colors()
    apply_theme()

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
                <div style='text-align:center;'><div style='font-size:24px;'>🗓️</div><b>3</b><br><span style='font-size:12px;'>Aufgaben</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>📚</div><b>1</b><br><span style='font-size:12px;'>Prüfung</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>⭐</div><b>5</b><br><span style='font-size:12px;'>Stufe</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>🏆</div><b>120</b><br><span style='font-size:12px;'>Punkte</span></div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        motivation = get_daily_motivation()
    st.markdown(f"""
        <div class="motivation-box">
            <div class="motivation-icon">🏁</div>
            <div class="motivation-text">„{motivation}“</div>
        </div>
    """, unsafe_allow_html=True)






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

    motivation = get_daily_motivation()
    st.success(f"„{motivation}“")

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


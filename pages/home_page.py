import streamlit as st
from datetime import datetime, timedelta

def show_home_page():
    # Theme-Auswahl (Session-State)
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    theme = st.session_state.theme

    # Theme-Auswahl UI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌸 Cozy"):
            st.session_state.theme = "Cozy"
    with col2:
        if st.button("⚡ Focus"):
            st.session_state.theme = "Focus"
    with col3:
        if st.button("🌞 Energy"):
            st.session_state.theme = "Energy"
    with col4:
        if st.button("📚 Minimal"):
            st.session_state.theme = "Minimal"

    # Theme-Styles anwenden
    if theme == "Cozy":
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #fdf6f0, #f3e8ff, #ffe4ef) !important;
                color: #6d4c41;
            }
            .card {background: #fff7f0cc !important; border-radius: 22px;}
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Focus":
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #1e1b4b, #7c3aed, #a5b4fc) !important;
                color: #fff;
            }
            .card {background: #312e81cc !important; border-radius: 18px;}
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Energy":
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #fef9c3, #fca311, #38bdf8) !important;
                color: #22223b;
            }
            .card {background: #fffbeacc !important; border-radius: 18px;}
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Minimal":
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #fff, #e5e7eb) !important;
                color: #222;
            }
            .card {background: #f5f5f5cc !important; border-radius: 10px;}
            </style>
        """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h1 style='color:#7c3aed;'>kipi✦</h1>", unsafe_allow_html=True)
        st.markdown("### Navigation")
        menu = [
            "Home", "Woche", "Aufgaben", "Prüfungen", "Produktivität",
            "Punkte", "Notizen", "Ziele", "Team"
        ]
        for item in menu:
            st.button(item, use_container_width=True)
        st.markdown("---")
        st.markdown(
            "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;'>"
            "<span style='font-size:24px;'>🔥</span>"
            "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
            "</div>", unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Logout", use_container_width=True)

    # --- Header ---
    st.markdown(
        "<div style='display:flex;justify-content:space-between;align-items:center;'>"
        "<div>"
        "<span style='color:#7c3aed;font-size:12px;font-weight:bold;'>HOME / STARTSEITE</span>"
        "<h2>Hey Lara! 👋</h2>"
        "<span style='color:#b0aeb8;'>Schön, dass du da bist. Bereit für einen produktiven Tag?</span>"
        "</div>"
        "<div style='display:flex;gap:16px;background:#fff;border-radius:18px;padding:12px 32px;box-shadow:0 2px 8px #f3eaff;'>"
        "<div style='text-align:center;'><div style='font-size:24px;'>🌸</div><div style='font-size:12px;'>Cozy</div></div>"
        "<div style='text-align:center;'><div style='font-size:24px;'>⚡</div><div style='font-size:12px;'>Focus</div></div>"
        "<div style='text-align:center;'><div style='font-size:24px;'>🔆</div><div style='font-size:12px;'>Energy</div></div>"
        "<div style='text-align:center;'><div style='font-size:24px;'>📖</div><div style='font-size:12px;'>Minimal</div></div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.write("")

    # --- Progress & Overview ---
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown("#### Tagesfortschritt")
        st.progress(0.7)
        st.markdown("<span style='color:#7c3aed;font-size:32px;font-weight:bold;'>70%</span>", unsafe_allow_html=True)
        st.caption("Super gemacht! Weiter so! 💪")
    with col2:
        st.markdown("#### Deine Übersicht")
        st.markdown(
            "<div style='display:flex;gap:24px;'>"
            "<div style='text-align:center;'><div style='font-size:24px;'>📅</div><b>3</b><br><span style='font-size:12px;'>Aufgaben</span></div>"
            "<div style='text-align:center;'><div style='font-size:24px;'>📚</div><b>1</b><br><span style='font-size:12px;'>Prüfung</span></div>"
            "<div style='text-align:center;'><div style='font-size:24px;'>⭐</div><b>5</b><br><span style='font-size:12px;'>Stufe</span></div>"
            "<div style='text-align:center;'><div style='font-size:24px;'>🏆</div><b>120</b><br><span style='font-size:12px;'>Punkte</span></div>"
            "</div>", unsafe_allow_html=True
        )
    with col3:
        st.markdown("#### Motivation für dich")
        st.info("„Disziplin heute, Stolz morgen.”")

    # --- Tasks & Exams ---
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("##### Nächste Aufgabe")
        st.success("Mathe Hausaufgaben\n\nBis morgen, 15:00")
        st.button("Jetzt starten")
    with col5:
        st.markdown("##### Nächste Prüfung")
        st.warning("Deutsch Prüfung\n\nFreitag, 17. Mai\n\nIn 3 Tagen")
        st.button("Prüfung ansehen")
    with col6:
        st.markdown("##### Motivation für dich")
        st.markdown("🏁", unsafe_allow_html=True)

    # --- Week Overview ---
    st.markdown("#### Deine Woche auf einen Blick")
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    today = datetime.now()
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**{days[i]}**")
            st.markdown(f"{(today + timedelta(days=i)).day}")
            st.progress([0.7, 0.3, 0.5, 0.8, 0.6, 0.2, 0.1][i])

    st.markdown("<div style='text-align:right;'><a href='#' style='color:#7c3aed;text-decoration:underline;'>Zur Wochenübersicht</a></div>", unsafe_allow_html=True)
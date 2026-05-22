import streamlit as st
from datetime import datetime, timedelta

def show_home_page():
    # --- Theme / Mood Switcher ---
    st.markdown("""
        <style>
        .sidebar .sidebar-content {width: 300px;}
        .sidebar .sidebar-content, .stApp {background: #faf8ff;}
        .sidebar .sidebar-content {padding-top: 32px;}
        .sidebar .sidebar-content h1 {font-size: 2rem;}
        .sidebar .sidebar-content .nav-btn {
            background: #f3eaff;
            color: #7c3aed;
            border-radius: 12px;
            margin-bottom: 8px;
            font-weight: bold;
            border: none;
            width: 100%;
            padding: 10px 0;
        }
        .sidebar .sidebar-content .nav-btn.selected {
            background: linear-gradient(90deg, #a78bfa 0%, #f3e8ff 100%);
            color: #fff;
        }
        .mood-switcher {
            display: flex;
            gap: 16px;
            background: #fff;
            border-radius: 18px;
            padding: 12px 32px;
            box-shadow: 0 2px 8px #f3eaff;
            margin-bottom: 32px;
            justify-content: flex-end;
        }
        .mood-switcher .mood-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 14px;
            color: #222;
            background: none;
            border: none;
            cursor: pointer;
        }
        .card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 2px 8px #f3eaff;
            padding: 24px;
            margin-bottom: 24px;
        }
        .stProgress > div > div > div > div {
            background-image: linear-gradient(90deg, #a78bfa 0%, #7c3aed 100%);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h1 style='color:#7c3aed;'>kipi✦</h1>", unsafe_allow_html=True)
        nav_items = [
            ("Home", "🏠"),
            ("Woche", "📅"),
            ("Aufgaben", "✅"),
            ("Prüfungen", "📚"),
            ("Produktivität", "⚡"),
            ("Punkte", "⭐"),
            ("Notizen", "📝"),
            ("Ziele", "🎯"),
            ("Team", "👥"),
        ]
        for name, icon in nav_items:
            st.button(f"{icon} {name}", key=name, use_container_width=True)
        st.markdown(
            "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;margin-top:32px;'>"
            "<span style='font-size:24px;'>🔥</span>"
            "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
            "</div>", unsafe_allow_html=True
        )
        st.button("Logout", use_container_width=True)

    # --- MOOD SWITCHER (rechts oben) ---
    st.markdown(
        """
        <div class="mood-switcher">
            <button class="mood-btn">🌸<span>Cozy</span></button>
            <button class="mood-btn">⚡<span>Focus</span></button>
            <button class="mood-btn">🌞<span>Energy</span></button>
            <button class="mood-btn">📚<span>Minimal</span></button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- HEADER ---
    st.markdown(
        """
        <div style='margin-bottom: 16px;'>
            <span style='color:#7c3aed;font-size:14px;font-weight:bold;'>HOME / STARTSEITE</span>
            <h2 style='margin:0;'>Hey Lara! 👋</h2>
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
        st.markdown("<span style='color:#7c3aed;font-size:32px;font-weight:bold;'>70%</span>", unsafe_allow_html=True)
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
        st.info("„Disziplin heute, Stolz morgen.”")
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
    st.markdown("<div style='text-align:right;'><a href='#' style='color:#7c3aed;text-decoration:underline;'>Zur Wochenübersicht</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
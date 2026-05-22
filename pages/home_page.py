import streamlit as st
from datetime import datetime
from utils.data_manager import DataManager

def show_home_page():
    username = st.session_state.get("username", "User")
    data_manager = DataManager(fs_protocol="webdav", fs_root_folder="lernapp")

    # Daten laden
    tasks = data_manager.load("tasks.json") or []
    exams = data_manager.load("exams.json") or []
    points = data_manager.load("points.json") or 0
    streak = data_manager.load("streak.json") or 0

    # Nächste Aufgabe
    next_task = None
    if tasks:
        next_task = sorted(tasks, key=lambda x: x.get("due_date", ""))[0]

    # Nächste Prüfung
    next_exam = None
    if exams:
        next_exam = sorted(exams, key=lambda x: x.get("date", ""))[0]

    # Theme Farben
    colors = st.session_state.get("theme_colors", {})

    # -------------------------
    # HEADER
    # -------------------------
    st.markdown(f"""
        <h2 style='margin-bottom: -10px;'>HOME / STARTSEITE</h2>
        <h1 style='font-weight:700;'>Hey {username}! 👋</h1>
        <p style='font-size:18px; margin-top:-10px;'>Schön, dass du da bist. Bereit für einen produktiven Tag?</p>
    """, unsafe_allow_html=True)

    # -------------------------
    # TAGESFORTSCHRITT
    # -------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Tagesfortschritt")

    progress = min(len([t for t in tasks if t.get("done")]), 1) * 100
    st.progress(progress)
    st.write(f"**{progress}%** – Super gemacht! Weiter so! 💪")
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # ÜBERSICHT
    # -------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Deine Übersicht")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Aufgaben", len(tasks))
    col2.metric("📚 Prüfungen", len(exams))
    col3.metric("⭐ Stufe", points // 100)
    col4.metric("🏆 Punkte", points)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # MOTIVATION
    # -------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Motivation für dich")
    st.write("„Disziplin heute, Stolz morgen.“")
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # NÄCHSTE AUFGABE
    # -------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Nächste Aufgabe")

    if next_task:
        st.write(f"**{next_task['title']}**")
        st.write(f"Bis: {next_task['due_date']}")
        if st.button("Jetzt starten", key="start_task"):
            st.session_state.page = "Aufgaben"
            st.rerun()
    else:
        st.write("Keine Aufgaben vorhanden.")
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # NÄCHSTE PRÜFUNG
    # -------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Nächste Prüfung")

    if next_exam:
        st.write(f"**{next_exam['title']}**")
        st.write(f"Am: {next_exam['date']}")
        if st.button("Prüfung ansehen", key="view_exam"):
            st.session_state.page = "Prüfungen"
            st.rerun()
    else:
        st.write("Keine Prüfungen vorhanden.")
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # WOCHE AUF EINEN BLICK
    # -------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Deine Woche auf einen Blick")

    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]

    for day in days:
        st.markdown(f"### {day}")
        day_tasks = [t for t in tasks if t.get("day") == day]
        day_exams = [e for e in exams if e.get("day") == day]

        if not day_tasks and not day_exams:
            st.write("Keine Einträge.")
        else:
            for t in day_tasks:
                st.write(f"📝 {t['title']}")
            for e in day_exams:
                st.write(f"📚 {e['title']}")

    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager
from datetime import datetime, timedelta

def show_exams_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    apply_theme()
    colors = get_theme_colors() or {}
    primary = colors.get("primary", "#7c3aed")

    st.markdown(f"<h3 style='color:{primary};margin-bottom:6px;'>PRÜFUNGEN</h3>", unsafe_allow_html=True)

    dm = DataManager()
    exams = dm.load_user_data("exams.json", initial_value=[])

    # ---------------- FORMULAR ----------------
    with st.form("exam_form"):
        st.markdown("### Neue Prüfung hinzufügen")

        title = st.text_input("Titel", placeholder="z. B. Deutsch Prüfung")
        subject = st.text_input("Fach", placeholder="z. B. Deutsch")

        exam_date = st.date_input("Datum", value=datetime.utcnow().date())

        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Startzeit", value=datetime.utcnow().time())
        with col2:
            end_time = st.time_input("Endzeit", value=(datetime.utcnow() + timedelta(hours=1)).time())

        topics_input = st.text_area("Themen (jede Zeile ein Thema)", height=80)
        notes = st.text_area("Notizen", height=80)

        st.markdown("### Lernfortschritt")
        study_goal = st.number_input("Lernziel (Minuten)", min_value=0, value=0)
        study_done = st.number_input("Bereits gelernt (Minuten)", min_value=0, value=0)

        submitted = st.form_submit_button("Speichern")

    if submitted:
        topics = [t.strip() for t in topics_input.splitlines() if t.strip()]
        date_str = exam_date.isoformat()

        start_str = start_time.strftime("%H:%M")
        end_str = end_time.strftime("%H:%M")
        time_str = f"{start_str} – {end_str}"

        record = {
            "title": title,
            "date": date_str,
            "time": time_str,
            "subject": subject,
            "topics": topics,
            "notes": notes,
            "study_goal_min": study_goal,
            "study_done_min": study_done,
            "created_at": datetime.utcnow().isoformat(),
        }

        exams.append(record)
        dm.save_user_data(exams, "exams.json")

        # Felder leeren OHNE Fehler
        st.session_state.clear()
        st.rerun()

    # ---------------- LISTE ----------------
    st.markdown("---")
    st.markdown("### Alle deine Prüfungen")

    if not exams:
        st.info("Noch keine Prüfungen vorhanden.")
        return

    for i, e in enumerate(exams):

        goal = e.get("study_goal_min", 0)
        done = e.get("study_done_min", 0)
        progress = int((done / goal) * 100) if goal > 0 else 0

        # Kompakte Kopfzeile
        with st.expander(f"{e['title']} — {e['subject']} — {e['date']}"):

            st.markdown(f"**Uhrzeit:** {e['time']}")

            st.markdown("**Themen:**")
            for t in e["topics"]:
                st.markdown(f"- {t}")

            st.markdown("**Notizen:**")
            st.markdown(e["notes"])

            st.markdown("**Fortschritt:**")
            st.progress(progress / 100)
            st.markdown(f"{progress}%")

            st.markdown("### Lernfortschritt aktualisieren")
            new_done = st.number_input(
                "Bereits gelernt (Minuten)",
                min_value=0,
                value=done,
                key=f"done_{i}"
            )
            new_goal = st.number_input(
                "Lernziel (Minuten)",
                min_value=0,
                value=goal,
                key=f"goal_{i}"
            )

            if st.button("Speichern", key=f"save_{i}"):
                e["study_done_min"] = new_done
                e["study_goal_min"] = new_goal
                dm.save_user_data(exams, "exams.json")
                st.success("Fortschritt aktualisiert.")
                st.rerun()

            if st.button("🗑️ Löschen", key=f"delete_{i}"):
                exams.pop(i)
                dm.save_user_data(exams, "exams.json")
                st.success("Prüfung gelöscht.")
                st.rerun()
        # ---------------- LISTE ----------------
    st.markdown("---")
    st.markdown("### Alle deine Prüfungen")

    # --- SUCHFELD + SORTIERUNG ---
    search_query = st.text_input("🔍 Prüfung suchen (Titel, Fach, Datum)", "")

    try:
        exams = sorted(exams, key=lambda x: datetime.fromisoformat(x["date"]))
    except:
        pass

    if search_query.strip():
        q = search_query.lower()
        exams = [
            e for e in exams
            if q in e["title"].lower()
            or q in e["subject"].lower()
            or q in e["date"].lower()
        ]

    if not exams:
        st.info("Keine Prüfungen gefunden.")
        return

    for i, e in enumerate(exams):
        ...


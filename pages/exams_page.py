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

    # Optionen für das Dropdown-Menü (10-Minuten-Intervalle von 0 bis 300 Minuten)
    minuten_optionen = [i for i in range(0, 301, 10)]

    # Helper, um den passenden Index für einen Minutenwert im Dropdown zu finden
    def get_index(wert):
        # Falls der gespeicherte Wert kein 10er-Schritt ist, runden wir ihn ab
        gerundeter_wert = (wert // 10) * 10
        if gerundeter_wert in minuten_optionen:
            return minuten_optionen.index(gerundeter_wert)
        return 0

    # ---------------- FORMULAR ----------------
    with st.form("exam_form"):
        st.markdown("### Neue Prüfung hinzufügen")

        title = st.text_input("Titel", placeholder="z. B. Deutsch Prüfung", key="exam_title")
        subject = st.text_input("Fach", placeholder="z. B. Deutsch", key="exam_subject")

        exam_date = st.date_input("Datum", value=datetime.utcnow().date())

        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Startzeit", value=datetime.utcnow().time())
        with col2:
            end_time = st.time_input("Endzeit", value=(datetime.utcnow() + timedelta(hours=1)).time())

        topics_input = st.text_area("Themen (jede Zeile ein Thema)", height=80, key="exam_topics")
        notes = st.text_area("Notizen", height=80, key="exam_notes")

        st.markdown("### Lernfortschritt")
        
        # Dropdowns statt st.number_input
        study_goal = st.selectbox(
            "Lernziel (Minuten)",
            options=minuten_optionen,
            index=0,
            key="study_goal_form"
        )
        study_done = st.selectbox(
            "Bereits gelernt (Minuten)",
            options=minuten_optionen,
            index=0,
            key="study_done_form"
        )

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

        # Formularfelder leeren
        for key in ["exam_title", "exam_subject", "exam_topics", "exam_notes", "study_goal_form", "study_done_form"]:
            if key in st.session_state:
                del st.session_state[key]

        st.success("Prüfung gespeichert.")
        st.rerun()

    # ---------------- LISTE ----------------
    st.markdown("---")
    st.markdown("### Alle deine Prüfungen")

    # --- SUCHFELD ---
    search_query = st.text_input("🔍 Prüfung suchen (Titel, Fach, Datum)", "")

    # --- SORTIERUNG NACH DATUM ---
    try:
        exams = sorted(exams, key=lambda x: datetime.fromisoformat(x["date"]))
    except:
        pass

    # --- FILTER ---
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
            st.progress(min(1.0, progress / 100))
            st.markdown(f"{progress}%")

            st.markdown("### Lernfortschritt aktualisieren")
            
            # Dropdowns auch in der Detailansicht der Liste
            new_done = st.selectbox(
                "Bereits gelernt (Minuten)",
                options=minuten_optionen,
                index=get_index(done),
                key=f"done_select_{i}"
            )
            new_goal = st.selectbox(
                "Lernziel (Minuten)",
                options=minuten_optionen,
                index=get_index(goal),
                key=f"goal_select_{i}"
            )

            col_btn1, col_btn2 = st.columns([1, 4])
            with col_btn1:
                if st.button("Speichern", key=f"save_{i}"):
                    e["study_done_min"] = new_done
                    e["study_goal_min"] = new_goal
                    dm.save_user_data(exams, "exams.json")
                    st.success("Fortschritt aktualisiert.")
                    st.rerun()
            with col_btn2:
                if st.button("🗑️ Löschen", key=f"delete_{i}"):
                    exams.pop(i)
                    dm.save_user_data(exams, "exams.json")
                    st.success("Prüfung gelöscht.")
                    st.rerun()

if __name__ == "__main__":
    show_exams_page()
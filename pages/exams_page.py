import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager
from datetime import datetime, timedelta

def show_exams_page():
    """Formular zum Anlegen, Speichern und Rückgängig machen von Prüfungen."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    apply_theme()
    colors = get_theme_colors() or {}
    primary = colors.get("primary", "#7c3aed")

    st.markdown(f"<h3 style='color:{primary};margin-bottom:6px;'>PRÜFUNGEN</h3>", unsafe_allow_html=True)

    dm = DataManager()
    exams = dm.load_user_data("exams.json", initial_value=[])

    # Eingabeformular
    with st.form("exam_form"):
        title = st.text_input("Titel", key="exam_title", placeholder="z. B. Deutsch Prüfung")
        exam_date = st.date_input("Datum", key="exam_date", value=datetime.utcnow().date())

        # Zeitpicker: Start- und Endzeit
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Startzeit", key="exam_start_time", value=(datetime.utcnow()).time())
        with col2:
            # Default: eine Stunde später
            default_end = (datetime.utcnow() + timedelta(hours=1)).time()
            end_time = st.time_input("Endzeit", key="exam_end_time", value=default_end)

        subject = st.text_input("Fach", key="exam_subject", placeholder="z. B. Deutsch")
        topics_input = st.text_area("Themen (jede Zeile ein Thema)", key="exam_topics", height=80, placeholder="Zusammenfassung schreiben\nTextanalyse\nGrammatik")
        progress = st.slider("Fortschritt (%)", min_value=0, max_value=100, value=0, key="exam_progress")
        notes = st.text_area("Notizen", key="exam_notes", height=80, placeholder="z. B. Alte Prüfungen lösen")

        submitted = st.form_submit_button("Speichern")

    if submitted:
        topics = [s.strip() for s in (topics_input or "").splitlines() if s.strip()]
        date_str = exam_date.isoformat() if exam_date else ""

        # Zeiten zu Strings konvertieren
        start_str = start_time.strftime("%H:%M") if start_time else ""
        end_str = end_time.strftime("%H:%M") if end_time else ""
        time_str = f"{start_str} - {end_str}" if end_str else start_str

        # Validierung: Endzeit muss nach Startzeit liegen
        if start_time and end_time:
            start_dt = datetime.combine(datetime.utcnow().date(), start_time)
            end_dt = datetime.combine(datetime.utcnow().date(), end_time)
            if end_dt <= start_dt:
                st.warning("Endzeit muss nach der Startzeit liegen. Bitte anpassen.")
                st.stop()

        record = {
            "title": title.strip(),
            "date": date_str,
            "time": time_str,
            "subject": subject.strip(),
            "topics": topics,
            "progress": int(progress or 0),
            "notes": notes.strip(),
            "created_at": datetime.utcnow().isoformat(),
        }

        st.session_state["exams_backup"] = exams.copy() if isinstance(exams, list) else list(exams)
        new_exams = DataManager.append_record(exams, record)
        dm.save_user_data(new_exams, "exams.json")
        st.success("Prüfung gespeichert. Du kannst die letzte Änderung rückgängig machen.")
        exams = new_exams

    # Rückgängig-Funktionalität
    if "exams_backup" in st.session_state:
        if st.button("Letzte Änderung rückgängig machen", key="undo_exam"):
            backup = st.session_state.pop("exams_backup")
            dm.save_user_data(backup, "exams.json")
            st.experimental_rerun()

        st.markdown("---")
    st.markdown("### Alle deine Prüfungen")

    if not exams:
        st.info("Noch keine Prüfungen vorhanden.")
    else:
        for i, e in enumerate(exams):

            # Titelzeile + Delete-Button NEBENAN
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(
                    f"**{e.get('title','(ohne Titel)')}** — {e.get('date','')}"
                )
            with cols[1]:
                if st.button("🗑️", key=f"delete_exam_{i}"):
                    exams.pop(i)
                    dm.save_user_data(exams, "exams.json")
                    st.success("Prüfung gelöscht.")
                    st.rerun()

            # Details im Expander
            with st.expander("Details anzeigen"):
                st.write(f"**Fach:** {e.get('subject','')}")
                st.write(f"**Uhrzeit:** {e.get('time','')}")
                st.write("**Themen:**")
                for top in e.get("topics", []):
                    st.write(f"- {top}")
                st.write(f"**Fortschritt:** {e.get('progress',0)}%")
                st.write(f"**Notizen:** {e.get('notes','')}")
                st.write(f"**Erstellt:** {e.get('created_at','')}")

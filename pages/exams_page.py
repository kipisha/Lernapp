import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager
from datetime import datetime

def show_exams_page():
    """Formular zum Anlegen, Speichern und Rückgängig machen von Prüfungen."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    apply_theme()
    colors = get_theme_colors() or {}
    primary = colors.get("primary", "#7c3aed")
    card_bg = colors.get("card", "#ffffff")
    text_color = colors.get("text", "#111827")

    st.markdown(f"<h3 style='color:{primary};margin-bottom:6px;'>PRÜFUNGEN</h3>", unsafe_allow_html=True)

    dm = DataManager()
    exams = dm.load_user_data("exams.json", initial_value=[])

    # Eingabeformular
    with st.form("exam_form"):
        st.text_input("Titel", key="exam_title", placeholder="z. B. Deutsch Prüfung")
        st.text_input("Datum", key="exam_date", placeholder="TT.MM.JJJJ oder 2024-05-17")
        st.text_input("Uhrzeit (z. B. 10:30 - 12:00)", key="exam_time", placeholder="10:30 - 12:00")
        st.text_input("Fach", key="exam_subject", placeholder="z. B. Deutsch")
        st.text_area("Themen (jede Zeile ein Thema)", key="exam_topics", height=80, placeholder="Zusammenfassung schreiben\nTextanalyse\nGrammatik")
        progress = st.slider("Fortschritt (%)", min_value=0, max_value=100, value=0, key="exam_progress")
        st.text_area("Notizen", key="exam_notes", height=80, placeholder="z. B. Alte Prüfungen lösen")

        submitted = st.form_submit_button("Speichern")

    if submitted:
        topics = [s.strip() for s in st.session_state.get("exam_topics","").splitlines() if s.strip()]
        record = {
            "title": st.session_state.get("exam_title","").strip(),
            "date": st.session_state.get("exam_date","").strip(),
            "time": st.session_state.get("exam_time","").strip(),
            "subject": st.session_state.get("exam_subject","").strip(),
            "topics": topics,
            "progress": int(st.session_state.get("exam_progress",0) or 0),
            "notes": st.session_state.get("exam_notes","").strip(),
            "created_at": datetime.utcnow().isoformat(),
        }

        st.session_state["exams_backup"] = exams.copy() if isinstance(exams, list) else list(exams)
        new_exams = DataManager.append_record(exams, record)
        dm.save_user_data(new_exams, "exams.json")
        st.success("Prüfung gespeichert. Du kannst die letzte Änderung rückgängig machen.")
        exams = new_exams

    if "exams_backup" in st.session_state:
        if st.button("Letzte Änderung rückgängig machen", key="undo_exam"):
            backup = st.session_state.pop("exams_backup")
            dm.save_user_data(backup, "exams.json")
            st.experimental_rerun()

    st.markdown("---")
    st.markdown("### Deine gespeicherten Prüfungen")
    if not exams:
        st.info("Noch keine Prüfungen vorhanden.")
    else:
        for i, e in enumerate(exams):
            with st.expander(f"{e.get('title','(ohne Titel)')} — {e.get('date','')}", expanded=False):
                st.write(f"**Fach:** {e.get('subject','')}")
                st.write(f"**Uhrzeit:** {e.get('time','')}")
                st.write("**Themen:**")
                for top in e.get("topics", []):
                    st.write(f"- {top}")
                st.write(f"**Fortschritt:** {e.get('progress',0)}%")
                st.write(f"**Notizen:** {e.get('notes','')}")
                st.write(f"**Erstellt:** {e.get('created_at','')}")
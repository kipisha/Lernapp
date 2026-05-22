import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager
from datetime import datetime

def show_tasks_page():
    """Formular zum Anlegen, Speichern und Rückgängig machen von Aufgaben."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    apply_theme()
    colors = get_theme_colors() or {}
    primary = colors.get("primary", "#0f172a")
    card_bg = colors.get("card", "#ffffff")
    text_color = colors.get("text", "#111827")

    st.markdown(f"<h3 style='color:{primary};margin-bottom:6px;'>AUFGABEN</h3>", unsafe_allow_html=True)

    dm = DataManager()
    tasks = dm.load_user_data("tasks.json", initial_value=[])

    # Eingabeformular
    with st.form("task_form"):
        st.text_input("Titel", key="task_title", placeholder="z. B. Mathe Hausaufgaben")
        st.text_input("Fälligkeitsdatum", key="task_due", placeholder="TT.MM.JJJJ oder 2024-05-13")
        st.text_input("Uhrzeit", key="task_time", placeholder="z. B. 15:00")
        st.number_input("Dauer (Minuten)", key="task_duration", min_value=0, step=5)
        st.text_input("Fach", key="task_subject", placeholder="z. B. Mathematik")
        st.text_input("Tag/Kategorie", key="task_tag", placeholder="z. B. Hausaufgaben")
        st.text_area("Notizen", key="task_notes", height=80, placeholder="Details / Aufgabenbeschreibung")

        submitted = st.form_submit_button("Speichern")

    if submitted:
        record = {
            "title": st.session_state.get("task_title", "").strip(),
            "due": st.session_state.get("task_due", "").strip(),
            "time": st.session_state.get("task_time", "").strip(),
            "duration_min": int(st.session_state.get("task_duration", 0) or 0),
            "subject": st.session_state.get("task_subject", "").strip(),
            "tag": st.session_state.get("task_tag", "").strip(),
            "notes": st.session_state.get("task_notes", "").strip(),
            "created_at": datetime.utcnow().isoformat(),
        }

        # Backup vor dem Schreiben (für Undo)
        st.session_state["tasks_backup"] = tasks.copy() if isinstance(tasks, list) else list(tasks)
        new_tasks = DataManager.append_record(tasks, record)
        dm.save_user_data(new_tasks, "tasks.json")
        st.success("Aufgabe gespeichert. Du kannst die letzte Änderung rückgängig machen.")

        # Aktualisiere lokale variable nach Save
        tasks = new_tasks

    # Rückgängig-Funktionalität
    if "tasks_backup" in st.session_state:
        if st.button("Letzte Änderung rückgängig machen", key="undo_task"):
            backup = st.session_state.pop("tasks_backup")
            dm.save_user_data(backup, "tasks.json")
            st.experimental_rerun()

    st.markdown("---")
    st.markdown("### Deine gespeicherten Aufgaben")
    if not tasks:
        st.info("Noch keine Aufgaben vorhanden.")
    else:
        for i, t in enumerate(tasks):
            with st.expander(f"{t.get('title','(ohne Titel)')} — {t.get('due','')}", expanded=False):
                st.write(f"**Fach:** {t.get('subject','')}")
                st.write(f"**Dauer:** {t.get('duration_min','')} min")
                st.write(f"**Tag:** {t.get('tag','')}")
                st.write(f"**Uhrzeit:** {t.get('time','')}")
                st.write(f"**Notizen:** {t.get('notes','')}")
                st.write(f"**Erstellt:** {t.get('created_at','')}")
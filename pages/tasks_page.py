import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager
from datetime import datetime

# Hilfsfunktion zum Erledigen von Aufgaben aus der Liste
def _mark_task_done_by_index(tasks, index, dm):
    tasks[index]["done"] = True
    tasks[index]["done_at"] = datetime.utcnow().isoformat()
    dm.save_user_data(tasks, "tasks.json")
    st.success("Aufgabe als erledigt markiert! 🎉")
    st.rerun()

def show_tasks_page():
    """Formular zum Anlegen, Speichern und Verwalten von Aufgaben."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    # Theme laden und Farben bestimmen
    apply_theme()
    colors = get_theme_colors() or {}
    primary = colors.get("primary", "#0f172a")

    st.markdown(f"<h3 style='color:{primary};margin-bottom:20px;'>AUFGABEN</h3>", unsafe_allow_html=True)

    dm = DataManager()
    tasks = dm.load_user_data("tasks.json", initial_value=[])

    # --- EINGABEFORMULAR (Direkt ganz oben) ---
    with st.form("task_form"):
        st.markdown("### Neue Aufgabe hinzufügen")
        title = st.text_input("Titel", key="task_title", placeholder="z. B. Mathe Hausaufgaben")
        due_date = st.date_input("Fälligkeitsdatum", key="task_due_date", value=datetime.utcnow().date())

        duration = st.number_input("Dauer (Minuten)", key="task_duration", min_value=0, step=5)
        subject = st.text_input("Fach", key="task_subject", placeholder="z. B. Mathematik")
        tag = st.text_input("Tag/Kategorie", key="task_tag", placeholder="z. B. Hausaufgaben")
        notes = st.text_area("Notizen", key="task_notes", height=80, placeholder="Details / Aufgabenbeschreibung")

        submitted = st.form_submit_button("Speichern")

    if submitted:
        if not title.strip():
            st.error("Bitte gib einen Titel für die Aufgabe ein.")
        else:
            due_str = due_date.isoformat() if due_date else ""

            checklist = ["Aufgabe lesen", "Lösen", "Kontrollieren"]
            record = {
                "title": title.strip(),
                "due": due_str,
                "time": "",
                "duration_min": int(duration or 0),
                "subject": subject.strip(),
                "tag": tag.strip(),
                "notes": notes.strip(),
                "created_at": datetime.utcnow().isoformat(),
                "done": False,        # Synchronisation mit der Home-Seite
                "points": 20,         # Belohnungssystem
                "checklist": checklist,
                "checked": [False, False, False]
            }

            # Backup erstellen und speichern
            st.session_state["tasks_backup"] = tasks.copy() if isinstance(tasks, list) else list(tasks)
            new_tasks = DataManager.append_record(tasks, record)
            dm.save_user_data(new_tasks, "tasks.json")
            st.success("Aufgabe erfolgreich gespeichert!")
            st.rerun()

    st.markdown("---")
    st.markdown("### Alle deine Aufgaben")

    if not tasks:
        st.info("Noch keine Aufgaben vorhanden.")
    else:
        for i, t in enumerate(tasks):
            # Status-Icon bestimmen
            status_icon = "✅" if t.get("done", False) else "⏳"
            
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(
                    f"{status_icon} **{t.get('title','(ohne Titel)')}** — {t.get('due','')}"
                )
            with cols[1]:
                if st.button("🗑️", key=f"delete_{i}"):
                    tasks.pop(i)
                    dm.save_user_data(tasks, "tasks.json")
                    st.success("Aufgabe gelöscht.")
                    st.rerun()

            # Details im Expander
            with st.expander("Details anzeigen"):
                st.write(f"**Status:** {'Erledigt' if t.get('done', False) else 'Offen'}")
                st.write(f"**Fach:** {t.get('subject','')}")
                st.write(f"**Dauer:** {t.get('duration_min','')} min")
                st.write(f"**Tag:** {t.get('tag','')}")
                st.write(f"**Notizen:** {t.get('notes','')}")
                
                # Erledigt-Button anzeigen, wenn die Aufgabe noch offen ist
                if not t.get("done", False):
                    if st.button("Als erledigt markieren", key=f"list_done_task_{i}", use_container_width=True):
                        _mark_task_done_by_index(tasks, i, dm)

if __name__ == "__main__":
    show_tasks_page()
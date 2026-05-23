import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager
from datetime import datetime

# --- Vorschau-Karten (oben) ---
def _render_task_card(entry, colors):
    title = entry.get("title", "Mathe Hausaufgaben")
    badge = entry.get("tag", "Hausaufgaben")
    due = entry.get("due", "")
    duration = entry.get("duration_min", "")
    subject = entry.get("subject", "")
    notes = entry.get("notes", "")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">'
        f'<img src="https://via.placeholder.com/40/9bf0c7/ffffff" style="border-radius:8px"/>'
        f'<div><strong>{title}</strong></div>'
        f'<div style="margin-left:auto;padding:6px 10px;border-radius:12px;background:linear-gradient(90deg,{colors.get("secondary")},{colors.get("primary")});color:#fff;font-weight:600;font-size:12px">{badge}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Fällig am:</strong> {due}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Dauer:</strong> {duration} min</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Fach:</strong> {subject}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Notizen:</strong> {notes}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:12px;margin-top:12px;">'
        '<button style="padding:8px 14px;border-radius:10px;border:1px solid #e5e7eb;background:transparent">Bearbeiten</button>'
        f'<button style="padding:8px 14px;border-radius:10px;border:1px solid {colors.get("primary")};background:white;color:{colors.get("primary")};font-weight:600">Als erledigt markieren</button>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

def _render_exam_card(entry, colors):
    title = entry.get("title", "Deutsch Prüfung")
    badge = "Prüfung"
    date = entry.get("date", "")
    time = entry.get("time", "")
    subject = entry.get("subject", "")
    topics = entry.get("topics", []) or []
    progress = entry.get("progress", 0)
    notes = entry.get("notes", "")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">'
        f'<img src="https://via.placeholder.com/40/ffb4b4/ffffff" style="border-radius:8px"/>'
        f'<div><strong>{title}</strong></div>'
        f'<div style="margin-left:auto;padding:6px 10px;border-radius:12px;background:linear-gradient(90deg,{colors.get("secondary")},{colors.get("primary")});color:#fff;font-weight:600;font-size:12px">{badge}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Datum:</strong> {date}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Uhrzeit:</strong> {time}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Fach:</strong> {subject}</div>', unsafe_allow_html=True)
    if topics:
        st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Themen:</strong></div>', unsafe_allow_html=True)
        for top in topics:
            st.markdown(f'<div style="margin-left:18px;color:#374151">• {top}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;margin-top:8px;">'
        f'<div style="width:160px;height:10px;background:#f3f4f6;border-radius:8px;overflow:hidden;">'
        f'<div style="width:{int(progress)}%;height:100%;background:linear-gradient(90deg,{colors.get("primary")},{colors.get("secondary")})"></div>'
        f'</div><div style="color:#6b7280">{int(progress)}%</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div style="color:#6b7280;margin:6px 0;"><strong>Notizen:</strong> {notes}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:12px;margin-top:12px;">'
        '<button style="padding:8px 14px;border-radius:10px;border:1px solid #e5e7eb;background:transparent">Bearbeiten</button>'
        '<button style="padding:8px 14px;border-radius:10px;border:1px solid #fb7185;background:white;color:#fb7185;font-weight:600">Als erledigt markieren</button>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

def show_preview_top_on_tasks(dm, colors):
    tasks = dm.load_user_data("tasks.json", initial_value=[]) or []
    exams = dm.load_user_data("exams.json", initial_value=[]) or []
    sample_task = tasks[0] if tasks else {"title":"Mathe Hausaufgaben","due":"13. Mai 2024","duration_min":90,"subject":"Mathematik","notes":"Kapitel 5 & 6 lösen","tag":"Hausaufgaben"}
    sample_exam = exams[0] if exams else {"title":"Deutsch Prüfung","date":"17. Mai 2024","time":"10:30 - 12:00","subject":"Deutsch","topics":["Zusammenfassung schreiben","Textanalyse","Grammatik"],"progress":60,"notes":"Alte Prüfungen lösen!"}

    c1, c2 = st.columns([1,1], gap="large")
    with c1:
        _render_task_card(sample_task, colors)
    with c2:
        _render_exam_card(sample_exam, colors)
# --- Ende Vorschau-Karten ---

def show_tasks_page():
    """Formular zum Anlegen, Speichern und Rückgängig machen von Aufgaben."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    apply_theme()
    colors = get_theme_colors() or {}
    primary = colors.get("primary", "#0f172a")

    st.markdown(f"<h3 style='color:{primary};margin-bottom:6px;'>AUFGABEN</h3>", unsafe_allow_html=True)

    dm = DataManager()
    tasks = dm.load_user_data("tasks.json", initial_value=[])

    # Eingabeformular
    with st.form("task_form"):
        title = st.text_input("Titel", key="task_title", placeholder="z. B. Mathe Hausaufgaben")
        due_date = st.date_input("Fälligkeitsdatum", key="task_due_date", value=datetime.utcnow().date())

        duration = st.number_input("Dauer (Minuten)", key="task_duration", min_value=0, step=5)
        subject = st.text_input("Fach", key="task_subject", placeholder="z. B. Mathematik")
        tag = st.text_input("Tag/Kategorie", key="task_tag", placeholder="z. B. Hausaufgaben")
        notes = st.text_area("Notizen", key="task_notes", height=80, placeholder="Details / Aufgabenbeschreibung")

        submitted = st.form_submit_button("Speichern")

    if submitted:
        due_str = due_date.isoformat() if due_date else ""
        time_str = ""

        record = {
            "title": title.strip(),
            "due": due_str,
            "time": time_str,
            "duration_min": int(duration or 0),
            "subject": subject.strip(),
            "tag": tag.strip(),
            "notes": notes.strip(),
            "created_at": datetime.utcnow().isoformat(),
        }

        # Backup vor dem Schreiben (für Undo)
        st.session_state["tasks_backup"] = tasks.copy() if isinstance(tasks, list) else list(tasks)
        new_tasks = DataManager.append_record(tasks, record)
        dm.save_user_data(new_tasks, "tasks.json")
        st.success("Aufgabe gespeichert. Du kannst die letzte Änderung rückgängig machen.")

        # Aktualisiere lokale variable nach Save
        tasks = new_tasks


    st.markdown("---")
    st.markdown("### Alle deine Aufgaben")

    if not tasks:
        st.info("Noch keine Aufgaben vorhanden.")
    else:
        for i, t in enumerate(tasks):

            # Titelzeile + Delete-Button NEBENAN
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(
                    f"**{t.get('title','(ohne Titel)')}** — {t.get('due','')}"
                )
            with cols[1]:
                if st.button("🗑️", key=f"delete_{i}"):
                    tasks.pop(i)
                    dm.save_user_data(tasks, "tasks.json")
                    st.success("Aufgabe gelöscht.")
                    st.rerun()

            # Details im Expander
            with st.expander("Details anzeigen"):
                st.write(f"**Fach:** {t.get('subject','')}")
                st.write(f"**Dauer:** {t.get('duration_min','')} min")
                st.write(f"**Tag:** {t.get('tag','')}")
                st.write(f"**Uhrzeit:** {t.get('time','')}")
                st.write(f"**Notizen:** {t.get('notes','')}")
                st.write(f"**Erstellt:** {t.get('created_at','')}")


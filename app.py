import streamlit as st
import pandas as pd 
from team.team_page import show_team_page
from datetime import datetime, timedelta

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(page_title="Lernapp", page_icon=":material/home:")

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="lernapp"
) 
login_manager = LoginManager(data_manager)
login_manager.login_register()
st.session_state["username"]

selected_page = st.sidebar.radio("Navigation", ["Home", "Woche", "Aufgaben", "Prüfungen", "Punkte","Team"])



# ---------------------------------------------------------
# ------------------------- HOME ---------------------------
# ---------------------------------------------------------
if selected_page == "Home":
    user_name = st.session_state.get("username", "Nutzer")
    st.title(f"👋 Hallo, {user_name}!")

    # Produktivität berechnen
    def calculate_productivity():
        tasks = st.session_state.get("tasks", [])
        checked = st.session_state.get("checked", {})
        if len(tasks) == 0:
            return 0
        done = sum(1 for t in tasks if checked.get(t["title"], False))
        return done / len(tasks)

    st.subheader("Deine heutige Produktivität")
    productivity = calculate_productivity()
    st.progress(productivity)
    st.caption(f"{int(productivity * 100)} % erledigt")

    st.write("———")
    st.subheader("📅 Aufgaben der nächsten 7 Tage")

    today = datetime.now().date()
    week_limit = today + timedelta(days=7)

    tasks = st.session_state.get("tasks", [])
    checked = st.session_state.get("checked", {})

    # Nur Aufgaben anzeigen, die NICHT erledigt sind
    upcoming_tasks = []

    for t in tasks:
        # Datum aus String in echtes Datum umwandeln
        date_obj = datetime.strptime(t["date"], "%Y-%m-%d").date()

        if date_obj >= today and date_obj <= week_limit:
            if not checked.get(t["title"], False):
                upcoming_tasks.append(t)

    if len(upcoming_tasks) == 0:
        st.info("Keine Aufgaben in den nächsten 7 Tagen.")
    else:
        for task in upcoming_tasks:
            is_checked = st.checkbox(
                f"{task['title']} – {task['date']}",
                value=checked.get(task["title"], False),
                key=f"chk_home_{task['title']}"
            )

            st.session_state.checked[task["title"]] = is_checked

            if is_checked:
                st.rerun()

    st.write("———")
    st.subheader("📚 Prüfungen der nächsten 7 Tage")

    exams = st.session_state.get("exams", [])
    upcoming_exams = [
        e for e in exams
        if e["date"] >= today and e["date"] <= week_limit
    ]

    if len(upcoming_exams) == 0:
        st.info("Keine Prüfungen in den nächsten 7 Tagen.")
    else:
        for exam in upcoming_exams:
            days_left = (exam["date"] - today).days
            st.write(f"📘 **{exam['title']} – {exam['date']}** ({days_left} Tage)")


# ---------------------------------------------------------
# ------------------------- WOCHE --------------------------
# ---------------------------------------------------------
elif selected_page == "Woche":
    st.title("📅 Wochenübersicht")
    selected_week = st.selectbox("Woche auswählen:", ["11–17 März", "18–24 März", "25–31 März"])
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"### {day}")
            st.write("🟦 Aufgabenplatzhalter")


# ---------------------------------------------------------
# ------------------------ AUFGABEN ------------------------
# ---------------------------------------------------------
elif selected_page == "Aufgaben":
    st.title("📝 Neue Aufgabe hinzufügen")

    # Aufgaben laden, falls noch nicht im Session State
    if "tasks" not in st.session_state:
        loaded_tasks = data_manager.load_user_data("tasks")
        st.session_state.tasks = loaded_tasks if loaded_tasks else []

    if "checked" not in st.session_state:
        st.session_state.checked = {}

    # --- Formular ---
    fach = st.selectbox(
        "Fach:",
        ["Mathe", "Deutsch", "Englisch", "Physik", "Chemie",
         "Biologie", "Geschichte", "Geografie", "Informatik", "Andere"]
    )

    aufgabe = st.text_input("Aufgabe:")
    datum = st.date_input("Datum:")
    priorität = st.radio("Priorität:", ["Hoch", "Mittel", "Niedrig"])
    punkte = st.number_input("Punkte:", min_value=0, max_value=50, value=5)
    beschreibung = st.text_area("Beschreibung:")

    if st.button("💾 SPEICHERN"):
        new_task = {
            "title": f"{fach} – {aufgabe}",
            "date": str(datum),
            "priority": priorität,
            "points": punkte,
            "description": beschreibung
        }

        st.session_state.tasks.append(new_task)
        data_manager.save_user_data("tasks", st.session_state.tasks)

        st.session_state.checked[new_task["title"]] = False
        st.success("Aufgabe gespeichert!")

    st.write("———")
    st.subheader("🗂️ Alte Aufgaben")

    if len(st.session_state.tasks) == 0:
        st.info("Noch keine Aufgaben vorhanden.")
    else:
        for task in st.session_state.tasks:
            col1, col2 = st.columns([4, 1])

            # Datum sicher formatieren
            try:
                date_obj = datetime.strptime(task["date"], "%Y-%m-%d").date()
                date_str = date_obj.strftime("%d.%m.%Y")
            except:
                date_str = task["date"]

            with col1:
                st.write(
                    f"**{task['title']}** – {date_str}  "
                    f"Priorität: {task['priority']} | Punkte: {task['points']}"
                )
                if task["description"]:
                    st.caption(task["description"])

            with col2:
                if st.button("🗑️", key=f"del_task_{task['title']}"):
                    st.session_state.tasks.remove(task)
                    data_manager.save_user_data("tasks", st.session_state.tasks)
                    st.session_state.checked.pop(task["title"], None)
                    st.rerun()


# ---------------------------------------------------------
# ------------------------ PRÜFUNGEN -----------------------
# ---------------------------------------------------------
elif selected_page == "Prüfungen":
    st.title("📚 Neue Prüfung hinzufügen")

    if "exams" not in st.session_state:
        loaded_exams = data_manager.load_user_data("exams") or []
        st.session_state.exams = loaded_exams if loaded_exams else []

    fach = st.selectbox(
        "Fach:",
        ["Mathe", "Deutsch", "Englisch", "Physik", "Chemie",
         "Biologie", "Geschichte", "Geografie", "Informatik", "Andere"]
    )

    datum = st.date_input("Datum:")
    lernplan = st.text_area("Lernplan:")

    if st.button("💾 SPEICHERN"):
        new_exam = {
            "title": fach,
            "date": str(datum),
            "plan": lernplan
        }

        st.session_state.exams.append(new_exam)
        data_manager.save_user_data("exams", st.session_state.exams)

        st.success("Prüfung gespeichert!")

    st.write("———")
    st.subheader("🗂️ Alle Prüfungen")

    if len(st.session_state.exams) == 0:
        st.info("Noch keine Prüfungen vorhanden.")
    else:
        for exam in st.session_state.exams:
            col1, col2 = st.columns([4, 1])

            with col1:
                try:
                    date_obj = datetime.strptime(exam["date"], "%Y-%m-%d").date()
                    date_str = date_obj.strftime("%d.%m.%Y")
                except:
                    date_str = exam["date"]

                st.write(f"**{exam['title']}** – {date_str}")

                if exam["plan"]:
                    st.caption(f"📘 Lernplan: {exam['plan']}")

            with col2:
                if st.button("🗑️", key=f"del_exam_{exam['title']}_{exam['date']}"):
                    st.session_state.exams.remove(exam)
                    data_manager.save_user_data("exams", st.session_state.exams)
                    st.rerun()


# ---------------------------------------------------------
# ------------------------- PUNKTE -------------------------
# ---------------------------------------------------------
elif selected_page == "Punkte":
    st.title("🏆 Punkte")
    st.write("Hier kommt dein Punktefortschritt hin.")


# ---------------------------------------------------------
# -------------------------- TEAM --------------------------
# ---------------------------------------------------------
elif selected_page == "Team":
    show_team_page()

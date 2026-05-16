import streamlit as st
import pandas as pd
from team.team_page import show_team_page
from datetime import datetime, timedelta

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(page_title="Lernapp", page_icon=":material/home:")
st.markdown("""
<style>

html, body, .stApp {
    height: 100%;
    background: linear-gradient(135deg, #dbeafe, #fce7f3);
    background-attachment: fixed;
}

/* Entfernt ALLE weißen Balken */
.stAppViewContainer, .main, .block-container {
    background: transparent !important;
}

/* Cards wirken wie schwebende Elemente */
.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

/* Eingabefelder */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
    border: 1px solid #d0d0d0;
    padding: 10px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(6px);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #9333ea);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: bold;
    border: none;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #4338ca, #7e22ce);
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ------------------------- CSS ----------------------------
# ---------------------------------------------------------
st.markdown("""
<style>

    .main {
        padding-top: 20px;
    }

    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
        border: 1px solid #d0d0d0;
        padding: 8px;
    }

    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }

    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ------------------------- LOGIN --------------------------
# ---------------------------------------------------------
data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="lernapp"
)
login_manager = LoginManager(data_manager)
login_manager.login_register()
st.session_state["username"]

selected_page = st.sidebar.radio("Navigation", ["Home", "Woche", "Aufgaben", "Prüfungen", "Punkte", "Team"])


# ---------------------------------------------------------
# ------------------------- HOME ---------------------------
# ---------------------------------------------------------
if selected_page == "Home":
    user_name = st.session_state.get("username", "Nutzer")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title(f"👋 Hallo, {user_name}!")

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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 Aufgaben der nächsten 7 Tage")

    today = datetime.now().date()
    week_limit = today + timedelta(days=7)

    tasks = st.session_state.get("tasks", [])
    checked = st.session_state.get("checked", {})

    upcoming_tasks = []

    for t in tasks:
        date_obj = datetime.strptime(t["date"], "%Y-%m-%d").date()
        if today <= date_obj <= week_limit:
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📚 Prüfungen der nächsten 7 Tage")

    exams = st.session_state.get("exams", [])
    upcoming_exams = []

    for e in exams:
        try:
            exam_date = datetime.strptime(e["date"], "%Y-%m-%d").date()
        except:
            continue
        if today <= exam_date <= week_limit:
            upcoming_exams.append({**e, "date": exam_date})

    if len(upcoming_exams) == 0:
        st.info("Keine Prüfungen in den nächsten 7 Tagen.")
    else:
        for exam in upcoming_exams:
            days_left = (exam["date"] - today).days
            st.write(f"📘 **{exam['title']} – {exam['date']}** ({days_left} Tage)")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ------------------------- WOCHE --------------------------
# ---------------------------------------------------------
elif selected_page == "Woche":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📅 Wochenübersicht")
    selected_week = st.selectbox("Woche auswählen:", ["11–17 März", "18–24 März", "25–31 März"])
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"### {day}")
            st.write("🟦 Aufgabenplatzhalter")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ------------------------ AUFGABEN ------------------------
# ---------------------------------------------------------
elif selected_page == "Aufgaben":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📝 Neue Aufgabe hinzufügen")

    if "tasks" not in st.session_state:
        loaded_tasks = data_manager.load_user_data("tasks.json")
        st.session_state.tasks = loaded_tasks if loaded_tasks else []

    if "checked" not in st.session_state:
        st.session_state.checked = {}

    # Fach-Auswahl + eigenes Fach
    fach_option = st.selectbox(
        "Fach:",
        ["Mathe", "Deutsch", "Englisch", "Physik", "Chemie",
         "Biologie", "Geschichte", "Geografie", "Informatik", "Andere"]
    )

    if fach_option == "Andere":
        fach = st.text_input("Eigenes Fach eingeben:")
    else:
        fach = fach_option

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
        data_manager.save_user_data(st.session_state.tasks, "tasks.json")
        st.session_state.checked[new_task["title"]] = False
        st.success("Aufgabe gespeichert!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Aufgabenliste
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🗂️ Alle Aufgaben")

    if len(st.session_state.tasks) == 0:
        st.info("Noch keine Aufgaben vorhanden.")
    else:
        priority_colors = {
            "Hoch": "#ff4d4d",
            "Mittel": "#ffa64d",
            "Niedrig": "#5cd65c"
        }

        table_data = []
        for i, task in enumerate(st.session_state.tasks):
            try:
                date_obj = datetime.strptime(task["date"], "%Y-%m-%d").date()
                date_str = date_obj.strftime("%d.%m.%Y")
            except:
                date_str = task["date"]

            table_data.append({
                "Fach": task["title"].split(" – ")[0],
                "Aufgabe": task["title"].split(" – ")[1],
                "Datum": date_str,
                "Priorität": task["priority"],
                "Punkte": task["points"],
                "Beschreibung": task["description"],
                "Index": i
            })

        df = pd.DataFrame(table_data)
        df_display = df.drop(columns=["Index"])

        def highlight(row):
            color = priority_colors.get(row["Priorität"], "white")
            return [
                f"background-color: {color}" if col == "Priorität" else ""
                for col in df_display.columns
            ]

        st.dataframe(df_display.style.apply(highlight, axis=1), use_container_width=True)

        st.write("### 🗑️ Aufgabe löschen")

        for i, task in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([6, 1])
            col1.write(f"{task['title']} – {task['date']}")
            if col2.button("🗑️", key=f"del_task_{i}"):
                st.session_state.tasks.pop(i)
                data_manager.save_user_data(st.session_state.tasks, "tasks.json")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ------------------------ PRÜFUNGEN -----------------------
# ---------------------------------------------------------
elif selected_page == "Prüfungen":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📝 Neue Prüfung hinzufügen")

    if "exams" not in st.session_state:
        loaded_exams = data_manager.load_user_data("exams.json")
        st.session_state.exams = loaded_exams if loaded_exams else []

    # Fach-Auswahl + eigenes Fach
    fach_option = st.selectbox(
        "Fach:",
        ["Mathe", "Deutsch", "Englisch", "Biologie", "Chemie", "Andere"]
    )

    if fach_option == "Andere":
        fach = st.text_input("Eigenes Fach eingeben:")
    else:
        fach = fach_option

    datum = st.date_input("Datum:")
    lernplan = st.text_area("Lernplan:")
    zeit_von = st.text_input("Uhrzeit von (z. B. 09:00):")
    zeit_bis = st.text_input("Uhrzeit bis (z. B. 11:30):")
    raum = st.text_input("Raum (optional):")

    if st.button("💾 SPEICHERN"):
        new_exam = {
            "title": fach,
            "date": str(datum),
            "time_from": zeit_von,
            "time_to": zeit_bis,
            "room": raum,
            "plan": lernplan
        }
        st.session_state.exams.append(new_exam)
        data_manager.save_user_data(st.session_state.exams, "exams.json")
        st.success("Prüfung gespeichert!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Prüfungsliste
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🗂️ Alle Prüfungen")

    if len(st.session_state.exams) == 0:
        st.info("Noch keine Prüfungen vorhanden.")
    else:
        table_data = []
        for i, exam in enumerate(st.session_state.exams):
            try:
                date_obj = datetime.strptime(exam["date"], "%Y-%m-%d").date()
                date_str = date_obj.strftime("%d.%m.%Y")
            except:
                date_str = exam["date"]

            time_range = ""
            if exam.get("time_from"):
                time_range += exam["time_from"]
            if exam.get("time_to"):
                time_range += f"–{exam['time_to']}"

            table_data.append({
                "Fach": exam["title"],
                "Datum": date_str,
                "Zeit": time_range,
                "Raum": exam.get("room", ""),
                "Lernplan": exam.get("plan", ""),
                "Index": i
            })

        df = pd.DataFrame(table_data).drop(columns=["Index"])
        st.dataframe(df, use_container_width=True)

        st.write("### 🗑️ Prüfung löschen")

        for i, exam in enumerate(st.session_state.exams):
            col1, col2 = st.columns([6, 1])
            col1.write(f"{exam['title']} – {exam['date']}")
            if col2.button("🗑️", key=f"del_exam_{i}"):
                st.session_state.exams.pop(i)
                data_manager.save_user_data(st.session_state.exams, "exams.json")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ------------------------- PUNKTE -------------------------
# ---------------------------------------------------------
elif selected_page == "Punkte":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("🏆 Punkte")
    st.write("Hier kommt dein Punktefortschritt hin.")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# -------------------------- TEAM --------------------------
# ---------------------------------------------------------
elif selected_page == "Team":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    show_team_page()
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from datetime import datetime, timedelta
from utils.data_manager import DataManager


def show_weekly_view(data_manager: DataManager):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📅 Wochenübersicht")

    # Lade Aufgaben falls noch nicht vorhanden
    if "tasks" not in st.session_state:
        loaded_tasks = data_manager.load_user_data("tasks.json")
        st.session_state.tasks = loaded_tasks if loaded_tasks else []

    today = datetime.now().date()
    current_monday = today - timedelta(days=today.weekday())
    week_starts = [current_monday + timedelta(weeks=i) for i in range(4)]
    week_options = [
        f"{start.strftime('%d.%m.')} – {(start + timedelta(days=6)).strftime('%d.%m.')}"
        for start in week_starts
    ]

    selected_week = st.selectbox("Woche auswählen:", week_options)
    selected_start = week_starts[week_options.index(selected_week)]
    week_dates = [selected_start + timedelta(days=i) for i in range(7)]
    day_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    # Aufgaben nach Datum gruppieren
    tasks_by_date = {date: [] for date in week_dates}
    for task in st.session_state.tasks:
        try:
            task_date = datetime.strptime(task["date"], "%Y-%m-%d").date()
        except Exception:
            continue
        if task_date in tasks_by_date:
            tasks_by_date[task_date].append(task)

    cols = st.columns(7)
    for i, date in enumerate(week_dates):
        with cols[i]:
            st.markdown(f"### {day_names[i]} {date.strftime('%d.%m.')}")
            if tasks_by_date[date]:
                for task in tasks_by_date[date]:
                    st.markdown(
                        f"- **{task['title']}** "
                        f"({task.get('priority',''), task.get('points','')} Pkt)"
                    )
                    if task.get("description"):
                        st.caption(task["description"])
            else:
                st.write("Keine Aufgaben")

    st.markdown('</div>', unsafe_allow_html=True)
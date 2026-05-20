import streamlit as st
from datetime import datetime, timedelta
from utils.data_manager import DataManager
import re
import html 

def escape_text(text: str) -> str:
    return html.escape(text or "")

def show_weekly_view(data_manager: DataManager):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📅 Wochenübersicht")

    # Lade Aufgaben falls noch nicht vorhanden
    if "tasks" not in st.session_state:
        loaded_tasks = data_manager.load_user_data("tasks.json")
        st.session_state.tasks = loaded_tasks if loaded_tasks else []

    # Lade Prüfungen falls noch nicht vorhanden
    if "exams" not in st.session_state:
        loaded_exams = data_manager.load_user_data("exams.json")
        st.session_state.exams = loaded_exams if loaded_exams else []

    today = datetime.now().date()
    current_monday = today - timedelta(days=today.weekday())
    today = datetime.now().date()
    selected_date = st.date_input("Wähle ein Datum für die Woche:", value=today)
    selected_start = selected_date - timedelta(days=selected_date.weekday())
    week_dates = [selected_start + timedelta(days=i) for i in range(7)]
    day_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    # Aufgaben nach Datum gruppieren
    items_by_date = {date: [] for date in week_dates}
    for task in st.session_state.tasks:
        try:
            date_obj = datetime.strptime(task["date"], "%Y-%m-%d").date()
        except Exception:
            continue
        if date_obj in items_by_date:
            items_by_date[date_obj].append({"type": "task", **task})

    for exam in st.session_state.exams:
            try:
                date_obj = datetime.strptime(exam["date"], "%Y-%m-%d").date()
            except Exception:
                continue
            if date_obj in items_by_date:
                items_by_date[date_obj].append({"type": "exam", **exam})

    cols = st.columns(7)
    for i, date in enumerate(week_dates):
        with cols[i]:
            st.markdown(f"### {day_names[i]} {date.strftime('%d.%m.')}")
            if items_by_date[date]:
                for item in items_by_date[date]:
                    if item["type"] == "task":
                        description_text = escape_text(item.get("description", ""))
                        st.markdown(
                            f'''
                            <div style="background:#e6f2ff; padding:10px; border-radius:10px; margin-bottom:8px;">
                                <strong>{escape_text(item["title"])}</strong><br>
                                <span style="font-size:0.9em; color:#333;">
                                    {description_text}
                                </span>
                            </div>
                            ''',
                            unsafe_allow_html=True,
                        )
                    else:
                        time_str = ""
                        if item.get("time_from"):
                            time_str = escape_text(item["time_from"])
                        if item.get("time_to"):
                            time_str += f"–{escape_text(item['time_to'])}" if time_str else escape_text(item["time_to"])

                        plan_text = escape_text(item.get("plan", ""))
                        room_text = escape_text(item.get("room", ""))
                        st.markdown(
                            f'''
                            <div style="background:#f3e6ff; padding:10px; border-radius:10px; margin-bottom:8px;">
                                <strong>{escape_text(item["title"])}</strong><br>
                                <span style="font-size:0.9em; color:#333;">
                                    {time_str}<br>
                                    {room_text}<br>
                                    {plan_text}
                                </span>
                            </div>
                            ''',
                            unsafe_allow_html=True,
    )
            else:
                st.write("Keine Aufgaben oder Prüfungen")

    st.markdown('<span style="font-size:0.9em"> hellblau = Aufgabe, lila = Prüfung </span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
from datetime import datetime, timedelta
from utils.data_manager import DataManager
import html

def escape_text(text: str) -> str:
    return html.escape(text or "")

def show_weekly_view(data_manager: DataManager):

    st.title("📅 Wochenübersicht")

    # Daten laden
    if "tasks" not in st.session_state:
        st.session_state.tasks = data_manager.load_user_data("tasks.json") or []

    if "exams" not in st.session_state:
        st.session_state.exams = data_manager.load_user_data("exams.json") or []

    # Datumsauswahl
    today = datetime.now().date()
    selected_date = st.date_input("Wähle ein Datum für die Woche:", value=today)
    week_start = selected_date - timedelta(days=selected_date.weekday())
    week_dates = [week_start + timedelta(days=i) for i in range(7)]
    day_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    # Items gruppieren
    items_by_date = {d: [] for d in week_dates}

    for t in st.session_state.tasks:
        try:
            d = datetime.strptime(t["date"], "%Y-%m-%d").date()
            if d in items_by_date:
                items_by_date[d].append({"type": "task", **t})
        except:
            pass

    for e in st.session_state.exams:
        try:
            d = datetime.strptime(e["date"], "%Y-%m-%d").date()
            if d in items_by_date:
                items_by_date[d].append({"type": "exam", **e})
        except:
            pass

    # CSS – keine divs in der Tabelle!
    st.markdown("""
        <style>
            table.week-table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
            }
            table.week-table th {
                background: #f2f2f2;
                padding: 10px;
                border: 1px solid #ddd;
                font-size: 16px;
            }
            table.week-table td {
                vertical-align: top;
                padding: 10px;
                border: 1px solid #ddd;
                height: 150px;
                font-size: 14px;
            }
            .task {
                background: #d8e8c8; /* Pastell-Olive-Grün */
                display: block;
                padding: 6px;
                border-radius: 6px;
                margin-bottom: 6px;
            }
            .exam {
                background: #d7e9ff; /* Pastell-Blau */
                display: block;
                padding: 6px;
                border-radius: 6px;
                margin-bottom: 6px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Tabelle erzeugen
    html_table = "<table class='week-table'><tr>"

    # Kopfzeile
    for i, d in enumerate(week_dates):
        html_table += f"<th>{day_names[i]}<br>{d.strftime('%d.%m.')}</th>"
    html_table += "</tr><tr>"

    # Inhalte
    for d in week_dates:
        html_table += "<td>"

        if items_by_date[d]:
            for item in items_by_date[d]:

                if item["type"] == "task":
                    html_table += (
                        f"<span class='task'><strong>{escape_text(item['title'])}</strong><br>"
                        f"{escape_text(item.get('description',''))}</span>"
                    )

                else:
                    time_str = ""
                    if item.get("time_from"):
                        time_str = escape_text(item["time_from"])
                    if item.get("time_to"):
                        time_str += f"–{escape_text(item['time_to'])}" if time_str else escape_text(item["time_to"])

                    html_table += (
                        f"<span class='exam'><strong>{escape_text(item['title'])}</strong><br>"
                        f"{time_str}<br>"
                        f"{escape_text(item.get('room',''))}<br>"
                        f"{escape_text(item.get('plan',''))}</span>"
                    )

        else:
            html_table += "<span style='color:#777;'>Keine Einträge</span>"

        html_table += "</td>"

    html_table += "</tr></table>"

    st.markdown(html_table, unsafe_allow_html=True)

    # Legende
    st.markdown("""
        <br>
        <div style="display:flex; gap:20px; align-items:center;">
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:18px; height:18px; background:#d8e8c8; border-radius:4px;"></div>
                <span>Aufgabe</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:18px; height:18px; background:#d7e9ff; border-radius:4px;"></div>
                <span>Prüfung</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

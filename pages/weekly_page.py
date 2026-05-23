import streamlit as st
from datetime import datetime, timedelta, date
from pages.themes_page import get_theme_colors, apply_theme, show_theme_switcher
from utils.data_manager import DataManager
import math

def _parse_tasks(raw):
    """Erwartet Liste von dicts mit mindestens 'title' und 'date' (YYYY-MM-DD)."""
    tasks = []
    if raw is None:
        return tasks
    if isinstance(raw, dict):
        raw = [raw]
    for r in raw:
        try:
            d = datetime.strptime(r.get("date", ""), "%Y-%m-%d").date()
        except Exception:
            # falls kein gültiges Datum, überspringen
            continue
        tasks.append({
            "title": r.get("title", "Unbenannte Aufgabe"),
            "date": d,
            "priority": r.get("priority", ""),
            "points": r.get("points", 0),
            "description": r.get("description", "")
        })
    return tasks

def _priority_color(priority, colors):
    p = (priority or "").lower()
    if "hoch" in p or "high" in p:
        return f"linear-gradient(90deg,{colors['primary']}, {colors['secondary']})"
    if "mittel" in p or "medium" in p:
        return "linear-gradient(90deg,#f7b267,#f49fbc)"
    if "niedrig" in p or "low" in p:
        return "linear-gradient(90deg,#a8e6cf,#dcedc1)"
    return "linear-gradient(90deg,#e0e0e0,#f6f6f6)"

def show_weekly_page():
    # THEME
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    apply_theme()
    colors = get_theme_colors()

    st.markdown(
        f"""
        <style>
        .week-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }}
        .week-range {{ font-weight:700; color:{colors['text']}; }}
        .add-btn {{ background:{colors['primary']}; color:white; padding:8px 12px; border-radius:10px; }}
        .day-pills {{ display:flex; gap:10px; padding:12px; background:rgba(255,255,255,0.6); border-radius:12px; }}
        .day-pill {{ text-align:center; padding:8px 10px; border-radius:10px; min-width:56px; }}
        .day-pill.selected {{ background:{colors['primary']}; color:white; box-shadow:0 4px 18px rgba(0,0,0,0.08); }}
        .timeline {{ background: white; border-radius:18px; padding:18px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        .hours {{ color:#9aa0a6; font-size:12px; width:56px; }}
        .slot {{ height:48px; border-bottom:1px dashed #f0f0f0; position:relative; }}
        .task-card {{ position:absolute; left:70px; right:12px; padding:10px 14px; border-radius:12px; color:#111; }}
        .sidebar-card {{ background: white; border-radius:12px; padding:14px; box-shadow:0 2px 8px rgba(0,0,0,0.05); }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # HEADER
    today = date.today()
    # berechne Montage der aktuellen Woche
    weekday = (today.weekday() + 0)  # Monday=0
    monday = today - timedelta(days=weekday)
    sunday = monday + timedelta(days=6)
    st.markdown("<div class='week-header'>", unsafe_allow_html=True)
    st.markdown(f"<div><div class='week-range'>WOCHE: {monday.strftime('%d. %b %Y')} — {sunday.strftime('%d. %b %Y')}</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Lade Tasks
    dm = DataManager()
    raw_tasks = dm.load_user_data("tasks.json", initial_value=[])
    tasks = _parse_tasks(raw_tasks)

    # Tages-Pills mit Zählung
    days = [monday + timedelta(days=i) for i in range(7)]
    counts = {d: sum(1 for t in tasks if t["date"] == d) for d in days}
    pill_html = "<div class='day-pills'>"
    for d in days:
        cls = "day-pill"
        if d == today:
            cls += " selected"
        pill_html += f"<div class='{cls}'><div style='font-weight:700'>{d.strftime('%a')}</div><div style='font-size:12px;color:#6b6f76'>{d.day} • {counts[d]} Aufgaben</div></div>"
    pill_html += "</div>"
    st.markdown(pill_html, unsafe_allow_html=True)

    st.write("")  # small gap

    # MAIN LAYOUT: timeline (3/4) + sidebar (1/4)
    left_col, right_col = st.columns([3, 1])

    # TIMELINE: Stunden 08-22
    with left_col:
        st.markdown("<div class='timeline'>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex;'>", unsafe_allow_html=True)

        # hours column
        hours_html = "<div style='width:70px;padding-right:8px;'>"
        for hour in range(8, 23):
            hours_html += f"<div class='slot'><div class='hours'>{hour:02d}:00</div></div>"
        hours_html += "</div>"
        st.markdown(hours_html, unsafe_allow_html=True)

        # timeline area with tasks placed by index for each day (simple stacking)
        timeline_area = "<div style='flex:1; position:relative;'>"
        # create empty slots to show lines
        for i in range(8, 23):
            timeline_area += "<div class='slot'></div>"

        # Render tasks for selected day (today) first — then others can be shown below
        displayed_tasks = [t for t in tasks if monday <= t["date"] <= sunday]
        # group by date for ordering
        grouped = {}
        for t in displayed_tasks:
            grouped.setdefault(t["date"], []).append(t)

        # For simplicity: render tasks for the week sequentially, giving each a vertical offset
        offset_base = 8  # start after the top padding
        step_px = 70
        i = 0
        for d in sorted(grouped.keys()):
            day_tasks = grouped[d]
            for idx, task in enumerate(day_tasks):
                top_px = offset_base + i * (step_px)
                color = _priority_color(task.get("priority", ""), colors)
                # simple card with title, date and points
                timeline_area += (
                    f"<div class='task-card' style='top:{top_px}px;background:{color}; box-shadow:0 6px 20px rgba(0,0,0,0.06);'>"
                    f"<div style='font-weight:700'>{task['title']}</div>"
                    f"<div style='font-size:12px;color:#444'>{d.strftime('%a %d.%m.%Y')} • {task.get('points',0)} Punkte</div>"
                    f"</div>"
                )
                i += 1

        timeline_area += "</div>"  # close flex:1
        st.markdown(timeline_area, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # SIDEBAR: Fortschritt + Statistik + Hinweis
    with right_col:
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Wochenfortschritt")
        # einfache Berechnung: erledigte Aufgaben / alle Aufgaben (hier: keine Erledigt-Flag in tasks.json, daher Demo)
        total = len(displayed_tasks)
        # demo: points as proxy: percentage = min(100, sum(points)/ (total*5) *100) if total>0
        if total > 0:
            percent = int(min(100, (sum(t.get("points",0) for t in displayed_tasks) / (total * 5 or 1)) * 100))
        else:
            percent = 0
        st.progress(percent / 100)
        st.markdown(f"<div style='font-weight:700;color:{colors['primary']};'>{percent}%</div>", unsafe_allow_html=True)
        st.caption("Super gemacht! 💜")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Deine Statistik")
        st.markdown(f"- **{total}** Aufgaben diese Woche")
        exams = sum(1 for t in displayed_tasks if "prüfung" in t["title"].lower() or "prüf" in t["title"].lower())
        st.markdown(f"- **{exams}** Prüfungen")
        st.markdown(f"- **{sum(t.get('points',0) for t in displayed_tasks)}** Punkte gesammelt")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Hinweis")
        if exams > 0:
            st.info("Du hast diese Woche mindestens eine Prüfung. Viel Erfolg! 🍀")
        else:
            st.info("Keine Prüfungen gefunden. Gut geplant!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Theme switcher unterhalb
    show_theme_switcher()
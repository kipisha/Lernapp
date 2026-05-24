import streamlit as st
from datetime import datetime, timedelta, date
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager

def _parse_tasks(raw):
    """Erwartet Liste von dicts. Nutzt 'due' für das Datum von Aufgaben."""
    tasks = []
    if raw is None:
        return tasks
    if isinstance(raw, dict):
        raw = [raw]
    for r in raw:
        # Aufgaben nutzen 'due', Prüfungen nutzen 'date' -> wir prüfen beides ab
        date_str = r.get("due") or r.get("date", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            # Falls kein gültiges Datum vorhanden ist, überspringen
            continue
            
        tasks.append({
            "title": r.get("title", "Unbenannte Aufgabe"),
            "date": d,
            "priority": r.get("priority", ""),
            "points": r.get("points", 0) or r.get("duration", 0) or 0,
            "subject": r.get("subject", "Allgemein"),
            "notes": r.get("notes", ""),
            "done": r.get("done", False)  # Richtigen Erledigt-Status auslesen
        })
    return tasks

def _priority_color(priority, colors):
    p = (priority or "").lower()
    if "hoch" in p or "high" in p:
        return f"linear-gradient(90deg, {colors.get('primary', '#7c3aed')}, #4c1d95)"
    if "mittel" in p or "medium" in p:
        return "linear-gradient(90deg, #f7b267, #f49fbc)"
    if "niedrig" in p or "low" in p:
        return "linear-gradient(90deg, #a8e6cf, #dcedc1)"
    return "linear-gradient(90deg, #e0e0e0, #f6f6f6)"

def show_weekly_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    apply_theme()
    colors = get_theme_colors() or {}
    primary_color = colors.get("primary", "#7c3aed")
    text_color = colors.get("text", "#000000")

    st.markdown(
        f"""
        <style>
        .week-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }}
        .week-range {{ font-weight:700; color:{text_color}; font-size: 20px; }}
        .day-pills {{ display:flex; gap:10px; padding:12px; background:rgba(255,255,255,0.6); border-radius:12px; justify-content: space-between; }}
        .day-pill {{ text-align:center; padding:8px 10px; border-radius:10px; flex:1; background: white; border: 1px solid #f0f0f0; }}
        .day-pill.selected {{ background:{primary_color}; color:white; box-shadow:0 4px 18px rgba(0,0,0,0.08); }}
        .day-pill.selected div {{ color: white !important; }}
        .timeline {{ background: white; border-radius:18px; padding:18px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        .hours {{ color:#9aa0a6; font-size:12px; width:56px; }}
        .slot {{ height:55px; border-bottom:1px dashed #f0f0f0; position:relative; }}
        .task-container {{ position: relative; flex: 1; }}
        .task-card {{ padding:10px 14px; border-radius:12px; color:#111; margin-bottom: 10px; border-left: 5px solid {primary_color}; background: #f9fafb; }}
        .sidebar-card {{ background: white; border-radius:12px; padding:14px; box-shadow:0 2px 8px rgba(0,0,0,0.05); }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- DATEN LADEN & PARSEN ---
    dm = DataManager()
    raw_tasks = dm.load_user_data("tasks.json", initial_value=[])
    raw_exams = dm.load_user_data("exams.json", initial_value=[])
    
    # Beide Datenquellen parsen und kombinieren
    all_items = _parse_tasks(raw_tasks) + _parse_tasks(raw_exams)

    # --- WOCHEN-NAVIGATION ---
    if "current_week_offset" not in st.session_state:
        st.session_state.current_week_offset = date.today()
        
    today = date.today()
    monday = st.session_state.current_week_offset - timedelta(days=st.session_state.current_week_offset.weekday())
    sunday = monday + timedelta(days=6)

    st.markdown("<div class='week-header'>", unsafe_allow_html=True)
    st.markdown(f"<div class='week-range'>📅 WOCHE: {monday.strftime('%d. %b %Y')} — {sunday.strftime('%d. %b %Y')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_nav1, col_nav2, col_nav3 = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("◀ Vorherige", key="prev_week"):
            st.session_state.current_week_offset -= timedelta(days=7)
            st.rerun()
    with col_nav3:
        if st.button("Nächste ▶", key="next_week"):
            st.session_state.current_week_offset += timedelta(days=7)
            st.rerun()

    # --- TAGES-PILLS MIT ECHTER ANZAHL ---
    days = [monday + timedelta(days=i) for i in range(7)]
    counts = {d: sum(1 for t in all_items if t["date"] == d and not t["done"]) for d in days}
    
    pill_html = "<div class='day-pills'>"
    for d in days:
        cls = "day-pill"
        if d == today:
            cls += " selected"
        pill_html += f"""
        <div class='{cls}'>
            <div style='font-weight:700;'>{d.strftime('%a')}</div>
            <div style='font-size:12px; color:#6b6f76;'>{d.day}.{d.month}</div>
            <div style='font-size:11px; font-weight:bold; color:{primary_color};'>{counts[d]} Offen</div>
        </div>"""
    pill_html += "</div>"
    st.markdown(pill_html, unsafe_allow_html=True)
    st.write("") 

    # --- MAIN LAYOUT ---
    left_col, right_col = st.columns([3, 1])

    # Relevante Items für diese Woche filtern
    displayed_items = [t for t in all_items if monday <= t["date"] <= sunday]

    with left_col:
        st.markdown("<div class='timeline'>", unsafe_allow_html=True)
        st.markdown("#### 📋 Deine Wochenübersicht nach Tagen")
        
        # Gruppierung der Aufgaben nach Wochentag
        grouped = {}
        for t in displayed_items:
            grouped.setdefault(t["date"], []).append(t)
            
        if not displayed_items:
            st.info("Keine Aufgaben oder Prüfungen für diese Woche geplant! 🎉")
        else:
            for d in sorted(grouped.keys()):
                st.markdown(f"<div style='font-weight:bold; margin-top:15px; border-bottom:1px solid #eee; padding-bottom:4px;'>{d.strftime('%A, %d.%m.%Y')}</div>", unsafe_allow_html=True)
                for task in grouped[d]:
                    status_icon = "✅ Erledigt" if task["done"] else "⏳ Offen"
                    color = _priority_color(task.get("priority", ""), colors)
                    
                    st.markdown(
                        f"""
                        <div class='task-card' style='background: #fafafa; border-left-color: {primary_color if not task['done'] else '#9ca3af'}; opacity: {0.6 if task['done'] else 1.0};'>
                            <div style='display:flex; justify-content:space-between; font-weight:700;'>
                                <span>{task['title']} <small style='color:#666;'>({task['subject']})</small></span>
                                <span style='font-size:12px; background:#fff; padding:2px 6px; border-radius:4px;'>{status_icon}</span>
                            </div>
                            <div style='font-size:12px; color:#555; margin-top:4px;'>
                                {task['notes'] if task['notes'] else 'Keine Notizen'}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SIDEBAR: STATISTIK & METRIKEN ---
    with right_col:
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Wochenfortschritt")
        
        total_tasks = len(displayed_items)
        completed_tasks = sum(1 for t in displayed_items if t["done"])
        
        if total_tasks > 0:
            percent = int((completed_tasks / total_tasks) * 100)
        else:
            percent = 0
            
        st.progress(percent / 100.0)
        st.markdown(f"<div style='font-weight:700; color:{primary_color};'>{percent}% abgeschlossen</div>", unsafe_allow_html=True)
        st.caption("Super gemacht! Weiter so! 🔥" if percent > 50 else "Guter Start, bleib dran! 💪")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Deine Statistik")
        st.markdown(f"- **{total_tasks}** Einträge insgesamt")
        st.markdown(f"- **{completed_tasks}** erledigt")
        
        exams_count = sum(1 for t in displayed_items if "prüfung" in t["title"].lower() or "prüf" in t["title"].lower() or "gks" in t["title"].lower())
        st.markdown(f"- **{exams_count}** Prüfungen")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Hinweis")
        if exams_count > 0:
            st.error("⚠️ Du hast diese Woche wichtige Prüfungen! Bereite dich gut vor. Viel Erfolg! 🍀")
        else:
            st.info("Keine Prüfungen diese Woche. Zeit, um entspannt alte Lücken zu schließen! 📚")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_weekly_page()
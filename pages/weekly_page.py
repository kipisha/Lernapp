import streamlit as st
from datetime import datetime, timedelta, date
from pages.themes_page import get_theme_colors, apply_theme
from utils.data_manager import DataManager

def _parse_items(raw, item_type="task"):
    """
    Parst Aufgaben und Prüfungen krisensicher. 
    Unterscheidet nach Typ, um im UI die korrekten Badges anzuzeigen.
    """
    items = []
    if raw is None:
        return items
    if isinstance(raw, dict):
        raw = [raw]
        
    for r in raw:
        # Aufgaben nutzen 'due', Prüfungen nutzen 'date'
        date_str = r.get("due") or r.get("date", "")
        try:
            # Falls Datum im ISO-Format mit Zeit kommt, splitten wir es
            if "T" in date_str:
                date_str = date_str.split("T")[0]
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            continue
            
        items.append({
            "title": r.get("title", "Unbenannter Eintrag"),
            "date": d,
            "subject": r.get("subject", "Allgemein"),
            "notes": r.get("notes", ""),
            "done": bool(r.get("done", False)),
            "type": item_type,
            "progress": r.get("progress", 0) if item_type == "exam" else None,
            "tag": r.get("tag", "Prüfung" if item_type == "exam" else "Hausaufgabe")
        })
    return items

def show_weekly_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    apply_theme()
    colors = get_theme_colors() or {}
    primary_color = colors.get("primary", "#7c3aed")
    text_color = colors.get("text", "#000000")

    # --- CSS STYLES ---
    st.markdown(
        f"""
        <style>
        .week-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }}
        .week-range {{ font-weight:700; color:{text_color}; font-size: 20px; }}
        .task-card {{ padding:14px; border-radius:12px; color:#111; margin-bottom: 12px; border-left: 5px solid {primary_color}; background: #ffffff; box-shadow: 0 2px 6px rgba(0,0,0,0.02); }}
        .sidebar-card {{ background: white; border-radius:12px; padding:14px; box-shadow:0 2px 8px rgba(0,0,0,0.05); }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- DATEN LADEN ---
    dm = DataManager()
    raw_tasks = dm.load_user_data("tasks.json", initial_value=[])
    raw_exams = dm.load_user_data("exams.json", initial_value=[])
    
    all_items = _parse_items(raw_tasks, "task") + _parse_items(raw_exams, "exam")

    # --- WOCHEN-NAVIGATION STATE ---
    if "current_week_offset" not in st.session_state:
        st.session_state.current_week_offset = date.today()
    if "selected_day_filter" not in st.session_state:
        st.session_state.selected_day_filter = None
        
    monday = st.session_state.current_week_offset - timedelta(days=st.session_state.current_week_offset.weekday())
    sunday = monday + timedelta(days=6)

    st.markdown("<div class='week-header'>", unsafe_allow_html=True)
    st.markdown(f"<div class='week-range'>📅 WOCHE: {monday.strftime('%d. %b')} — {sunday.strftime('%d. %b %Y')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Navigations-Buttons
    col_nav1, col_nav2, col_nav3 = st.columns([1.5, 3, 1.5])
    with col_nav1:
        if st.button("◀ Vorherige Woche", use_container_width=True, key="prev_week"):
            st.session_state.current_week_offset -= timedelta(days=7)
            st.session_state.selected_day_filter = None # Filter zurücksetzen
            st.rerun()
    with col_nav2:
        if st.button("Zur aktuellen Woche springen", use_container_width=True, key="today_week"):
            st.session_state.current_week_offset = date.today()
            st.session_state.selected_day_filter = None
            st.rerun()
    with col_nav3:
        if st.button("Nächste Woche ▶", use_container_width=True, key="next_week"):
            st.session_state.current_week_offset += timedelta(days=7)
            st.session_state.selected_day_filter = None
            st.rerun()

    st.write("")

    # --- INTERAKTIVE TAGES-PILLS (BUTTONS) ---
    days = [monday + timedelta(days=i) for i in range(7)]
    day_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    
    # Zähle offene Items für jeden Tag
    counts = {d: sum(1 for t in all_items if t["date"] == d and not t["done"]) for d in days}
    
    st.markdown("##### Wähle einen Tag zum Filtern oder betrachte die ganze Woche:")
    pill_cols = st.columns(7)
    
    for i, col in enumerate(pill_cols):
        d = days[i]
        is_selected = (st.session_state.selected_day_filter == d)
        is_today = (d == date.today())
        
        # Label-Styling für den Button
        button_label = f"{day_names[i]}\n{d.day}.{d.month}.\n({counts[d]} ⏳)"
        
        with col:
            # Hervorhebung verändern je nach Auswahl oder "Heute"-Status
            if is_selected:
                type_style = "primary"
            elif is_today:
                type_style = "secondary"
            else:
                type_style = "tertiary"
                
            if st.button(button_label, key=f"pill_btn_{d.isoformat()}", use_container_width=True, type=type_style):
                if st.session_state.selected_day_filter == d:
                    st.session_state.selected_day_filter = None # Klick hebt Filter wieder auf
                else:
                    st.session_state.selected_day_filter = d
                st.rerun()

    st.write("") 

    # --- FILTRATION DER ITEMS ---
    # Grundfilter für die aktuelle Woche
    displayed_items = [t for t in all_items if monday <= t["date"] <= sunday]
    
    # Zusatzfilter falls eine Day-Pill aktiv ausgewählt ist
    if st.session_state.selected_day_filter:
        displayed_items = [t for t in displayed_items if t["date"] == st.session_state.selected_day_filter]
        heading_text = f"📋 Einträge am {st.session_state.selected_day_filter.strftime('%A, %d.%m.%Y')}"
    else:
        heading_text = "📋 Deine Wochenübersicht nach Tagen"

    # --- MAIN LAYOUT ---
    left_col, right_col = st.columns([2.5, 1])

    with left_col:
        st.markdown(f"#### {heading_text}")
        
        # Gruppierung der gefilterten Aufgaben nach Wochentag
        grouped = {}
        for t in displayed_items:
            grouped.setdefault(t["date"], []).append(t)
            
        if not displayed_items:
            if st.session_state.selected_day_filter:
                st.info("Keine Aufgaben oder Prüfungen für diesen Tag geplant! ☕")
            else:
                st.info("Keine Aufgaben oder Prüfungen für diese Woche geplant! 🎉")
        else:
            for d in sorted(grouped.keys()):
                st.markdown(f"<div style='font-weight:bold; margin-top:14px; margin-bottom:6px; border-bottom:1px solid #ddd; padding-bottom:2px; color:{text_color};'>{d.strftime('%A, %d.%m.%Y')}</div>", unsafe_allow_html=True)
                for item in grouped[d]:
                    status_icon = "✅ Erledigt" if item["done"] else "⏳ Offen"
                    
                    # Visuelle Trennung: Prüfungen rot/orange anhauchen, Aufgaben violett/cozy
                    if item["type"] == "exam":
                        card_border_color = "#f43f5e" # Prüfungen bekommen ein markantes Rot
                        badge_html = f"<span style='font-size:11px; background:#fff1f2; color:#e11d48; padding:2px 8px; border-radius:6px; font-weight:bold;'>📚 {item['tag']}</span>"
                    else:
                        card_border_color = primary_color
                        badge_html = f"<span style='font-size:11px; background:#f3e8ff; color:#7e22ce; padding:2px 8px; border-radius:6px; font-weight:bold;'>📅 {item['tag']}</span>"
                    
                    st.markdown(
                        f"""
                        <div class='task-card' style='border-left-color: {card_border_color if not item['done'] else '#9ca3af'}; opacity: {0.55 if item['done'] else 1.0};'>
                            <div style='display:flex; justify-content:space-between; align-items:center; font-weight:700;'>
                                <span>{item['title']} <small style='color:#6b7280; font-weight:normal;'>({item['subject']})</small></span>
                                <div style='display:flex; gap:6px;'>
                                    {badge_html}
                                    <span style='font-size:11px; background:#f3f4f6; padding:2px 6px; border-radius:6px;'>{status_icon}</span>
                                </div>
                            </div>
                            <div style='font-size:13px; color:#4b5563; margin-top:6px; font-style: italic;'>
                                {item['notes'] if item['notes'] else 'Keine zusätzlichen Notizen hinterlegt.'}
                            </div>
                            {f"<div style='margin-top:8px; font-size:11px; color:#6b7280;'>Vorbereitungsstatus: <b>{int(item['progress'])}%</b></div>" if item['type']=='exam' else ''}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # --- SIDEBAR: STATISTIK & METRIKEN ---
    with right_col:
        # Wochen-Basis-Items (immer auf die ganze Woche bezogen für stabile Statistiken)
        week_items = [t for t in all_items if monday <= t["date"] <= sunday]
        total_tasks = len(week_items)
        completed_tasks = sum(1 for t in week_items if t["done"])
        exams_count = sum(1 for t in week_items if t["type"] == "exam")
        
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Wochenfortschritt")
        
        if total_tasks > 0:
            percent = int((completed_tasks / total_tasks) * 100)
        else:
            percent = 0
            
        st.progress(percent / 100.0)
        st.markdown(f"<div style='font-weight:700; color:{primary_color}; text-align:center; margin-top:4px;'>{percent}% abgeschlossen</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Statistik (Ganze Woche)")
        st.markdown(f"- **{total_tasks}** Einträge geplant")
        st.markdown(f"- **{completed_tasks}** davon erledigt")
        st.markdown(f"- **{total_tasks - completed_tasks}** noch offen")
        st.markdown(f"- **{exams_count}** wichtige Prüfung(en)")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### Status-Hinweis")
        if exams_count > 0:
            st.error("⚠️ Achtung! Du hast diese Woche wichtige Prüfungen auf deinem Zettel! Plane genug Pufferzeiten zum Lernen ein. Viel Erfolg! 🍀")
        else:
            st.info("Hervorragend! Keine Prüfungen in dieser Woche. Eine super Gelegenheit, um offene Hausaufgaben abzuarbeiten oder entspannt vorzulernen! 📚")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_weekly_page()
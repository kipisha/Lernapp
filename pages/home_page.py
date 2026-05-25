import streamlit as st
from datetime import datetime, timedelta, date
from pages.themes_page import get_theme_colors, apply_theme, show_theme_switcher
from utils.data_manager import DataManager
from pages.point_system_page import calc_level_and_progress
import random
import copy

# --- Data load helpers ---
def load_data(filename):
    return DataManager().load_user_data(filename, initial_value=[])

def save_done(item, filename):
    dm = DataManager()
    data = load_data(filename)
    updated = _find_and_update(
        data,
        item,
        lambda e: {
            **e,
            "done": True,
            "done_at": datetime.utcnow().isoformat()}
    )
    if updated:
        dm.save_user_data(data, filename)
    return updated

def load_tasks():
    return load_data("tasks.json")

def load_exams():
    return load_data("exams.json")

def mark_task_done(task):
    return save_done(task, "tasks.json")

def mark_exam_done(exam):
    return save_done(exam, "exams.json")

# Aufgaben ignorieren, die bereits erledigt sind
def get_next_item(items, date_key):
    if not items:
        return None
    pending = [i for i in items if not i.get("done", False)]
    if not pending:
        return None
    return min(pending, key=lambda i: i.get(date_key, "9999-12-31"))

def get_next_task(tasks):
    return get_next_item(tasks, "due")

def get_next_exam(exams):
    return get_next_item(exams, "date")

# --- Persist changes ---
def _find_and_update(list_data, item, update_fn):
    task_id = item.get("created_at") or item.get("timestamp")
    for i, entry in enumerate(list_data):
        if task_id:
            same_id = (entry.get("created_at") == task_id) or (entry.get("timestamp") == task_id)
        else:
            same_title = entry.get("title") == item.get("title")
            same_due = (entry.get("due") == item.get("due")) or (entry.get("date") == item.get("date"))
            same_id = same_title and same_due

        if same_id:
            list_data[i] = update_fn(entry)
            return True
    return False

# --- Motivation ---
MOTIVATION_LIST = [
    "Disziplin heute, Stolz morgen.",
    "Auch kleine Schritte bringen dich ans Ziel.",
    "Du bist stärker als deine Ausreden.",
    "Jeder Tag ist eine neue Chance.",
    "Erfolg beginnt im Kopf.",
    "Mach es für dein zukünftiges Ich.",
    "Wenn du aufgibst, wird es nie passieren.",
    "Heute ist ein guter Tag, um anzufangen.",
    "Du wächst an deinen Herausforderungen.",
    "Konstanz schlägt Talent."
]
def get_daily_motivation():
    if "daily_motivation" not in st.session_state:
        st.session_state.daily_motivation = random.choice(MOTIVATION_LIST)
    return st.session_state.daily_motivation

# --- Checkliste-Werte speichern ---
def save_task_checklist(task, checked_states):
    dm = DataManager()
    tasks = dm.load_user_data("tasks.json", initial_value=[])
    updated = _find_and_update(tasks, task, lambda e: {**e, "checked": checked_states})
    if updated:
        dm.save_user_data(tasks, "tasks.json")
        return True
    return False

# --- Detail renderers ---
def render_task_detail(task, colors):
    st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin:0'>{task.get('title','Untitled')}</h3>", unsafe_allow_html=True)
    st.markdown(f"<span style='background:#eef9f1;padding:6px;border-radius:8px;color:#2e8b57;font-weight:600;'>Aufgabe</span>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:8px;color:#666'>{task.get('subject','')}</div>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    due = task.get("due", "—")
    duration = task.get("duration_min", task.get("duration", "—"))
    notes = task.get("notes", "")
    st.markdown(f"<b>Fällig am</b><br><div style='color:#333'>{due}</div>", unsafe_allow_html=True)
    st.markdown(f"<b>Dauer</b><br><div style='color:#333'>{duration} Minuten</div>", unsafe_allow_html=True)
    if notes:
        st.markdown("<b>Notizen</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#444'>{notes}</div>", unsafe_allow_html=True)

    st.markdown("<b>Checkliste</b>", unsafe_allow_html=True)
    checklist = task.get("checklist", ["Aufgaben lesen", "Lösen", "Kontrollieren"])
    checked = task.get("checked", [False] * len(checklist))
    new_checked = []
    for i, item in enumerate(checklist):
        key = f"task_chk_{task.get('created_at', task.get('timestamp',''))}_{i}"
        ch = checked[i] if i < len(checked) else False
        new_val = st.checkbox(item, value=ch, key=key)
        new_checked.append(new_val)
        
    if new_checked != checked:
        ok = save_task_checklist(task, new_checked)
        if ok:
            task["checked"] = new_checked
            st.success("Checkliste gespeichert")

    st.markdown("<div style='display:flex;gap:12px;margin-top:12px;'>", unsafe_allow_html=True)
    if st.button("Als erledigt markieren", key="done_task"):
        ok = mark_task_done(task)
        if ok:
            st.success("Aufgabe als erledigt markiert")
            st.session_state.selected = None
            st.rerun()  # Behebt st.experimental_rerun()
        else:
            st.error("Konnte Aufgabe nicht als erledigt markieren")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_exam_detail(exam, colors):
    st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin:0'>{exam.get('title','Untitled')}</h3>", unsafe_allow_html=True)
    st.markdown(f"<span style='background:#fff0f3;padding:6px;border-radius:8px;color:#c0392b;font-weight:600;'>Prüfung</span>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)

    date_str = exam.get("date", "—")
    time_str = exam.get("time", exam.get("time", "—"))
    subject = exam.get("subject", "")
    notes = exam.get("notes", "")
    topics = exam.get("topics", [])

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f"<b>Datum</b><br><div style='color:#333'>{date_str}</div>", unsafe_allow_html=True)
    st.markdown(f"<b>Uhrzeit</b><br><div style='color:#333'>{time_str}</div>", unsafe_allow_html=True)
    st.markdown(f"<b>Fach</b><br><div style='color:#333'>{subject}</div>", unsafe_allow_html=True)

    if topics:
        st.markdown("<b>Themen</b>", unsafe_allow_html=True)
        for t in topics:
            st.markdown(f"• {t}")

    prog = exam.get("progress", 0)
    try:
        p = float(prog)
        if p > 1:
            p = p / 100.0
    except Exception:
        p = 0.0
    st.markdown("<b>Fortschritt</b>", unsafe_allow_html=True)
    st.progress(p)
    st.markdown(f"<div style='text-align:right;color:#666'>{int(p*100)}%</div>", unsafe_allow_html=True)
    if notes:
        st.markdown("<b>Notizen</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#444'>{notes}</div>", unsafe_allow_html=True)

    st.markdown("<div style='display:flex;gap:12px;margin-top:12px;'>", unsafe_allow_html=True)
    if st.button("Als erledigt markieren", key="done_exam"):
        ok = mark_exam_done(exam)
        if ok:
            st.success("Prüfung als erledigt markiert")
            st.session_state.selected = None
            st.rerun()  # Behebt st.experimental_rerun()
        else:
            st.error("Konnte Prüfung nicht als erledigt markieren")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Styles ---
st.markdown("""
<style>
.card { background:#fff;border-radius:12px;padding:14px;box-shadow:0 2px 6px rgba(0,0,0,0.04); }
.detail-card { background:#fff;border-radius:12px;padding:18px;box-shadow:0 6px 18px rgba(0,0,0,0.06); margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
def show_profile_sidebar_button():
    if st.session_state.get("authentication_status") is True:
        with st.sidebar:
            if st.button("👤 Profil", use_container_width=True, key="nav_btn_Profil"):
                st.session_state.page = "Profil"
                st.rerun()

            st.markdown(
                "<div style='margin: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.1);'></div>",
                unsafe_allow_html=True,
            )

def show_sidebar_nav():
    with st.sidebar:
        st.markdown("<h1 style='color:#7c3aed;'>smartplan ✦</h1>", unsafe_allow_html=True)
        nav_items = [
            ("🏠 Home", "Home"),
            ("📅 Woche", "Woche"),
            ("✅ Aufgaben", "Aufgaben"),
            ("📚 Prüfungen", "Prüfungen"),
            ("⭐ Punkte", "Punkte"),
            ("👥 Team", "Team"),
        ]
        for label, page in nav_items:
            if st.button(label, use_container_width=True, key=f"nav_btn_{page}"):
                st.session_state.page = page
                st.rerun()

# --- Main page ---
def show_home_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    if "selected" not in st.session_state:
        st.session_state.selected = None

    colors = get_theme_colors()
    apply_theme()
    
    # Verhindert DuplicateKey Error, falls show_theme_switcher() schon woanders geladen wird
    try:
        show_theme_switcher()
    except Exception:
        pass
    
        st.markdown("""
<div style='padding:10px;border-radius:8px;background:#f5f5f7;border:1px solid #e2e2e6;margin-top:10px;'>
💡 Wähle eines der 4 Themes und passe die App deinem Mood an.
</div>
""", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='margin-bottom: 16px;'>
            <span style='color:{colors['primary']};font-size:14px;font-weight:bold;'>HOME / STARTSEITE</span>
            <h2 style='margin:0;color:{colors['text']};'>Hey {st.session_state.get('username','Gast')}! 👋</h2>
            <span style='color:#b0aeb8;'>Schön, dass du da bist. Bereit für einen produktiven Tag?</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- DATEN LADEN ---
    tasks = load_tasks()
    exams = load_exams()
    
    # --- DYNAMISCHE PUNKTE- & LEVELBERECHNUNG ---
    # Berechnet Punkte dynamisch (z.B. 20 Punkte pro erledigter Aufgabe / Prüfung)
    total_points = sum(int(t.get("points", 20)) for t in tasks if t.get("done", False)) + sum(int(e.get("points", 50)) for e in exams if e.get("done", False))
    
    # Nutzt deine Logik aus der point_system_page.py
    level_data = calc_level_and_progress(total_points)
    aktuelle_stufe = level_data.get("level", 1)

    # --- DYNAMISCHE TAGESFORTSCHRITT-BERECHNUNG ---
    done_tasks = sum(1 for t in tasks if t.get("done", False))
    done_exams = sum(1 for e in exams if e.get("done", False))
    
    total_items = len(tasks) + len(exams)
    total_done = done_tasks + done_exams
    
    fortschritt_prozent = int((total_done / total_items) * 100) if total_items > 0 else 0

    # --- TAGESFORTSCHRITT ANZEIGEN ---
    st.markdown("<div class='card' style='margin-bottom: 24px;'>", unsafe_allow_html=True)
    st.markdown("#### Tagesfortschritt")
    st.progress(fortschritt_prozent / 100.0)
    st.markdown(f"<span style='color:{colors['primary']};font-size:32px;font-weight:bold;'>{fortschritt_prozent}%</span>", unsafe_allow_html=True)
    st.caption("Super gemacht! Weiter so! 💪")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- ÜBERSICHT MIT DYNAMISCHEN BADGES ---
    st.markdown("#### Deine Übersicht")
    task_count_todo = len([t for t in tasks if not t.get("done", False)])
    exam_count_todo = len([e for e in exams if not e.get("done", False)])

    st.markdown(
        f"""
        <div style='display:flex;gap:40px;justify-content:center;margin-top:12px;margin-bottom:24px;'>
            <div style='text-align:center;'><div style='font-size:56px;margin-bottom:6px;'>📅</div><b style='font-size:16px;'>{task_count_todo}</b><br><span style='font-size:12px;color:#374151;'>Aufgaben</span></div>
            <div style='text-align:center;'><div style='font-size:56px;margin-bottom:6px;'>📚</div><b style='font-size:16px;'>{exam_count_todo}</b><br><span style='font-size:12px;color:#374151;'>Prüfungen</span></div>
            <div style='text-align:center;'><div style='font-size:56px;margin-bottom:6px;'>⭐</div><b style='font-size:16px;'>{aktuelle_stufe}</b><br><span style='font-size:12px;color:#374151;'>Stufe</span></div>
            <div style='text-align:center;'><div style='font-size:56px;margin-bottom:6px;'>🏆</div><b style='font-size:16px;'>{total_points}</b><br><span style='font-size:12px;color:#374151;'>Punkte</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Falls ein Element zur Detailansicht ausgewählt wurde
    if st.session_state.selected:
        sel = st.session_state.selected
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;'>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='margin:0'>{'Aufgabe' if sel['type']=='task' else 'Prüfung'} — Detailansicht</h4>", unsafe_allow_html=True)
        if st.button("Zurück", key="back_from_detail"):
            st.session_state.selected = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if sel['type'] == 'task':
            render_task_detail(sel['item'], colors)
        else:
            render_exam_detail(sel['item'], colors)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # --- KARTEN-SEKTION (Nächste Aufgabe / Prüfung) ---
    col4, col5, col6 = st.columns(3)
    next_task = get_next_task(tasks)

    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Aufgabe")
        if next_task:
            st.success(f"**{next_task.get('title','')}**\n\nFällig am: {next_task.get('due','')}")
            if st.button("Jetzt starten", key="start_now"):
                st.session_state.selected = {'type':'task','item': copy.deepcopy(next_task)}
                st.rerun()
        else:
            st.info("Keine Aufgaben vorhanden.")
        st.markdown("</div>", unsafe_allow_html=True)

    next_exam = get_next_exam(exams)
    with col5:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Prüfung")
        if next_exam:
            st.warning(f"**{next_exam.get('title','')}**\n\nDatum: {next_exam.get('date','')}")
            if st.button("Prüfung ansehen", key="view_exam"):
                st.session_state.selected = {'type':'exam','item': copy.deepcopy(next_exam)}
                st.rerun()
        else:
            st.info("Keine Prüfungen vorhanden.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col6:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Motivation für dich")
        motivation = get_daily_motivation()
        st.success(f"„{motivation}“")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- DYNAMISCHE WOCHENÜBERSICHT ---
    st.markdown("<div class='card' style='margin-top: 24px;'>", unsafe_allow_html=True)
    st.markdown("#### Deine Woche auf einen Blick")
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    
    # Aktuellen Montag als Startpunkt ermitteln
    today_date = date.today()
    monday_date = today_date - timedelta(days=today_date.weekday())
    
    cols = st.columns(7)
    for i, col in enumerate(cols):
        current_day = monday_date + timedelta(days=i)
        day_str = current_day.isoformat()
        
        # Holen aller Aufgaben und Prüfungen für diesen Wochentag
        day_items = [t for t in tasks if t.get("due") == day_str] + [e for e in exams if e.get("date") == day_str]
        day_done = sum(1 for item in day_items if item.get("done", False))
        
        # Berechnen des Erledigungsgrades für diesen Wochentag
        day_progress = (day_done / len(day_items)) if len(day_items) > 0 else 0.0
        
        with col:
            st.markdown(f"**{days[i]}**")
            st.markdown(f"{current_day.day}.{current_day.month}.")
            st.progress(day_progress)
            
    st.markdown("</div>", unsafe_allow_html=True)
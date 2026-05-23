import streamlit as st
from datetime import datetime, timedelta, date
from pages.themes_page import get_theme_colors, apply_theme, show_theme_switcher
from utils.data_manager import DataManager
import random
import copy

# --- Data load helpers ---
def load_tasks():
    dm = DataManager()
    return dm.load_user_data("tasks.json", initial_value=[])

def load_exams():
    dm = DataManager()
    return dm.load_user_data("exams.json", initial_value=[])

# ignore tasks/exams that have been marked done
def get_next_task(tasks):
    if not tasks:
        return None
    todo = [t for t in tasks if not t.get("done", False)]
    if not todo:
        return None
    tasks_sorted = sorted(todo, key=lambda t: t.get("due", "9999-12-31"))
    return tasks_sorted[0]

def get_next_exam(exams):
    if not exams:
        return None
    todo = [e for e in exams if not e.get("done", False)]
    if not todo:
        return None
    exams_sorted = sorted(todo, key=lambda e: e.get("date", "9999-12-31"))
    return exams_sorted[0]

# --- Persist changes ---
def _find_and_update(list_data, item, update_fn):
    """
    Find an item in list_data matching by 'timestamp' and 'title', apply update_fn on it.
    Returns True if an item was updated.
    """
    for i, entry in enumerate(list_data):
        if entry.get("timestamp") and item.get("timestamp"):
            same = entry.get("timestamp") == item.get("timestamp") and entry.get("title") == item.get("title")
        else:
            # fallback: match by title + created_at if possible
            same = entry.get("title") == item.get("title") and (
                (entry.get("created_at") and item.get("created_at") and entry.get("created_at") == item.get("created_at"))
                or True
            )
        if same:
            list_data[i] = update_fn(entry)
            return True
    return False

def mark_task_done(task):
    dm = DataManager()
    tasks = dm.load_user_data("tasks.json", initial_value=[])
    updated = _find_and_update(tasks, task, lambda e: {**e, "done": True, "done_at": datetime.utcnow().isoformat()})
    if updated:
        dm.save_user_data(tasks, "tasks.json")
        return True
    return False

def mark_exam_done(exam):
    dm = DataManager()
    exams = dm.load_user_data("exams.json", initial_value=[])
    updated = _find_and_update(exams, exam, lambda e: {**e, "done": True, "done_at": datetime.utcnow().isoformat()})
    if updated:
        dm.save_user_data(exams, "exams.json")
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
    today = date.today().toordinal()
    random.seed(today)
    return random.choice(MOTIVATION_LIST)

# --- Detail renderers ---
def render_task_detail(task, colors):
    st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<h3 style='margin:0'>{task.get('title','Untitled')}</h3>"
                f"<span style='background:#eef9f1;padding:6px;border-radius:8px;color:#2e8b57;font-weight:600;'>Aufgabe</span>"
                f"</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='margin-top:8px;color:#666'>{task.get('subject','')}</div>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    due = task.get("due", "—")
    duration = task.get("duration_min", task.get("duration", "—"))
    notes = task.get("notes", "")
    st.markdown(f"<b>Fällig am</b><br><div style='color:#333'>{due}</div>", unsafe_allow_html=True)
    st.markdown(f"<b>Dauer</b><br><div style='color:#333'>{duration}</div>", unsafe_allow_html=True)
    if notes:
        st.markdown("<b>Notizen</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#444'>{notes}</div>", unsafe_allow_html=True)

    st.markdown("<b>Checkliste</b>", unsafe_allow_html=True)
    checklist = task.get("checklist", ["Aufgaben lesen", "Lösen", "Kontrollieren"])
    checked = task.get("checked", [False] * len(checklist))
    for i, item in enumerate(checklist):
        ch = checked[i] if i < len(checked) else False
        st.checkbox(item, value=ch, key=f"task_chk_{task.get('timestamp','')}_{i}")

    st.markdown("<div style='display:flex;gap:12px;margin-top:12px;'>", unsafe_allow_html=True)
    if st.button("Bearbeiten", key="edit_task"):
        st.info("Bearbeiten: noch nicht implementiert")
    if st.button("Als erledigt markieren", key="done_task"):
        ok = mark_task_done(task)
        if ok:
            st.success("Aufgabe als erledigt markiert")
            st.session_state.selected = None
            st.experimental_rerun()
        else:
            st.error("Konnte Aufgabe nicht als erledigt markieren")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_exam_detail(exam, colors):
    st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<h3 style='margin:0'>{exam.get('title','Untitled')}</h3>"
                f"<span style='background:#fff0f3;padding:6px;border-radius:8px;color:#c0392b;font-weight:600;'>Prüfung</span>"
                f"</div>", unsafe_allow_html=True)

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
    if st.button("Bearbeiten", key="edit_exam"):
        st.info("Bearbeiten: noch nicht implementiert")
    if st.button("Als erledigt markieren", key="done_exam"):
        ok = mark_exam_done(exam)
        if ok:
            st.success("Prüfung als erledigt markiert")
            st.session_state.selected = None
            st.experimental_rerun()
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

# --- Sidebar (keine Änderung nötig) ---
def show_sidebar_nav():
    colors = get_theme_colors()
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
            if st.button(label, use_container_width=True):
                st.session_state.page = page
                st.rerun()
        st.markdown("---")
        st.markdown(
            "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;'>"
            "<span style='font-size:24px;'>🔥</span>"
            "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
            "</div>",
            unsafe_allow_html=True
        )
        if st.button("Logout", use_container_width=True):
            st.session_state.username = None
            st.rerun()

# --- Main page ---
def show_home_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    if "selected" not in st.session_state:
        st.session_state.selected = None

    colors = get_theme_colors()
    apply_theme()
    show_theme_switcher()

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

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### Tagesfortschritt")
        st.progress(0.7)
        st.markdown(f"<span style='color:{colors['primary']};font-size:32px;font-weight:bold;'>70%</span>", unsafe_allow_html=True)
        st.caption("Super gemacht! Weiter so! 💪")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Deine Übersicht")
    tasks = load_tasks()
    exams = load_exams()
    task_count = len([t for t in tasks if not t.get("done", False)])
    exam_count = len([e for e in exams if not e.get("done", False)])

    st.markdown(
        f"""
        <div style='display:flex;gap:24px;justify-content:center;'>
            <div style='text-align:center;'><div style='font-size:24px;'>📅</div><b>{task_count}</b><br><span style='font-size:12px;'>Aufgaben</span></div>
            <div style='text-align:center;'><div style='font-size:24px;'>📚</div><b>{exam_count}</b><br><span style='font-size:12px;'>Prüfungen</span></div>
            <div style='text-align:center;'><div style='font-size:24px;'>⭐</div><b>5</b><br><span style='font-size:12px;'>Stufe</span></div>
            <div style='text-align:center;'><div style='font-size:24px;'>🏆</div><b>120</b><br><span style='font-size:12px;'>Punkte</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # If an item is selected, render its detail view
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

    # --- TASKS & EXAMS (Karten) ---
    col4, col5, col6 = st.columns(3)
    next_task = get_next_task(tasks)

    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Aufgabe")
        if next_task:
            st.success(f"{next_task.get('title','')}\n\nFällig am: {next_task.get('due','')}")
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
            st.warning(f"{next_exam.get('title','')}\n\nDatum: {next_exam.get('date','')}")
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

    # --- WEEK OVERVIEW ---
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### Deine Woche auf einen Blick")
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    today = datetime.now()
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**{days[i]}**")
            st.markdown(f"{(today + timedelta(days=i)).day}")
            st.progress([0.7, 0.3, 0.5, 0.8, 0.6, 0.2, 0.1][i])
    st.markdown(f"<div style='text-align:right;'><a href='#' style='color:{colors['primary']};text-decoration:underline;'>Zur Wochenübersicht</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) 
    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("##### Nächste Aufgabe")

    if next_task:

        # Checkbox zum Abhaken
        done = st.checkbox(
            "Erledigt?",
            value=next_task.get("done", False),
            key=f"done_{next_task.get('title')}"
        )

        # Speichern wenn abgehakt
        if done and not next_task.get("done", False):
            next_task["done"] = True
            dm = DataManager()
            tasks = dm.load_user_data("tasks.json", initial_value=[])
            for t in tasks:
                if t.get("title") == next_task.get("title") and t.get("due") == next_task.get("due"):
                    t["done"] = True
            dm.save_user_data("tasks.json", tasks)

        # Aufgabe anzeigen
        st.success(f"{next_task.get('title','')}\n\nFällig am: {next_task.get('due','')}")

        # Start-Button (mit key!)
        if st.button("Jetzt starten", key="start_next_task"):
            st.session_state.selected_task = next_task
            st.session_state.page = "Timer"
            st.rerun()

    else:
        st.info("Keine Aufgaben vorhanden.")

    st.markdown("</div>", unsafe_allow_html=True)




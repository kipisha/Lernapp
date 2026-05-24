import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from pages.themes_page import get_theme_colors, apply_theme, show_theme_switcher

# Punktwerte (anpassbar)
POINTS_PER_TASK = 20
POINTS_PER_EXAM = 50

# Level / Reward-Definition (Schwellenwerte in Punkten)
LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000]  # Beginnpunkte für Level 1..6
LEVEL_NAMES = {
    1: "Bronze",
    2: "Silber",
    3: "Gold",
    4: "Platin",
    5: "Diamond",
    6: "Legend"
}
REWARDS = {
    1: "Starter-Badge",
    2: "Fortgeschrittenen-Badge",
    3: "Profi-Badge",
    4: "Experten-Badge",
    5: "Champion-Badge",
    6: "Legende-Badge"
}

def load_tasks():
    dm = DataManager()
    return dm.load_user_data("tasks.json", initial_value=[])

def load_exams():
    dm = DataManager()
    return dm.load_user_data("exams.json", initial_value=[])

def load_history():
    dm = DataManager()
    return dm.load_user_data("productivity_history.json", initial_value=[])

def compute_points(tasks, exams):
    tasks_done = sum(1 for t in tasks if t.get("done", False))
    exams_done = sum(1 for e in exams if e.get("done", False))
    points_tasks = tasks_done * POINTS_PER_TASK
    points_exams = exams_done * POINTS_PER_EXAM
    total_points = points_tasks + points_exams
    return {
        "tasks_done": tasks_done,
        "exams_done": exams_done,
        "points_tasks": points_tasks,
        "points_exams": points_exams,
        "total_points": total_points,
    }

def prepare_history_df(history_raw):
    if not history_raw:
        return None
    df = pd.DataFrame(history_raw)
    if "date" not in df.columns:
        return None
    df = df.set_index(pd.to_datetime(df["date"])).sort_index()
    if "points" in df.columns:
        ser = df["points"].fillna(0)
    elif "productivity" in df.columns:
        ser = (df["productivity"].fillna(0) * 100).astype(int)
    else:
        ser = pd.Series(dtype=float, index=df.index)
    ser.index.name = "date"
    return ser

def calc_level_and_progress(total_points: int):
    # Bestimme Level anhand LEVEL_THRESHOLDS (highest threshold <= points)
    level = 1
    for i, thresh in enumerate(LEVEL_THRESHOLDS):
        if total_points >= thresh:
            level = i + 1  # thresholds[0] => level 1
        else:
            break
    # Upper bound: if beyond last threshold, level = len(thresholds)
    max_level = len(LEVEL_THRESHOLDS)
    if level > max_level:
        level = max_level

    current_threshold = LEVEL_THRESHOLDS[level - 1]
    next_threshold = LEVEL_THRESHOLDS[level] if level < len(LEVEL_THRESHOLDS) else current_threshold + 1000
    points_into_level = total_points - current_threshold
    points_for_level = max(1, next_threshold - current_threshold)
    progress_fraction = min(1.0, max(0.0, points_into_level / points_for_level))
    points_to_next = max(0, next_threshold - total_points)
    return {
        "level": level,
        "level_name": LEVEL_NAMES.get(level, f"Level {level}"),
        "reward": REWARDS.get(level, None),
        "current_threshold": current_threshold,
        "next_threshold": next_threshold,
        "progress_fraction": progress_fraction,
        "points_to_next": points_to_next
    }

def unlocked_rewards(total_points: int):
    unlocked = []
    for i, thresh in enumerate(LEVEL_THRESHOLDS):
        lvl = i + 1
        if total_points >= thresh:
            unlocked.append({"level": lvl, "name": LEVEL_NAMES.get(lvl, f"Level {lvl}"), "reward": REWARDS.get(lvl)})
    return unlocked

def show_point_system_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    colors = get_theme_colors()
    apply_theme()
    show_theme_switcher()

    st.markdown(f"<h3 style='color:{colors['text']}'>Punktsystem & Level</h3>", unsafe_allow_html=True)
    st.write("Dein Level basiert auf gesammelten Punkten (Aufgaben & Prüfungen).")

    tasks = load_tasks()
    exams = load_exams()
    history_raw = load_history()

    stats = compute_points(tasks, exams)
    total_points = stats["total_points"]

    # Optionales Ziel (z.B. Wochenziel)
    weekly_goal = st.number_input("Punkte-Ziel (für Fortschrittsanzeige)", min_value=10, value=200, step=10)

    left, right = st.columns([2, 1])

    # Level-Berechnung
    lvl_info = calc_level_and_progress(total_points)
    unlocked = unlocked_rewards(total_points)

    with left:
        st.markdown("<div style='background:#fff;border-radius:12px;padding:14px;'>", unsafe_allow_html=True)
        st.markdown("**Deine Punkte & Level**")
        st.metric(label="Gesamtpunkte", value=total_points)
        st.markdown(f"**Level:** {lvl_info['level']} — {lvl_info['level_name']}")
        st.markdown(f"**Belohnung freigeschaltet:** {lvl_info.get('reward') or '—'}")

        # Fortschritt zum nächsten Level
        st.markdown("<div style='margin-top:8px;'>**Fortschritt zum nächsten Level**</div>", unsafe_allow_html=True)
        st.progress(lvl_info["progress_fraction"])
        st.caption(f"{total_points} / {lvl_info['next_threshold']} P ({int(lvl_info['progress_fraction']*100)}%) — noch {lvl_info['points_to_next']} P bis Level {lvl_info['level']+1}")

        # Fortschritt gegen Wochenziel
        percent_goal = int(min(100, (total_points / weekly_goal) * 100)) if weekly_goal > 0 else 0
        st.markdown("<div style='margin-top:12px;'>**Fortschritt gegen Ziel**</div>", unsafe_allow_html=True)
        st.progress(percent_goal / 100)
        st.caption(f"{percent_goal}% von {weekly_goal} P erreicht")

        # Verlaufs-Chart aus history
        ser = prepare_history_df(history_raw)
        if ser is not None and not ser.empty:
            st.markdown("<div style='margin-top:12px;'>**Punkteverlauf**</div>", unsafe_allow_html=True)
            df_chart = ser.rename("Punkte").to_frame()
            st.line_chart(df_chart)
        else:
            st.info("Keine Verlaufdaten gefunden. Sammle Punkte, um den Verlauf zu sehen.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div style='background:#fff;border-radius:12px;padding:14px;'>", unsafe_allow_html=True)
        st.markdown("**So erreichst du Level & Belohnungen**")
        st.markdown(f"- Aufgabe erledigt: **+{POINTS_PER_TASK} Punkte**")
        st.markdown(f"- Prüfung erledigt: **+{POINTS_PER_EXAM} Punkte**")
        st.markdown("---")
        st.markdown("**Deine freigeschalteten Belohnungen**")
        for u in unlocked:
            st.markdown(f"- Level {u['level']}: **{u['name']}** — {u.get('reward','')}")
        st.markdown("---")
        st.markdown("**Belohnungs-Übersicht**")
        for lvl, name in LEVEL_NAMES.items():
            thresh = LEVEL_THRESHOLDS[lvl - 1] if lvl - 1 < len(LEVEL_THRESHOLDS) else "—"
            st.markdown(f"- {name} (ab {thresh} P): {REWARDS.get(lvl)}")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Details anzeigen"):
        st.json({
            "tasks_total": len(tasks),
            "exams_total": len(exams),
            **stats,
            "level_info": lvl_info
        })


    show_point_system_page()
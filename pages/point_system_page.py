import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from utils.data_manager import DataManager
from pages.themes_page import get_theme_colors, apply_theme

# --- LEVEL DESIGN CONFIGURATION ---
LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000]
LEVEL_NAMES = {
    1: "Bronze — Starter",
    2: "Silber — Fortgeschrittenen",
    3: "Gold — Profi",
    4: "Platin — Experten",
    5: "Diamond — Champion",
    6: "Legend — Legende"
}
REWARDS = {
    1: "Starter-Badge",
    2: "Fortgeschrittenen-Badge",
    3: "Profi-Badge",
    4: "Experten-Badge",
    5: "Champion-Badge",
    6: "Legende-Badge"
}

def calc_level_and_progress(total_points: int):
    level = 1
    for i, thresh in enumerate(LEVEL_THRESHOLDS):
        if total_points >= thresh:
            level = i + 1
        else:
            break
            
    max_level = len(LEVEL_THRESHOLDS)
    if level > max_level:
        level = max_level
        
    current_threshold = LEVEL_THRESHOLDS[level - 1]
    next_threshold = LEVEL_THRESHOLDS[level] if level < len(LEVEL_THRESHOLDS) else current_threshold + 100
    
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
            unlocked.append({
                "level": lvl,
                "name": LEVEL_NAMES.get(lvl, f"Level {lvl}"),
                "reward": REWARDS.get(lvl, "")
            })
    return unlocked

def load_points_data():
    dm = DataManager()
    # Versucht die echten Verlaufdaten zu laden
    history = dm.load_user_data("points_history.json", initial_value=[])
    
    # FALLBACK: Wenn die Datei leer ist, erstellen wir Testdaten für das Diagramm
    if not history:
        today = datetime.now()
        base_points = 50
        history = []
        for i in range(7, -1, -1):
            day = today - timedelta(days=i)
            base_points += random.choice([0, 15, 20, 30])
            history.append({
                "date": day.strftime("%Y-%m-%d"),
                "points": base_points
            })
    return history

def show_point_system_page():
    colors = get_theme_colors()
    apply_theme()
    
    # HINWEIS: show_theme_switcher() wurde hier entfernt, 
    # da es bereits auf der Home-Page existiert und den Fehler verursacht hat!

    # Hier ermitteln wir die Gesamtpunkte aus den echten Daten oder dem Fallback
    history_data = load_points_data()
    total_points = history_data[-1]["points"] if history_data else 160
    
    lvl_info = calc_level_and_progress(total_points)
    
    st.title("⭐ Punkte & Level-System")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### Aktueller Stand")
        st.subheader(f"Punkte gesamt: {total_points} P")
        
        st.markdown(f"**Level: {lvl_info['level']} — {lvl_info['level_name'].split('—')[0]}**")
        st.markdown(f"Belohnung freigeschaltet: *{lvl_info['reward']}*")
        
        st.markdown("**Fortschritt zum nächsten Level**")
        st.progress(lvl_info['progress_fraction'])
        st.caption(f"{total_points} / {lvl_info['next_threshold']} P ({int(lvl_info['progress_fraction']*100)}%) — noch {lvl_info['points_to_next']} P bis Level {lvl_info['level'] + 1}")
        
        st.markdown("---")
        st.markdown("### 📈 Dein Punkteverlauf")
        
        if history_data:
            df = pd.DataFrame(history_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Zeigt das Liniendiagramm mit dem Verlauf an
            st.line_chart(df.set_index('date')['points'])
        else:
            st.info("Keine Verlaufdaten gefunden.")

    with col2:
        st.markdown("### Deine freigeschalteten Belohnungen")
        rewards_list = unlocked_rewards(total_points)
        for r in rewards_list:
            st.markdown(f"• **Level {r['level']}:** {r['reward']}")
            
        st.markdown("---")
        st.markdown("### Belohnungs-Übersicht")
        for lvl, name in LEVEL_NAMES.items():
            thresh = LEVEL_THRESHOLDS[lvl-1]
            st.markdown(f"• {name} (ab {thresh} P): {REWARDS[lvl]}")

if __name__ == "__main__":
    show_point_system_page()
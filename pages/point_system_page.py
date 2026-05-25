import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from pages.themes_page import get_theme_colors, apply_theme

# --- LEVEL DESIGN CONFIGURATION ---
LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000]
LEVEL_NAMES = {
    1: "Bronze — Weltenbummler",
    2: "Silber — Code-Ritter",
    3: "Gold — Wissens-Meister",
    4: "Platin — Denk-Titan",
    5: "Diamond — Elite-Champion",
    6: "Legend — Unsterbliche Legende"
}
REWARDS = {
    1: "🥉 Starter-Badge",
    2: "🥈 Fortgeschrittenen-Badge",
    3: "🥇 Profi-Badge",
    4: "🔮 Experten-Badge",
    5: "💎 Champion-Badge",
    6: "👑 Legenden-Krone"
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

def calculate_live_points():
    """ Berechnet die echten Punkte live aus den Benutzerdateien """
    dm = DataManager()
    tasks = dm.load_user_data("tasks.json", initial_value=[])
    exams = dm.load_user_data("exams.json", initial_value=[])
    
    # Punkte zählen: Erledigte Aufgaben bringen ihre Punkte (Default 20), Prüfungen bringen 50
    task_points = sum(int(t.get("points", 20)) for t in tasks if t.get("done", False))
    exam_points = sum(int(e.get("points", 50)) for e in exams if e.get("done", False))
    
    return task_points + exam_points

def generate_live_history(total_points):
    """ Generiert einen Verlaufschart basierend auf dem echten aktuellen Punktestand """
    today = datetime.now()
    history = []
    
    # Wir simulieren eine Wachstumskurve hin zum echten aktuellen Punktestand des Nutzers
    step = total_points / 7 if total_points > 0 else 0
    for i in range(7, -1, -1):
        day = today - timedelta(days=i)
        simulated_points = int(total_points - (i * step))
        history.append({
            "date": day.strftime("%Y-%m-%d"),
            "points": max(0, simulated_points)
        })
    return history

def show_point_system_page():
    colors = get_theme_colors()
    apply_theme()
    
    # Bestimmung der Textfarbe für die Cards basierend auf dem Theme
    card_text_color = colors.get('text', '#000000')
    
    st.markdown(f"""
    <style>
    /* Das große Profilbanner passt sich nun farblich dem Theme an */
    .hero-banner {{
        background: linear-gradient(135deg, {colors.get('primary', '#7c3aed')} 0%, {colors.get('secondary', '#4c1d95')} 100%);
        color: white !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        text-align: center;
    }}
    
    /* Die "Bubbles" / White-Cards ziehen nun die korrekte Hintergrundfarbe des Themes */
    .game-card {{
        background-color: {colors.get('card', '#ffffff')} !important;
        color: {card_text_color} !important;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    /* Die Listen-Einträge der Erfolge */
    .reward-item {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 8px;
    }}
    
    /* Freigeschaltete Quests erhalten einen dezenten Akzent der Theme-Sekundärfarbe */
    .reward-unlocked {{
        background: rgba(16, 185, 129, 0.12);
        border-left: 5px solid #10b981;
        color: {card_text_color} !important;
    }}
    
    /* Gesperrte Quests passen sich ebenfalls an */
    .reward-locked {{
        background: rgba(0, 0, 0, 0.04);
        opacity: 0.5;
        border-left: 5px solid #9ca3af;
        color: {card_text_color} !important;
    }}
    
    .badge-pill {{
        background: rgba(0,0,0,0.06);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
    }}
    
    /* Erzwinge korrekte Überschriftenfarben innerhalb der Cards */
    .game-card h3 {{
        color: {card_text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Echte Punkte live berechnen
    total_points = calculate_live_points()
    lvl_info = calc_level_and_progress(total_points)
    history_data = generate_live_history(total_points)
    
    # --- HERO BANNER ---
    st.markdown(f"""
    <div class="hero-banner">
        <span style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; opacity: 0.9;">Spieler-Profil</span>
        <h1 style="margin: 5px 0 15px 0; color: white !important; font-size: 40px;">👑 {st.session_state.get('username','Held')}</h1>
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 10px;">
            <div>
                <div style="font-size: 13px; opacity: 0.8;">AKTUELLES LEVEL</div>
                <div style="font-size: 24px; font-weight: bold; color: white !important;">LVL {lvl_info['level']}</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.3); height: 40px;"></div>
            <div>
                <div style="font-size: 13px; opacity: 0.8;">SCORE</div>
                <div style="font-size: 24px; font-weight: bold; color: white !important;">{total_points} EXP</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.3); height: 40px;"></div>
            <div>
                <div style="font-size: 13px; opacity: 0.8;">RANKING</div>
                <div style="font-size: 24px; font-weight: bold; color: white !important;">{lvl_info['level_name'].split('— ')[1]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # --- PROGRESS CARD ---
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown(f"### ⚡ Nächstes Level-Up")
        
        prog_percent = int(lvl_info['progress_fraction'] * 100)
        
        # Nutzen der Theme-Farben für den inneren Ladebalken
        st.markdown(f"""
        <div style="width: 100%; background-color: rgba(0,0,0,0.08); border-radius: 10px; margin: 12px 0 6px 0;">
            <div style="width: {prog_percent}%; background: linear-gradient(90deg, {colors.get('primary', '#10b981')}, {colors.get('secondary', '#34d399')}); height: 16px; border-radius: 10px; text-align: center; color: white !important; font-size: 11px; font-weight: bold; line-height: 16px;">
                {prog_percent}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; font-size: 14px; opacity: 0.8;">
            <span><b>{total_points}</b> / {lvl_info['next_threshold']} EXP</span>
            <span>Noch <b>{lvl_info['points_to_next']} EXP</b> bis Level {lvl_info['level'] + 1}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- CHART CARD ---
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### 📈 EP-Verlauf & Fortschritt")
        if total_points > 0:
            df = pd.DataFrame(history_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            st.line_chart(df.set_index('date')['points'])
        else:
            st.info("Noch keine Erfahrungspunkte vorhanden. Erledige Aufgaben auf der Startseite, um dein Punktekonto zu füllen!")
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        # --- QUESTS & REWARDS LOG ---
        st.markdown('<div class="game-card" style="padding-bottom: 10px;">', unsafe_allow_html=True)
        st.markdown("### ⚔️ Quest-Erfolge")
        
        for lvl, name in LEVEL_NAMES.items():
            thresh = LEVEL_THRESHOLDS[lvl-1]
            badge = REWARDS[lvl]
            clean_name = name.split("— ")[1]
            
            if total_points >= thresh:
                st.markdown(f"""
                <div class="reward-item reward-unlocked">
                    <div>
                        <span style="font-size: 12px; font-weight: bold;">LVL {lvl} • {clean_name}</span><br>
                        <span style="font-size: 14px;">{badge}</span>
                    </div>
                    <span class="badge-pill">✅ Bereit</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="reward-item reward-locked">
                    <div>
                        <span style="font-size: 12px; font-weight: bold;">LVL {lvl} • ???</span><br>
                        <span style="font-size: 14px; opacity: 0.7;">{badge.split(" ")[0]} Ab {thresh} EXP</span>
                    </div>
                    <span class="badge-pill">🔒 Locked</span>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_point_system_page()
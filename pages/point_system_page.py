import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
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

def load_points_data():
    dm = DataManager()
    history = dm.load_user_data("points_history.json", initial_value=[])
    
    if not history:
        today = datetime.now()
        base_points = 50
        history = []
        for i in range(7, -1, -1):
            day = today - timedelta(days=i)
            base_points += random.choice([10, 15, 20, 25])
            history.append({
                "date": day.strftime("%Y-%m-%d"),
                "points": base_points
            })
    return history

def show_point_system_page():
    colors = get_theme_colors()
    apply_theme()
    
    # --- GAMING STYLES (CSS Injection) ---
    st.markdown(f"""
    <style>
    .hero-banner {{
        background: linear-gradient(135deg, {colors.get('primary', '#7c3aed')} 0%, #4c1d95 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.25);
        margin-bottom: 25px;
        text-align: center;
    }}
    .game-card {{
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #f3f4f6;
    }}
    .reward-item {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 8px;
        background: #f9fafb;
    }}
    .reward-unlocked {{
        background: #ecfdf5;
        border-left: 5px solid #10b981;
    }}
    .reward-locked {{
        background: #f3f4f6;
        opacity: 0.6;
        border-left: 5px solid #9ca3af;
    }}
    .badge-pill {{
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Daten laden
    history_data = load_points_data()
    total_points = history_data[-1]["points"] if history_data else 185
    lvl_info = calc_level_and_progress(total_points)
    
    # --- HERO HERO BANNER ---
    st.markdown(f"""
    <div class="hero-banner">
        <span style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; opacity: 0.8;">Spieler-Profil</span>
        <h1 style="margin: 5px 0 15px 0; color: white; font-size: 40px;">👑 {st.session_state.get('username','Held')}</h1>
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 10px;">
            <div>
                <div style="font-size: 13px; opacity: 0.7;">AKTUELLES LEVEL</div>
                <div style="font-size: 24px; font-weight: bold;">LVL {lvl_info['level']}</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.3); height: 40px;"></div>
            <div>
                <div style="font-size: 13px; opacity: 0.7;">SCORE</div>
                <div style="font-size: 24px; font-weight: bold;">{total_points} EXP</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.3); height: 40px;"></div>
            <div>
                <div style="font-size: 13px; opacity: 0.7;">RANKING</div>
                <div style="font-size: 24px; font-weight: bold;">{lvl_info['level_name'].split('— ')[1]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Layout Splitting
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # --- PROGRESS CARD ---
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown(f"### ⚡ Nächstes Level-Up")
        
        # Schönerer Custom Progress-Bar
        prog_percent = int(lvl_info['progress_fraction'] * 100)
        st.markdown(f"""
        <div style="width: 100%; background-color: #e5e7eb; border-radius: 10px; margin: 12px 0 6px 0;">
            <div style="width: {prog_percent}%; background: linear-gradient(90deg, #10b981, #34d399); height: 16px; border-radius: 10px; text-align: center; color: white; font-size: 11px; font-weight: bold; line-height: 16px;">
                {prog_percent}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; font-size: 14px; color: #4b5563;">
            <span><b>{total_points}</b> / {lvl_info['next_threshold']} EXP</span>
            <span>Noch <b>{lvl_info['points_to_next']} EXP</b> bis Level {lvl_info['level'] + 1}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- CHART CARD ---
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("### 📈 EP-Verlauf & Fortschritt")
        if history_data:
            df = pd.DataFrame(history_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            st.line_chart(df.set_index('date')['points'])
        else:
            st.info("Noch kein Aktivitäten-Log vorhanden. Schließe Quests ab, um Punkte aufzuzeichnen!")
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
                # Freigeschaltetes Level
                st.markdown(f"""
                <div class="reward-item reward-unlocked">
                    <div>
                        <span style="font-size: 12px; font-weight: bold; color: #065f46;">LVL {lvl} • {clean_name}</span><br>
                        <span style="font-size: 14px; color: #111827;">{badge}</span>
                    </div>
                    <span class="badge-pill" style="background: #d1fae5; color: #065f46;">✅ Bereit</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Gesperrtes Level
                st.markdown(f"""
                <div class="reward-item reward-locked">
                    <div>
                        <span style="font-size: 12px; font-weight: bold; color: #374151;">LVL {lvl} • ???</span><br>
                        <span style="font-size: 14px; color: #6b7280;">{badge.split(" ")[0]} Ab {thresh} EXP</span>
                    </div>
                    <span class="badge-pill" style="background: #e5e7eb; color: #4b5563;">🔒 Locked</span>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_point_system_page()
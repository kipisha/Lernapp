import streamlit as st

if "theme" not in st.session_state:
    st.session_state["theme"] = "Cozy"

# Zuordnung der Button-Farben passend zum jeweiligen Mood
button_colors = {
    "Cozy": "#E26DBF",     # Dein primäres Cozy-Pink
    "Focus": "#337b1d",    # Dein Focus-Grün
    "Energy": "#fca311",   # Dein Energy-Orange/Gelb
    "Minimal": "#000000"   # Dein Minimal-Schwarz
}

def get_theme_colors():
    """Gibt die Farben des aktuellen Themes zurück"""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    
    themes = {
        "Cozy": {
            "primary": "#E26DBF",
            "secondary": "#bf60df",
            "background": "#ffe6f6",
            "card": "#fffadc",
            "text": "#000000"
        },
        "Focus": {
            "primary": "#337b1d",
            "secondary": "#f1ba53",
            "background": "#d4f0cc",
            "card": "#508662",
            "text": "#000000"
        },
        "Energy": {
            "primary": "#fca311",
            "secondary": "#38bdf8",
            "background": "#fef9c3",
            "card": "#fffbea",
            "text": "#22223b"
        },
        "Minimal": {
            "primary": "#000000",
            "secondary": "#1f2937",
            "background": "#fff9ec",
            "card": "#f5f5f5",
            "text": "#222"
        }
    }
    
    return themes.get(st.session_state.theme, themes["Cozy"])

def get_button_color():
    """Gibt die spezifische Button-Farbe für das aktuelle Theme zurück"""
    return button_colors.get(st.session_state.theme, "#4b5563")

def apply_theme():
    """Wendet die Theme-Styles an inklusive dynamischer Button-Färbung"""
    colors = get_theme_colors()
    btn_color = get_button_color()
    
    st.markdown(f"""
        <style>
        /* App-Hintergrund */
        .stApp {{
            background: {colors['background']} !important;
            color: {colors['text']};
        }}
        
        /* Karten-Styling */
        .card {{
            background: {colors['card']};
            border-radius: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 24px;
            margin-bottom: 24px;
        }}
        
        /* Fortschrittsbalken */
        .stProgress > div > div > div > div {{
            background-image: linear-gradient(90deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        }}
        
        /* --- DYNAMISCHE BUTTON-FÄRBUNG (Streamlit Standard-Buttons) --- */
        /* Normale Primär- und Sekundärbuttons in Streamlit ansprechen */
        div.stButton > button {{
            background-color: {btn_color} !important;
            color: white !important;
            border: 1px solid {btn_color} !important;
            border-radius: 10px;
            transition: all 0.3s ease;
        }}
        
        /* Hover-Effekt: Button wird beim Drüberfahren leicht transparent oder dunkler */
        div.stButton > button:hover {{
            background-color: {btn_color}ee !important;
            border-color: {btn_color} !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateY(-1px);
        }}
        
        /* Fokus-Effekt (Klick-Zustand) */
        div.stButton > button:focus:not(:active) {{
            border-color: {btn_color} !important;
            color: white !important;
        }}
        div.stButton > button:active {{
            background-color: {btn_color}cc !important;
            border-color: {btn_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def show_theme_switcher():
    """Zeigt die Theme-Buttons an"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌸 Cozy", key="theme_btn_cozy"):
            st.session_state.theme = "Cozy"
            st.rerun()
    with col2:
        if st.button("⚡ Focus", key="theme_btn_focus"):
            st.session_state.theme = "Focus"
            st.rerun()
    with col3:
        if st.button("🌞 Energy", key="theme_btn_energy"):
            st.session_state.theme = "Energy"
            st.rerun()
    with col4:
        if st.button("📚 Minimal", key="theme_btn_minimal"):
            st.session_state.theme = "Minimal"
            st.rerun()
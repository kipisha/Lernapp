import streamlit as st

def get_theme_colors():
    """Gibt die Farben des aktuellen Themes zurück"""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"
    
    themes = {
        "Cozy": {
            "primary": "#629BB6",
            "secondary": "#73a3ec",
            "background": "#ffe6f6",
            "card": "#fffadc",
            "text": "#000000"
        },
        "Focus": {
            "primary": "#82d868",
            "secondary": "#83da8b",
            "background": "#d4f0cc",
            "card": "#f3d572",
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
            "primary": "#3b82f6",
            "secondary": "#1f2937",
            "background": "#ffffff",
            "card": "#f5f5f5",
            "text": "#222"
        }
    }
    
    return themes.get(st.session_state.theme, themes["Cozy"])

def apply_theme():
    """Wendet die Theme-Styles an"""
    colors = get_theme_colors()
    
    st.markdown(f"""
        <style>
        .stApp {{
            background: {colors['background']} !important;
            color: {colors['text']};
        }}
        .card {{
            background: {colors['card']};
            border-radius: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 24px;
            margin-bottom: 24px;
        }}
        .stProgress > div > div > div > div {{
            background-image: linear-gradient(90deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        }}
        </style>
    """, unsafe_allow_html=True)

def show_theme_switcher():
    """Zeigt die Theme-Buttons an"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌸 Cozy"):
            st.session_state.theme = "Cozy"
            st.rerun()
    with col2:
        if st.button("⚡ Focus"):
            st.session_state.theme = "Focus"
            st.rerun()
    with col3:
        if st.button("🌞 Energy"):
            st.session_state.theme = "Energy"
            st.rerun()
    with col4:
        if st.button("📚 Minimal"):
            st.session_state.theme = "Minimal"
            st.rerun()

button_colors = {
    "Cozy": "#ec4899",     # pink
    "Focus": "#22c55e",    # grün
    "Energy": "#facc15",   # gelb
    "Minimal": "#4b5563"   # bleibt neutral
}

button_color = button_colors.get(st.session_state.theme, "#4b5563")
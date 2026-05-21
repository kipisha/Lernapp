import streamlit as st

def show_home_page():

    # -----------------------------
    # PAGE CONFIG
    # -----------------------------
    st.set_page_config(
        page_title="smartplan",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # -----------------------------
    # CUSTOM CSS
    # -----------------------------
    st.markdown("""
    <style>
    /* ... dein kompletter CSS Code hier ... */
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # SIDEBAR
    # -----------------------------
    with st.sidebar:
        st.markdown('<div class="sidebar-title">kipi✦</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item active-nav">🏠 Home</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">📅 Woche</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">📚 Aufgaben</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">📝 Prüfungen</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">⚡ Produktivität</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">⭐ Punkte</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">🎯 Ziele</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item">👥 Team</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>🔥 7 Tage Streak</h3>
            <p>Weiter so 💪</p>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # TOP SECTION
    # -----------------------------
    left, right = st.columns([5,2])

    with left:
        st.markdown(
            '<div class="search">🔍 Suche nach Aufgaben, Prüfungen...</div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown("""
        <div class="theme-wrapper">
            <div class="theme-card">🌸<br>Cozy</div>
            <div class="theme-card theme-card-active">⚡<br>Focus</div>
            <div class="theme-card">🌞<br>Energy</div>
            <div class="theme-card">📚<br>Minimal</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # TITLE
    # -----------------------------
    st.markdown('<div class="main-title">Hey Lara! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Schön, dass du da bist. Bereit für einen produktiven Tag?</div>', unsafe_allow_html=True)

    # -----------------------------
    # MAIN GRID
    # -----------------------------
    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        <div class="card progress-card">
            <div class="card-title">Tagesfortschritt</div>
            <div class="metric-number">70%</div>
            <div class="progress-container"><div class="progress-fill"></div></div>
            <br>
            <div class="metric-label">Super gemacht! Weiter so 💪</div>
        </div>
        """, unsafe_allow_html=True)

        # ... Rest deines Codes ...

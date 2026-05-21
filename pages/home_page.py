import streamlit as st

def show_home_page():
    import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Kipi+",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main Background */
.stApp {
    background: #f8f7fc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #ece9f6;
    width: 260px !important;
}

/* Sidebar Text */
.sidebar-title {
    font-size: 32px;
    font-weight: 800;
    color: #7c4dff;
    margin-bottom: 30px;
}

.nav-item {
    padding: 14px 18px;
    border-radius: 16px;
    margin-bottom: 10px;
    font-weight: 500;
    color: #5f6480;
    transition: 0.2s;
    cursor: pointer;
}

.nav-item:hover {
    background: #f4efff;
    color: #7c4dff;
}

.active-nav {
    background: #f4efff;
    color: #7c4dff;
    font-weight: 700;
}

/* Main Title */
.main-title {
    font-size: 52px;
    font-weight: 800;
    color: #1f1f39;
    margin-bottom: 8px;
}

.subtitle {
    color: #7a7a92;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: white;
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 6px 30px rgba(149, 157, 165, 0.08);
    margin-bottom: 24px;
}

/* Progress Card */
.progress-card {
    background: linear-gradient(
        135deg,
        #f7f3ff 0%,
        #eef3ff 100%
    );
}

/* Small cards */
.small-card {
    text-align: center;
    padding: 25px;
}

/* Card Titles */
.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #1f1f39;
    margin-bottom: 18px;
}

/* Purple Gradient Button */
.stButton>button {
    background: linear-gradient(
        135deg,
        #7c4dff,
        #9b6dff
    );
    color: white;
    border: none;
    border-radius: 14px;
    padding: 10px 22px;
    font-weight: 600;
}

/* Search Bar */
.search {
    background: white;
    padding: 16px 20px;
    border-radius: 18px;
    color: #9a9ab0;
    border: 1px solid #ece9f6;
    margin-bottom: 30px;
}

/* Theme Switcher */
.theme-wrapper {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
}

.theme-card {
    background: white;
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    width: 90px;
    border: 2px solid #f0ebff;
}

.theme-card-active {
    background: #2a174d;
    color: white;
}

/* Progress Bar */
.progress-container {
    background: #e9e4ff;
    height: 12px;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 15px;
}

.progress-fill {
    width: 70%;
    background: linear-gradient(
        90deg,
        #7c4dff,
        #9d71ff
    );
    height: 100%;
    border-radius: 20px;
}

/* Week Cards */
.week-card {
    background: white;
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    min-height: 120px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
}

/* Quote */
.quote {
    font-size: 28px;
    font-weight: 700;
    line-height: 1.4;
    color: #1f1f39;
}

/* Metrics */
.metric-number {
    font-size: 38px;
    font-weight: 800;
    color: #7c4dff;
}

.metric-label {
    color: #76768a;
    font-size: 15px;
}

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

        <div class="theme-card">
            🌸<br>Cozy
        </div>

        <div class="theme-card theme-card-active">
            ⚡<br>Focus
        </div>

        <div class="theme-card">
            🌞<br>Energy
        </div>

        <div class="theme-card">
            📚<br>Minimal
        </div>

    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="main-title">Hey Lara! 👋</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Schön, dass du da bist. Bereit für einen produktiven Tag?</div>',
    unsafe_allow_html=True
)

# -----------------------------
# MAIN GRID
# -----------------------------
col1, col2 = st.columns([2,1])

# LEFT SIDE
with col1:

    # Progress
    st.markdown("""
    <div class="card progress-card">

        <div class="card-title">Tagesfortschritt</div>

        <div class="metric-number">70%</div>

        <div class="progress-container">
            <div class="progress-fill"></div>
        </div>

        <br>

        <div class="metric-label">
            Super gemacht! Weiter so 💪
        </div>

    </div>
    """, unsafe_allow_html=True)

    # Small Cards
    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("📘", "3", "Aufgaben"),
        ("📝", "1", "Prüfung"),
        ("📅", "5", "Tage"),
        ("⭐", "120", "Punkte")
    ]

    for col, card in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
            <div class="card small-card">
                <div style="font-size:30px;">{card[0]}</div>
                <div class="metric-number">{card[1]}</div>
                <div class="metric-label">{card[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Task Cards
    a1, a2 = st.columns(2)

    with a1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Nächste Aufgabe</div>

            <h4>📗 Mathe Hausaufgaben</h4>
            <p>Bis morgen, 15:00</p>

        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Nächste Prüfung</div>

            <h4>📝 Deutsch Prüfung</h4>
            <p>Freitag, 17. Mai</p>

        </div>
        """, unsafe_allow_html=True)

    # Week Overview
    st.markdown("""
    <div class="card-title" style="margin-top:30px;">
    Deine Woche auf einen Blick
    </div>
    """, unsafe_allow_html=True)

    week_cols = st.columns(7)

    days = [
        ("Mo", "3 Aufgaben"),
        ("Di", "1 Prüfung"),
        ("Mi", "2 Aufgaben"),
        ("Do", "1 Prüfung"),
        ("Fr", "3 Aufgaben"),
        ("Sa", "-"),
        ("So", "-")
    ]

    for col, day in zip(week_cols, days):
        with col:
            st.markdown(f"""
            <div class="week-card">
                <h4>{day[0]}</h4>
                <p>{day[1]}</p>
            </div>
            """, unsafe_allow_html=True)

# RIGHT SIDE
with col2:

    st.markdown("""
    <div class="card">
        <div class="card-title">
        ⚡ Motivation für dich
        </div>

        <div class="quote">
        „Disziplin heute,<br>
        Stolz morgen.“
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">
        Wochenfortschritt
        </div>

        <div class="metric-number">70%</div>

        <div class="progress-container">
            <div class="progress-fill"></div>
        </div>

    </div>
    """, unsafe_allow_html=True)

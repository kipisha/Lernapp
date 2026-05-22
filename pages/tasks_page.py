import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme

def show_tasks_page():
    """Zeigt eine einzelne Aufgaben-Karte im Stil des Screenshots."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Cozy"

    colors = get_theme_colors()
    apply_theme()

    st.markdown(f"<h3 style='color:{colors['primary']};margin-bottom:6px;'>AUFGABE (EINTRAG)</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <style>
    .task-card {{
        background: white;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        max-width: 760px;
    }}
    .task-header {{
        display:flex;
        align-items:center;
        justify-content:space-between;
    }}
    .task-title {{
        font-weight:700;
        font-size:18px;
    }}
    .task-tag {{
        background:{colors['card']};
        color:{colors['primary']};
        padding:6px 10px;
        border-radius:999px;
        font-size:13px;
        font-weight:600;
    }}
    .meta { color: #666; font-size:13px; margin-top:8px; }
    .notes { margin-top:10px; color:#333; }
    .buttons { margin-top:14px; display:flex; gap:10px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='task-card'>", unsafe_allow_html=True)

    # Header: Icon + Title + Tag
    st.markdown(
        "<div class='task-header'>"
        "<div style='display:flex;align-items:center;gap:12px'>"
        "<div style='width:44px;height:44px;border-radius:10px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-size:20px;'>📗</div>"
        "<div><div class='task-title'>Mathe Hausaufgaben</div><div class='meta'>Fällig am <b>13. Mai 2024, 15:00</b></div></div>"
        "</div>"
        f"<div class='task-tag'>Hausaufgaben</div>"
        "</div>",
        unsafe_allow_html=True
    )

    # Details: Dauer, Fach, Notizen
    st.markdown("<div class='meta' style='margin-top:14px;'>Dauer: <b>90 min</b> &nbsp;•&nbsp; Fach: <b>Mathematik</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='notes'><b>Notizen:</b> Kapitel 5 & 6 lösen, Aufgaben im Buch Seite 120–125.</div>", unsafe_allow_html=True)

    # Checkliste (Streamlit native checkboxes for interactivity)
    st.markdown("<div style='margin-top:12px;'><b>Checkliste</b></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    with col1:
        done1 = st.checkbox("Aufgaben lesen", value=True, key="task_read")
        done2 = st.checkbox("Lösen", value=False, key="task_solve")
    with col2:
        done3 = st.checkbox("Kontrollieren", value=False, key="task_check")
        st.write("")  # spacing

    # Buttons
    cols = st.columns([1,1.2])
    with cols[0]:
        if st.button("Bearbeiten"):
            st.info("Bearbeiten: noch nicht implementiert")
    with cols[1]:
        if st.button("Als erledigt markieren"):
            st.success("Aufgabe als erledigt markiert")

    st.markdown("</div>", unsafe_allow_html=True)
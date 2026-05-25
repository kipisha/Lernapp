import streamlit as st
import time
from datetime import datetime, timedelta

def show_timer_page():
    task = st.session_state.get("selected_task")
    if not task:
        st.error("Keine Aufgabe ausgewählt.")
        if st.button("Zurück zur Startseite"):
            st.session_state.page = "Home"
            st.rerun()
        return

    st.markdown(f"### Timer für: {task.get('title','')}")

    # Dauer wählen
    duration_min = st.number_input(
        "Wie viele Minuten möchtest du arbeiten?",
        min_value=1,
        max_value=180,
        value=25,
        step=5,
        key="timer_duration"
    )

    # Start-Button
    if st.button("Timer starten", key="start_timer"):
        st.session_state.timer_end = datetime.now() + timedelta(minutes=duration_min)
        st.session_state.timer_running = True
        st.rerun()

    # Wenn Timer läuft
    if st.session_state.get("timer_running", False):
        remaining = st.session_state.timer_end - datetime.now()
        if remaining.total_seconds() <= 0:
            st.session_state.timer_running = False
            st.success("Zeit ist abgelaufen! 🎉")
        else:
            mins = int(remaining.total_seconds() // 60)
            secs = int(remaining.total_seconds() % 60)
            st.metric("Verbleibende Zeit", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            st.rerun()

    # Stop-Button
    if st.button("Stop", key="stop_timer"):
        st.session_state.timer_running = False
        st.session_state.page = "Home"
        st.rerun()

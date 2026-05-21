import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from utils.data_manager import DataManager

data_manager = DataManager()

def show_productivity_view():

    # Lade History (Liste von dicts: {"date": "YYYY-MM-DD", "points": int})
    history = data_manager.load_user_data("productivity_history.json") or []

    # Normalisieren
    normalized = []
    for r in history:
        d = r.get("date")
        pts = r.get("points", r.get("value", None))
        try:
            pts = float(pts)
        except:
            continue
        normalized.append({"date": pd.to_datetime(d), "points": pts})

    # Letzte 7 Tage
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    df_days = pd.DataFrame([{"date": d, "points": None} for d in days])
    df_days["date"] = pd.to_datetime(df_days["date"])

    if normalized:
        hist_df = pd.DataFrame(normalized)
        hist_df["date"] = pd.to_datetime(hist_df["date"])
        merged = df_days.merge(hist_df, on="date", how="left", suffixes=("_req", ""))
        merged["points"] = merged["points"].fillna(merged.get("points_req"))
    else:
        merged = df_days

    merged["points"] = merged["points"].fillna(0)
    merged["date_str"] = merged["date"].dt.strftime("%d.%m.%Y")

    st.title("📈 Punkte — Produktivität (letzte 7 Tage)")

    # Linien-Diagramm
    chart = (
        alt.Chart(merged)
        .mark_line(point=True, strokeWidth=3, color="#7aa874")  # Pastell-Olivgrün
        .encode(
            x=alt.X("date:T", title="Datum", axis=alt.Axis(format="%d.%m", labelAngle=-45)),
            y=alt.Y("points:Q", title="Erreichte Punkte", scale=alt.Scale(domain=[0, merged["points"].max() + 1])),
            tooltip=[
                alt.Tooltip("date_str:N", title="Datum"),
                alt.Tooltip("points:Q", title="Punkte")
            ]
        )
        .properties(height=320)
    )

    st.altair_chart(chart, use_container_width=True)

    st.write("Legende: Punkte = erledigte Aufgaben / erreichte Tagesleistung.")

    # Punkte für heute berechnen
    def calc_points_today():
        tasks = st.session_state.get("tasks", [])
        checked = st.session_state.get("checked", {})

        if not tasks:
            tasks = data_manager.load_user_data("tasks.json") or []

        if len(tasks) == 0:
            return 0

        return sum(1 for t in tasks if checked.get(t.get("title"), False))

    # Button: heutigen Punktestand speichern
    if st.button("📌 Heutige Punkte speichern"):
        pts = calc_points_today()
        today_str = str(today)

        updated = [r for r in history if r.get("date") != today_str]
        updated.append({"date": today_str, "points": pts})

        data_manager.save_user_data(updated, "productivity_history.json")
        st.success(f"Heutige Punkte gespeichert: {pts}")


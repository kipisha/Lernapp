import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from utils.data_manager import DataManager
data_manager = DataManager() 

def show_productivity_view():

    # Lade vorhandene History (Liste von dicts mit "date" im Format "YYYY-MM-DD" und "productivity" als 0..1)
    history = data_manager.load_user_data("productivity_history.json") or []

    # Normalisiere Einträge
    normalized = []
    for r in history:
        d = r.get("date")
        prod = r.get("productivity", r.get("percent", None))
        if prod is None and "value" in r:
            prod = r["value"]
        try:
            prod = float(prod)
        except:
            continue
        if prod > 1:  # falls Prozentwerte 0-100 gespeichert wurden
            prod = prod / 100.0
        normalized.append({"date": pd.to_datetime(d), "productivity": prod})

    # Erzeuge DataFrame für die letzten 7 Tage (inkl. heute)
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    df_days = pd.DataFrame([{"date": d, "productivity": None} for d in days])
    df_days["date"] = pd.to_datetime(df_days["date"])

    if normalized:
        hist_df = pd.DataFrame(normalized)
        hist_df["date"] = pd.to_datetime(hist_df["date"])
        merged = df_days.merge(hist_df, on="date", how="left", suffixes=("_req", ""))
        merged["productivity"] = merged["productivity"].fillna(merged.get("productivity_req"))
    else:
        merged = df_days

    merged["productivity"] = merged["productivity"].fillna(0.0)
    merged["productivity_pct"] = (merged["productivity"].astype(float) * 100).round(1)
    merged["date"] = pd.to_datetime(merged["date"])
    merged["date_str"] = merged["date"].dt.strftime("%d.%m.%Y")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("🏆 Punkte — Produktivität (letzte 7 Tage)")

    # Chart
    chart = alt.Chart(merged).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("date:T", title="Datum", axis=alt.Axis(format="%d.%m", labelAngle=-45)),
        y=alt.Y("productivity_pct:Q", title="Produktivität (%)", scale=alt.Scale(domain=[0, 100])),
        tooltip=[alt.Tooltip("date_str:N", title="Datum"), alt.Tooltip("productivity_pct:Q", title="Produktivität (%)")]
    ).properties(height=320)

    st.altair_chart(chart, use_container_width=True)

    st.write("Legende: Werte sind End-of-day-Snapshots (0–100%).")

    # Button: heutigen Snapshot speichern (berechnet wie auf Home)
    def calc_current_productivity():
        tasks = st.session_state.get("tasks", [])  # falls in Session geladen
        checked = st.session_state.get("checked", {})
        if not tasks:
            # fallback: lade gespeicherte tasks
            saved = data_manager.load_user_data("tasks.json") or []
            tasks = saved
        if len(tasks) == 0:
            return 0.0
        done = sum(1 for t in tasks if checked.get(t.get("title"), False))
        return done / len(tasks)

    if st.button("📌 Heutigen Produktivitäts-Snapshot speichern"):
        prod = calc_current_productivity()
        today_str = str(today)
        # aktualisiere oder append
        updated = [r for r in history if r.get("date") != today_str]
        updated.append({"date": today_str, "productivity": prod})
        data_manager.save_user_data(updated, "productivity_history.json")
        st.success(f"Heutiger Snapshot gespeichert: {int(prod*100)} %")

    st.markdown('</div>', unsafe_allow_html=True)
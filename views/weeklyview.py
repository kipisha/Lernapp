import streamlit as st
from datetime import datetime

st.title("Wochenansicht")

days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

if "weekly_entries" not in st.session_state:
    st.session_state.weekly_entries = {
        day: [] for day in days
    }

with st.form("weekly_input", clear_on_submit=True):
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        selected_day = st.selectbox("Wochentag", days)
    with col2:
        task_name = st.text_input("Eintrag")
    with col3:
        deadline = st.date_input("Deadline", value=datetime.now())
    add_button = st.form_submit_button("Eintrag hinzufügen")

if add_button and task_name:
    st.session_state.weekly_entries[selected_day].append({
        "task": task_name,
        "deadline": deadline.strftime("%d.%m.%Y"),
        "done": False
    })

st.subheader("Wochenübersicht")

cols = st.columns(7)
for i, day in enumerate(days):
    with cols[i]:
        st.markdown(f"### {day}")
        entries = st.session_state.weekly_entries[day]
        if not entries:
            st.write("Keine Einträge")
        else:
            for idx, entry in enumerate(entries):
                checkbox_key = f"{day}_{idx}_done"
                done = st.checkbox(entry["task"], value=entry["done"], key=checkbox_key)
                if done != entry["done"]:
                    st.session_state.weekly_entries[day][idx]["done"] = done
                st.caption(f"Deadline: {entry['deadline']}")
                if done:
                    st.markdown("✅ Erledigt")



# Löschen von Einträgen
st.markdown("---")
st.subheader("Eintrag löschen")

all_entries = []
entry_map = {}
for day, entries in st.session_state.weekly_entries.items():
    for idx, entry in enumerate(entries):
        label = f"{day}: {entry['task']} (Deadline: {entry['deadline']})"
        all_entries.append(label)
        entry_map[label] = (day, idx)

if all_entries:
    entry_to_delete = st.selectbox("Wähle einen Eintrag zum Löschen", all_entries)
    if st.button("Löschen"):
        day, idx = entry_map[entry_to_delete]
        del st.session_state.weekly_entries[day][idx]
else:
    st.write("Keine Einträge zum Löschen")

st.markdown("---")
st.subheader("Eintrag löschen")
delete_day = st.selectbox("Tag wählen", days)
if st.button("Alle Einträge für Tag löschen"):
    st.session_state.weekly_entries[delete_day] = []

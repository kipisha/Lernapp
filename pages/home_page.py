import streamlit as st
from datetime import datetime, timedelta
import json
import os

# Hilfsfunktionen zum Laden/Speichern
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --- Sidebar Navigation ---
def show_sidebar_nav():
    st.markdown("""
        <style>
        .sidebar-nav .sidebar-item {
            padding: 12px 18px;
            border-radius: 12px;
            margin-bottom: 6px;
            font-weight: 500;
            color: #6c63ff;
            transition: background 0.2s;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .sidebar-nav .sidebar-item:hover {
            background: #f3f0ff;
        }
        </style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("<h1 style='color:#7c3aed;'>kipi✦</h1>", unsafe_allow_html=True)
        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
        nav_items = [
            ("🏠", "Home"),
            ("📅", "Woche"),
            ("✅", "Aufgaben"),
            ("📚", "Prüfungen"),
            ("⚡", "Produktivität"),
            ("⭐", "Punkte"),
            ("📝", "Notizen"),
            ("🎯", "Ziele"),
            ("👥", "Team"),
        ]
        for icon, label in nav_items:
            st.markdown(f'<div class="sidebar-item">{icon} {label}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
            "<div style='background:#fff7f0;padding:10px;border-radius:12px;display:flex;align-items:center;'>"
            "<span style='font-size:24px;'>🔥</span>"
            "<div style='margin-left:10px;'><b>7 Tage Streak</b><br><span style='font-size:12px;color:#b0aeb8;'>Weiter so! 🔥</span></div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.button("Logout", use_container_width=True)

# --- Theme Switcher ---
def show_theme_switcher():
    st.markdown("""
        <style>
        .theme-switcher {display:flex;gap:12px;justify-content:flex-end;}
        .theme-btn {
            padding: 8px 18px;
            border-radius: 16px;
            border: none;
            background: #f3f0ff;
            color: #6c63ff;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        .theme-btn:hover {background: #e0dcff;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown(
        "<div class='theme-switcher'>"
        "<button class='theme-btn'>🌸 Cozy</button>"
        "<button class='theme-btn'>⚡ Focus</button>"
        "<button class='theme-btn'>🔆 Energy</button>"
        "<button class='theme-btn'>📖 Minimal</button>"
        "</div>",
        unsafe_allow_html=True
    )

# --- Hauptseite ---
def show_home_page():
    show_sidebar_nav()
    show_theme_switcher()

    st.markdown(
        """
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
            <span style='color:#7c3aed;font-size:14px;font-weight:bold;'>HOME / STARTSEITE</span>
            <input style='padding:8px 16px;border-radius:12px;border:1px solid #eee;width:320px;' placeholder='Suche nach Aufgaben, Prüfungen...'>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("<h2 style='margin:0;color:#222;'>Hey Lara! 👋</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color:#b0aeb8;'>Schön, dass du da bist. Bereit für einen produktiven Tag?</span>", unsafe_allow_html=True)

    # --- Progress & Übersicht ---
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.markdown("<div style='background:#fff7f0;padding:24px 18px;border-radius:18px;box-shadow:0 2px 12px #f3f0ff;margin-bottom:12px;'>", unsafe_allow_html=True)
        st.markdown("#### Tagesfortschritt")
        st.progress(0.7)
        st.markdown("<span style='color:#7c3aed;font-size:32px;font-weight:bold;'>70%</span>", unsafe_allow_html=True)
        st.caption("Super gemacht! Weiter so! 💪")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='background:#fff7f0;padding:24px 18px;border-radius:18px;box-shadow:0 2px 12px #f3f0ff;margin-bottom:12px;'>", unsafe_allow_html=True)
        st.markdown("#### Deine Übersicht")
        st.markdown(
            """
            <div style='display:flex;gap:24px;justify-content:center;'>
                <div style='text-align:center;'><div style='font-size:24px;'>📅</div><b>3</b><br><span style='font-size:12px;'>Aufgaben</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>📚</div><b>1</b><br><span style='font-size:12px;'>Prüfung</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>⭐</div><b>5</b><br><span style='font-size:12px;'>Stufe</span></div>
                <div style='text-align:center;'><div style='font-size:24px;'>🏆</div><b>120</b><br><span style='font-size:12px;'>Punkte</span></div>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='background:#fff7f0;padding:24px 18px;border-radius:18px;box-shadow:0 2px 12px #f3f0ff;margin-bottom:12px;'>", unsafe_allow_html=True)
        st.markdown("#### Motivation für dich")
        st.info("„Disziplin heute, Stolz morgen.\"")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Aufgaben & Prüfungen laden ---
    aufgaben = load_json("app_data/user_data_kselv/tasks.json")
    pruefungen = load_json("app_data/user_data_kselv/exams.json")

    # --- Aufgaben & Prüfungen Cards ---
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("<div style='background:#f6f6fa;padding:18px 14px;border-radius:16px;box-shadow:0 2px 8px #f3f0ff;'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Aufgabe")
        if aufgaben:
            aufgabe = aufgaben[0]
            st.success(f"{aufgabe['title']}\n\nBis {aufgabe['due']}")
        else:
            st.info("Keine Aufgaben vorhanden.")
        if st.button("Jetzt starten"):
            st.info("Aufgaben-Detailseite (Demo)")
        st.markdown("</div>", unsafe_allow_html=True)
    with col5:
        st.markdown("<div style='background:#f6f6fa;padding:18px 14px;border-radius:16px;box-shadow:0 2px 8px #f3f0ff;'>", unsafe_allow_html=True)
        st.markdown("##### Nächste Prüfung")
        if pruefungen:
            pruefung = pruefungen[0]
            st.warning(f"{pruefung['title']}\n\n{pruefung['date']}\n\nIn {pruefung['days_left']} Tagen")
        else:
            st.info("Keine Prüfungen vorhanden.")
        if st.button("Prüfung ansehen"):
            st.info("Prüfungs-Detailseite (Demo)")
        st.markdown("</div>", unsafe_allow_html=True)
    with col6:
        st.markdown("<div style='background:#f6f6fa;padding:18px 14px;border-radius:16px;box-shadow:0 2px 8px #f3f0ff;'>", unsafe_allow_html=True)
        st.markdown("##### Motivation für dich")
        st.markdown("🏁", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Aufgaben/Prüfungen hinzufügen ---
    with st.expander("➕ Aufgabe hinzufügen"):
        title = st.text_input("Titel")
        due = st.text_input("Fällig bis (z.B. 23.05.2026, 15:00)")
        if st.button("Aufgabe speichern"):
            aufgaben.append({"title": title, "due": due})
            save_json("app_data/user_data_kselv/tasks.json", aufgaben)
            st.success("Aufgabe gespeichert! Seite neu laden.")
    with st.expander("➕ Prüfung hinzufügen"):
        title = st.text_input("Prüfungstitel")
        date = st.text_input("Datum (z.B. 24.05.2026)")
        days_left = (datetime.strptime(date, "%d.%m.%Y") - datetime.now()).days if date else ""
        if st.button("Prüfung speichern"):
            pruefungen.append({"title": title, "date": date, "days_left": days_left})
            save_json("app_data/user_data_kselv/exams.json", pruefungen)
            st.success("Prüfung gespeichert! Seite neu laden.")

    # --- Woche auf einen Blick ---
    st.markdown("<div style='background:#fff7f0;padding:18px 14px;border-radius:16px;box-shadow:0 2px 8px #f3f0ff;margin-top:18px;'>", unsafe_allow_html=True)
    st.markdown("#### Deine Woche auf einen Blick")
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    today = datetime.now()
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**{days[i]}**")
            st.markdown(f"{(today + timedelta(days=i)).day}")
            st.progress([0.7, 0.3, 0.5, 0.8, 0.6, 0.2, 0.1][i])
    st.markdown(f"<div style='text-align:right;'><a href='#' style='color:#7c3aed;text-decoration:underline;'>Zur Wochenübersicht</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Hauptaufruf ---
show_home_page()
import streamlit as st
from pages.themes_page import get_theme_colors, apply_theme

def show_team_page():
    # 1. Theme-Farben laden und CSS-Anpassungen aktivieren
    colors = get_theme_colors()
    apply_theme()
    
    # 2. Spezifische Link-Farbe je nach Theme definieren
    link_color = colors.get('primary', '#7c3aed') 
    if st.session_state.theme == "Minimal":
        link_color = "#000000"
    elif st.session_state.theme == "Focus":
        link_color = "#1e4d12"

    # 3. Custom CSS für die Team-Liste injizieren
    st.markdown(f"""
    <style>
    /* Passt die Farbe aller normalen Markdown-Links auf dieser Seite an */
    div.stMarkdown a {{
        color: {link_color} !important;
        text-decoration: none;
        font-weight: 500;
        transition: opacity 0.2s ease-in-out;
    }}
    div.stMarkdown a:hover {{
        opacity: 0.8;
        text-decoration: underline;
    }}
    /* Sorgt dafür, dass Überschriften und Fließtext die Theme-Textfarbe nutzen */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp li {{
        color: {colors.get('text', '#000000')} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 4. Dein originaler Inhalt – erweitert um echte Mailto-Links, damit sie einfärbbar sind
    st.title("👥 Projektteam & Dozenten")

    st.write("## Teammitglieder")
    st.write("- Darlene Armenio – [armdar01@students.zhaw.ch](mailto:armdar01@students.zhaw.ch)")
    st.write("- Kipisha Selvan – [selvakip@students.zhaw.ch](mailto:selvakip@students.zhaw.ch)")
    st.write("- Hannah Jung – [junghan1@students.zhaw.ch](mailto:junghan1@students.zhaw.ch)")
    st.write("- Mimoza Mehmeti – [mehmemig@students.zhaw.ch](mailto:mehmemig@students.zhaw.ch)")

    st.write("---")

    st.write("## Dozenten")
    st.write("- Samuel Wehrli – [wehs@zhaw.ch](mailto:wehs@zhaw.ch)")
    st.write("- Paul Fox – [foxpax@zhaw.ch](mailto:foxpax@zhaw.ch)")
    st.write("- Ho Ka Men – [hokam001@students.zhaw.ch](mailto:hokam001@students.zhaw.ch)")

if __name__ == "__main__":
    show_team_page()
import streamlit as st
from utils.data_manager import DataManager
from pages.themes_page import get_theme_colors, apply_theme

def show_profile_page():
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

    dm = DataManager()
    creds = dm.load_app_data("credentials.yaml", initial_value={"usernames": {}})
    username = st.session_state.get("username", None)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 👤 Mein Profil")

    if not username:
        st.info("Kein Benutzer angemeldet.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    user = creds.get("usernames", {}).get(username, {})

    st.write("**Benutzername:**", username)
    st.write("**Vorname:**", user.get("first_name", "—").capitalize())
    st.write("**Nachname:**", user.get("last_name", "—").capitalize())
    st.write("**Email:**", user.get("email", "—"))

    st.markdown("</div>", unsafe_allow_html=True)
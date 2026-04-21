import streamlit as st

st.set_page_config(page_title="Lernapp", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_weeklyview = st.Page("views/weeklyview.py", title="Wochenansicht", icon=":material/info:")
pg_progresspoints = st.Page("views/progresspoints.py", title="Punktefortschritt", icon=":material/info:")

pg = st.navigation([pg_home, pg_weeklyview, pg_progresspoints])
pg.run()
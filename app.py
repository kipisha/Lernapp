import streamlit as st
import pandas as pd 

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="BMLD_App_DB"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in


# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---



st.set_page_config(page_title="Lernapp", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_weeklyview = st.Page("views/weeklyview.py", title="Wochenansicht", icon=":material/info:")
pg_progresspoints = st.Page("views/progresspoints.py", title="Punktefortschritt", icon=":material/show_chart:")

pg = st.navigation([pg_home, pg_weeklyview, pg_progresspoints])
pg.run()
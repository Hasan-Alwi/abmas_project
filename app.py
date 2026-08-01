import streamlit as st
import pandas as pd
import numpy as np
from supabase_client import supabase  # koneksi supabase, siap dipakai di semua page

st.set_page_config(page_title='Self Cash Flow')

home_page = st.Page('home.py', title='Home')
input_page = st.Page('input.py', title='Input Pemasukan')  # tambahkan icon="___"
dashboard_page = st.Page('dashboard.py', title='Dashboard')  # tambahkan icon="___"

pg = st.navigation([home_page, input_page, dashboard_page])
pg.run()

import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import numpy as np 

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(url, key)

# def get_todos():
#     response = supabase.table('todos').select('*').execute()
#     return response.data

# def add_todo()  

home_page = st.Page('home.py', title='Home')
input_page = st.Page('input.py', title='Input Pemasukan') #tambahkan icon="___"
dashboard_page = st.Page('dashboard.py', title='Dashboard') #tambahkan icon="___"

pg = st.navigation([home_page, input_page, dashboard_page])
st.set_page_config(page_title='Self Cash Fow')
pg.run()
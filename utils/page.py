# utils/page.py
import streamlit as st
from utils.css import load_css
from utils.nav import top_nav
from utils.auth import require_login, sidebar_user

def setup(active: str):
    st.set_page_config(
        page_title="Dashboard Keuangan Syariah | SMA Ar-Rohmah",
        page_icon="🌙", layout="wide", initial_sidebar_state="expanded",
    )
    load_css()
    auth = require_login() # berhenti di sini kalau belum login
    top_nav(active)
    sidebar_user(auth)
    return auth
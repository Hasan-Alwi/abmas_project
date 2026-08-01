"""
Modul koneksi Supabase.
Import fungsi get_supabase_client() dari file manapun (home.py, input.py, dashboard.py)
untuk mendapatkan client Supabase yang sudah siap dipakai.
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """
    Membuat (dan meng-cache) koneksi ke Supabase.
    Kredensial diambil dari st.secrets (.streamlit/secrets.toml),
    supaya tidak hardcode langsung di kode.
    """
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


# Client siap pakai — cukup import `supabase` dari modul ini
supabase = get_supabase_client()

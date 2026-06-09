import streamlit as st
import pandas as pd
import numpy as np

st.title('🗂️SELF CASH FLOW🗂️')

with st.container(border=False):
    st.text('Selamat datang di website SELF CASH FLOW, web ini merupakan web pendukung untuk memanajamen keuangan teman-teman kedepannya.')

with st.container(border=False):
    st.text('Mari mulai menjadi pribadi yang peduli keuangan')

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('Mulai Input'):
            st.switch_page('input.py')
    with col2:
        if st.button('lihat Dashboard'):
            st.switch_page('dashboard.py.py')
    with col3:
        if st.button('LIhat Video'):
            st.switch_page('input.py')
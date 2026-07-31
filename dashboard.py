import streamlit as st
import pandas as pd
import numpy as np
from input import uang_input

def abs():
    with st.container(border=True):
        st.title('🗂️LIHAT SEMUA ALOKASIMU🗂️')
        st.text('Masih dalam maintence ....')

    with st.container(border=True):
        st.header('Bagaiaman pengeluaranmu')
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.metric(label='Pemasukan', value=uang _input)
        with col2:
            st.metric(label='Pengeluaran', value='Rp. 200.000')

if __name__ == '__main__':
    abs()
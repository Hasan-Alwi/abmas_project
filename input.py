import streamlit as st
import pandas as pd
import numpy as np  
from streamlit_gsheets import GSheetsConnection

# --- Google SPreadsheets---
# Link
url = "https://docs.google.com/spreadsheets/d/1pnXUIFCxfEF6-pMHEzjJefcbbFo3gWAlTVyom9_RH1s/edit?usp=sharing"
# Connection
conn = st.connection("gsheets", type=GSheetsConnection)
# Ambil Data Spreadsheet
df = conn.read(spreadsheet=url, worksheet="0")

j_pengeluaran = ['Makan dan jajan', 
                'Sekolah', 
                'Donasi (Sedekah)',
                'Kebutuhan Pribadi',
                'Acara Pondhok',
                'Investasi',
                'Transportasi',
                'Sosial dan Hiburan',
                'Olahraga'
                ]

def app():
    st.title('Self Cash Flow Maker')

    if 'awal' not in st.session_state:
        st.session_state.awal = False
    if 'alokasi' not in st.session_state:
        st.session_state.alokasi = False
    if 'nominal_uang' not in st.session_state:
        st.session_state.nominal_uang = 0.0
    if 'pengeluaran' not in st.session_state:
        st.session_state.pengeluaran = []

    with st.container(border=True):
        st.text('Dalam beberapa literasi disebutkan bahwa pemasukan perlu dibagi menjadi 3 bagian:')
        col1, col2, col3 = st.columns(3, border=True)
        with col1:
            st.metric(label="Kebutuhan", value='50%')

        with col2:
            st.metric(label="Keinginan", value='30%')
        
        with col3:
            st.metric(label="Tabungan", value='20%')

    if st.button('Mulai'):
        st.session_state.awal = True

    if st.session_state.awal:

        uang_input = st.number_input(
            'Masukkan nominal uang saku (Rp.)',
            min_value=0,
            step=1000 
            # format="%.0f"
        )

        if uang_input > 0:
            st.success('Klik tombol untuk menyimpan dan lanjut')

            if st.button('Simpan & Lanjut'):
                st.session_state.nominal_uang = uang_input
                st.session_state.awal = False
                st.session_state.alokasi = True
                st.rerun()
        else:
            st.info('Silakan isi nominal uang terlebih dahulu')

    if st.session_state.alokasi:

        uang_saku = st.session_state.nominal_uang
        st.write(f'Mari alokasikan Rp {uang_saku:,.0f}')

        terpakai = sum(item['nominal'] for item in st.session_state.pengeluaran)
        sisa = uang_saku - terpakai

        st.info(f'Sisa uang: Rp {sisa:,.0f}')

        if sisa > 0:
            with st.form('alokasi_form', clear_on_submit=True):
                kategori = st.selectbox('Jenis Pengeluaran', j_pengeluaran, index=None)
                duit = st.number_input(
                    'Berapa yang Ingin antum Alokasikan?',
                    min_value=0, 
                    placeholder='Silahkan di isi ....')
                persen = (duit/uang_saku)*100
                submit = st.form_submit_button('Tambah')

                if submit:

                    if kategori is None or duit is None:
                        st.warning("Harap isi semua field")
                    else:
                        # nominal_hitung = (persen / 100) * sisa

                        if duit > sisa:
                            st.error("Melebihi sisa uang!")
                        else:
                            st.session_state.pengeluaran.append({
                                "Kategori": kategori,
                                "Persentase": f"{persen}%",
                                "nominal": duit
                            })

                            st.rerun()
        else:
            st.success("Semua uang sudah teralokasi!")

        if st.session_state.pengeluaran:
            df = pd.DataFrame(st.session_state.pengeluaran)
            st.subheader("Data Pengeluaran")
            st.dataframe(df)
            st.bar_chart(df.set_index("Kategori")["nominal"])

if __name__ == '__main__':
    app()
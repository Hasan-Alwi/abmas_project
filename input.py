import streamlit as st
import pandas as pd
import numpy as np  
from datetime import date
from streamlit_gsheets import GSheetsConnection

# --- Google SPreadsheets---
# Link
url = "https://docs.google.com/spreadsheets/d/1pnXUIFCxfEF6-pMHEzjJefcbbFo3gWAlTVyom9_RH1s/edit?usp=sharing"
# Connection
conn = st.connection("gsheets", type=GSheetsConnection)
# Ambil Data Spreadsheet
# df = conn.read(spreadsheet=url, worksheet="DataInput")

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

# def app():
#     st.title('Self Cash Flow Maker')

#     if 'awal' not in st.session_state:
#         st.session_state.awal = False
#     if 'alokasi' not in st.session_state:
#         st.session_state.alokasi = False
#     if 'nominal_uang' not in st.session_state:
#         st.session_state.nominal_uang = 0.0
#     if 'pengeluaran' not in st.session_state:
#         st.session_state.pengeluaran = []

#     with st.container(border=True):
#         st.text('Dalam beberapa literasi disebutkan bahwa pemasukan perlu dibagi menjadi 3 bagian:')
#         col1, col2, col3 = st.columns(3, border=True)
#         with col1:
#             st.metric(label="Kebutuhan", value='50%')

#         with col2:
#             st.metric(label="Keinginan", value='30%')
        
#         with col3:
#             st.metric(label="Tabungan", value='20%')

#     if st.button('Mulai'):
#         st.session_state.awal = True

#     if st.session_state.awal:

#         uang_input = st.number_input(
#             'Masukkan nominal uang saku (Rp.)',
#             min_value=0,
#             step=1000 
#             # format="%.0f"
#         )

#         if uang_input > 0:
#             st.success('Klik tombol untuk menyimpan dan lanjut')

#             if st.button('Simpan & Lanjut'):
#                 st.session_state.nominal_uang = uang_input
#                 st.session_state.awal = False
#                 st.session_state.alokasi = True
#                 st.rerun()
#         else:
#             st.info('Silakan isi nominal uang terlebih dahulu')

#     if st.session_state.alokasi:

#         uang_saku = st.session_state.nominal_uang
#         st.write(f'Mari alokasikan Rp {uang_saku:,.0f}')

#         terpakai = sum(item['nominal'] for item in st.session_state.pengeluaran)
#         sisa = uang_saku - terpakai

#         st.info(f'Sisa uang: Rp {sisa:,.0f}')

#         if sisa > 0:
#             with st.form('alokasi_form', clear_on_submit=True):
#                 kategori = st.selectbox('Jenis Pengeluaran', j_pengeluaran, index=None)
#                 duit = st.number_input(
#                     'Berapa yang Ingin antum Alokasikan?',
#                     min_value=0, 
#                     placeholder='Silahkan di isi ....')
#                 persen = (duit/uang_saku)*100
#                 submit = st.form_submit_button('Tambah')

#                 if submit:

#                     if kategori is None or duit is None:
#                         st.warning("Harap isi semua field")
#                     else:
#                         # nominal_hitung = (persen / 100) * sisa

#                         if duit > sisa:
#                             st.error("Melebihi sisa uang!")
#                         else:
#                             st.session_state.pengeluaran.append({
#                                 "Kategori": kategori,
#                                 "Persentase": f"{persen}%",
#                                 "nominal": duit
#                             })

#                             st.rerun()
#         else:
#             st.success("Semua uang sudah teralokasi!")

#         if st.session_state.pengeluaran:
#             df = pd.DataFrame(st.session_state.pengeluaran)
#             st.subheader("Data Pengeluaran")
#             st.dataframe(df)
#             st.bar_chart(df.set_index("Kategori")["nominal"])

# if __name__ == '__main__':
#     app()

def simpan_ke_spreadsheet(uang_saku, daftar_pengeluaran):
    """
    Mengubah daftar alokasi (list of dict di session_state.pengeluaran)
    menjadi satu row, lalu append ke worksheet DataInput.
    """
    # Inisialisasi semua kategori dengan nilai 0
    row_kategori = {kategori: 0 for kategori in j_pengeluaran}

    # Akumulasi nominal per kategori (kalau ada kategori yang diisi lebih dari sekali)
    for item in daftar_pengeluaran:
        kategori = item["Kategori"]
        nominal = item["nominal"]
        row_kategori[kategori] = row_kategori.get(kategori, 0) + nominal

    # Susun row final: Tanggal, Pendapatan, lalu kolom-kolom kategori
    row_final = {
        "Tanggal": date.today().strftime("%Y-%m-%d"),
        "Pemasukan": uang_saku,
        **row_kategori
    }

    df_baru = pd.DataFrame([row_final])

    # Baca data lama dengan ttl=0 supaya tidak kena cache
    try:
        df_lama = conn.read(spreadsheet=url, worksheet="DataInput", ttl=0)
        df_lama = df_lama.dropna(how="all")
    except Exception:
        df_lama = pd.DataFrame(columns=row_final.keys())

    df_gabungan = pd.concat([df_lama, df_baru], ignore_index=True)

    conn.update(spreadsheet=url, worksheet="DataInput", data=df_gabungan)


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
    if 'tersimpan' not in st.session_state:
        st.session_state.tersimpan = False

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
        st.session_state.tersimpan = False

    if st.session_state.awal:

        uang_input = st.number_input(
            'Masukkan nominal uang saku (Rp.)',
            min_value=0,
            step=1000 
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
            df_alokasi = pd.DataFrame(st.session_state.pengeluaran)
            st.subheader("Data Pengeluaran")
            st.dataframe(df_alokasi)
            st.bar_chart(df_alokasi.set_index("Kategori")["nominal"])

            st.divider()

            if st.button("Simpan ke Spreadsheet"):
                try:
                    simpan_ke_spreadsheet(uang_saku, st.session_state.pengeluaran)
                    st.session_state.tersimpan = True
                    st.success("Data berhasil tersimpan ke Google Sheets!")
                except Exception as e:
                    st.error(f"Gagal menyimpan data: {e}")

        if st.session_state.tersimpan:
            if st.button("Mulai Sesi Baru"):
                st.session_state.awal = False
                st.session_state.alokasi = False
                st.session_state.nominal_uang = 0.0
                st.session_state.pengeluaran = []
                st.session_state.tersimpan = False
                st.rerun()


if __name__ == '__main__':
    app()
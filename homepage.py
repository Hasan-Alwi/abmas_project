# import streamlit as st
# import pandas as pd
# import numpy as np

# # st.header('Self Cash Flow Dashboard')
# # st.write('On Going .... 🐦')

# def app():
#     st.title('Self Cash FLow Maker')

#     # instalasi session state
#     if 'awal' not in st.session_state :
#         st.session_state.awal = None
#     if 'alokasi' not in st.session_state :
#         st.session_state.alokasi = None
#     if 'nominal_uang' not in st.session_state :
#         st.session_state.nominal_uang = 0

#     if st.button('Mulai'):
#         st.session_state.awal = True

#     if st.session_state.awal:
#         uang_input = st.number_input('Masukkan nominal uang saku antum (Rp.)', format = '%.0f',  key = 'nominal_uang')
#         uang_awal = st.session_state.nominal_uang

#         if uang_awal > 0 :
#             st.success('Lanjut Alokasikan Uang sakumu')

#             if st.button('Lanjut Alokasi'):
#                 st.session_state.awal = False
#                 st.session_state.alokasi = True
#                 st.rerun()

#         else :
#             st.info('Silahkan mengisi terlebih dahulu nominal uangmu')

#     if st.session_state.get('alokasi', False):
#         if st.session_state.nominal_uang is not None:
#             uang_saku = st.session_state.nominal_uang
#             st.write(f'Mari Alokasikan {uang_saku} ini ke berbagai pengeluaran')
#             if 'pengeluaran' not in st.session_state :
#                 st.session_state.pengeluaran = []
            
#             terpakai = sum([item['nominal'] for item in st.session_state.pengeluaran]) 
#             sisa = uang_saku - terpakai

#             st.info(f'Uang yang belum kamu alokasikan sebesar {sisa} Rupiah')

#             if sisa > 0 :
#                 st.write('Tambah Alokasi')
#                 with st.form('Alokasi'):
#                     pil_1 = ['A', 'B', 'C']
#                     pil_2 = [10, 20, 30]
#                     col1, col2 = st.columns([3,1])
#                     kategori = st.selectbox('Jenis Pengeluaran', pil_1, index = None)
#                     persen = st.selectbox('Persentase', pil_2, index = None)

#                     if st.form_submit_button('submit', type = 'primary'):
#                         nominal_hitung = (persen / 100) * uang_saku
                        
#                         if nominal_hitung > sisa:
#                             st.error(f"Gagal! Nominal (Rp {nominal_hitung:,.0f}) melebihi sisa uang.")
#                         else:
#                             # Masukkan ke list di session state
#                             st.session_state.pengeluaran.append({
#                                 "Kategori": kategori,
#                                 "Persentase": f"{persen}%",
#                                 "nominal": nominal_hitung
#                             })
#                             st.rerun() # Refresh untuk update sisa uang
#             else:
#                 st.success("Mantap! Semua uang saku sudah teralokasikan habis.") 
                        
# if __name__ == '__main__':
#     app()

import streamlit as st
import pandas as pd
import numpy as np  

def app():
    st.title('Self Cash Flow Maker')

    if 'awal' not in st.session_state:
        st.session_state.awal = False
    if 'alokasi' not in st.session_state:
        st.session_state.alokasi = False
    if 'nominal_uang' not in st.session_state:
        st.session_state.nominal_uang = 0
    if 'pengeluaran' not in st.session_state:
        st.session_state.pengeluaran = []

    if st.button('Mulai'):
        st.session_state.awal = True

    if st.session_state.awal:

        uang_input = st.number_input(
            'Masukkan nominal uang saku (Rp.)',
            min_value=0,
            step=1000,
            format="%.0f"
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
            with st.form('alokasi_form'):
                kategori = st.selectbox('Jenis Pengeluaran', ['A', 'B', 'C'], index=None)
                persen = st.selectbox('Persentase', [10, 20, 30], index=None)

                submit = st.form_submit_button('Tambah')

                if submit:
                    if kategori is None or persen is None:
                        st.warning("Harap isi semua field")
                    else:
                        nominal_hitung = (persen / 100) * sisa

                        if nominal_hitung > sisa:
                            st.error("Melebihi sisa uang!")
                        else:
                            st.session_state.pengeluaran.append({
                                "Kategori": kategori,
                                "Persentase": f"{persen}%",
                                "nominal": nominal_hitung
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
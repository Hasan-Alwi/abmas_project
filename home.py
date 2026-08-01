import streamlit as st

st.title("💰 Self Cash Flow")
st.subheader("Kelola keuanganmu, raih mimpimu.")

st.write(
    "\"Sedikit demi sedikit, lama-lama menjadi bukit.\" "
    "Setiap rupiah yang kamu catat dan alokasikan hari ini "
    "adalah langkah kecil menuju kebebasan finansial di masa depan."
)

st.divider()
st.markdown("### Mau mulai dari mana?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📝 Input Keuangan")
    st.caption("Catat pemasukan & alokasikan ke kategori kamu.")
    st.page_link("input.py", label="Buka Input Keuangan", icon="📝")

    st.markdown("#### 📚 Financial Education Syariah")
    st.caption("Video edukasi seputar keuangan syariah.")
    st.button("Segera Hadir", key="btn_edukasi", disabled=True)

with col2:
    st.markdown("#### 📊 Dashboard")
    st.caption("Pantau perkembangan keuanganmu lewat grafik.")
    st.page_link("dashboard.py", label="Buka Dashboard", icon="📊")

    st.markdown("#### 🧮 Budget Example")
    st.caption("Contoh alokasi anggaran yang bisa jadi acuan.")
    st.button("Segera Hadir", key="btn_budget", disabled=True)
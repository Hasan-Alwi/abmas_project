import streamlit as st
import pandas as pd
from supabase_client import supabase

KATEGORI_KOLOM = ["alocation_1", "alocation_2", "investment"]

st.title("📊 Dashboard")
st.caption("Pantau perkembangan keuanganmu dari waktu ke waktu.")

try:
    response = supabase.table("user_data").select("*").execute()
    data = response.data

    if not data:
        st.info("Belum ada data untuk ditampilkan. Yuk mulai input pemasukan kamu!")
        st.page_link("input.py", label="Input Sekarang", icon="📝")
    else:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # ------------------------------------------------------
        # Ringkasan angka utama
        # ------------------------------------------------------
        total_pemasukan = df["money"].sum()
        total_alokasi = df[KATEGORI_KOLOM].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")

        if "tabungan" in KATEGORI_KOLOM:
            total_tabungan = df["tabungan"].sum()
            col2.metric("Total Tabungan", f"Rp {total_tabungan:,.0f}")
            persen_tabungan = (total_tabungan / total_pemasukan * 100) if total_pemasukan else 0
            col3.metric("% dari Pemasukan", f"{persen_tabungan:,.1f}%")
        else:
            col2.metric("Total Teralokasi", f"Rp {total_alokasi.sum():,.0f}")

        st.divider()

        # ------------------------------------------------------
        # Tren pertumbuhan pemasukan & tabungan (kumulatif)
        # ------------------------------------------------------
        st.subheader("Tren Pertumbuhan")
        harian = df.groupby(df["date"].dt.date).agg(
            {**{"money": "sum"}, **{k: "sum" for k in KATEGORI_KOLOM}}
        )
        kumulatif = harian.cumsum()

        tren_df = pd.DataFrame({"Total Pemasukan": kumulatif["money"]})
        if "tabungan" in KATEGORI_KOLOM:
            tren_df["Total Tabungan"] = kumulatif["tabungan"]

        st.line_chart(tren_df)

        # ------------------------------------------------------
        # Breakdown alokasi per kategori
        # ------------------------------------------------------
        st.subheader("Alokasi per Kategori")
        ringkasan = df[KATEGORI_KOLOM].sum().sort_values(ascending=False)
        st.bar_chart(ringkasan)

        persen = (ringkasan / ringkasan.sum() * 100).round(1) if ringkasan.sum() else ringkasan
        st.dataframe(persen.rename("Persentase (%)"))

        # ------------------------------------------------------
        # Riwayat data
        # ------------------------------------------------------
        st.subheader("Riwayat Data")
        st.dataframe(df.sort_values("date", ascending=False))

except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
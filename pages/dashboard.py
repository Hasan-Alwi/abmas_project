import streamlit as st
from supabase_client import supabase
from utils.theme import inject_css, sidebar_brand, navbar, hero, info_card
from utils.auth import require_login, sidebar_user
from utils.dashboard_view import siapkan_df, render_dashboard

# ------------------------------------------------------------
# Tema + gerbang login
# ------------------------------------------------------------
inject_css()

siswa = require_login()

with st.sidebar:
    sidebar_brand(active="Laporan & Visualisasi")
    sidebar_user()

navbar(active="Dashboard")

# ------------------------------------------------------------
# Identitas pemilik catatan
# ------------------------------------------------------------
KOLOM_NIS_SISWA = "nis_siswa"
NIS_BERTIPE_ANGKA = True

HALAMAN_INPUT = "pages/input_user.py"

NIS_SISWA = str(siswa.get("nis", "")).strip()
USERNAME_SISWA = str(siswa.get("username", "")).strip()


def nis_nilai():
    if NIS_BERTIPE_ANGKA and NIS_SISWA.isdigit():
        return int(NIS_SISWA)
    return NIS_SISWA


# ------------------------------------------------------------
# Banner
# ------------------------------------------------------------
hero(
    eyebrow="Laporan & Visualisasi",
    title="Pantau Ke Mana Uangmu Pergi",
    lead=(
        "Ringkasan seluruh catatan keuanganmu: berapa yang masuk, ke mana saja dibagi, "
        "dan sejauh mana investasimu bertumbuh dari waktu ke waktu."
    ),
    chips=[f"Catatan {USERNAME_SISWA}", f"NIS {NIS_SISWA}"],
)

# ------------------------------------------------------------
# Ambil data milik siswa yang sedang masuk saja
# ------------------------------------------------------------
try:
    response = (
        supabase.table("user_data")
        .select("*")
        .eq(KOLOM_NIS_SISWA, nis_nilai())
        .execute()
    )
    data = response.data
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

if not data:
    info_card(
        "📭",
        "Belum ada data untuk ditampilkan",
        "Yuk mulai catat pemasukan dan alokasimu dulu, nanti grafiknya muncul di sini. "
        "Ingin lihat contoh tampilannya? Buka halaman Budget Example.",
    )
    st.page_link(HALAMAN_INPUT, label="Input Sekarang", icon="📝")
    st.stop()

df = siapkan_df(data)

if df.empty:
    info_card("📭", "Belum ada data yang bisa ditampilkan",
              "Catatan yang tersimpan belum punya tanggal yang valid.")
    st.stop()

render_dashboard(df, key_prefix="dash")
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.theme import inject_css, sidebar_brand, navbar, hero, info_card
from utils.dashboard_view import siapkan_df, render_dashboard

# ------------------------------------------------------------
# Tema (sama dengan halaman lain)
# ------------------------------------------------------------
inject_css()
siswa = require_login() 

with st.sidebar:
    sidebar_brand(active="Perencanaan Anggaran")

navbar(active="Budget Example")

HALAMAN_INPUT = "pages/input_user.py"

# ------------------------------------------------------------
# Sumber data contoh — file CSV, bukan Supabase.
# Path dicari relatif terhadap lokasi file ini supaya tetap ketemu
# dari folder kerja mana pun (lokal maupun Streamlit Cloud).
# ------------------------------------------------------------
NAMA_FILE = "data/contoh_keuangan.csv"
KANDIDAT_PATH = [
    Path(__file__).resolve().parent.parent / NAMA_FILE,  # <root>/data/... (file ini di pages/)
    Path(__file__).resolve().parent / NAMA_FILE,         # <folder ini>/data/...
    Path.cwd() / NAMA_FILE,                              # folder kerja saat dijalankan
]


@st.cache_data
def muat_data_contoh() -> pd.DataFrame:
    for path in KANDIDAT_PATH:
        if path.exists():
            df = pd.read_csv(path)
            df["keterangan"] = df.get("keterangan", "").fillna("")
            return df
    raise FileNotFoundError(NAMA_FILE)


# ------------------------------------------------------------
# Banner
# ------------------------------------------------------------
hero(
    eyebrow="Contoh Perencanaan",
    title="Begini Tampilan Dashboard Setelah Rutin Mencatat",
    lead=(
        "Halaman ini memakai data contoh seorang siswa dengan uang saku sekitar Rp 500.000 "
        "per bulan selama delapan bulan. Perhatikan bagaimana pos Investasi tumbuh pelan-pelan "
        "ketika porsinya dinaikkan sedikit demi sedikit."
    ),
    chips=["8 bulan pencatatan", "Uang saku ± Rp 500.000", "Data contoh"],
)

info_card(
    "🧪",
    "Ini data contoh, bukan catatanmu",
    "Angka di halaman ini dibaca dari file contoh dan tidak berubah. "
    "Catatanmu sendiri ada di halaman Dashboard.",
)

# ------------------------------------------------------------
# Render — fungsi yang sama persis dengan halaman Dashboard
# ------------------------------------------------------------
try:
    data_contoh = muat_data_contoh()
except FileNotFoundError:
    st.error(
        f"File contoh `{NAMA_FILE}` tidak ditemukan. "
        "Pastikan file CSV-nya ikut ter-upload ke repositori."
    )
    st.stop()

df = siapkan_df(data_contoh.to_dict("records"))
render_dashboard(df, key_prefix="contoh")

st.write("")
st.page_link(HALAMAN_INPUT, label="Mulai Catat Punyamu Sendiri", icon="📝")
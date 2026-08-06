"""
Dashboard Perencanaan Keuangan & Penguatan Literasi Keuangan Syariah
SMA Integral Ar-Rohmah, Malang  |  Abmas - Statistika Bisnis, Vokasi ITS

HOMEPAGE
Jalankan:  streamlit run home.py
Butuh:  pip install streamlit pandas altair supabase

CATATAN PENTING
Seluruh perpindahan halaman memakai st.page_link, bukan tag <a href>.
Tag <a> memuat ulang browser sehingga sesi login terhapus dan siswa
diminta masuk berulang kali.
"""

import streamlit as st

from utils.theme import (
    inject_css,
    sidebar_brand,
    navbar,
    hero,
    info_card,
    section_title,
    menu_card,
)
from utils.auth import require_login, sidebar_user

# ----------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Keuangan Syariah | SMA Ar-Rohmah",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ----------------------------------------------------------------------------
# GERBANG LOGIN
# Baris ini menghentikan halaman selama siswa belum masuk.
# ----------------------------------------------------------------------------
siswa = require_login()

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    sidebar_brand(active="Beranda")
    sidebar_user()

navbar(active="Beranda")

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
hero(
    eyebrow="Dashboard Perencanaan Keuangan",
    title="Kelola Keuangan Dengan Bijak, Tumbuh Berkah Sesuai Prinsip Syariah",
    lead=(
        "Catat pemasukan, atur anggaran, rencanakan tujuan, dan tunaikan sedekah — "
        "satu tempat untuk membangun kebiasaan finansial yang sehat sejak dini."
    ),
    chips=[
        "Statistika Bisnis · ITS",
        "Galeri Investasi Vokasi ITS",
        "Bursa Efek Indonesia",
        "Sucor Sekuritas",
    ],
)

info_card(
    "👋",
    f"Assalamu'alaikum, {siswa.get('username', '')}!",
    "Mulailah mengelola uangmu dengan cara yang terstruktur dan sesuai prinsip syariah. "
    "Pilih salah satu menu di bawah untuk mulai mencatat dan merencanakan.",
)

# ----------------------------------------------------------------------------
# MENU UTAMA
# ----------------------------------------------------------------------------
section_title("Menu Utama")

MENU = [
    ("Input User", "Catat pemasukan & pengeluaran harianmu secara rapi.",
     "🟨", "pages/input_user.py"),
    ("Dashboard", "Atur alokasi kebutuhan, tabungan, dan sedekah.",
     "📊", "pages/dashboard.py"),
    ("Budget Example", "Rencanakan dan pantau capaian targetmu.",
     "🎯", "pages/budget_example.py"),
    ("Financial Education Syariah", "Pelajari riba, gharar, maysir, & instrumen syariah.",
     "📖", "pages/edukasi.py"),
]

kartu = st.columns(4, gap="medium")
for kolom, (judul, deskripsi, ikon, path) in zip(kartu, MENU):
    with kolom:
        menu_card(judul, deskripsi, ikon, path)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.write("")
st.markdown(
    '<div style="background:linear-gradient(135deg,var(--green-700) 0%,var(--green-600) 100%);'
    'border-radius:18px;padding:34px 40px;text-align:center;color:#fff;margin-top:8px">'
    '<div style="font-family:Amiri,\'Traditional Arabic\',serif;font-size:1.5rem;'
    'color:var(--gold-400);margin-bottom:14px">وَأَنفِقُوا۟ فِى سَبِيلِ ٱللَّهِ</div>'
    '<div style="font-size:15px;line-height:1.7;font-style:italic;'
    'color:rgba(255,255,255,.9);max-width:70ch;margin:0 auto 14px">'
    '"Kelola keuangan dengan bijak, hindari riba, tingkatkan tabungan, dan tunaikan sedekah. '
    'Keuangan yang sehat membawa keberkahan."</div>'
    '<div style="font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;'
    'color:rgba(255,255,255,.7)">Dashboard Keuangan Syariah · SMA Integral Ar-Rohmah Malang</div>'
    "</div>",
    unsafe_allow_html=True,
)
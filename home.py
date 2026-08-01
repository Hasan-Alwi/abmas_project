"""
Dashboard Perencanaan Keuangan & Penguatan Literasi Keuangan Syariah
SMA Integral Ar-Rohmah, Malang  |  Abmas - Statistika Bisnis, Vokasi ITS

HOMEPAGE
Jalankan:  streamlit run home.py
Butuh:  pip install streamlit plotly streamlit-authenticator
"""

import streamlit as st
import plotly.graph_objects as go
from utils.css import load_css
from utils.nav import top_nav
from utils.auth import require_login, sidebar_user, user_aktif

# ----------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Keuangan Syariah | SMA Ar-Rohmah",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Desain Visual
#   Identitas: emerald pesantren + emas (barakah/sedekah) + kertas hangat.
#   Font: Plus Jakarta Sans (buatan Indonesia) + Amiri untuk kutipan.
# ----------------------------------------------------------------------------
load_css()

# ----------------------------------------------------------------------------
# GERBANG LOGIN  (NIS + Username, sumber akun: CSV)
# Baris di bawah ini menghentikan halaman selama siswa belum masuk.
# ----------------------------------------------------------------------------
authenticator = require_login()

top_nav("/")

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="t">🌙 Keuangan Syariah</div>
      <div class="s">SMA Integral Ar-Rohmah · Malang</div>
    </div>
    <div class="sb-nav">
      <div class="active">🏠&nbsp;&nbsp;Beranda</div>
      <a class="nav-link" href="/input_user" target="_self">
        <div class="item">📒&nbsp;&nbsp;Pencatatan Keuangan</div>
      </a>
      <a class="nav-link" href="/dashboard" target="_self">
        <div class="item">🧮&nbsp;&nbsp;Perencanaan Anggaran</div>
      </a>
      <a class="nav-link" href="/budget_example" target="_self">
        <div class="item">🎯&nbsp;&nbsp;Tujuan Keuangan</div>
      </a>
      <a class="nav-link" href="/financial_education" target="_self">
        <div class="item">📖&nbsp;&nbsp;Edukasi Keuangan Syariah</div>
      </a>
      <a class="nav-link" href="/laporan" target="_self">
        <div class="item">📊&nbsp;&nbsp;Laporan & Visualisasi</div>
      </a>
    </div>
    """, unsafe_allow_html=True)

# Kartu identitas siswa + tombol keluar
sidebar_user(authenticator)


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow"><span></span>Dashboard Perencanaan Keuangan</div>
  <h1>Kelola Keuangan Dengan Bijak, Tumbuh Berkah Sesuai Prinsip Syariah</h1>
  <p>Catat pemasukan, atur anggaran, rencanakan tujuan, dan tunaikan sedekah —
  satu tempat untuk membangun kebiasaan finansial yang sehat sejak dini.</p>
  <div class="partners">
    <div class="chip">Statistika Bisnis · ITS</div>
    <div class="chip">Galeri Investasi Vokasi ITS</div>
    <div class="chip">Bursa Efek Indonesia</div>
    <div class="chip">Sucor Sekuritas</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="welcome">
  <div class="ico">👋</div>
  <div>
    <b>Assalamu'alaikum, {user_aktif().get('nama', '')}!</b>
    <p>Mulailah mengelola uangmu dengan cara yang terstruktur dan sesuai prinsip syariah.
    Pilih menu di samping untuk mulai mencatat dan merencanakan.</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# MENU UTAMA
# ----------------------------------------------------------------------------
st.markdown('<div class="sec-title"><h3>Menu Utama</h3><div class="rule"></div></div>',
            unsafe_allow_html=True)

menu = [
    ("📒", "#E2F1EA", "Input User", "Catat pemasukan & pengeluaran harianmu secara rapi.", "/input_user"),
    ("🧮", "#E4EEFB", "Dashboard", "Atur alokasi kebutuhan, tabungan, dan sedekah.", "/dashboard"),
    ("🎯", "#F3E7F7", "Budget Example", "Rencanakan dan pantau capaian targetmu.", "/budget_example"),
    ("📖", "#F7EFD3", "Financal Education Syariah", "Pelajari riba, gharar, maysir, & instrumen syariah.", "/financial_education"),
]
cols = st.columns(4, gap="medium")
for col, (icon, bg, title, desc, href) in zip(cols, menu):
    tag = ('<span class="soon">Segera hadir</span>' if not href
           else '<span class="soon" style="background:#0d6b4f;color:#fff">Buka halaman →</span>')
    card = f"""
      <div class="menu-card">
        <div class="badge" style="background:{bg}">{icon}</div>
        <h5>{title}</h5>
        <p>{desc}</p>
        {tag}
      </div>"""
    if href:
        card = f'<a class="card-link" href="{href}" target="_self">{card}</a>'
    col.markdown(card, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="quote">
  <div class="ar">وَأَنفِقُوا۟ فِى سَبِيلِ ٱللَّهِ</div>
  <div class="id">"Kelola keuangan dengan bijak, hindari riba, tingkatkan tabungan,
  dan tunaikan sedekah. Keuangan yang sehat membawa keberkahan."</div>
  <div class="src">DASHBOARD KEUANGAN SYARIAH · SMA INTEGRAL AR-ROHMAH MALANG</div>
</div>
""", unsafe_allow_html=True)
